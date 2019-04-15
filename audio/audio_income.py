# -*- coding: UTF-8 -*-
#调用httplib实现网络通信
import httplib
#调用json解析和打包json格式数据
import json
#调用pydub，wave，io进行音频格式转换
from pydub import AudioSegment
import wave 
import io
#调用RPi.GPIO控制小灯
import RPi.GPIO as GPIO

def audio_income(fileName):
  	#这里需要修改成自己的appKey和token
    print "configuring...\n"
    appKey = 'qmGczilTKT3s6CAQ'
    token = 'a7f32476ef3344768bfa32ad5f205e5f'
		#一句话识别url
    url = 'http://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'
    print "tranfering...\n"
    
    #音频格式转换
    trans_mp3_to_wav(fileName)
    audioFile = 'now.wav'
    format = 'pcm'
    sampleRate = 8000
    enablePunctuationPrediction  = True
    enableInverseTextNormalization = True
    enableVoiceDetection  = False

    request = url + '?appkey=' + appKey
    request = request + '&format=' + format
    request = request + '&sample_rate=' + str(sampleRate)
    if enablePunctuationPrediction :
            request = request + '&enable_punctuation_prediction=' + 'true'
    if enableInverseTextNormalization :
            request = request + '&enable_inverse_text_normalization=' + 'true'
    if enableVoiceDetection :
            request = request + '&enable_voice_detection=' + 'true'
    #print 'Request: ' + request
    print "waiting for response..."
		#发送请求，得到文本
    result=process(request, token, audioFile)
    print('Recognize result: ' + result)
    #根据结果控制小灯
    command(result)
	
def process(request, token, audioFile):
    # 读取音频文件
    with open(audioFile, mode='rb') as f:
        audioContent = f.read()
    host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    # 设置HTTP请求头部
    httpHeaders = {
        'X-NLS-Token': token,
        'Content-type': 'application/octet-stream',
        'Content-Length': len(audioContent)
    }
    # Python 2.x 请使用httplib
    conn = httplib.HTTPConnection(host)
    # Python 3.x 请使用http.client
    #conn = http.client.HTTPConnection(host)
    conn.request(method='POST', url=request,
                 body=audioContent, headers=httpHeaders)
    response = conn.getresponse()
    print('Response status and response reason:')
    print(response.status, response.reason)
    body = response.read()
    try:
        #print('Recognize response is:')
        body = json.loads(body)
        #print(body)
        status = body['status']
        if status == 20000000:
            result = body['result']
            return result
        else:
            print('Recognizer failed!')
    except ValueError:
        print('The response is not json format string')
    conn.close()

def trans_mp3_to_wav(file_path):
    song = AudioSegment.from_mp3(file_path)
    song.export("now.wav",format="wav")
    fp=open(file_path,'rb')
    data=fp.read()
    fp.close()
    print 'data read'
    #主要部分
    aud=io.BytesIO(data)
    sound=AudioSegment.from_file(aud,format='mp3')
    raw_data = sound._data
    print 'AudioSegment'
    #写入到文件，验证结果是否正确。
    l=len(raw_data)
    f=wave.open("now.wav",'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(8000)
    f.setnframes(l)
    f.writeframes(raw_data)
    f.close()
    print 'done'

def command(result):
    if u"开灯" in result:
        GPIO.output(18,GPIO.HIGH)
    if u"关灯" in result:
        GPIO.output(18,GPIO.LOW)
    
if __name__ == "__main__":
    audio_income("test.mp3")

