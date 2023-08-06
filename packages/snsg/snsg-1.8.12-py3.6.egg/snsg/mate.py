#!/usr/bin/python3

"""
@author: 张伟
@time: 2018/3/7 9:28
"""
import os


class Mate(object):
    data = list()
    text = str()

    def __init__(self, list_file=None):
        """
        初始化
        :param list_file 分词字典,可以是链表也可以是文件地址
        """
        self.p = os.path.sep
        if type(list_file) is list:
            self.load_list(list_file)
        elif type(list_file) is str:
            self.load_file(list_file)

    def load_list(self, ls):
        """
        加载链表字典，注意如果链表中包含换行符，自动清除。
        :param ls: 链表，一维链表[key,key,.....]
        :return: None
        """
        if '\n' in ls[0]:
            self.data = [f[:-1] for f in ls]
        else:
            self.data = ls

    def load_file(self, file):
        """
        加载文件字典
        :param file: 词库文件地址
        :return: None
        """
        with open(file=file, encoding='utf-8-sig') as f:
            self.load_list(f.readlines())

    def mate(self, input_string):
        """
        分词文本
        :param input_string:  输入文本字符串
        :return: 分割好的字符串
        """
        self.text = input_string + " "
        out_string = str()
        lens = len(self.text) + 1
        j = 0
        flag = 0
        while j < lens:
            for k in range(j + 2, lens):
                word = self.text[j:k]
                deviation = 0
                while word in self.data:
                    deviation += 1
                    word = self.text[j:k + deviation]

                if deviation != 0:
                    if self.text[flag:j] not in '':
                        out_string += self.text[flag:j] + self.p
                    out_string += word[:-1] + self.p
                    j = k + deviation - 1
                    flag = j
                    j -= 1
                    break
            j += 1
        out_string += self.text[flag:]
        return out_string
