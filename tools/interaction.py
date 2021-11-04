# -*-coding: utf-8-*-
from bram import BramConfig, BRAM
import numpy as np

class FLAG(object): 
    '''标记位00、01控制

    使用方法：FLAG.flag_OO()这样使用即可'''

    def flag_00(is_int=False):
        flag_00 = b"\x00\x00\x00\x00"
        if is_int:
            flag_00 = FLAG._int(flag_00)
        return flag_00

    def flag_01(is_int=False):
        flag_01 = b"\x01\x00\x00\x00"
        if is_int:
            flag_01 = FLAG._int(flag_01)
        return flag_01

    def _int(flag):
        return int.from_bytes(flag, 'little')


class Comunicator(object):
    '''实现PS、PL交互接口，包括写数据、读结果两大部分'''
    
    def __init__(self):
        self.bram = BRAM()

    def send_flag(self, block_name, offset='flag'):
        '''设置flag信号'''
        self.bram.write(FLAG.flag_01(), block_name, offset)

    def wait_for_flag(self, block_name, offset='flag'):
        '''等待对方的flag信号'''
        while True:
            if int(self.bram.read(1, block_name, offset)) == FLAG.flag_00(is_int=True):
                break

    def construct_instr(self, data_startaddr, data_length, sync_cycle):
        '''构建指令，指令包含以下字段：

            uint32 data_startaddr ;  // 块内偏移，用于双缓冲的时候
            uint32 data_length ;  // byte
            uint32 sync_cycle ;   // 65536
        '''
        return np.array([data_startaddr, data_length, sync_cycle], dtype=np.uint32)

    def write(self, data: np.ndarray, block_name: str, offset='default'):
        '''写数据至PL侧，若数据量大于size则拆分，分多次写入

            Args:
                data: 要传输的数据，np.ndarray
                block_name: BramConfig中设置的块名称
                offset: BramConfig中配置的offset字典key值
        '''

        block_size = BramConfig.block_info[block_name]['size']

        # 确保block_size能够放下整数个data元素
        assert (block_size / data.itemsize) % 1 == 0
        
        data = data.flatten()   # 展平成1维
        for i in range(0, data.size, block_size / data.itemsize):
            # 等待信号返回，可以开始下一次写入
            self.wait_for_flag('write_ir')

            # 写入块数据
            block_data = data[i: i + block_size / data.itemsize]
            self.bram.write(block_data, block_name, offset)

            # 写指令
            instr = self.construct_instr(0x0, block_data.nbytes, 65536)
            self.bram.write(instr, 'write_ir', offset='instr')

            # 写flag
            self.send_flag('write_ir')

    def read_instr(self):
        '''写入read块的指令和flag，让PL部分先开始工作'''
        # 写指令
        instr = self.construct_instr(0x0, len, 65536)
        self.bram.write(instr, 'write_ir', offset='instr')
        # 写flag
        self.send_flag('read_ir')

    def read_result(self, len, block_name: str, offset='default') -> np.ndarray:
        '''等待信号并接收结果

            Args:
                len: 读取的数据长度
                block_name: BramConfig中设置的块名称
                offset: BramConfig中配置的offset字典key值

            Return:
                返回numpy数组
        '''
        # 等待信号
        self.wait_for_flag('read_ir')

        # 读取结果
        result = self.bram.read(len, block_name, dtype=np.int32)
        return result


if __name__ == '__main__':
    comunicator = Comunicator()

    data = np.random.randint(0, 256, size=(640, 480), dtype=np.uint8)
    comunicator.read_instr()
    comunicator.write(data, 'write_buffer')
    result = comunicator.read_result(40, 'read_buffer')