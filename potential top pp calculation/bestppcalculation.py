def floatcheck(n):
    try:
        return float(n)
    except ValueError:
        floatcheck(input("Invalid, please retype: "))
rankedmaps=floatcheck(input("Number of ranked maps: "))
pppool=[]
#while True:
#    score=input("PP score: ")
#    if score=="end":
#        break
#    else:
#        pppool.append(floatcheck(score))
script=open("Untitled.txt","r")
scriptline=0
for line in script:
    if scriptline==0:
        pppool.append(float(line[-8:]))
        scriptline=1
    else:
        scriptline=0

#pplist=open("pplist.txt","r")
#linecount=0
#for line in pplist:
#    if linecount==0:
#        linecount=1
#        #xdddd I like meme
#    if linecount==1:
#        tempppvariable=int(line[

pppool.sort()
pppool.reverse()
print(len(pppool))
print(pppool)
pptotal=0
for i in range(0,len(pppool)):
    pptotal=pptotal+pppool[i]*(0.95**i)
print(pptotal)
print(round(pptotal+416.6667*(1-0.9994**rankedmaps),3))
    
    
    
