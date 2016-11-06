import urllib.request
import time
timer=60
realtimer=0
while True:
    if timer==60:
        timer=0
        try:
            print(urllib.request.urlopen("http://google.com",data=None))
            print("Internet alive at {} minutes.".format(realtimer/60))
        except:
            print("Error at {} minutes.".format(realtimer/60))
    time.sleep(1)
    timer=timer+1
    realtimer=realtimer+1
            
            
    
