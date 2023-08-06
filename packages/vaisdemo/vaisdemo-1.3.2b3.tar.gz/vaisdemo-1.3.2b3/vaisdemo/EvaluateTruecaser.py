from vaisdemo.Truecaser import*
import pickle
import os
import time
import string
class MyTrueCaser():
 def __init__(J):
  J.uniDist=None
  J.backwardBiDist=None
  J.forwardBiDist=None
  J.trigramDist=None
  J.wordCasingLookup=None
 def evaluateTrueCaser(J,sentence):
  if not J.uniDist:
   print("TrueCaser model is not loaded. Skip!")
   return sentence
  e=0
  K=0
  Q=sentence.lower().split()
  A=[token for token in Q]
  q=getTrueCase(A,'title',J.wordCasingLookup,J.uniDist,J.backwardBiDist,J.forwardBiDist,J.trigramDist)
  return " ".join(q)
 def load_model(J):
  time.sleep(5)
  c=os.path.dirname(os.path.abspath(__file__))
  U=os.path.join(c,'distributions.obj')
  if os.path.exists(U):
   f=open(U,'rb')
   J.wordCasingLookup=pickle.load(f)
   J.uniDist=pickle.load(f)
   J.backwardBiDist=pickle.load(f)
   J.forwardBiDist=pickle.load(f)
   f.close()

