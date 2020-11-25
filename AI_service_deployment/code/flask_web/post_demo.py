import requests


def post_demo():
    url = 'http://127.0.0.1:5000/recognize'
    files = {'file': ('test.png', open('static/images/image_04052_1556160963748259.jpg', 'rb'), 'image/png')}
    res = requests.post(url, files=files)
    print(res.text)
    return res


if __name__ == '__main__':
    post_demo()
