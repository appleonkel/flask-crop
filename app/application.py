from flask import Flask, send_from_directory, request, send_file
from thumbs import thumbnail
import os
import re

app = Flask(__name__)

MEDIA_ROOT=os.path.join('/tmp/test/')

@app.route('/<path:subpath>')
def get_image(subpath):
    # sanitize
    subpath = os.path.normpath(subpath)
    
    # Let the webserver handle this if
    if os.path.isfile(os.path.join(MEDIA_ROOT, subpath)):
        return send_from_directory(
            MEDIA_ROOT,
            subpath
        )

    # get size and original path
    p = re.compile(r'_(\d+)x(\d+)\.(\w+)$')
    m = p.search(subpath)
    filepath = os.path.join(
        MEDIA_ROOT, 
        subpath.replace(m.group(0), '.'+m.group(3))
    )
    if os.path.isfile(filepath):
        pic = thumbnail(filepath, m.group(1)+'x'+m.group(2))
        return send_file(pic)
    return '404'

if __name__ == '__main__':
    app.run()
