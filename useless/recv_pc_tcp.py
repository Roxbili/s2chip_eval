#-*- encoding: utf-8 -*-

import socketserver
import numpy as np
import cv2
import time
import sys

class MyTcpHandler(socketserver.BaseRequestHandler):
    # def __init__(self, request, client_address, server):
    #     super(MyTcpHandler, self).__init__(request, client_address, server)
    #     self.data = ''

    def handle(self):
        print('...connected from:', self.client_address)
        frame_rate_monitor = FrameRateMonitor()
        while True:
            try:
                data = self.request.recv(1024 * 100)
                data = np.frombuffer(data, dtype=np.uint8)
                image = cv2.imdecode(data, cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # self.server.data = data

                # print(image.shape)
                # print(data.shape)
                # print(self.data_obj.data)

                fps = frame_rate_monitor.get_fps()
                if fps != None:
                    print(fps)

                # cv2.imshow('video', data)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

            except Exception as e:
                print("Error:", e)
                break
            
            except KeyboardInterrupt:
                print('Connection close')
                break


class FrameRateMonitor:
    '''使用平均采样法统计帧率'''
    def __init__(self):
        self.avg_time = 0.0
        self.alpha = 1 / 100.   # 采样率
        self.last_time = None   # 上一次统计开始时间

    def get_fps(self):
        if self.last_time is None:
            self.last_time = time.time()
            return None
        
        current_time = time.time()
        if self.avg_time == 0:
            self.avg_time = current_time - self.last_time
        else:
            self.avg_time = self.avg_time * (1 - self.alpha) + (current_time - self.last_time) * self.alpha
        self.last_time = current_time

        fps = round(1. / self.avg_time)
        return fps
        

if __name__ == '__main__':
    # HOST, PORT = "localhost", 6887     # 这里localhost务必换成本机ip地址，否则一般外部无法访问！！！！
    # HOST, PORT = "192.168.2.117", 6887     # 这里localhost务必换成本机ip地址，否则一般外部无法访问！！！！
    HOST, PORT = "192.168.2.166", 6887     # 这里localhost务必换成本机ip地址，否则一般外部无法访问！！！！
    tcpSerSock = socketserver.ThreadingTCPServer((HOST, PORT), MyTcpHandler)
    # tcpSerSock.data = '###'
    tcpSerSock.daemon_threads = True    # 作为守护进程，主要是可以终止程序
    print('waiting for conneting...')

    try:
        tcpSerSock.serve_forever()
    except:
        print("Connect failed.")
    finally:
        tcpSerSock.server_close()
        print('Server close')
