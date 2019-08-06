class robot_console(object):
    import time
    # serial port
    ser = ''

    # table1 default(by arduino)
    #      motor  default  order
    table1 = [['A', '50',  0],
              ['B', '140', 1],
              ['F', '55',  3],
              ['C', '80'],
              ['G', '20']]

    table2 = [['A', '50',  2],
              ['B', '140', 1],
              ['F', '55',  0],
              ['C', '80'],
              ['G', '20']]

    def __init__(self):
        print('Initialising...')
        try:
            self.ser = self.list_ports()
            print('Initialised')
            return
        except:
            print('Initialise - Failed')
            self.ser.close()

    def list_ports(self):
        import serial.tools.list_ports
        print('============== Available COM Ports ==============')
        ports = []
        for n, (port, desc, hwid) in enumerate(sorted(serial.tools.list_ports.comports()), 1):
            print('--- {:2}: {:20} {}\n'.format(n, port, desc))
            ports.append(port)
        while True:
            port = input('--- Enter port index or full name: ')
            try:
                index = int(port) - 1
                if not 0 <= index < len(ports):  # the port doesn't exist
                    print('--- Invalid index!\n')
                    continue
            except ValueError:
                print('invalid value')
                pass
            else:
                port = ports[index]
            print(port)
            ser = serial.Serial(port, 9600, timeout=1)
            return ser

    def aihuan_algrithm(self, dir_obj):
        x = dir_obj[0]
        y = dir_obj[1]
        z = dir_obj[2]
        # 转到一定角度后 此时的侧面坐标
        import numpy as np
        import math
        # a1:第一个杆的长度 ； a2:第二个杆的长度
        a1 = 12
        a2 = 26  # 含爪子长度
        h = 12  # 底座高度
        level = 55
        # 得水平转动到的角度
        tan_angle = abs(x) / abs(y)
        # 水平归位为55度或者80度
        if y != 0:
            tan_angle = abs(x) / abs(y)
            # 水平归位为55度或者80度
            if x < 0:
                angle = (level / 180 * math.pi + math.atan(tan_angle)) * 180 / math.pi
            else:
                angle = (level / 180 * math.pi - math.atan(tan_angle)) * 180 / math.pi
        elif x > 0:
            angle = (level / 180 * math.pi - math.pi / 2) * 180 / math.pi
        else:
            angle = (level / 180 * math.pi + math.pi / 2) * 180 / math.pi
        s = math.sqrt(x * x + y * y)  # 新二维平面（侧面）的X轴位置坐标

        if z >= h:
            # angleA = (35 / 180 * math.pi - (angleB - theta1)) * 180 / math.pi
            tan_alpha1 = abs(z - h) / abs(s)
            alpha1 = math.atan(tan_alpha1)
            cos_alpha2 = (a1 * a1 + (s * s + (h - z) * (h - z)) - a2 * a2) / (
                        2 * a1 * math.sqrt((h - z) * (h - z) + s * s))
            alpha2 = math.acos(cos_alpha2)
            theta1 = math.pi - (alpha1 + alpha2)
            angleB = (alpha1 + alpha2) * 180 / math.pi

            cos_anti_theta2 = (a1 * a1 + a2 * a2 - (s * s + (h - z) * (h - z))) / (2 * a1 * a2)
            theta2 = math.pi - math.acos(cos_anti_theta2)
            angleA = (35 / 180 * math.pi - (math.pi - (theta1 + theta2))) * 180 / math.pi
        else:
            # angleA = (35 / 180 * math.pi - (theta1 - angleB)) * 180 / math.pi
            tan_alpha1 = abs(s) / abs(z)
            alpha1 = math.atan(tan_alpha1)
            tan_beta1 = abs(s) / abs(h - z)
            beta1 = math.atan(tan_beta1)
            cos_beta2 = (a1 * a1 + (s * s + (h - z) * (h - z)) - a2 * a2) / (
                        2 * a1 * math.sqrt((h - z) * (h - z) + s * s))
            beta2 = math.acos(cos_beta2)
            theta1 = math.pi - beta1 - beta2
            angleB = (math.pi / 2 - theta1) * 180 / math.pi

            cos_anti_theta2 = (a1 * a1 + a2 * a2 - (s * s + (h - z) * (h - z))) / (2 * a1 * a2)
            theta2 = math.pi - math.acos(cos_anti_theta2)
            angleA = (35 / 180 * math.pi + theta1 + theta2 - math.pi / 2) * 180 / math.pi

        F = int(angle)
        B = int(angleB)
        A = int(angleA)
        self.table2[0][1] = str(A)
        self.table2[1][1] = str(B)
        self.table2[2][1] = str(F)

    def get_degree(self):
        command = 'SHOW DEGREE'
        self.ser.write(command.encode())
        s = self.ser.readlines(40)
        st = s[1].decode('utf-8')
        'A 0 B 0 C 0 D 0 E 0 F 0 G 0'
        angle_degree = st.split()
        print(angle_degree)
        self.table1[0][1] = str(angle_degree[1])
        self.table1[1][1] = str(angle_degree[3])
        self.table1[3][1] = str(angle_degree[5])
        self.table1[2][1] = str(angle_degree[11])
        self.table1[4][1] = str(angle_degree[13])

    def execute(self, command_table):
        # import time
        for command in command_table:
            self.ser.write(command.encode())
            s = self.ser.readlines(40)
            if type(s) == str:
                print('\t' + s.decode('utf-8'))
            else:
                for i in range(len(s)):
                    print('\t' + s[i].decode('utf-8'))

    def reset_table(self):
        reset_table = []
        for i in [0, 1, 2]:
            reset_table.append('SET' + ' ' + self.table1[i][0] + ' ' + self.table1[i][1])

    def move_table(self, dir_obj, speed=5):
        self.aihuan_algrithm(dir_obj)
        self.get_degree()
        print(self.table1)
        print(self.table2)
        if self.table1 == self.table2:
            return
        #         motor        +/-         degree
        table_ = [['A',        'ADD',      '0'],
                  ['B',        'ADD',      '0'],
                  ['F',        'ADD',      '0']]
        for i in [0, 1, 2]:
            if int(self.table1[i][1]) > int(self.table2[i][1]):
                table_[i][1] = 'MINUS'
                table_[i][2] = str(int(self.table1[i][1])-int(self.table2[i][1]))
            elif int(self.table1[i][1]) < int(self.table2[i][1]):
                table_[i][1] = 'ADD'
                table_[i][2] = str(int(self.table2[i][1])-int(self.table1[i][1]))
            else:
                pass
        move_table = []
        for i in [0, 1, 2]:
            for k in [0, 1, 2]:
                if self.table2[k][2] == i:
                    break
            if table_[k][2] == '0':
                continue
            num__ = int(table_[k][2])
            step__ = (num__ + speed - 1) // speed
            for j in list(range(step__)):
                if speed * (j + 1) < num__:
                    cur_num_ = speed
                else:
                    cur_num_ = num__ - speed*j
                move_table.append(table_[k][1] + ' ' + table_[k][0] + ' ' + str(cur_num_))
        return move_table

    def claw_table(self, angle=90, os='CLOSE', degree=0):
        self.get_degree()
        claw_table = []
        if self.table1[3][1] != angle:
            claw_table.append('SET C' + ' ' + str(angle))
            self.table1[3][1] = angle
        if os == 'OPEN':
            if self.table1[4][1] != 0:
                claw_table.append('SET G 0')
                self.table1[4][1] = 0
        elif os == 'CLOSE':
            if self.table1[4][1] != 58:
                claw_table.append('SET G 58')
                self.table1[4][1] = 58
        elif os == 'DIY':
            if self.table1[4][1] != degree:
                claw_table.append('SET G' + ' ' + str(degree))
                self.table1[4][1] = degree
        return claw_table

    def arm_up_table(self, speed=5, angle_A=35, angle_B=90):
        try:
            self.get_degree()
            #         motor        +/-         degree
            table_ = [['A',       'ADD',        '0'],
                      ['B',       'ADD',        '0'],
                      ['F',       'ADD',        '0']]
            table3 = [['A', str(angle_A),  1],
                      ['B', str(angle_B),  0]]
            for i in [0, 1]:
                if int(self.table1[i][1]) > int(table3[i][1]):
                    table_[i][1] = 'MINUS'
                    table_[i][2] = str(int(self.table1[i][1]) - int(table3[i][1]))
                elif int(self.table1[i][1]) < int(table3[i][1]):
                    table_[i][1] = 'ADD'
                    table_[i][2] = str(int(table3[i][1]) - int(self.table1[i][1]))
                else:
                    pass
            arm_up_table = []
            for i in [0, 1]:
                for k in [0, 1]:
                    if table3[k][2] == i:
                        break
                if table_[k][2] == '0':
                    continue
                num__ = int(table_[k][2])
                step__ = (num__ + speed - 1) // speed
                for j in list(range(step__)):
                    if speed * (j + 1) < num__:
                        cur_num_ = speed
                    else:
                        cur_num_ = num__ - speed * j
                    arm_up_table.append(table_[k][1] + ' ' + table_[k][0] + ' ' + str(cur_num_))
            return arm_up_table
        except:
            return

    def do_pick(self, dir_obj, angle=90, speed=5):
        command_table1 = self.arm_up_table(speed)
        if command_table1:
            self.execute(command_table1)
        # time.sleep(1)
        command_table2 = self.move_table(dir_obj, speed)
        if command_table2:
            self.execute(command_table2)
        # time.sleep(1)
        command_table3 = self.claw_table(angle)
        if command_table3:
            self.execute(command_table3)

    def do_place(self, dir_destination, speed=5):
        command_table1 = self.arm_up_table(speed)
        if command_table1:
            self.execute(command_table1)
        # time.sleep(1)
        command_table2 = self.move_table(dir_destination, speed)
        if command_table2:
            self.execute(command_table2)
        # time.sleep(1)
        command_table3 = self.claw_table(90, 'OPEN')
        if command_table3:
            self.execute(command_table3)

    def place_instrument(self, instrument):
        '''
        在已经成功抓取目标后，根据工具类型，将其放置到对应方位
        :param instrument: str 工具类型
        :return:
        '''
        # todo 根据实际空间完善放置代码
        if instrument == 'knife':
            self.do_pick([0, 0, 0])
        if instrument == 'fork':
            self.do_pick([1, 1, 1])
        if instrument == 'spoon':
            self.do_pick([2, 2, 2])
        time.sleep(1.5)
        if instrument == 'knife':
            self.do_place([0, 0, 0])
        if instrument == 'fork':
            self.do_place([1, 1, 1])
        if instrument == 'spoon':
            self.do_place([2, 2, 2])

    def pick_instrument(self, instrument):
        '''
        根据工具类型，从对应方位抓取工具并移动机械臂至最左侧合适方位
        :param instument:
        :return:
        '''
        # todo 根据实际空间完善放置代码
        if instrument == 'knife':
            self.do_pick([-25, 14, 0.3])
        if instrument == 'fork':
            self.do_pick([-25, 19, 0.3])
        if instrument == 'spoon':
            self.do_pick([-25, 9, 0.3])
        time.sleep(0.5)
        if instrument == 'knife':
            self.do_place([20, 25, 0.3])
        if instrument == 'fork':
            self.do_place([20, 25, 0.3])
        if instrument == 'spoon':
            self.do_place([20, 25, 0.3])


import time
a = robot_console()
# a.do_place([-25, 20, 0.3])
a.pick_instrument('spoon')
time.sleep(1)
a.pick_instrument('knife')
time.sleep(1)
a.pick_instrument('fork')
