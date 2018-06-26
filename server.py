# -*- coding: utf-8 -*-
import socketserver  # 导入socketserver模块
import requests
import json
import time
import struct


url = 'http://39.106.213.217:8080/api/products/add/'
url_command = 'http://39.106.213.217:8080/api/command/'




class MyServer(socketserver.BaseRequestHandler):  # 创建一个类，继承自socketserver模块下的BaseRequestHandler类


    def handle(self):  # 要想实现并发效果必须重写父类中的handler方法，
        # 在此方法中实现服务端的逻辑代码（不用再写连接准备，包括bind()、listen()、accept()方法）
        while 1:
            print('开启等待')
            conn = self.request
            addr = self.client_address
            print('%s客户端已经连接，准备处理数据' % addr[0])
            # 上面两行代码，等于 conn,addr = socket.accept()，只不过在socketserver模块中已经替我们
            # 包装好了，还替我们包装了包括bind()、listen()、accept()方法
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
                    # rec = ''.join(hex(x) for x in accept_data)
                    # r = post_test(rec,url)
                    # 存储数据，并解析
                    if accept_data[0] == 0x10:
                        rec = data_parse(accept_data)
                        if(rec['head'] == 1):
                            print(">>>数据解析成功，下一步处理：")
                            if(rec['end'] == 5):  # 配置成功，通知数据库连接设备和用户
                                connect(rec['user'], rec['device'])
                                print(">>>>>配置设备和用户")
                            elif(rec['end'] == 0):
                                print(">>>>>>>与数据库通信")
                                content = post(productJSON(rec, addr[0]), url)
                        else:
                            content['r'] = None
                    time.sleep(1)
                    if content['r'] == None:
                        send_data = b'send error'
                        conn.sendall(send_data)
                    elif content['r'].status_code == 404:
                        send_data = b'send 404'
                        conn.sendall(send_data)
                    elif content['r'].status_code == 201 or content['r'].status_code == 200:
                        print(">>>>>>>>>>>>>查询控制信息")
                        get_control(conn, content['device'])
                        # send_data = b'send ok'
                    else:
                        send_data = b'unknown error'
                        conn.sendall(send_data)

                time.sleep(0.5)
            conn.close()


"""
---------------------------
    连接设备与用户
---------------------------
"""
def connect(user, device):
    url = "http://39.106.213.217:8080/api/connect/" + str(user) +"/"+ str(device) + "/"
    # 定义一些文件头
    headerdata = {
        "content-type": "application/json",
    }
    try:
        r = requests.get(url, headers=headerdata)  # 发送数据，json编码，添加定制头
        r.raise_for_status()  # 抛出异常
        # print(r.status_code)
    except requests.RequestException as e:
        print("----error-----")
        print(e)
        r = None
    finally:
        return r
"""
------------------------
    测试方法
------------------------
"""
# # 测试用post方法
# def post_test(data, url):
#     postJson = {
#         "testMessage": data
#     }
#     print(postJson)
#     # 定义需要进行发送的数据
#     postData = json.dumps(postJson)
#
#     # 定义一些文件头
#     headerdata = {
#         "content-type": "application/json",
#     }
#
#     # 接口  需按需求改动
#     # url = "http://127.0.0.1:8080/api/product/"
#
#     try:
#         r = requests.post(url, data=postData, headers=headerdata)  # 发送数据，json编码，添加定制头
#         r.raise_for_status()  # 抛出异常
#         # print(r.status_code)
#     except requests.RequestException as e:
#         print("----error-----")
#         print(e)
#         r = None
#     finally:
#         return r


"""
------------------------
    获取控制指令
------------------------
"""
def get_control(conn, device):
    url = "http://39.106.213.217:8080/api/control/" + str(device) + "/get/"
    # print("控制指令url为：", url)

    try:
        r = requests.get(url)
    except requests.RequestException as e:
        print("----error-----")
        print(e)
        r = None
    finally:
        # print("r=",r)
        if(r != None):
            send_control(json.loads(r.text), conn)


"""
--------------------------
    控制指令封装与发送下位机
    content['state'] 返回为 1，当前有指令，发送
                        为  0，当前无指令，不执行
--------------------------
"""
def send_control(content, conn):
    print(content)
    if(content['state'] == 1):  # 当前有指令
        top = content['control'] // 0xFF
        end = content['control'] %  0xFF
        # 封装命令
        print(">>当前有指令")
        command = [0x10, 0x02, content['state'], top, end,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x20]
        data = struct.pack("%dB"%(len(command)),*command)
        # control_command = '\\a' + str(content['control']) + '\\b'
        # print(control_command)
        # conn.sendall(bytes(control_command, encoding="utf8"))
        conn.sendall(data)
    else:
        print(">>当前无指令惹")
        command = [0x10, 0x02, content['state'], 0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x20]
        data = struct.pack("%dB" % (len(command)), *command)
        # conn.sendall(bytes('\\a0\\b',encoding="utf8"))
        conn.sendall(data)


"""
------------------------
    发送的设备信息JSON
------------------------
"""
def productJSON(data, address):
    postJson = {
        "message": address,
        "hum": data['hum'],
        "temp": data['temp'],
        "hcho": data['hcho'],
        "pm2_5": data['pm2_5'],
        "user": data['user'],
        "device": data['device'],
    }
    return postJson


"""
------------------------
    Email 邮箱警报
------------------------
"""
def EmailAlarm():
    url_alarm = 'http://39.106.213.217:8080/mail/mail/'
    url_hcho = 'http://39.106.213.217:8080/mail/hcho/'
    # 定义一些文件头
    headerdata = {
        "content-type": "text/html",
    }
    r = requests.get(url_hcho , headerdata)


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
    POST，向数据库发送
------------------------
"""
# POST 方法
def post(postJson, url):

    print(postJson)
    # 定义需要进行发送的数据
    postData = json.dumps(postJson)
    content = {}
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
        content['r'] = r
        content['device'] = postJson['device']
        return content

"""
-----------------------
    下位机数据解析
-----------------------
"""
# 数据解析
def data_parse(data_temp):
    data = {}
    flag = 0
    # print(data_temp[1])
    data['head'] = data_temp[flag + 1] // 16 # 方向位
    data['end'] = data_temp[flag + 1] % 16  # 类型位
    # 判断类型位
    if (data['end'] == 1):
        # 警报
        print('>>>>>>>这是条警报消息')
        data['alarm'] = 1
        EmailAlarm()
        r = post(noticeJSON("4"), url_command)
    elif(data['end'] == 5):
        # 配置消息
        data['alarm'] = 2
    else:
        # 正常数据
        data['alarm'] = 0
        data['temp'] = 1.0 * ((data_temp[flag + 6] << 8) + data_temp[flag + 5]) / 10
        data['hum'] = 1.0 * ((data_temp[flag + 8] << 8) + data_temp[flag + 7]) / 10
        data['hcho'] = (data_temp[flag + 10] << 8) + data_temp[flag + 9]
        data['pm2_5'] = (data_temp[flag + 12] << 8) + data_temp[flag + 11]
        data['user'] = data_temp[flag + 2]
        data['device'] = (data_temp[flag + 3] << 8) + data_temp[flag + 4]
    return data




if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 8888),
                                            MyServer,bind_and_activate = False)  # 传入 端口地址 和 我们新建的继承自
                                                            # socketserver模块下的BaseRequestHandler类  实例化对象
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    server.serve_forever()  # 通过调用对象的serve_forever()方法来激活服务端

