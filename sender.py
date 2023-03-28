# -*- coding=utf-8 -*-
# @Time : 2023/3/18 14:55
# @Author : mortallyn
# @File : sender.py
# @Software : PyCharm

import socket

# 创建UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 设置响应超时时间
client_socket.settimeout(1)

# 目标主机和端口
server_address = ('localhost', 5000)

# 数据帧
frames = ['frame1', 'frame2', 'frame3', 'frame4', 'frame5', 'frame6', 'frame7']

# 实现发送数据帧总数，注意这里假设第一次交流没有如何错误
total_frames = len(frames)
client_socket.sendto(str(total_frames).encode('utf-8'), server_address)

# 每个帧的大小
frame_size = 1024

# 滑动窗口大小
window_size = 3

# 窗口开始和结束位置
window_start = 0
window_end = window_size - 1
for i in range(window_start, window_end + 1):  # 先发送窗口内的帧
    data = frames[i].encode('utf-8')
    client_socket.sendto(data, server_address)

while True:
    # 接收帧
    try:
        response, server = client_socket.recvfrom(frame_size)
        status, num = response.decode('utf-8').split()
        num = int(num)
        if num == window_start + 1:  # 接收方成功收到
            print(f"\033[32mACK {num} success to send\033[0m")
            window_start += 1
            window_end += 1
            if window_end < len(frames):  # 发送下一个帧
                data = frames[window_end].encode('utf-8')
                client_socket.sendto(data, server_address)
            else:  # 所有帧都已发送，只是等待接收方确认
                window_end = len(frames) - 1
            if num == total_frames:  # 所有帧都已确认
                break
        else:
            print(f"ACK {window_start + 1} fail to send, resend...")
            for i in range(window_start, window_end + 1):  # 重发
                data = frames[i].encode('utf-8')
                client_socket.sendto(data, server_address)
    except socket.timeout:  # 超时
        print("Timeout")
        for i in range(window_start, window_end + 1):  # 重发
            data = frames[i].encode('utf-8')
            client_socket.sendto(data, server_address)
