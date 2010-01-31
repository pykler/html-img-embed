'''
Script to embed imgs into html using base64 encode
'''

import sys
import base64
import re

imgsrc_re = re.compile(r'<img[^>]+src="([^ ]+)"', re.IGNORECASE)

f = sys.stdin
d = f.read()
n = []

last = 0
for m in imgsrc_re.finditer(d):
    uri = m.groups()[0]
    rep = m.group()
    start, end = m.span()
    n.append(d[last:start])
    imgtype = uri.split('.')[-1].lower() # simple img type inference
    with open(uri, 'r+') as imgf:
        n.append(rep.replace(uri, "data:image/%s;base64,%s" % (
            imgtype,
            base64.b64encode(imgf.read()))))
    last = end

print ''.join(n)
