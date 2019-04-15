# -*- coding: UTF-8 -*-
#引入验证函数，时间模块和摄像头模块
from face_verification import *
from time import sleep
from picamera import PiCamera

#调用GPIO库，用于控制小灯
import RPi.GPIO as GPIO
#设置引脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)+
#设置可信度阈值
Threshold = 80

#设置相机，进行拍照
camera = PiCamera()
camera.resolution = (1024,768)
camera.start_preview()
sleep(2)
print 'taking photo...'
camera.capture('attempt.jpg')
print 'done!'
camera.stop_preview()

#调用验证函数
c=confidence('enrollment.jpg','attempt.jpg')
print 'confidence: '+str(c)

#根据结果控制小灯
if c>Threshold:
  #验证成功则常亮4s
	print 'Success!'
	GPIO.output(18,GPIO.HIGH)
	sleep(4)
	GPIO.output(18,GPIO.LOW)

if c<=Threshold:
  #验证失败则闪烁4s
	print 'Failed!'
	i=0
	while i<10:
		GPIO.output(18,GPIO.HIGH)
		sleep(0.2)
		GPIO.output(18,GPIO.LOW)
		sleep(0.2)
		i=i+1
GPIO.cleanup()
