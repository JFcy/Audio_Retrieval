# author:Fcy
# @File: compare.py
# @Time: 2023/5/31 23:05
# @description:受制于技术问题，这里采用最简单的滑动窗口方法模拟听歌识曲。6月1日完工，真是一件美事啊！
# 2023年6月19日，上手将代码上传到github，顺便改正一下自己版本管理混乱的陋习。
# coding=utf-8
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
import os
import sqlite3
from loadmusic import recode
import voices
import time

class memory():
    
    def __init__(self, db):
    
        '''
        初始化存储类
        :param db:数据库名
        '''
        self.level = {"low":60,"mid":100,"high":150}
        self.db = db
        self.Tightness = 200
        self.Tightness_f = 40
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("create table if not exists musicdata(songname text primary key ,high_point text)")

    def addsong(self, path):
    
        '''
        添加歌曲方法，将指定路径的歌曲提取指纹后放到数据库
        :param path:路径
        :return:
        '''
    
        if type(path) != str:
            print ('path need string')
            return None
        basename = os.path.basename(path)
        try:
            # 创建与数据库的连接
            conn = sqlite3.connect(self.db)
        except:
            print('DataBase error')
            return None
        cur = conn.cursor()
        namecount = cur.execute("select * from musicdata WHERE songname = '%s'" % basename).fetchall()
        # 查询新添加的歌曲是否已经在曲库中了

        if len(namecount) > 0:
            print('the song has been record!')
            return None
    
        v = voices.voice()
        v.loaddata(path)
        v.fft()
        # 将新歌曲的名字和指纹存到数据库中
        cur.execute("insert into musicdata VALUES('%s','%s')" % (basename, v.high_point.__str__()))
        conn.commit()
        cur.close()
        conn.close()
    
    def  fp_compare(self, search_fp, match_fp):
        '''
        指纹比对方法。
        :param search_fp: 查询指纹
        :param match_fp: 库中指纹
        :return:最大相似值 float
        '''
        if len(search_fp) > len(match_fp):
            return 0
        max_similar = 0
        search_fp_len = len(search_fp)
        match_fp_len = len(match_fp)
        for i in range(match_fp_len - search_fp_len):
            temp = 0
            for j in range(search_fp_len):
                # if match_fp[i + j] == search_fp[j]:
                #     temp += 1
                loss = 0
                for k in range(len( match_fp[i + j])):
                    loss = loss + abs(match_fp[i + j][k] - search_fp[j][k])
                if loss < self.Tightness_f:
                    temp += 1
            if temp > max_similar:
                max_similar = temp
        return max_similar

    def search(self, path,t):
        '''
        从数据库检索出
        :param path: 需要检索的音频的路径
        :return:返回列表，元素是二元组，第一项是匹配的相似值，第二项是歌曲名
        '''
        self.Tightness = self.level[t]
        v = voices.voice()
        v.loaddata(path)
        v.fft()
        try:
            conn = sqlite3.connect(self.db)
        except:
            print('DataBase error')
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM musicdata")
        result = cur.fetchall()
        compare_res = []
        for i in result:
            compare_res.append((self.fp_compare(v.high_point[:-1], eval(i[1])), i[0]))
    
        compare_res.sort(reverse=True)
        cur.close()
        conn.close()

        if int(compare_res[0][0]) < self.Tightness:
            print("您播放的歌曲不在库中！",compare_res[0][0])
        else:
            print("识别结果:", compare_res[0][1])
        print(compare_res)
        return compare_res
    
    def search_and_play(self, path):
        '''
        跟上个方法一样，不过增加了将搜索出的最优结果直接播放的功能
        :param path: 带检索歌曲路径
        :return:
        '''
    
        v = voices.voice()
        v.loaddata(path)
        v.fft()

        try:
            conn = sqlite3.connect(self.db)
        except:
            print('DataBase error')
            return None
    
        cur = conn.cursor()
        cur.execute("SELECT * FROM musicdata")
        result = cur.fetchall()
        compare_res = []
        for i in result:
            compare_res.append((self.fp_compare(v.high_point[:-1], eval(i[1])), i[0]))

        compare_res.sort(reverse=True)
        cur.close()
        conn.close()
    
        print(compare_res)
        if compare_res[0][1] >= self.Tightness:
            v.play(compare_res[0][1])
        else :
            print("您播放的歌曲不在库中！")
        return compare_res

    def clear_all(self):
        sql = "Delete from musicdata"
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

if __name__ == '__main__':

    sss = memory('identifier')

    # print(sss)
    # sss.clear_all()
    # sss.addsong('./WAV/走马.wav')

    # for each in os.listdir('./WAV'):
    #     print(each + "记录完成")
    #     sss.addsong('./WAV/' + each)

    # sss.search('./WAV/走马.wav')

    # 测试数据1：切割下的音乐片段
    # music_path = "./TEST/S5/test5_I Need You To Stay.wav"
    # sss.search(music_path,"low")
    path = './TEST/S5/'
    for each in os.listdir(path):
        startTime = time.time()
        print(each,end="\t-------------\t")

        sss.search(os.path.join(path,each),"low")

        endtime=time.time()
        diffrentTime = endtime - startTime
        print(diffrentTime)

    # 测试数据1：麦克风内容
    # a = recode()
    # a.recode(RECORD_SECONDS=15, WAVE_OUTPUT_FILENAME='test.wav')
    # sss.search_and_play('test.wav',"high")

