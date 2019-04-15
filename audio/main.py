# -*- coding: UTF-8 -*-

#调用web微信库itchat，实现树莓派的微信登陆
import itchat
from itchat.content import *
#调用自定义函数，处理数据，进行控制
from audio_income import *
from text_income import *
#调用GPIO库，用于控制小灯
import RPi.GPIO as GPIO
#设置引脚
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

#文字类消息处理
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    msg.user.send('%s: %s' % (msg.type, msg.text))
    text_income(msg.text)

#图片等消息处理
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.fileName='./cache/'+msg.fileName
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    #处理录音消息
    if msg.type == "Recording":
        print("Recieved a recording...")
        audio_income(msg.fileName)
    return '@%s@%s' % (typeSymbol, msg.fileName)

#设置登录模式，命令行二维码enableCmdQR = 2
itchat.auto_login(enableCmdQR = 2)
itchat.run(True)
