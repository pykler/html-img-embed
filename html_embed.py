'''
Script to embed imgs into html using base64 encode
'''

import os
import sys
import base64
import re
from urllib2 import urlopen as _urlopen

from contextlib import contextmanager

imgsrc_re = re.compile(r'<img[^>]+src="([^ ]+)"', re.IGNORECASE)
img_na = 'data:image/png;base64,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'

class ReadException(Exception):
    pass

@contextmanager
def urlopen(*args, **kwargs):
    f = _urlopen(*args, **kwargs)
    try:
        yield f
    finally:
        f.close()

def fread(fn):
    '''
    Attempt to read a file, local or a web url and return its contents
    Returns a tuple (s,rfn) where s is the file contents and rfn is the real fn
    (NOTE: rfn may != fn if there were any web redirects)
    '''
    rfn = fn
    for openfunc in open,urlopen:
        try:
            with openfunc(fn) as f:
                s = f.read()
                if openfunc is urlopen:
                    rfn = f.url
                return s,rfn
        except (ValueError,IOError):
            pass
    raise ReadException("Couldn't open file '%s' (not url or local file)" %fn)

def b64img(uri, baseuri):
    '''
    Download and base64 encode the img at `uri`
    `baseuri` is the uri of the original
    '''
    if uri.startswith('.'):
        furi = '/'.join([baseuri, uri])
    else:
        furi = uri
    return base64.b64encode(fread(furi)[0])

def process_html(d, uri):
    '''
    Embed images into the html represented by string `d`
    `uri` is the uri of the file represented in string d
    '''
    bdir = os.path.dirname(uri) or '.'
    n = []
    last = 0
    for m in imgsrc_re.finditer(d):
        uri = m.groups()[0]
        rep = m.group()
        start, end = m.span()
        n.append(d[last:start])
        imgtype = os.path.splitext(uri)[1].strip('.').lower() # simple img type inference
        try:
            n.append(rep.replace(uri, "data:image/%s;base64,%s" % (
                imgtype,
                b64img(uri, bdir))))
        except ReadException:
            n.append(rep.replace(uri, img_na))
        last = end
    return ''.join(n)

def main():
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        d,fn = fread(fn)
    else:
        d = sys.stdin.read()
        fn = './'
    print process_html(d, fn)

if __name__ == '__main__':
    main()
