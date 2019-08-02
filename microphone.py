import time
import speech_recognition as sr

class Microphone(object):
    '''
    手动选择“在线/离线模式”，使用蓝牙耳机（默认x3耳机)，持续收听并翻译，直到收到“terminate the programme”时退出程序
    '''

    def __init__(self,device_index=2):
        self.device_index=2
        self.r=sr.Recognizer()
        self.mic=sr.Microphone(device_index=self.device_index)
        self.mode='online'
        self.INSTRUMENTS_DICT=['knife', 'scissors','scissor', 'tweezers','tweezer', 'spoon']
        self.KEYWORDS=[['I want a knife',1.0],['I want a scissors',1.0],['I want a tweezers',1.0],['I want a spoon',1.0],['terminate the programme',1.0]]

    def list_microphone_names(self):
        # 查看可用microphone
        return sr.Microphone.list_microphone_names()

    def listen(self):
        '''
        使用microphone持续收听，收到特定指令时返回对应指令码。
        :return:respond list 指令码
        list[0]=='0':从surgeon手上取设备至对应区域
        list[0]=='1':根据list[1]具体工具，从器材区取工具给surgeon
            具体器具见self.INSTRUMENTS_DICT
        list[0]=='2':退出
        list[0]=='3':异常处理
        '''
        respond=['3','None']
        while(True):
            with self.mic as source:
                print("\nsay something -.-")
                audio = self.r.listen(source)

            print('recognizing...')
            if self.mode=='online':
                # recognize speech using Google Speech Recognition
                try:
                    result=self.r.recognize_google(audio)
                    print("Google: " + result)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                finally:
                    if 'result' not in locals():
                        result='not understand.'
            else:
                #offline mode
                # recognize speech using Sphinx
                try:

                    result = self.r.recognize_sphinx(audio)
                    print("Sphinx: " + result)
                except sr.UnknownValueError:
                    print("Sphinx could not understand audio")
                except sr.RequestError as e:
                    print("Sphinx error; {0}".format(e))
                finally:
                    if 'result' not in locals():
                        result='not understand.'

            for instrument in self.INSTRUMENTS_DICT:
                if instrument in result:
                    print("got it！here the "+instrument)

            if 'terminate' or 'terminator' in result:
                print("bye")
                break


