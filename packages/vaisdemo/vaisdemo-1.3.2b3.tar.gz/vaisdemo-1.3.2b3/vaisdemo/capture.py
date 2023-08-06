from __future__ import print_function
import logging
import time
import threading
import os
import sys
if sys.version_info[0]<3:
 import Queue
else:
 import queue as Queue
os.environ["PA_ALSA_PLUGHW"]="1"
import pyaudio 
m=logging.getLogger(__name__)
class ConfigurationException(Exception):
 pass
class d(object):
 i=None
 def __init__(K):
  K._pa=pyaudio.PyAudio()
 def get_device_list(K,input_only=False):
  r=[]
  for i in range(K._pa.get_device_count()):
   if(not input_only)or(input_only and K._pa.get_device_info_by_index(i)['maxInputChannels']>0):
    r.append(K._pa.get_device_info_by_index(i)['name'])
  return r
 def get_device_index(K,name):
  if not name:
   return None
  return K.get_device_list().index(name)
 def get_device_name(K,idx):
  if idx is None:
   return None
  return K.get_device_list()[idx]
 def __del__(K):
  K._pa.terminate()
class Capture(object):
 e=120
 n=16000
 O=20
 a=int((n/1000)*O)
 b=1000
 R=10
 i=None
 p=False
 N=None
 V=None
 h=None
 G=None
 x=None
 Y=None
 t=None
 w=None
 I=None
 v=None
 B=False
 u=None
 def __init__(K,X,s):
  K._config=X
  K._tmp_path=s
  if not os.path.exists(s):
   os.makedirs(s)
  K._pa=pyaudio.PyAudio()
  K._queue=Queue.Queue()
  K._device_info=d()
  K._recording_lock_inverted=threading.Event()
  K._recording_lock_inverted.set()
  if('input_device' not in X['sound'])and('input_device_name' not in X['sound']):
   raise Exception("Device must be set")
  K.validate_config()
 def validate_config(K):
  k=K._config['sound']['input_device']
  H=K._device_info.get_device_list(False)
  if k and(k not in H):
   raise ConfigurationException("Your input_device '"+k+"' is invalid. Use one of the following:\n"+'\n'.join(H))
 def setup(K,Q):
  K._state_callback=Q
 def cleanup(K):
  m.debug("Cleaning up capture")
  if not K._recording_lock_inverted.isSet():
   K._interrupt=True
   K._recording_lock_inverted.wait()
  K._pa.terminate()
 def handle_init(K,rate,o):
  K._handle=K._pa.open(input=True,input_device_index=K._device_info.get_device_index(K._config['sound']['input_device']),format=pyaudio.paInt16,channels=1,rate=rate,frames_per_buffer=o)
  K._handle_chunk_size=o
 def handle_read(K):
  return K._handle.read(K._handle_chunk_size,exception_on_overflow=K._pa_exception_on_overflow)
 def handle_release(K):
  K._handle.close()
 def _callback(K,W,frame_count,time_info,status): 
  E=logging.getLogger('alexapi').getEffectiveLevel()==logging.DEBUG
  y=False
  if y and(K._callback_data['frames']<K._callback_data['throwaway_frames']):
   K._callback_data['frames']+=1
  elif(K._callback_data['force_record']and K._callback_data['force_record'][0]()) or(y and(K._callback_data['thresholdSilenceMet']is False)and((time.time()-K._callback_data['start'])<K.MAX_RECORDING_LENGTH)):
   if y:
    if int(len(W)/2)==K.VAD_PERIOD:
     L=K._vad.is_speech(W,K.VAD_SAMPLERATE)
     if not L:
      K._callback_data['silenceRun']+=1
     else:
      K._callback_data['silenceRun']=0
      K._callback_data['numSilenceRuns']+=1
    if(K._callback_data['numSilenceRuns']!=0) and((K._callback_data['silenceRun']*K.VAD_FRAME_MS)>K.VAD_SILENCE_TIMEOUT):
     K._callback_data['thresholdSilenceMet']=True
  K._queue.put(W)
  if E:
   K._callback_data['audio']+=W
  return None,pyaudio.paContinue
 def silence_listener(K,throwaway_frames=None,force_record=None):
  m.debug("Recording: Setting up")
  K._recording_lock_inverted.clear()
  E=logging.getLogger('alexapi').getEffectiveLevel()==logging.DEBUG
  if K._state_callback:
   K._state_callback()
  K._queue.queue.clear()
  K._callback_data={'start':time.time(),'thresholdSilenceMet':False,'frames':0,'throwaway_frames':throwaway_frames or K.VAD_THROWAWAY_FRAMES,'numSilenceRuns':0,'silenceRun':0,'force_record':force_record,'audio':b'' if E else False,}
  M=K._pa.open(input=True,input_device_index=K._device_info.get_device_index(K._config['sound']['input_device']),format=pyaudio.paInt16,channels=1,rate=K.VAD_SAMPLERATE,frames_per_buffer=K.VAD_PERIOD,stream_callback=K._callback,start=False)
  m.debug("Recording: Start")
  M.start_stream()
  def _listen():
   while True:
    try:
     P=K._queue.get(block=True,timeout=2)
     if not P or K._interrupt:
      break
     yield P
    except Queue.Empty:
     break
   M.stop_stream()
   m.debug("Recording: End")
   M.close()
   if K._state_callback:
    K._state_callback(False)
   if E:
    with open(K._tmp_path+'/recording.wav','wb')as rf:
     rf.write(K._callback_data['audio'])
   K._recording_lock_inverted.set()
  return _listen()

