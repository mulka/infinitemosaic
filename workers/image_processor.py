#!/usr/bin/env python

from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TMP_DIR

# processes the image before hand
# 
import amqplib.client_0_8 as amqp
import simplejson as json
import S3
import mimetypes
from httplib import HTTPConnection
from urlparse import urlparse
from uuid import uuid1

from os import path, mkdir, rmdir
from subprocess import call
from hashlib import md5

#"metapixel-prepare" "-r" "source" "destination" "--width=48" "--height=48"

def hash(seed):
    m = md5()
    m.update(seed)
    return m.hexdigest()

class MsgWrapper(object):
    def __init__(self, message):
        self.body = message

def make_call(args):
    print(args)
    try:
        ret = call(args)
        if ret != 0:
            return False
        else:   
            return True
    except OSError:
        return False

def get_file(url):
    print("GET_FILE URL: %s" % url)
    url_hash = hash(url)
    url = urlparse(url)
    file_type = url.path[-3:]

    file_path = path.join(TMP_DIR, "%s.%s" % (url_hash, file_type))

    if file_type == "tar":
        end_file_path = path.join(TMP_DIR, "%s/" % url_hash)
    else:
        end_file_path = file_path

    if path.exists(end_file_path):
        if (file_type == "tar"
           and not path.exists(path.join(end_file_path, "tables.mxt"))):
            pass
        else:
            print("PATH EXISTS: %s" % end_file_path)
            return end_file_path

    conn = HTTPConnection(url.netloc)
    conn.request("GET", url.path)
    response = conn.getresponse()
    #check response codes

    data = response.read()
    file = open(file_path, "w")
    file.write(data)

    if file_type == "tar":
        print("UNTARING")

        try:
            mkdir(end_file_path)
        except OSError:
            rmdir(end_file_path)
            mkdir(end_file_path)

        if not make_call(["tar", "-xvpf", file_path, "-C", end_file_path]):
            print("Tar Failed")
            return False
        else:
            return end_file_path

    return file_path

def make_mosaic(in_file, image_collection, output_image, output_txt,
                scale=1, height=128, width=128):
    return make_call(["metapixel", "--metapixel", in_file, output_image, "-l", image_collection, "-s", str(scale),
                     "-h", str(height), "-w", str(width), "--out", output_txt])

def process_base_image(file_name):
    return True

def callback(msg):
    p_msg = json.loads(msg.body)

    image_collection_url = p_msg['image_collection_url']
    base_image_url = p_msg['base_image_url']
    bucket_name = p_msg['mosaic_bucket']
    mosaic_key = p_msg['mosaic_key']

    u1 = uuid1()
    u2 = uuid1()
    u3 = "%s+%s" % (u1, u2)
    output_image = path.join(TMP_DIR, "%s.jpg" % u3)
    output_txt = path.join(TMP_DIR, "%s.txt" % u3)

    base_file_name = get_file(base_image_url)
    process_base_image(base_file_name)
    image_collection = get_file(image_collection_url)
    print("Image Collection URL: %s" % image_collection_url)

    make_mosaic(base_file_name, image_collection, output_image, output_txt)

    s3_image = S3.S3Object(open(path.join(TMP_DIR, output_image), 'rb').read())
    s3_txt = S3.S3Object(open(path.join(TMP_DIR, output_txt), 'rb').read())

    conn = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    headers1 = {'x-amz-acl': 'public-read', 'Content-Type': "image/png"}
    conn.put(bucket_name, "%s.jpg" % mosaic_key, s3_image, headers1)

    headers2 = {'x-amz-acl': 'public-read', 'Content-Type': "text/plain"}
    conn.put(bucket_name, "%s.txt" % mosaic_key, s3_txt, headers2)
    
def main():
    parser = OptionParser()
    parser.add_option('--host', dest='host',
                        help='AMQP server to connect to (default: %default)',
                        default='localhost')
    parser.add_option('-u', '--userid', dest='userid',
                        help='userid to authenticate as (default: %default)',
                        default='guest')
    parser.add_option('-p', '--password', dest='password',
                        help='password to authenticate with (default: %default)',
                        default='guest')
    parser.add_option('--ssl', dest='ssl', action='store_true',
                        help='Enable SSL (default: not enabled)',
                        default=False)

    options, args = parser.parse_args()

    conn = amqp.Connection(options.host, userid=options.userid, password=options.password, ssl=options.ssl)

    ch = conn.channel()
    ch.access_request('/data', active=True, read=True)

    ch.exchange_declare('myfan', 'fanout', auto_delete=True)
    qname, _, _ = ch.queue_declare()
    ch.queue_bind(qname, 'myfan')
    ch.basic_consume(qname, callback=callback)

    #
    # Loop as long as the channel has callbacks registered
    #
    while ch.callbacks:
        ch.wait()

    ch.close()
    conn.close()

def test():
    message = MsgWrapper(json.dumps({
            'base_image_url': "http://farm4.static.flickr.com/3500/3262123066_b7c87c09ea_o.jpg",
            'image_collection_url': "http://infinitemosaic.com/prepared.tar",
            'mosaic_bucket': "infmos",
            'mosaic_key': "ssw2"
        }))
    callback(message)
 

if __name__ == '__main__':
    main()
