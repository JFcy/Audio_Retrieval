from random import random

from ffmpy import FFmpeg as mpy
import os #  文件系统操作对象

from pydub import AudioSegment


def trans_to_wav(mp3_file, wav_folder):
    '''
    格式转换格式
    :param mp3_file:
    :param wav_folder:
    :return:
    '''
    # 格式化文件
    file_fmt = os.path.basename(mp3_file).strip()
    # 获取文件格式
    file_fmt = file_fmt.split('.')[-1]
    # 校验文件格式
    if file_fmt.strip() != 'mp3':
        raise Exception('改文件不是MP3格式，请检查！')
    elif file_fmt.strip() == '':
        raise Exception('文件格式出现异常，请检查！')
    # 创建wav的文件以供转换完成后输出
    wav_file_path = os.path.join(wav_folder)
    wav_file_path = os.path.join(wav_file_path, '{}.{}'.format(
        os.path.basename(mp3_file).strip().split('.')[0], 'wav'
    ))
    # 创建转换时的命令行参数字符串
    cmder = '-f wav -ac 1 -ar 44100'
    # 创建转换器对象
    mpy_obj = mpy(
        inputs={
            mp3_file: None
        },
        outputs={
            wav_file_path: cmder
        }
    )
    print('执行CMDER 命令：{}'.format(mpy_obj.cmd))

    # 执行转换
    mpy_obj.run()

def cut_mp3(filepath,output_file,time):
    """
    # 程序流程
    1. 读取一个mp3文件,指定文件路径即可
    2. 根据用户选择设置截取片段，使用切片, 单位为ms
    3. 导出文件并保存, 指定导出文件名以及路径，最后指定导出的格式
    （其他编码格式，参考ffmpeg上的专业知识）

    :param filepath: 音乐文件路径, path
    :return: None
    """
    music = AudioSegment.from_mp3(file=filepath)
    sound_time = music.duration_seconds
    print(f"music duration time: {sound_time}")

    # 使用切片截取, 单位毫秒， 1s -> 1000ms
    time_start = random() * 120 * 1000
    out_music = music[time_start: time_start + time * 1000]

    # 导出
    out_music.export(out_f=output_file, format='wav')   # 可以指定bitrate为64k比特率 None为源文件

    print('done')


if __name__ == '__main__':
    # trans_to_wav('./走马.mp3','./WAV/')
    # cut_mp3('./WAV/If_We_Ever_Broke_Up.wav')
    for each in os.listdir('./WAV/'):
        cut_mp3(os.path.join('./WAV/',each),'./TEST/S5/test5_' + each,5)
        cut_mp3(os.path.join('./WAV/', each), './TEST/S10/test10_'+ each, 10)
        cut_mp3(os.path.join('./WAV/', each), './TEST/S15/test15_'+ each, 15)
