
==============================
Deep Neural Networks Library
==============================

It is for eliminating repeat jobs of machine learning. Also it can makes your code more beautifully and Pythonic.

.. contents:: Table of Contents

Building Deep Neural Network 
==============================

mydnn.py,

.. code-block:: python

  import dnn
  import tensorflow as tf
  
  class MyDNN (dnn.DNN):
    n_seq_len = 24    
    n_channels = 1024    
    n_output = 3
        
    def make_place_holders (self):
        self.x = tf.placeholder ("float", [None, self.n_seq_len, self.n_channels])
        self.y = tf.placeholder ("float", [None, self.n_output])
        
    def make_logit (self):
        # building neural network with convolution 1d, rnn and dense layers
        
        # (-1, 24, 1024) => (-1, 12, 2048)        
        layer = self.conv1d (self.x, 2048, activation = tf.nn.relu)
        layer = self.avg_pool1d (layer)
        
        # rnn
        output = self.lstm_with_dropout (
          conv, 2048, lstm_layers = 2, activation = tf.tanh
        )
        
        # hidden dense layers
        layer = self.dense (output [-1], 1024)
        layer = self.batch_norm_with_dropout (layer, self.nn.relu)
        layer = self.dense (layer, 256)
        layer = self.batch_norm_with_dropout (layer, self.nn.relu)
        
        # finally, my logit        
        return self.dense (layer, self.n_output)
    
    def make_label (self):
      # prediction method 
    	return tf.argmax (self.logit, 1)
    	
    def make_cost (self):
        return tf.reduce_mean (tf.nn.softmax_cross_entropy_with_logits (
            logits = self.logit, labels = self.y
        ))
    
    def make_optimizer (self):
       return self.optimizer ("adam")
    
    def calculate_accuracy (self):
        correct_prediction = tf.equal (tf.argmax(self.y, 1), tf.argmax(self.logit, 1))
        return tf.reduce_mean (tf.cast (correct_prediction, "float"))

Sometimes it is very annoying to calculate complex accuracy with tensors, then can replace with calculate_complex_accuracy for calculating with numpy, python math and loop statement. 

.. code-block:: python

  import dnn
  import numpy as np
  
  class MyDNN (dnn.DNN):    
    # can get additional arguments as you need calculate accuracy
    def calculate_complex_accuracy (self, logit, y, *args, **karg):
        return np.mean ((np.argmax (logit, 1) == np.argmax (y, 1)))
    

Training 
=============

Import mydnn.py,

.. code-block:: python

  import mydnn
  from tqdm import tqdm

  net = mydnn.MyDNN (gpu_usage = 0.4)
  net.reset_dir ('./checkpoint')
  net.trainable (
    start_learning_rate=0.0001, 
    decay_step=500, decay_rate=0.99, 
    overfit_threshold = 0.1
  )
  net.reset_tensor_board ("./logs")
  net.make_writers ('Param', 'Train', 'Valid')
  
  train_minibatches = split.minibatch (train_xs, train_ys, 128)
  valid_minibatches = split.minibatch (test_xs, test_ys, 128)
    
  for epoch in tqdm (range (1000)): # 1000 epoch
    # training ---------------------------------
    batch_xs, batch_ys = next (train_minibatches)
    _, lr = net.run (
      net.train_op, net.learning_rate, 
      x = batch_xs, y = batch_ys, dropout_rate = 0.5, is_training = True
    )
    net.write_summary ('Param', {"Learning Rate": lr})
    
    # train loss ------------------------------
    cost, logit = net.run (s
      net.cost, net.logit, 
      x = batch_xs, y = batch_ys, dropout_rate = 0.0, is_training = True
    )
    acc = net.calculate_complex_accuracy (logit, batch_ys)
    net.write_summary ('Train', {"Accuracy": acc, "Cost": cost})
    
    # valid loss -------------------------------
    vaild_xs, vaild_ys = next (valid_minibatches)
    cost, logit = net.run (
      net.cost, net.logit, 
      x = vaild_xs, y = vaild_ys, dropout_rate = 0.0
    )
    acc = net.calculate_complex_accuracy (logit, vaild_ys)    
    net.write_summary ('Valid', {"Accuracy": acc, "Cost": cost})
    
    # check overfit or save checkpoint if cost is the new lowest cost.     
    if net.is_overfit (cost, './checkpoint'):
        break


Multi Model Training
=======================

You can train complete seperated models at same time. 

Not like `Multi Task Training`_ in this case models share the part of training data and there're no shared layers between models - for example, model A is a logistic regression and B is a calssification problem.

Anyway, it provides some benefits for model, dataset and code management rather than handles as two complete seperated models. 

First of all, you give name to each models for saving checkpoint or tensorboard logging. 

.. code-block:: python
  
  import mydnn
  import dnn
  
  net1 = mydnn.ModelA (0.3, name = 'my_model_A')
  net2 = mydnn.ModelB (0.2, name = 'my_model_B')

Your checkpoint, tensorflow log and export pathes will remaped seperately to each model names like this:

.. code-block:: bash

  checkpoint/my_model_A
  checkpoint/my_model_B
  
  logs/my_model_A
  logs/my_model_B
  
  export/my_model_A
  export/my_model_B

Next, y should be concated. Assume ModelA use first 4, and ModelB use last 3. 
  
.. code-block:: python
  
  # y length is 7
  y = [0.5, 4.3, 5.6, 9.4, 0, 1, 0]  

Then combine models into MultiDNN.

.. code-block:: python
  
  net = dnn.MultiDNN (net1, 4, net2, 3)

And rest of code is very same as a single DNN case.

If you need exclude data from specific model, you can use exclusion filter function.

.. code-block:: python

  def exclude (ys, xs = None):
    nxs, nys = [], []
    for i, y in enumerate (ys):
        if np.sum (y) > 0:            
            nys.append (y)
            if xs is not None:
                nxs.append (xs [i])
    return np.array (nys), np.array (nxs)
  net1.set_filter (exclude)

.. _`Multi Task Training`: https://jg8610.github.io/Multi-Task/


Export Model
===============

For serving model,

.. code-block:: python

  import mydnn
  
  net = mydnn.MyDNN ()
  net.restore ('./checkpoint')
  version = net.export ( 
    './export', 
    'predict_something', 
    inputs = {'x': net.x},
    outputs={'label': net.label, 'logit': net.logit}
  )
  print ("version {} has been exported".format (version))
 

Helpers
============

There're several helper modules.

Generic DNN Model Helper
------------------------------

.. code-block:: python

  from dnn import costs, predutil


Data Processing Helper
------------------------------

.. code-block:: python
  
  from dnn import split, vector
  import dnn.video
  import dnn.audio
  import dnn.image
  import dnn.text


History
=========

- 0.1: project initialized
