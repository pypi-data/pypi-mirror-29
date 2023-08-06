from auditok import ADSFactory,AudioEnergyValidator,StreamTokenizer,player_for,dataset
from auditok.io import PyAudioSource,BufferAudioSource,StdinAudioSource,player_for
import operator
import os
from collections import OrderedDict
from pydub import AudioSegment
import sys
from threading import Thread
import threading
import time
from queue import Queue,Empty
import vaisdemo.vais as vais
import logging
import site
for l in site.getsitepackages():
 e=os.path.dirname(sys.executable)
 print("Setting path")
 os.environ["PATH"]+=os.pathsep+e
 os.environ["PATH"]+=os.pathsep+os.path.join(e,"Scripts")
 os.system("ffmpeg")
def file_to_audio_source(filename,filetype=None,**z):
 w=filename.lower()
 D=False
 if filetype is not None:
  filetype=filetype.lower()
 if filetype=="raw" or(filetype is None and w.endswith(".raw")):
  a=z.pop("sampling_rate",None)
  if a is None:
   a=z.pop("sr",None)
  g=z.pop("sample_width",None)
  if g is None:
   g=z.pop("sw",None)
  ch=z.pop("channels",None)
  if ch is None:
   ch=z.pop("ch",None)
  if None in(g,a,ch):
   raise Exception("All audio parameters are required for raw data")
  d=open(filename).read()
  D=True
 x=z.pop("use_channel",None)
 if x is None:
  x=z.pop("uc",None)
 if x is None:
  x=1
 else:
  try:
   x=int(x)
  except ValueError:
   pass
 if not isinstance(x,(int))and not x.lower()in["left","right","mix"]:
  raise ValueError("channel must be an integer or one of 'left', 'right' or 'mix'")
 N=None
 if D:
  N=AudioSegment(d,sample_width=g,frame_rate=a,channels=ch)
 if filetype in("wave","wav")or(filetype is None and w.endswith(".wav")):
  N=AudioSegment.from_wav(filename)
 elif filetype=="mp3" or(filetype is None and w.endswith(".mp3")):
  N=AudioSegment.from_mp3(filename)
 elif filetype=="ogg" or(filetype is None and w.endswith(".ogg")):
  N=AudioSegment.from_ogg(filename)
 elif filetype=="flv" or(filetype is None and w.endswith(".flv")):
  N=AudioSegment.from_flv(filename)
 else:
  N=AudioSegment.from_file(filename)
 if N.channels>1:
  if isinstance(x,int):
   if x>N.channels:
    raise ValueError("Can not use channel '{0}', audio file has only {1} channels".format(x,N.channels))
   else:
    N=N.split_to_mono()[x-1]
  else:
   q=x.lower()
   if q=="mix":
    N=N.set_channels(1)
   elif x.lower()=="left":
    N=N.split_to_mono()[0]
   elif x.lower()=="right":
    N=N.split_to_mono()[1]
 if N.frame_rate<16000:
  raise Exception("Audio frame_rate is %d which is below 16000"%(N.frame_rate))
 if N.frame_rate>16000:
  print("Downsampling from %d to 16000"%(N.frame_rate))
  N=N.set_frame_rate(16000)
 if N.sample_width!=2:
  print("Convert sample with from %d to 2"%(N.sample_width))
  N=N.set_sample_width(2)
 Q=len(N)/float(60000)
 if Q>4.5:
  print("Audio length: ",Q)
  raise Exception("Audio too long")
 return v(data_buffer=N._data,sampling_rate=N.frame_rate,sample_width=N.sample_width,channels=N.channels)
class t(Thread):
 def __init__(R,timeout=0.2):
  R.timeout=timeout
  R.logger=None
  if sys.executable.endswith("pythonw.exe"):
   sys.stdout=open(os.devnull,"w");
   sys.stderr=open(os.path.join(os.getenv("TEMP"),"stderr-"+os.path.basename(sys.argv[0])),"w")
  else:
   R.logger=logging.getLogger(__name__)
  R._inbox=B()
  R._stop_request=B()
  Thread.__init__(R)
 def debug_message(R,m):
  if R.logger:
   R.logger.debug(m)
 def _stop_requested(R):
  try:
   m=R._stop_request.get_nowait()
   if m=="stop":
    return True
  except Empty:
   return False
 def stop(R):
  R._stop_request.put("stop")
  if R.isAlive():
   R.join()
 def send(R,m):
  R._inbox.put(m)
 def _get_message(R):
  try:
   m=R._inbox.get(timeout=R.timeout)
   return m
  except Empty:
   return None
class TokenizerWorker(t):
 T="END_OF_PROCESSING"
 def __init__(R,K,b,C,j):
  R.ads=K
  R.tokenizer=b
  R.analysis_window=C
  R.observer=j
  R._inbox=B()
  R.count=0
  t.__init__(R)
 def run(R):
  def notify_observers(d,start,end):
   S=b''.join(d)
   R.count+=1
   s=start*R.analysis_window
   i=(end+1)*R.analysis_window
   u=(end-start+1)*R.analysis_window
   R.observer.notify({"id":R.count,"audio_data":S,"start":start,"end":end,"start_time":s,"end_time":i,"duration":u})
  R.ads.open()
  R.tokenizer.tokenize(data_source=self,callback=notify_observers)
  R.observer.notify(TokenizerWorker.END_OF_PROCESSING)
 def read(R):
  if R._stop_requested():
   return None
  else:
   return R.ads.read()
class TokenSaverWorker(t):
 def __init__(R,L,timeout=0.2,callback=None,**z):
  R.kwargs=z
  R.max_asr_thread=7
  R.total_data=0
  R.api_key=L
  R.callback=callback
  R.asr_queue=B()
  R.data_queue=B()
  R.results=J()
  R.stop_request=False
  t.__init__(R,timeout=timeout)
 def run_asr(R,W,A,S):
  def on_result(f,is_final):
   if is_final:
    if f:
     f=f.replace("<SPOKEN_NOISE>","").strip()
     if W not in R.results:
      R.results[W]=[A,[f]]
     else:
      R.results[W][1].append(f)
  with vais.VaisService(R.api_key,record=False)as r:
   r.asr_callback=on_result
   r.asr(audio_data=audio_data)
  if W in R.results:
   R.results[W][1]=" ".join(R.results[W][1])
 def do_the_work(R):
  P=[]
  try:
   while True:
    try:
     W,A,S=R.data_queue.get(timeout=1)
     if W is None:
      break
    except Empty:
     continue
    if R._stop_requested()or R.stop_request:
     R.debug_message({"status":"Got stop request"})
     R.stop_request=True
     break
    R.debug_message({"status":"queue new asr session","start_time":W})
    R.run_asr(W,A,S)
    R.data_queue.task_done()
    if R.callback:
     P=[]
     V=100*float(R.total_data-R.data_queue.qsize())/R.total_data
     for s,(e,f)in R.results.items():
      if isinstance(f,list):
       f=" ".join(f)
      P.append("--> %s ..."%(f[:40]))
     R.callback(V,"\n".join(P[-10:]))
  except Exception as e:
   R.debug_message({"status":e})
  R.asr_queue.task_done()
 def run(R):
  R.asr_queue=B()
  for i in range(R.max_asr_thread):
   t=Thread(target=R.do_the_work)
   t.daemon=True
   t.start()
   R.asr_queue.put(t)
  k=time.time()
  while True:
   if R._stop_requested():
    break
   m=R._get_message()
   if m is not None:
    if m==TokenizerWorker.END_OF_PROCESSING:
     break
    S=m.pop("audio_data",None)
    s=m.pop("start_time",None)
    i=m.pop("end_time",None)
    O=m.pop("id",None)
    R.debug_message({"status":"new segment %.2f %.2f"%(s,i)})
    R.data_queue.put((s,i,S))
  for i in range(R.max_asr_thread):
   R.data_queue.put((None,None,None))
  R.asr_queue.join()
  o=time.time()
  R.callback(100,"Done! Spent %.2fs"%(o-k),is_finished=True)
 def notify(R,m):
  R.total_data+=1
  R.send(m)
def segment_audio(fname,L,energy_threshold=50,min_duration=0.2,max_duration=20,max_silence=0.3,callback=None):
 Y=None
 h=[]
 j=TokenSaverWorker(L,callback=callback)
 C=0.01
 y=None
 try:
  y=file_to_audio_source(fname)
 except Exception as e:
  callback(-1,"File audio không được hỗ trợ, hoặc độ dài quá 4 phút!",False)
  return None,None
 K=ADSFactory.ads(audio_source=y,block_dur=C,max_time=None,record=False)
 c=AudioEnergyValidator(sample_width=y.get_sample_width(),energy_threshold=energy_threshold)
 U=0
 n=1./C
 b=StreamTokenizer(validator=c,min_length=min_duration*n,max_length=int(max_duration*n),max_continuous_silence=max_silence*n,mode=U)
 Y=TokenizerWorker(K,b,C,j)
 return Y,j
if __name__=="__main__":
 d=segment_audio("/home/truong-d/work/vais/vlsp18/wav/002192e360_4m.wav","demo","output.csv")

