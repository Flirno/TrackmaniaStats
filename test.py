import urllib.request, json 

req = urllib.request('http://www.example.com/')
req.add_header('Referer', 'http://www.python.org/')
resp = urllib.urlopen(req)
content = resp.read()