# author:Fcy
# @File: loadmusic.py
# @Time: 2023/5/31 21:55
# @description: 听歌识曲第4次尝试，环境真难装，论文真不好看懂啊！！！recode函数用于录音。compare为主函数，从那里开始运行。


# coding=utf8

import wave
import pyaudio

class recode():

    def recode(self, CHUNK=44100, FORMAT=pyaudio.paInt16, CHANNELS=2, RATE=44100, RECORD_SECONDS=2,WAVE_OUTPUT_FILENAME="record.wav"):

        '''
        :param CHUNK: 缓冲区大小
        :param FORMAT: 采样大小
        :param CHANNELS:通道数
        :param RATE:采样率
        :param RECORD_SECONDS:录的时间
        :param WAVE_OUTPUT_FILENAME:输出文件路径
        :return:
        '''
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

        frames = []
        print("开始录音！！")
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("录音结束")

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

if __name__ == '__main__':
    a = recode()
    a.recode(RECORD_SECONDS=5, WAVE_OUTPUT_FILENAME='test.wav')
