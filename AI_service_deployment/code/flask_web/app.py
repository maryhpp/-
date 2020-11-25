from flask import Flask, render_template, request, jsonify
import os
import time
from utils.utils import RedisUtils


# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg',  'jpeg','JPG', 'PNG', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)

# 设置静态文件缓存过期时间
# app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/recognize', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"code": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        split_filename = f.filename.rsplit('.', 1)
        new_filename = '{}_{}.{}'.format(split_filename[0], str(int(time.time()*1000000)), split_filename[1])   # 把原图片名加上时间戳，防止出现重名文件

        upload_path = os.path.join(basepath, 'static/images', new_filename)  # 注意：没有该文件夹要先创建，不然会提示没有该路径
        f.save(upload_path)     # 保存上传的图片

        redis_utils = RedisUtils()      # 初始化redis工具类
        task_value = {'path': upload_path, 'key': new_filename}     # 生成任务,key对应图片名称
        redis_utils.push_task(task_value)      # 任务下发到redis

        result = redis_utils.get_result(new_filename)   # 从redis中读取识别结果
        # time.sleep(5)
        # result = [{'name': 'f1', 'prob': 0.5}, {'name': 'f2', 'prob': 0.3}]
        if not isinstance(result, list):
            result = []
        return render_template('recognize_result.html', result=result, fn='./static/images/{}'.format(new_filename))
        # return jsonify({'result': result})    # rest api

    return render_template('recognize.html')


if __name__ == '__main__':
    app.run(debug=True)
