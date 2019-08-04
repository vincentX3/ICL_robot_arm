import pyrealsense2 as rs
import numpy as np
import pandas as pd


class Camera(object):
    def __init__(self):
        # interval: 搜索的时间段长度（对应文件中的等时间段的记录）
        self.interval = 10
        # file_path:文件默认地址
        self.file_path = 'obj_data\\output.csv'

    def set_interval(self, interval):
        self.interval = interval

    def set_file_path(self, path):
        self.file_path = path

    def get_coordinate(self):
        '''
        读yolo obj detection的文件，对interval时间间隔内的数据进行搜索过滤，返回识别出的物体类别及坐标
        :return:
            class_name str 物体类别
            coordinate np.array 物体坐标
        '''
        instrument_dict = {'knife': 0, 'fork': 0, 'spoon': 0}
        pd_data = pd.read_csv(self.file_path, header=None)
        record_amount = pd_data.shape[0] + 1
        if record_amount < self.interval:
            aim_data = pd_data[-record_amount:]
        else:
            aim_data = pd_data[-self.interval:]

        count = aim_data[0].value_counts()
        for instrument in instrument_dict.keys():
            instrument_dict[instrument] = count[instrument]
        aim_instrument=max(instrument_dict,key=instrument_dict.get) #若两个工具检测到的次数相同，返回第一个
        temp=np.array(aim_data[aim_data[0].isin([aim_instrument])])[-1]
        aim_coordinate=temp[2:]

        return aim_instrument,aim_coordinate
        

    def refresh_obj_file(self):
        '''
        清空obj文件内容（用于每次成功检测后对文件的清除）
        :return:
        '''
        with open(self.file_path, 'r+') as source:
            source.truncate()

    def arm_tracker(self):
        pass


if __name__ == '__main__':
    camera = Camera()
    camera.refresh_obj_file()
