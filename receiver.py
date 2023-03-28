# -*- coding=utf-8 -*-
# @Time : 2023/3/18 14:55
# @Author : mortallyn
# @File : receiver.py
# @Software : PyCharm
import random
import socket
import time

# 创建UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

random.seed(time.time())
# 监听地址和端口
server_address = ('localhost', 5000)
server_socket.bind(server_address)
# 接收数据帧总数，注意这里假设第一次交流没有如何错误
total_frames = int(server_socket.recvfrom(1024)[0].decode('utf-8'))

num = 0

# 等待接收数据帧
while True:
    data, client = server_socket.recvfrom(1024)
    # 模拟超时
    if random.random() < 0.2:
        time.sleep(1)
        print("Timeout")
        continue

    # 模拟帧错误率
    if random.random() < 0.2:
        print(f"Frame {data.decode('utf-8')} is corrupted")
    else:  # 帧正确
        if int(data.decode('utf-8').split('frame')[1]) != num + 1:  # 帧序号错误
            print(f"Frame {data.decode('utf-8')} is out of order")
        else:
            # 把数据送上上层
            print(f"\033[32mFrame {data.decode('utf-8')} received successfully, sending ACK...\033[0m")
            num += 1
    server_socket.sendto(f"ACK {num}".encode('utf-8'), client)
    if num == total_frames:
        break
