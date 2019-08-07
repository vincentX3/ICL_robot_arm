import time
import speech_recognition as sr
import pyaudio
import wave
class Microphone(object):
    '''
    手动选择“在线/离线模式”，使用蓝牙耳机（默认x3耳机)，持续收听并翻译，直到收到“terminate the programme”时退出程序
    '''

    def __init__(self):
        self.r=sr.Recognizer()
        self.mic=sr.Microphone(device_index=1)
        self.mode='online'
        self.ORDER_DICT=['here you are','come here','you are','are']
        self.INSTRUMENTS_DICT=['knife', 'fork', 'spoon']
        self.KEYWORDS=[['I want a knife',1.0],['I want a fork',1.0],['I want a spoon',1.0],['terminate the programme',1.0]]
        self.p = pyaudio.PyAudio() # instantiate PyAudio (1)

    def list_microphone_names(self):
        # 查看可用microphone
        return sr.Microphone.list_microphone_names()

    def set_Microphone(self,index):
        self.mic=sr.Microphone(index)

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
                self.feedback('alert')
                print("\nsay something -.-")
                audio = self.r.listen(source)

            print('recognizing...')
            self.feedback('waiting')
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
                        self.feedback('say_again')
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
                    self.feedback(instrument)
                    print("got it！here the "+instrument)
                    respond=['1',instrument]
                    return respond

            for order in self.ORDER_DICT:
                if order in result:
                    self.feedback('pick_from_hand')
                    print('Here I come~')
                    respond[0]='0'
                    return respond

            if ('terminate' in result) or ('terminator' in result):
                self.feedback('exit')
                print("bye")
                respond[0]='2'
                return respond

            self.feedback('say_again')

    def feedback(self, situation):
        voice_path={'alert':r'resource\start.wav'
            ,'say_again':r'resource\not_understand.wav'
            ,'exit':r'resource\Thankyou.wav'
            ,'pick_from_hand':r'resource\fetch.wav'
            ,'waiting':r'resource\recognizing.wav'
            ,'knife':r'resource\knife.wav'
            ,'fork':r'resource\fork.wav'
            ,'spoon':r'resource\spoon.wav'}
        CHUNK = 1024

        wf = wave.open(voice_path[situation], 'rb')

        # open stream (2)
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data
        data = wf.readframes(CHUNK)

        # play stream (3)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)

        # stop stream (4)
        stream.stop_stream()
        stream.close()

    def destory(self):
        # close PyAudio
        self.p.terminate()

if __name__=='__main__':
    mic=Microphone()
    # print(mic.list_microphone_names())
    # mic.set_Microphone(int(input("device index:")))
    mic.set_Microphone(1)
    respond=mic.listen()
    print(respond)
    while(respond[0]!='2'):
        respond=mic.listen()
        print(respond)
