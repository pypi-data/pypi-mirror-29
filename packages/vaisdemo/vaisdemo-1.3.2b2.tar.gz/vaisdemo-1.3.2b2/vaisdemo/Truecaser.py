import string
import math
def getScore(I,S,C,wordCasingLookup,K,G,R,f):
 v=5.0
 W=0
 i=K[S]+v
 x=0
 for E in wordCasingLookup[S.lower()]:
  x+=K[E]+v
 o=i/x
 W=math.log(o)
 X=1
 if G:
  if I!=None:
   i=G[I+'_'+S]+v
   x=0
   for E in wordCasingLookup[S.lower()]:
    x+=G[I+'_'+E]+v
   X=i/x
  W+=math.log(X)
 a=1
 if R:
  if C!=None:
   C=C.lower()
   i=R[S+"_"+C]+v
   x=0
   for E in wordCasingLookup[S.lower()]:
    x+=R[E+"_"+C]+v
   a=i/x
  W+=math.log(a)
 z=1
 if f:
  if I!=None and C!=None:
   C=C.lower()
   i=f[I+"_"+S+"_"+C]+v
   x=0
   for E in wordCasingLookup[S.lower()]:
    x+=f[I+"_"+E+"_"+C]+v
   z=i/x
  W+=math.log(z)
 return W
def getTrueCase(tokens,outOfVocabularyTokenOption,wordCasingLookup,K,G,R,f):
 Q=[]
 for P in range(len(tokens)):
  F=tokens[P]
  if F in string.punctuation or F.isdigit():
   Q.append(F)
  else:
   if F in wordCasingLookup:
    if len(wordCasingLookup[F])==1:
     Q.append(list(wordCasingLookup[F])[0])
    else:
     I=Q[P-1]if P>0 else None
     C=tokens[P+1]if P<len(tokens)-1 else None
     j=None
     d=float("-inf")
     for S in wordCasingLookup[F]:
      D=getScore(I,S,C,wordCasingLookup,K,G,R,f)
      if D>d:
       j=S
       d=D
     Q.append(j)
    if P==0:
     Q[0]=Q[0].title();
   else:
    if outOfVocabularyTokenOption=='title':
     Q.append(F.title())
    elif outOfVocabularyTokenOption=='lower':
     Q.append(F.lower())
    else:
     Q.append(F)
 return Q

