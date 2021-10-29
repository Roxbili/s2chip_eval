#-*- encoding: utf-8 -*-

import socketserver
import numpy as np
import cv2
import time

class MyUdpHandler(socketserver.BaseRequestHandler):
    # def __init__(self, request, client_address, server):
    #     super(MyTcpHandler, self).__init__(request, client_address, server)
    #     self.data = ''

    def handle(self):
        # print('...received from:', self.client_address)
        while True:
            try:
                data, sock = self.request
                data = np.frombuffer(data, dtype=np.uint8)
                image = cv2.imdecode(data, cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # self.server.data = data

                # print(image.shape)
                # print(data.shape)
                # print(self.data_obj.data)

                cv2.imshow('video', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                print("Error:", e)
                break
            
            except KeyboardInterrupt:
                print('Connection close')
                break


            # data, sock = self.request
            # data = np.frombuffer(data, dtype=np.uint8)
            # image = cv2.imdecode(data, cv2.IMREAD_COLOR)
            # print(type(image))
            # print(self.data_obj.data)
            
if __name__ == '__main__':
    # HOST, PORT = "localhost", 6887     # 这里localhost务必换成本机ip地址，否则一般外部无法访问！！！！
    # HOST, PORT = "192.168.2.117", 6887     # 这里localhost务必换成本机ip地址，否则一般外部无法访问！！！！
    HOST, PORT = "192.168.2.166", 6887     # 这里localhost务必换成本机ip地址，否则一般外部无法访问！！！！
    udpSerSock = socketserver.ThreadingUDPServer((HOST, PORT), MyUdpHandler)
    # udpSerSock.data = '###'
    udpSerSock.daemon_threads = True    # 作为守护进程，主要是可以终止程序
    print('waiting for video...')

    try:
        udpSerSock.serve_forever()
    except:
        print("Connect failed.")
    finally:
        udpSerSock.server_close()
        print('Server close')
