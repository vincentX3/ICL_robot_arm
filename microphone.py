import time
import speech_recognition as sr



'''
手动选择“在线/离线模式”，使用蓝牙耳机（默认x3耳机)，持续收听并翻译，直到收到“terminate the programme”时退出程序
'''
MODE='online'
INSTRUMENTS_DICT=['knife', 'scissors','scissor', 'tweezers','tweezer', 'spoon']
KEYWORDS=[['I want a knife',1.0],['I want a scissors',1.0],['I want a tweezers',1.0],['I want a spoon',1.0],['terminate the programme',1.0]]

r=sr.Recognizer()
# sr.Microphone.list_microphone_names() #查看可用microphone
mic=sr.Microphone(device_index=2)

while(True):
    with mic as source:
        print("\nsay something -.-")
        audio = r.listen(source)

    print('recognizing...')
    if MODE=='online':
        # recognize speech using Google Speech Recognition
        try:
            result=r.recognize_google(audio)
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

            result = r.recognize_sphinx(audio)
            print("Sphinx: " + result)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
        finally:
            if 'result' not in locals():
                result='not understand.'

    for instrument in INSTRUMENTS_DICT:
        if instrument in result:
            print("got it！here the "+instrument)

    if 'terminate' or 'terminator' in result:
        print("bye")
        break


