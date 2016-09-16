import os
from flask import Flask, request, jsonify
import cv2
import numpy as np
import uuid

from flask import send_file

app = Flask(__name__)


@app.route("/")
def hello():
    return "into it POC server"


@app.route('/upload', methods=['POST'])
def upload_file():
    request_uuid = str(uuid.uuid1())
    pattern_file = request.files['pattern']
    website_file = request.files['webpage']
    pattern_filename = request_uuid + '_pattern.png'
    website_filename = request_uuid + '_webpage.png'
    pattern_file.save(os.path.join('uploaded_files', pattern_filename))
    website_file.save(os.path.join('uploaded_files', website_filename))
    pattern_file.close()
    website_file.close()
    result_file = find_result(request_uuid)
    return send_file(result_file, mimetype='image/png')


def find_result(request_uuid):
    img_rgb = cv2.imread('uploaded_files/' + request_uuid + '_webpage.png')
    pattern = cv2.imread('uploaded_files/' + request_uuid + '_pattern.png')
    h, w = pattern.shape[:-1]
    res = cv2.matchTemplate(img_rgb, pattern, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (10, 247, 49), 2)
    result_file = 'results/' + request_uuid + '_result.png'
    cv2.imwrite(result_file, img_rgb)
    return result_file

if __name__ == "__main__":
    app.run()