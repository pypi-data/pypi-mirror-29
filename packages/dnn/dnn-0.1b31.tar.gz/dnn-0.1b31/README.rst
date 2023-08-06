
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
    n_output = 8
        
    def make_place_holders (self):
        # should be defined as self.x and self.y
        self.x = tf.placeholder ("float", [None, self.n_seq_len, self.n_channels])
        self.y = tf.placeholder ("float", [None, self.n_output])
        
    def make_logit (self):
        # building neural network with convolution 1d, rnn and dense layers
        
        layer = self.conv1d (self.x, 2048, activation = tf.nn.relu)
        layer = self.avg_pool1d (layer)
        
        outputs = self.lstm_with_dropout (
          layer, 2048, lstm_layers = 2, activation = tf.tanh
        )
        
        # hidden dense layers
        layer = self.dense (outputs [-1], 1024)
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
        return YourOptimizer (self.cost, self.learning_rate, self.global_step, ...)
    
    def calculate_accuracy (self):
        correct_prediction = tf.equal (tf.argmax(self.y, 1), tf.argmax(self.logit, 1))
        return tf.reduce_mean (tf.cast (correct_prediction, "float"))

Sometimes it is very annoying to calculate complex accuracy with tensors, then can replace with calculate_complex_accuracy for calculating with numpy, python math and loop statement. 

.. code-block:: python

  import dnn
  import numpy as np
  
  class MyDNN (dnn.DNN):    
    # can get additional arguments for calculating accuracy as you need
    def calculate_complex_accuracy (self, logit, y, *args, **karg):
        return np.mean ((np.argmax (logit, 1) == np.argmax (y, 1)))


Predefined Operations & Creating
---------------------------------------------------

You should or could create these operations by overriding methods,
 
- train_op: create with 'make_optimizer'
- logit: create with 'DNN.make_logit'
- cost: create with 'DNN.make_cost'
- accuracy (optional): create with 'DNN.make_accuracy'
- label (optional): create with 'DNN.make_label', making your label from your logit

Predefined Place Holders
--------------------------------

- x
- y
- dropout_rate: if negative value, dropout rate will be selected randomly. 
- is_training
- n_sample: Numner of x (or y) set. This value will be fed automatically, do not feed.

Training 
--------------

- fit
- train
- valid
- trainable
- run
- get_epoch: equivalant with DNN.eval (self.global_step)

Optimizers
-----------------

You can use predefined optimizers.

.. code-block:: python

  def make_optimizer (self):
    return self.optimizer ("adam")

Available names are,

- "adam"    
- "rmsprob"
- "momentum"
- "clip"

see dnn/optimizers.py


Layering
----------------------------

- dense
- batch_norm
- batch_norm_with_dropout
- lstm
- lstm_with_dropout
- dropout
- full_connect
- conv1d
- conv2d
- conv3d
- max_pool1d
- max_pool2d
- max_pool3d
- avg_pool1d
- avg_pool2d
- avg_pool3d
- sequencial_connect


Model 
------------

- save
- restore
- export
- reset_dir
- eval

Tensor Board
-----------------------

- reset_tensor_board
- get_writers
- make_writers
- write_summary


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
  
  minibatches = split.minibatch (train_xs, train_ys, 128)
    
  for epoch in tqdm (range (1000)): # 1000 epoch
    # training ---------------------------------
    batch_xs, batch_ys = next (minibatches)
    lr = net.fit (batch_xs, batch_ys, dropout_rate = 0.5)
    # Or you can run ops directly, 
    _, lr = net.run (
      net.train_op, net.learning_rate, 
      x = batch_xs, y = batch_ys, dropout_rate = 0.5
    )
    net.write_summary ('Param', {"Learning Rate": lr})
    
    # train loss ------------------------------
    logit, cost, acc = net.train (train_xs, train_ys, dropout_rate = 0.0)
    net.write_summary ('Train', {"Accuracy": acc, "Cost": cost})
    
    # valid loss -------------------------------
    logit, cost, acc = net.valid (test_xs, test_ys, dropout_rate = 0.0)
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
