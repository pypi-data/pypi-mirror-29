import subprocess
import math
import shutil

DEBUG = False

def set_debug (flag = True):
    global DEBUG    
    DEBUG = flag
    
def run_process (command):
    global DEBUG   
     
    res = subprocess.run(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)    
    out, err = res.stdout.decode ("utf8"), res.stderr.decode ("utf8")
    if DEBUG:
        print (out)
        print (err)
    return out, err

def get_movie_length (video_file_path):
    duration = subprocess.check_output(['ffprobe', '-i', video_file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
    floatDu = float(duration.decode('utf-8'))
    intDu = math.floor(floatDu)
    return intDu

def extract_wav (inp, outp):
    command = 'ffmpeg -y -i "{}" -vn -ac 1 "{}"'.format(inp, outp)
    run_process (command)
    assert os.path.isfile (outp)

def crop (inp, outp, offset, for_sec, video_length):
    if video_length <= for_sec:
        shutil.copy2 (inp, outp)
    else:
        command = 'ffmpeg -y -i "{}" -ss "{}" -t "{}" -vcodec copy -acodec copy "{}"'.format(inp, offset, for_sec, outp)
        run_process (command)
    assert os.path.isfile (outp)    

def crop_by_stamp (inp, outp, stamp): 
    command = 'ffmpeg -y -i "{}" -ss {} -to {} -acodec aac -vcodec libx264 "{}"'.format(inp, str(stamp[0]), str(stamp[1]), outp)
    run_process (command)
    assert os.path.isfile (outp)

def make_thumbnail (inp, outp, offset):  
    command = 'ffmpeg -y -i "{}" -ss {} -vframes 1 "{}"'.format(inp, offset, outp)
    run_process (command)
    assert os.path.isfile (outp)
