class RobotConsole(object):
    # serial port
    ser = ''

    # table1 default(by arduino)
    #      motor  default  order
    table1 = [['A', '50',  0],
              ['B', '140', 1],
              ['F', '55',  3]]

    table2 = [['A', '50',  2],
              ['B', '140', 1],
              ['F', '55',  0]]

    [C, G] = [90, 0]

    def __init__(self):
        print('Initialising...')
        while True:
            try:
                self.ser = self.list_ports()
                print('Initialised')
                return
            except:
                print('Initialise - Failed')
                self.ser.close()
                continue

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
        try:
            x = dir_obj[0]
            y = dir_obj[1]
            z = dir_obj[2]
            # 转到一定角度后 此时的侧面坐标
            import math
            # a1:第一个杆的长度 ； a2:第二个杆的长度
            a1 = 12
            a2 = 26  # 含爪子长度
            h = 12  # 底座高度

            # 得水平转动到的角度
            if y != 0:
                tan_angle = abs(x) / abs(y)
                # 水平归位为55度或者80度
                if x < 0:
                    angle = (55 / 180 * math.pi + math.atan(tan_angle)) * 180 / math.pi
                else:
                    angle = (55 / 180 * math.pi - math.atan(tan_angle)) * 180 / math.pi
            elif x > 0:
                angle = (55 / 180 * math.pi - math.pi/2) * 180 / math.pi
            else:
                angle = (55 / 180 * math.pi + math.pi/2) * 180 / math.pi

            s = math.sqrt(x * x + y * y)  # 新二维平面（侧面）的X轴位置坐标

            if z >= h:
                # angleA = (35 / 180 * math.pi - (angleB - theta1)) * 180 / math.pi
                tan_alpha1 = abs(z - h) / abs(s)
                alpha1 = math.atan(tan_alpha1)
                cos_alpha2 = (a1 * a1 + (s * s + (h - z) * (h - z)) - a2 * a2) / (2 * a1 * math.sqrt((h - z) * (h - z) + s * s))
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
                cos_beta2 = (a1 * a1 + (s * s + (h - z) * (h - z)) - a2 * a2) / (2 * a1 * math.sqrt((h - z) * (h - z) + s * s))
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
            self.table2[0][2] = str(B)
            self.table2[0][3] = str(F)
        except:
            print("超出算法边界，无法执行运算")
            return

    def execute(self, command_table):
        if command_table == '':
            return
        for command in command_table:
            self.ser.write(command.encode())

    def do_reset(self):
        reset_table = []
        for i in [0, 1, 2]:
            reset_table.append('SET' + ' ' + self.table1[i][0] + ' ' + self.table1[i][1])
        self.execute(reset_table)

    def do_move(self, dir_obj, speed=5):
        try:
            self.aihuan_algrithm(dir_obj)
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
            self.execute(move_table)
            self.table1 = self.table2
        except:
            self.do_reset()

    def do_crew(self, angle=90, os='CLOSE', degree=0):
        crew_table = []
        if self.C != angle:
            crew_table.append('SET C' + ' ' + str(angle))
            self.C = angle
        if os == 'OPEN':
            if self.G != 0:
                crew_table.append('SET G 0')
                self.G = 0
        elif os == 'CLOSE':
            if self.G != 58:
                crew_table.append('SET G 58')
                self.G = 58
        elif os == 'DIY':
            if self.G != degree:
                crew_table.append('SET G' + ' ' + str(degree))
                self.G = degree
        if crew_table:
            self.execute(crew_table)
        else:
            return

    def place_instrument(self,instrument):
        '''
        在已经成功抓取目标后，根据工具类型，将其放置到对应方位
        :param instrument: str 工具类型
        :return:
        '''
        #todo 根据实际空间完善放置代码

    def pick_instrument(self,instument):
        '''
        根据工具类型，从对应方位抓取工具并移动机械臂至最左侧合适方位
        :param instument: 
        :return: 
        '''
        # todo 根据实际空间完善放置代码
        

def input_dir_obj():  # For test
    string_ = input('the location is:').split()
    dir_obj = [float(string_[0]), float(string_[1]), float(string_[2])]
    return dir_obj
