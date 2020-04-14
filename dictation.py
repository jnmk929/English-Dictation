#
#機能:
# 入力:
# ○ ・大文字小文字関係なく入力できる　入力は小文字に統一
# △・スペース等はスキップ ひとまず２連続　後々固有名詞など長めでも対応できるように
# ○ ・いい感じで自動改行する 単位ごとに改行
#   ・１文字ヒント機能
# ○ ・タイプミスの効果
# 音声:
# △・wavファイルが再生できる　子プロセスが終了しても音声は止まらないから、pygame pyaudio等に変えたほうがいい
# ○ ・繰り返し　一時停止
# ☓ ・数秒飛ばし戻し 3s 5s
# ○    変更 -> soundファイルを空白部分で分割  分割の調整が必要
# △            キーボードとマウスの入力から再生箇所を変える
# ○            プロセス間でのデータのやりとり
# その他:
#   ・採点機能　間違い数のカウント　
#   ・入力後に解答の表示
#   ・複数の問題に対応
#   ・入力文字を予め ＿ で伏せて見せておく
#   ・同じ問題が連続して流れないように
#   ・経過時間の計測,表示
#   ・全体のリセットやり直し
#
#キーボード機能:
#   ・space -> stop or start
#   ・Shift_L -> back one track
#   ・Shift_R -> skip one track
#   ・Return(Enter) -> repeat

import tkinter as tk
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import subprocess
from multiprocessing import Process,Value
import glob
import time
import re

class Application(tk.Frame):
    count = 0
    row = 1
    true_word = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
    skip_word = [" ",".",",",";","'","-","?","’"]
    row_limit_word = 60
    def __init__(self,master,sentence,num):
        super().__init__(master)
        self.pack()
        self.sentence = sentence
        self.num = num
        self.master.geometry('1400x800')
        self.master.title('ディクテーション')
        self.buffer = tk.StringVar()
        self.a = tk.Label(textvariable=self.buffer,font=('',30)) 
        self.a.pack()
        self.a.bind('<Key>',self.input)
        self.a.focus_set()
    
    def input(self,event):
        self.a['fg'] = '#000000'
        flag_keyword = False
        flag_skip = 0
        flag_row = False
        key = event.keysym  #入力の受取
        if key == self.sentence[self.count].lower():
            self.count += 1
            flag_keyword = True
        if self.sentence[self.count] in self.skip_word:
            if not self.sentence[self.count+1] in self.skip_word:
                self.count += 1
                flag_skip = 1
            else:
                self.count += 2
                flag_skip = 2
        if self.count > self.row_limit_word*self.row and self.sentence[self.count-1] == ' ':
            self.sentence.insert(self.count,'\n')
            self.count += 1
            self.row += 1
            flag_row = True

        if (flag_skip == 0 and flag_keyword == True and key == self.sentence[self.count-1].lower()) \
          or (flag_skip == 1 and key == self.sentence[self.count-2].lower())\
          or flag_row == True:
            self.buffer.set(''.join(self.sentence[:self.count]))
        elif flag_skip == 2:
            self.buffer.set(''.join(self.sentence[:self.count-1]))
        else:
            if key in self.true_word:
                self.a['fg'] = '#ff0000'
                self.buffer.set(''.join(self.sentence[:self.count])+key)
            elif key == 'space':
                self.num.value = 1
            elif key == 'Shift_L':
                self.num.value = 2
            elif key == 'Shift_R':
                self.num.value = 3
            elif key == 'Return':
                self.num.value = 4

def sound(audio_file,num):
    track = 0
    while(1):
        if track >= 0:
            subprocess.run(['aplay',audio_file[track]])
            track += 1
        if num.value != -1:
            if num.value == 1:  #press space and stop  start
                track = -track
            elif num.value == 2:  #press Shift_L and back one track
                track -= 2
            elif num.value == 3:  #press Shift_R and skip one track
                track += 1
            elif num.value == 4:  #press Retrun(Enter) and repeat this track
                track -= 1
            num.value = -1
        if track >= len(audio_file):
            track = -1


textfile = './data/text/part4.txt'
origin_sound_file = './data/sound/listening85.wav'
split_sound_dir = './data/split_sound/'

def main():
    with open(textfile,'r') as f:
        line = f.readlines()
    sentence = list(line[0])    #ファイルには1行の文章の予定
    
    for path in glob.glob(split_sound_dir+'*.wav'):
        os.remove(path)
    origin_sound = AudioSegment.from_file(origin_sound_file,format='wav')   #無音部分で区切る
    chunks = split_on_silence(origin_sound, min_silence_len=150, silence_thresh=-55, keep_silence=6)
    for i, chunk in enumerate(chunks):
        chunk.export(split_sound_dir+ str(i) +'.wav', format='wav')

    audio_file = glob.glob(split_sound_dir+'*.wav')
    num = lambda val : int(re.sub("\\D","",val))  #\\D  任意の数字以外置換
    audio_file.sort(key=num)
    num = Value('i',-1)
    p = Process(target=sound,args=(audio_file,num))
    p.start()
    root = tk.Tk()
    app = Application(master=root,sentence=sentence,num=num)
    app.mainloop()
    p.terminate()


if __name__ == "__main__":
    main()