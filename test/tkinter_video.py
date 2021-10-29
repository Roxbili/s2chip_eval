import cv2
import numpy as np
import tkinter
from PIL import Image, ImageTk
import time

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # 打开video source
        self.vid = MyVideoCapture(video_source)

        # 创建FPS监测器
        self.frame_rate_monitor = FrameRateMonitor()

        # FPS TK组件
        self.fps_var = tkinter.StringVar()
        self.fps_var.set('fps: None')
        self.fps_label = tkinter.Label(window)
        self.fps_label.config(textvariable=self.fps_var, font=("Times", 15, 'bold'))
        self.fps_label.pack()

        # 创建能够容纳上面视频大小的画布
        # self.canvas = tkinter.Canvas(window, width=640, height=480)
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)  # illegal instruction(float不支持，换成int解决)
        self.canvas.pack()

        self.delay = 1
        self.update()

        self.window.mainloop()

    def update(self):
        # 获得frame
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        # 获得fps
        fps = self.frame_rate_monitor.get_fps()
        if fps != None:
            self.fps_var.set('fps: {}'.format(fps))

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open vidio source, make sure /dev/video{} existed.".format(video_source))

        # 获得摄像头采集的高和宽(注意转成int，否则报错非法指令)
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # 返回获得视频帧成功标记位和RGB格式的frame(读取到的frame是BGR格式)
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA))
            else:
                return (ret, None)


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
    App(tkinter.Tk(), "Tkinter and OpenCV")