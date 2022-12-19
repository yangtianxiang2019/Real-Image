import base64
import datetime
import random
import time

from django.http import HttpResponse
import json
import logging
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger('django')


def test(request):
    return 'this is a test'


@csrf_exempt
def process_image(request):
    try:
        requestBody = json.loads(request.body)
        # check data
        if 'data' not in requestBody.keys():
            return errResponse('参数错误')
        data = requestBody['data']
        if 'file' not in data.keys():
            return errResponse('参数file不存在')
        file = data['file']
        if len(file) == 0:
            return errResponse('参数file格式不正确')
        # check file is base64 format
        if 'base64,' not in file:
            return errResponse('参数file不能为空')
        split_data = file.split(';base64,')
        if len(split_data) < 2:
            return errResponse('参数file格式错误')

        b64_data = split_data[1]
        data = base64.b64decode(b64_data)
        file_name = '%s_%s.%s' % (
        int(time.time()), random.randint(1, 1000), image_suffix(split_data[0]))
        today_path = str(datetime.date.today()) + '/'
        input_image_path = os.path.join(
            settings.BASE_IMAGE_DIR + '/input/' + today_path, file_name)
        output_image_path = settings.BASE_IMAGE_DIR + '/output/' + today_path

        if not os.path.exists(settings.BASE_IMAGE_DIR + '/input/' + today_path):
            os.mkdir(settings.BASE_IMAGE_DIR + '/input/' + today_path)
        if not os.path.exists(output_image_path):
            os.mkdir(output_image_path)

        with open(input_image_path, 'wb') as f:
            f.write(data)

        rs = os.system(
            'cd ' + settings.REAL_ESRGAN_PATH + ' && '
            + settings.PYTHON_PATH + ' inference_realesrgan.py -n RealESRGAN_x4plus -i '
            + input_image_path +
            ' -o ' + output_image_path + ' --suffix "" --fp32')
        if rs != 0:
            return errResponse('python图片处理程序失败')
        return response('success', {'file': '/process/media/' + today_path + file_name})
    except Exception as e:
        logger.error(e)
        return errResponse(e)


def image_suffix(s):
    return s.split('/')[1]


def errResponse(e):
    res = {"status": "0", "message": e}
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")


def response(e, data):
    res = {"status": "1", "message": e, "data": data}
    return HttpResponse(json.dumps(res, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")
