import socketserver  # 导入socketserver模块
import requests
import json
import datetime
import time

url = 'http://39.106.213.217:8080/api/product/'

class MyServer(socketserver.BaseRequestHandler):  # 创建一个类，继承自socketserver模块下的BaseRequestHandler类
    def handle(self):  # 要想实现并发效果必须重写父类中的handler方法，在此方法中实现服务端的逻辑代码（不用再写连接准备，包括bind()、listen()、accept()方法）
        while 1:
            conn = self.request
            addr = self.client_address
            # 上面两行代码，等于 conn,addr = socket.accept()，只不过在socketserver模块中已经替我们包装好了，还替我们包装了包括bind()、listen()、accept()方法
            while 1:
                accept_data = conn.recv(1024)
                print(accept_data)
                if accept_data == b'byebye':
                    break
                # rec = str(accept_data,'utf-8')
                if (accept_data[0] >= 65 and accept_data[0] <= 90) or (accept_data[0] >= 97 and accept_data[0] <= 122):
                    rec = str(accept_data, 'utf-8')
                    send_data = b'ok'
                    conn.sendall(send_data)
                else:
                    # 仅存储数据
                    rec = ''.join(hex(x) for x in accept_data)
                    r = post_test(rec,url)
                    # 存储数据，并解析
                    # rec = data_parse(accept_data)
                    # r = post(rec, url)
                    if r == None:
                        send_data = b'send error'
                    elif r.status_code == 404:
                        send_data = b'send 404'
                    elif r.status_code == 201:
                        send_data = b'send ok'
                    else:
                        send_data = b'unknown error'
                    conn.sendall(send_data)
                time.sleep(0.5)
            conn.close()

# 测试用post方法
def post_test(data,url):
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


# POST 方法
def post(data, url):
    postJson = {
        "hum": data['hum'],
        "temp":data['temp'],
        "hcho":data['hcho'],
        "pm2_5":data['pm2_5'],
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


# 数据解析
def data_parse(data_temp):
    data = {}
    flag = 0
    data['temp'] = (data_temp[flag + 6] <<8) + data_temp[flag + 5]
    data['hum'] = (data_temp[flag + 8] <<8) + data_temp[flag + 7]
    data['hcho'] = (data_temp[flag + 10] <<8) + data_temp[flag + 9]
    data['pm2_5'] = (data_temp[flag + 12] <<8) + data_temp[flag + 11]
    return data

if __name__ == '__main__':
    sever = socketserver.ThreadingTCPServer(("0.0.0.0", 8888),
                                            MyServer)  # 传入 端口地址 和 我们新建的继承自socketserver模块下的BaseRequestHandler类  实例化对象

    sever.serve_forever()  # 通过调用对象的serve_forever()方法来激活服务端
