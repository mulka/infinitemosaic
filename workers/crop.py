#! /usr/local/bin/python
#

import Image
import string, sys

def usage():
    u = """crop.py infile outfile"""

if len(sys.argv) == 1:
    usage()
    sys.exit(0)

format = None
options = {"quality" : 100 }
convert = "L"

if len(sys.argv) != 2:
    usage()

try:
    im = Image.open(sys.argv[1])
    print im.size
    h, v = im.size
    small = min(h,v)
    large = max(h,v)
    offset = (large - small) / 2
    box = (offset, 0, offset + small, small)
    print box
    im = im.crop(box)

    im.draft(convert, im.size)
    im = im.convert(convert)
    im.thumbnail((640, 640), Image.ANTIALIAS)

    im.save('file_name.jpg', options)
except:
    print "cannot convert image",
    print "(%s:%s)" % (sys.exc_type, sys.exc_value)
