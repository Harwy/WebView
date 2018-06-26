# coding=utf-8
from socket import *
import requests
import json
import time

"""URL for API"""
url = 'http://39.106.213.217:8080/api/product/'
url_command = 'http://39.106.213.217:8080/api/command/'

tcpSocket = socket(AF_INET, SOCK_STREAM)

# 重复使用绑定信息,不必等待2MSL时间
tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

address = ('0.0.0.0', 8888)
tcpSocket.bind(address)

tcpSocket.listen(5)


"""
------------------------
    附加方法
------------------------
"""
# 测试用post方法
def post_test(data, url):
    postJson = {
        "testMessage": data
    }
    print(postJson)
    # 定义需要进行发送的数据
    postData = json.dumps(postJson)

    # 定义一些文件头
    headerdata = {
        "content-type": "application/json",
    }

    # 接口  需按需求改动
    # url = "http://127.0.0.1:8080/api/product/"

    try:
        r = requests.post(url, data=postData, headers=headerdata)  # 发送数据，json编码，添加定制头
        r.raise_for_status()  # 抛出异常
        print(r.status_code)
    except requests.RequestException as e:
        print("----error-----")
        print(e)
        r = None
    finally:
        return r


"""
------------------------
    设备信息JSON
------------------------
"""
def productJSON(data):
    if (data['alarm'] == 1):
        postJson = {
            "message": "alarm",
            "hum": data['hum'],
            "temp": data['temp'],
            "hcho": data['hcho'],
            "pm2_5": data['pm2_5'],
            "device": 5,
        }
    else:
        postJson = {
            "message": "normal",
            "hum": data['hum'],
            "temp": data['temp'],
            "hcho": data['hcho'],
            "pm2_5": data['pm2_5'],
            "device": 5,
        }
    return postJson


"""
------------------------
    Email 邮箱警报
------------------------
"""
def EmailAlarm():
    url_alarm = 'http://39.106.213.217:8080/mail/mail/'
    # 定义一些文件头
    headerdata = {
        "content-type": "text/html",
    }
    r = requests.get(url_alarm , headerdata)


"""
------------------------
    通知事件队列新增 警报
------------------------
"""
def noticeJSON(data):
    postJson = {
        "command": data,
    }
    return postJson



"""
------------------------
    POST
------------------------
"""
# POST 方法
def post(postJson, url):

    print(postJson)
    # 定义需要进行发送的数据
    postData = json.dumps(postJson)

    # 定义一些文件头
    headerdata = {
        "content-type": "application/json",
    }

    try:
        r = requests.post(url, data=postData, headers=headerdata)  # 发送数据，json编码，添加定制头
        r.raise_for_status()  # 抛出异常
        print(r.status_code)
    except requests.RequestException as e:
        print("----error-----")
        print(e)
        r = None
    finally:
        return r


# 数据解析
def data_parse(data_temp):
    data = {}
    flag = 0
    if (data_temp[1] % 16) == 1:
        data['alarm'] = 1
        EmailAlarm()
        r = post(noticeJSON("1"), url_command)
    else:
        data['alarm'] = 0
    data['temp'] = 1.0 * ((data_temp[flag + 6] <<8) + data_temp[flag + 5]) / 10
    data['hum'] = 1.0 * ((data_temp[flag + 8] <<8) + data_temp[flag + 7]) / 10
    data['hcho'] = (data_temp[flag + 10] <<8) + data_temp[flag + 9]
    data['pm2_5'] = (data_temp[flag + 12] <<8) + data_temp[flag + 11]
    return data



while True:
    time.sleep(0.01)
    print('开启等待')
    newData, newAddr = tcpSocket.accept()
    print('%s客户端已经连接，准备处理数据' % newAddr[0])
    try:
        while True:
            recvData = newData.recv(1024)
            if (recvData[0] >= 65 and recvData[0] <= 90) or (recvData[0] >= 97 and recvData[0] <= 122):
                rec = str(recvData, 'utf-8')
                send_data = b'ok'
                newData.sendall(send_data)
            else:
                rec = data_parse(recvData)
                r = post(productJSON(rec), url)
                if r == None:
                    send_data = b'send error'
                elif r.status_code == 404:
                    send_data = b'send 404'
                elif r.status_code == 201:
                    send_data = b'send ok'
                else:
                    send_data = b'unknown error'
                newData.sendall(send_data)
                print('%s客户端已经关闭' % newAddr[0])
            break
    finally:
        newData.close()

tcpSocket.close()