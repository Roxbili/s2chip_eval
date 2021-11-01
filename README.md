# S2Chip 验证方案

不使用上位机，使用cv+tkinter显示：6-7帧  
使用上位机：
1. UDP：9帧
2. TCP：8帧(100Mbit/s网线), 15帧(1000Mbit/s网线)

因此，最终方案请看tcp文件夹。


## 文件夹介绍
tcp: 最终显示方案，使用tcp协议实现
udp：废弃的udp协议显示方案
useless: 一些废弃的显示类代码
tools: 工具文件夹，包含
- bram.py: bram读写操作，地址管理
- interaction.py: 和PL交互，是bram.py更高层次的接口
- utils.py: 提供如Log，Timer等功能性类

--------------------------------------------------------

## USB摄像头查询
```bash
ls -ltrh /dev/video*
```

## 摄像头权限问题
一般默认情况下，只有root用户和dialout组的用户会有读写的权限，所以可以将用户加入到dialout组中获取串口读取权限，**弄完用户需要重新登录**。

```bash
sudo usermod -a -G dialout {your_user_name}
```

还不行就用which python，用sudo运行吧，没办法了。

## 服务器一些命令

### root使用conda python执行脚本
用户下执行：
```bash
which python | xargs -I {} sudo {} main.py
```

### VNC server更高分辨率
```bash
vncserver -geometry 1600x1200 -randr 1600x1200,1440x900,1024x768
```


## zynq linux 配置等
用户：root
密码：root
VNC密码：root123

### rootf
linaro-jessie-alip-20161117-32.tar.gz

### 使用root就能登录ssh
设置`sshd_config`允许root登录：
```bash
vim /etc/ssh/sshd_config
```

修改`PermitRootLogin`：
```bash
PermitRootLogin yes
```

### VNC配置
1. 安装vnc
    ```bash
    sudo apt install tightvnserver
    sudo apt install xfce4 xfce4-goodies
    ```

2. 安装字体
    ```bash
    sudo apt install xfonts-base
    ```

3. 使用vncserver命令创建vnc，然后kill，然后修改配置文件
    ```bash
    vncserver
    vncserver -kill :1
    vim ~/.vnc/xstartup
    ```
    在最后添加
    ```bash
    startxfce4 &
    ```

4. 给root x-window访问权限(不确定是不是这个修好的，但应该是xhost命令，使用的时候基本都报错，但是莫名其妙好了)
    ```bash
    xhost LOCAL:root
    ```
    备选方案：
    ```bash
    xhost LOCAL:fanding
    xhost + root
    xhost +
    ```

### conda安装
使用Berryconda：https://github.com/jjhelmus/berryconda

### 图像显示问题
新建conda环境：
```bash
conda create -n s2chip python=3.6 opencv Pillow
```

Pillow底层显示调用系统图片软件，linaro这个文件系统里面没有，自己安装一个：
```bash
apt update
apt install imagemagick
```

Tkinter图像显示，canvas需要`pil的imagetk`库(根本不知道是下面哪一句话修好的),
[参考链接](https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/)：
*(不得不说，在cv2.show用不了的时候最佳的解决方案，因为几乎没有什么第三方库的支持)*
```bash
apt install python3-pil.imagetk
conda uninstall Pillow
pip install image
```