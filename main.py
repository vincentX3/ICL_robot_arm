'''
总控台
'''
from configuration import *

class PickAndPlace(object):
    # 属性

    def __init__(self):
        #初始化microphone 类
        self.microphone=Microphone()
        # self.microphone.set_Microphone(1)  #选择microphone
        #机械臂：初始化串口
        #摄像头初始化
    def run(self):
        respond=[]
        while(True):
            respond=self.microphone.listen()
            if respond[0]=='0':
                self.pipeline_from_hand()
            elif respond[0]=='1':
                self.pipeline_to_hand(respond[1])
            elif respond[0]=='2':
                return 

    def pipeline_from_hand(self):
        pass

    def pipeline_to_hand(self,class_name):
        pass

    def log(self):
        pass

if __name__=='__main__':
    pap=PickAndPlace()
    pap.run()

