"""Author: Xuran Sun, 2020-08-05"""

from pydub import AudioSegment
import os, re


def get_second_part_wav(main_wav_path, start_time, end_time, part_wav_path):
    """
    音频切片，获取部分音频，单位秒
    :param main_wav_path: 原音频文件路径
    :param start_time: 截取的开始时间
    :param end_time: 截取的结束时间
    :param part_wav_path: 截取后的音频路径
    :return:
    """
    start_time = int(start_time)
    end_time = int(end_time)

    sound = AudioSegment.from_mp3(main_wav_path)
    word = sound[start_time:end_time]

    word.export(part_wav_path, format="wav")


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'\u0039' >= uchar >= u'\u0030' or uchar == '.':
        return True
    else:
        return False


def extract_num(string):
    """从字符串中提出数字"""
    num_str = ''
    for i in string:
        if is_number(i):
            num_str += i
    return float(num_str)


def extract_text(string):
    """从字符串中提出文本"""
    pattern = re.compile('"(.*)"')
    a = pattern.findall(string)
    if a:
        return a[0]
    else:
        return ''


def get_filename(filename):
    """获取文件名和扩展名"""
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    res = [shotname, extension]
    return res


def main():
    wav_path = "wav"
    text_path = "text"
    wav_output = "wav_output"
    text_output = "text_output"
    wav_list = os.listdir(wav_path)
    text_list = os.listdir(text_path)

    wav_list.sort()
    text_list.sort()

    if len(wav_list) != len(text_list):
        raise ValueError('the number of wav unmatch the number of text')


    for i in range(len(text_list)):
        textfile = text_path + '/' + text_list[i]
        wavfile = wav_path + '/' + wav_list[i]

        with open(textfile, 'r', encoding="utf8")as f:
            lines = f.readlines()
        xmin = []
        xmax = []
        for line in lines:
            if "xmin = " in line:
                xmin.append(extract_num(line))
            if "xmax = " in line:
                xmax.append(extract_num(line))

        xmin = xmin[2:]
        xmax = xmax[2:]
        string_list = []
        head = ""
        text_outfile = text_output + '/' + text_list[i]
        fo = open(text_outfile.replace('textGrid','txt'), 'w', encoding='utf-8')

        with open(textfile, 'r', encoding="utf8") as f:
            lines = f.readlines()
        for line in lines:
            if 'intervals [' in line:
                string = head+str(int(extract_num(line))).zfill(6)+".wav" + "\t"
            if 'text = "' in line:
                string += extract_text(line) + '\n'
                string_list.append(string)
                if len(string) <= 19:
                    continue

                fo.write(string)
        fo.close()
        count2 = 0
        num = 0
        for j in range(len(xmin)):
            if len(string_list[j]) > 19:
                s = xmin[j] * 1000
                e = xmax[j] * 1000
                print(s)
                count2 = j + 1
                wav_outfile = wav_output + '/' + wav_list[i].replace('.wav', '')
                try:
                    os.makedirs(wav_outfile)
                except:
                    pass
                part_path = wav_outfile + '/' +head+str(count2).zfill(6) + ".wav"
                get_second_part_wav(wavfile, s, e, part_path)


if __name__ == '__main__':
    main()
