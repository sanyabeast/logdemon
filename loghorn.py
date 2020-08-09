import sys
import urllib.request
import urllib.parse
import json
import time
argline=" ".join(sys.argv[1:len(sys.argv)])
args=argline.split("/")
url=None
source=None
text=None
color=None
if(len(args)>=1):url=args[0]
if(len(args)>=2):source=args[1]
if(len(args)>=3):text=args[2]
if(len(args)>=4):color=args[3]
if(url==None):
    print("unknown destination")
    sys.exit(1)
else:source=source if source!=None else"logcast anonymous"
text=text if text!=None else"..."
color=color if color!=None else"RED"
def send():
    payload={"event":"log","data":{"text":text,"source":source,"text_color":color}}
    full_url=f"http://{url}/{ urllib.parse.quote(json.dumps( payload ), safe='') }"
    try:urllib.request.urlopen(full_url).read()
    except Exception as e:print(str(e))
    
send()
sys.exit(1)