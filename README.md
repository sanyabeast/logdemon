
# LOGDEMON
Easy-to-use python-based websocket`s text-logging server

## Launching Server

```
py logdemon.py --ws localhost:8001 --http localhost:8002
```

## Opening Logcat dashboard
Just open ```logcat.html``` and specify host and port at metworking settings (wi-fi button)

## Requesting log via command line
execute ```longhorn.py``` script with such argument pattern:
```
py loghorn.py httpserverhost:httpserverport/context/text/color
```
e.g:
```
py loghorn.py localhost:8716/Rihanna/Shine Bright Like a Diamond!/BLUE
```
color is an optional part of argument query

## Requesting log using other ways
Using XMLHttpREquest (JS)
```javascript
let x = new XMLHttpRequest()
x.open("get", `localhost:8002/${JSON.stringify({
  "event": "log",
  "source: "Rihanna",
  "data":{
    "text": "Shine Bright Like a Diamond!",
    "text_color": "BLUE"
  }
})}`)
x.send()
```
