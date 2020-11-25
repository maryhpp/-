import redis
import json
import time

#建立redis连接，将decode_responses设置为True则是将结果由bytes解码为string
redis_con = redis.StrictRedis(decode_responses=True)


class RedisUtils:

    def __init__(self):
        self.con = redis_con
        self.task_list = 'image_recognize_task'

    def push_task(self, value):
        """下发图片识别任务到任务队列"""
        self.con.lpush(self.task_list, json.dumps(value))

    def get_task(self, max_num=1):
        """
        获取任务，可一次获取多个任务
        :param max_num: 最大任务数，默认是1
        :return: 任务列表
        """
        # self.con.brpop-->('image_recognize_task', '{"path": "/home/ubuntu/MyFiles/flask_web/static/images/ \
        # image_06687_1556105676710988.jpg", "key": "image_06687_1556105676710988.jpg"}')
        task = self.con.brpop(self.task_list)[1]  # 从redis队列获取任务，该方法会一直阻塞直到队列中有任务
        tasks = []
        # print(task)
        tasks.append(json.loads(task))
        for i in range(max_num - 1):
            task = self.con.lpop(self.task_list)
            if task:
                tasks.append(json.loads(task))
            else:
                break
        return tasks

    def save_result(self, result):
        """识别结果写入redis"""
        # result = json.dumps(result)
        key = result['key']
        value = result['result']
        #print(value)
        self.con.set(key, value, ex=60)    # 识别结果在redis中保留1分钟

    def get_result(self, key):
        """根据key（每次上传的图片都对应一个key），在redis中获取对应图片的识别结果，如果超过10s还没拿到结果则认为识别失败"""
        i = 1
        while i < 200:  # 若20*0.5s都未读到结果，return None
            result = self.con.get(key)
            if result:
                return eval(result)  # 将字符串转化为list
            time.sleep(0.5)
            i += 1
        return None


if __name__ == '__main__':
    pass
