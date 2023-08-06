import numpy as np
import sys
import os
import glob
import wave
import multiprocessing
from functools import partial
from scipy.fftpack import fft
from scipy.io import wavfile
from scipy import signal
from tqdm import tqdm
import librosa
import librosa.util
import random 
from scipy.stats import skew, kurtosis
import warnings

SAMPLE_RATE = 22050
TIME_LAP = 0.2

def _save (data, wavfile, target_path):
    savedir = os.path.join (target_path, os.path.basename (os.path.dirname (os.path.dirname (wavfile))))
    if not os.path.isdir (savedir):
        os.mkdir (savedir)
    target_file = os.path.join(savedir, "%s.npy" % os.path.basename (wavfile))
    np.save(target_file, data)

def _normalize (y):
    return y / np.max (np.abs (y))
    
def log (x, name = ""):
    return np.log (np.abs (x) + 1e-3) / 6.7
    
def _compress (data, name, valid_max = 2.0, valid_min = -2.0):
    data = data.real
    if name == "poly_features":
        data = data / 10.
    elif name == "rmse":
        data = data / 4.
    elif name == "spectral_contrast":
        data = data / 50.
    elif name == "mel":
        data = data / -80.
    elif name in ("stft", "spectral_centroid", "spectral_bandwidth", "spectral_rolloff"):        
        data = log (data, name)
                          
    features = np.array ([
        np.mean (data, axis = 1),
        np.max (data, axis = 1),
        np.min (data, axis = 1),
        np.median (data, axis = 1),
        np.var (data, axis = 1),
        skew (data, axis = 1) / 15.,
        np.log (abs (kurtosis (data, axis = 1)) + 1e-3) / 6.7
    ])    
    
    if np.min (features) < valid_min or np.max (features) > valid_max:
        #print (name, int (np.max (features)), int (np.max (features)))
        raise AssertionError
    return features

def load (wavfile, sample_rate = SAMPLE_RATE, time_lap = 0.2, due_limit = (1, 5), time_stretch = False, pitch_shift = False, random_laps = False, add_noise = False):
    y, sr = librosa.load (wavfile, sample_rate, True)
    if add_noise:
        noise = np.random.normal (0, 1, y.shape)
        gain = max (0.02, random.random () * 0.1)        
        y = y + gain * noise

    if time_stretch:
        rate = 1.0
        if random.randrange (2):
            rate += max (0.05, random.random () / 4.)
        else:
            rate -= max (0.05, random.random () / 4.)    
        y = librosa.effects.time_stretch (y, rate)
        #print ("time_stretch", rate)
    
    if pitch_shift:
        n_step = random.choice ([-4,-3,-2,-1,1,2,3,4])
        y = librosa.effects.pitch_shift (y, sr, n_step)
        #print ("pitch_shift", n_step)
    
    if random_laps:
       time_lap += random.random () / 3
    
    removable = int (sample_rate * time_lap)
    y = y [removable:len (y) - removable]
    # Trim the beginning and ending silence
    y, index = librosa.effects.trim (y)    
    duration = librosa.get_duration(y)     
    if duration < due_limit [0] or duration > due_limit [1]:
        warnings.warn ("audio file length is invalid, ignored")
        return None, sr    
    # normalize
    return y, sr
 
DEFAULT_RECIPE = {
    "mel", "mfcc", "chroma_cqt", "chroma_cens", "zero_crossing_rate", "tonnetz", "rmse", 
    "spectral_contrast", "poly_features", "chroma_stft", 
    "spectral_centroid", "spectral_bandwidth", "spectral_rolloff"
}
   
def generate (y, sample_rate = SAMPLE_RATE, recipe = DEFAULT_RECIPE, n_mfcc = 40, n_mel = 40):
    feature_stack = []
    numfeat = []
    
    # stft ----------------------------------------------------
    stft = librosa.stft (y, n_fft=1024, win_length=512, hop_length=256)
    if "mel" in recipe:
        # mel specrogram ------------------------------------------
        D = np.abs (stft) ** 2
        S = librosa.feature.melspectrogram(S = D, n_mels = n_mel)
        vec = librosa.power_to_db (S, ref = np.max)
        feature_stack.extend (_compress (vec, "mel"))
        numfeat.append (vec.shape [0])        
        
    if "stft" in recipe:
        feature_stack.extend (_compress (vec, "stft"))
        numfeat.append (vec.shape [0])
        
    if "mfcc" in recipe:
        vec = librosa.feature.mfcc(S = stft, sr = sample_rate, n_mfcc = n_mfcc, n_fft=512, hop_length = 256)
        feature_stack.extend (_compress (vec, "mfcc"))
        numfeat.append (vec.shape [0])
        
    if "chroma_cqt" in recipe:        
        vec = librosa.feature.chroma_cqt (y=y, sr = sample_rate, n_chroma = 12, hop_length = 256)
        feature_stack.extend (_compress (vec, "chroma_cqt"))
        numfeat.append (vec.shape [0])
        
    if "chroma_cens" in recipe:
        vec = librosa.feature.chroma_cens (y=y, sr = sample_rate, n_chroma = 12, hop_length = 256)
        feature_stack.extend (_compress (vec, "chroma_cens"))    
        numfeat.append (vec.shape [0])
        
    if "zero_crossing_rate" in recipe:
        vec = librosa.feature.zero_crossing_rate (y = y)
        feature_stack.extend (_compress (vec, "zero_crossing_rate"))
        numfeat.append (vec.shape [0])
        
    if "tonnetz" in recipe:
        vec = librosa.feature.tonnetz (y=y, sr = sample_rate)
        feature_stack.extend (_compress (vec, "tonnetz"))
        numfeat.append (vec.shape [0])
        
    if "rmse" in recipe:
        vec = librosa.feature.rmse (S = stft, hop_length = 256)
        feature_stack.extend (_compress (vec, "rmse"))
        numfeat.append (vec.shape [0])
        
    for ff in [each for each in recipe if each in ("spectral_contrast", "poly_features", "chroma_stft", "spectral_centroid", "spectral_bandwidth", "spectral_rolloff")]:
        vec = getattr (librosa.feature, ff) (y = y, sr = sample_rate, hop_length = 256)
        feature_stack.extend (_compress (vec, ff))        
        numfeat.append (vec.shape [0])    
    features = np.hstack (tuple (feature_stack))    
    assert features.shape == (sum (numfeat) * 7,)
    return features

AUDIO_ERRS = 0
def make (wavfile, sample_rate = SAMPLE_RATE, time_lap = 0.2, due_limit = (1, 5), recipe = DEFAULT_RECIPE, time_stretch = False, pitch_shift = False, random_laps = False, add_noise = False):
    global AUDIO_ERRS
    
    y, sr = load (wavfile, sample_rate, time_lap, due_limit, time_stretch, pitch_shift, random_laps, add_noise)
    if y is None:
        return
    try:
        return generate (y, sr, recipe)
    except AssertionError:
        AUDIO_ERRS += 1
        print ("audio file may be irregular, ignored ({})".format (AUDIO_ERRS))
        return None    

def save (wavfile, target_path, sample_rate = SAMPLE_RATE, time_lap = 0.2, due_limit = (1, 5), recipe = DEFAULT_RECIPE):
    features = make (wavfile, sample_rate, time_lap, due_limit, recipe)
    if features is None:
        return False
    _save (features, wavfile, target_path)
    return True

def puff (wavfile, target_path, sample_rate = SAMPLE_RATE, time_lap = 0.2, due_limit = (1, 5), recipe = DEFAULT_RECIPE, n_gen = 10):    
    _saved = save (wavfile, target_path, sample_rate, time_lap, due_limit, recipe)
    if not _saved:
        return 0
     
    n = 1
    for i in range (n_gen * 2):
        params = (random.randrange (2), random.randrange (2), random.randrange (2), random.randrange (2))
        if sum (params) == 0:
            continue
        features = make (wavfile, sample_rate, time_lap, due_limit, recipe, time_stretch = params [0], pitch_shift = params [1], random_laps = params [2], add_noise = params [3])
        if features is None:
            continue        
        _save (features, "{}.{}".format (wavfile, n), target_path)
        n += 1
        if n == n_gen:
            break
    
    return n    


if __name__ == '__main__':    
    y, sr = load  (os.path.join (os.path.dirname (__file__), "test.wav"))
    print (y.shape)   
    print (librosa.get_duration(y [:sr])) 
    stft = librosa.stft (y [:sr], n_fft=2048, win_length=1200, hop_length=256)
    print (stft.shape)
    ft = generate (y, sr)
    print (ft.shape)
    
    