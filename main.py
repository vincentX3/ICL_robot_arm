'''
总控台v1，无误差修正版本
'''
from configuration import *

class PickAndPlace(object):
    # 属性

    def __init__(self):
        #初始化microphone 类
        self.microphone=Microphone()
        # self.microphone.set_Microphone(1)  #选择microphone
        #机械臂：初始化串口
        self.console=robot_console()
        #摄像头初始化
        self.camera=Camera()

    def run(self):
        '''
        运行系统
        :return:
        '''
        respond=[]
        while(True):
            respond=self.microphone.listen()
            if respond[0]=='0':
                #从医生手上取工具
                self.pipeline_from_hand()
            elif respond[0]=='1':
                #取对应工具给医生
                self.pipeline_to_hand(respond[1])
            elif respond[0]=='2':
                #退出程序
                return 

    def pipeline_from_hand(self):
        # class_name,real_coordinate=self.camera.get_coordinate()
        # # aim_coordinate=self.console.aihuan_algrithm(real_coordinate)
        # aim_coordinate=list(real_coordinate)
        # #假设直接抓取并能成功
        # print(aim_coordinate)
        # print(class_name)
        # self.console.to_xyz(aim_coordinate)
        # self.console.claw_close()
        # self.console.place_instrument(class_name)
        #
        self.console.claw_open()
        self.console.to_xyz([25,20,10])
        self.console.claw_close()
        self.console.place_instrument('fork')

    def pipeline_to_hand(self,class_name):
        self.console.pick_instrument(class_name)

    def log(self):
        pass

if __name__=='__main__':
    pap=PickAndPlace()
    pap.run()

