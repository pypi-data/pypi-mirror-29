from __future__ import print_function
import uuid
import grpc
import json
import audioop
import shutil
import yaml
import vaisdemo.speech.v1.cloud_speech_pb2_grpc as cloud_speech_pb2_grpc
import vaisdemo.speech.v1.cloud_speech_pb2 as cloud_speech_pb2
import threading
import importlib
import vaisdemo.capture as capture
import wave
try:
 import pyaudio
except Exception as e:
 exit(1)
E=640
w=pyaudio.paInt16
Q=1
G=16000
h=15
e=threading.Lock()
class VaisService():
 def __init__(v,d,resources_path=None,silence=False,mic_name=None,record=True):
  v.api_key=d
  v.record=record
  v.url="service.grpc.vais.vn:50051"
  v.channel=grpc.insecure_channel(v.url)
  v.channel.subscribe(callback=v.connectivity_callback,try_to_connect=True)
  v.stop=False
  v.stub=cloud_speech_pb2_grpc.SpeechStub(v.channel)
  v.volume=0
  v.mic_name=mic_name
  if v.record:
   v.capture=capture.Capture({'sound':{'input_device':mic_name}},"/tmp/audio")
  v.asr_callback=None
  v.encoder=None
  try:
   from speex import WBEncoder
   v.encoder=x()
   v.encoder.quality=10
   C=v.encoder.frame_size
   E=C
  except Exception as e:
   pass
 def state_callback(*args):
  pass
 def __enter__(v):
  if v.record:
   v.capture.setup(v.state_callback)
  return v
 def __exit__(v,*args):
  if v.record:
   v.capture.cleanup()
  try:
   shutil.rmtree("/tmp/audio")
  except Exception as e:
   pass
 def connectivity_callback(v,c):
  pass
 def get_speech(v):
  try:
   B=v.capture.silence_listener()
   for Y in B:
    v.volume=audioop.max(Y,2)
    if v.encoder:
     with e:
      Y=v.encoder.encode(Y)
    yield Y
  except Exception as e:
   v.asr_callback(e.message,False)
 def load_audio(v,fname):
  m=wave.open(fname)
  T=m.getnframes()
  k=640
  I=0
  P=0
  while I<T:
   P+=1
   s=T-I
   j=k
   if k>s:
    j=s
   Y=m.readframes(j)
   v.volume=audioop.max(Y,2)
   if v.encoder:
    with e:
     Y=v.encoder.encode(Y)
   I+=j
   yield Y
 def load_audio_bin(v,all_data):
  T=len(all_data)
  k=640
  I=0
  P=0
  for r in range(0,T,k):
   O=r+k
   Y=all_data[r:O]
   a=len(Y)
   if a==k:
    if v.encoder:
     with e:
      Y=v.encoder.encode(Y)
    yield Y
 def generate_messages(v,filename=None,audio_data=None):
  D=cloud_speech_pb2.RecognitionConfig.SPEEX_WITH_HEADER_BYTE
  if v.encoder is None:
   D=cloud_speech_pb2.RecognitionConfig.LINEAR16
  n=cloud_speech_pb2.RecognitionConfig(encoding=D)
  X=cloud_speech_pb2.StreamingRecognitionConfig(config=n,single_utterance=False,interim_results=True)
  H=cloud_speech_pb2.StreamingRecognizeRequest(streaming_config=X)
  yield H
  R=None
  if(not filename)and(not audio_data):
   R=v.get_speech()
  elif not audio_data:
   R=v.load_audio(filename)
  else:
   R=v.load_audio_bin(audio_data)
  v.asr_callback("Ready!",False)
  for u in R:
   H=cloud_speech_pb2.StreamingRecognizeRequest(audio_content=u)
   yield H
 def asr(v,filename=None,audio_data=None):
  v.asr_callback("Connecting ...",False)
  J=[(b'api-key',v.api_key)]
  U=v.stub.StreamingRecognize(v.generate_messages(filename=filename,audio_data=audio_data),metadata=J)
  for V in U:
   if V.results:
    if V.results[0].alternatives:
     v.asr_callback(V.results[0].alternatives[0].transcript,V.results[0].is_final)

