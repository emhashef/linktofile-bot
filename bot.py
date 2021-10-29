from sys import path
path.append('..')
from client import Client
from os.path import getsize
import ntpath
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from urllib.parse import urlparse
import os
import cgi
import uuid
import sys

bot_token = 'wlLNGViL8f2csG5I3m3v00ayia2CyvoWU05ai0qiaBT1vdrVOdrT0lahwViZrqhjUV9exO39p1xFdMuwg0Fnibkrra2dg-rEZ2P1WnXqGBfxH5U2gK-zTH1LnK6KEB18JekA2Od0-pxnY6rf'

bot = Client(bot_token)

last_percent = 0

def upload_file(message):
    global last_percent

    file = requests.get(message['body'], stream=True)
    content_size = int(file.headers['Content-Length'])

    value, params = cgi.parse_header(file.headers.get('Content-Disposition',''))

    file_name = params.get('filename') or os.path.basename(urlparse(message['body']).path) or uuid.uuid4()

    file_name = str(file_name)

    last_percent = 0

    def monitor_callback(monitor):
        global last_percent
        percent = (monitor.bytes_read / content_size) * 100

        sys.stdout.write("\r" + '{:05.2f} %'.format(percent))
        sys.stdout.flush()

        
        if(last_percent + 20 <= percent):
            bot.send_message({
                **message,
                'body' : '{:.2f} درصد'.format(percent)
            })

            last_percent = percent

    with file.raw as f:
        f.len = content_size

        e = MultipartEncoder({
            'file' : (file_name, f)
        })

        m = MultipartEncoderMonitor(e, monitor_callback)

        [error, url] = bot.upload_file_raw(m, {'Content-Type': m.content_type})

    return [url, content_size, file_name]



messages = bot.get_messages()
for message in messages:
    print("New message from {} \nType: {}\nBody: {}".format(message['from'], message['type'], message['body']))
    message['to'] = message['from']
    message.pop('from')
    message.pop('time')




    [url, content_size, file_name] = upload_file(message)

    [error, success] = bot.send_attachment(message['to'], url, file_name,content_size, caption='Your File')

    if success:
        print('Message sent successfully')
    else:
        print('Sending message failed: {}' .format(error))
