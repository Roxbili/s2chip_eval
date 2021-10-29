import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
from tkinter_video import FrameRateMonitor

def read_usb_capture(camera_index):
    # 选择摄像头的编号
    cap = cv2.VideoCapture(camera_index)
    print('cap opened status: {}'.format(cap.isOpened()))
    # 添加这句是可以用鼠标拖动弹出的窗体
    cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)
    while(cap.isOpened()):
        # 读取摄像头的画面
        ret, frame = cap.read() # 和cv.imread的BGR是一样的格式
        # 真实图
        cv2.imshow('real_img', frame)
        # 按下'q'就退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放画面
    cap.release()
    cv2.destroyAllWindows()

def read_usb_capture_matplotlib(camera_index):
    # 选择摄像头的编号
    cap = cv2.VideoCapture(camera_index)
    print('cap opened status: {}'.format(cap.isOpened()))

    # 读取摄像头的画面
    ret, frame = cap.read()
    image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

    plt.imshow(image)
    plt.show()

def read_usb_capture_PIL(camera_index):
    # 选择摄像头的编号
    cap = cv2.VideoCapture(camera_index)
    print('cap opened status: {}'.format(cap.isOpened()))

    # while(cap.isOpened()):
    for i in range(3):
        # 读取摄像头的画面
        ret, frame = cap.read()

        image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        image.show()
        plt.show()
        break

def fps_without_show(camera_index):
    # 选择摄像头的编号
    cap = cv2.VideoCapture(camera_index)
    print('cap opened status: {}'.format(cap.isOpened()))

    # 读取摄像头的画面
    frame_rate_monitor = FrameRateMonitor()

    while(cap.isOpened()):
        ret, frame = cap.read()
        print(frame.shape, frame.dtype, frame.nbytes)
        fps = frame_rate_monitor.get_fps()
        if fps != None:
            print(fps)


if __name__ == '__main__':
    # read_usb_capture(0)
    # read_usb_capture_matplotlib(0)
    # read_usb_capture_PIL(0)
    fps_without_show(0)