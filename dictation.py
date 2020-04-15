#
#機能:
# 入力:
# ○ ・大文字小文字関係なく入力できる　入力は小文字に統一
# △・スペース等はスキップ ひとまず２連続　後々固有名詞など長めでも対応できるように
# ○ ・いい感じで自動改行する 単位ごとに改行
# ○ ・１文字ヒント機能
# ○ ・タイプミスの効果
# 音声:
# △・wavファイルが再生できる　子プロセスが終了しても音声は止まらないから、pygame pyaudio等に変えたほうがいい
# ○ ・繰り返し　一時停止
# ☓ ・数秒飛ばし戻し 3s 5s
# ○    変更 -> soundファイルを空白部分で分割  分割の調整が必要
# ○            キーボードとマウスの入力から再生箇所を変える
# ○            プロセス間でのデータのやりとり
# その他:
#   ・採点機能　間違い数のカウント　
#   ・複数の問題に対応
#      ・同じ問題が連続して流れないように
#   ・入力文字を予め ＿ で伏せて見せておく
#   ・経過時間の計測,表示
# ○ ・全体のリセットやり直し
#
#キーボード機能:
#   ・space -> start repeat
#   ・Shift_L -> back one track
#   ・Shift_R -> next track

import tkinter as tk
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import subprocess
from multiprocessing import Process,Value
import glob
import time
import re
from functools import partial

class Application(tk.Frame):
    count = 0
    row = 1
    true_word = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
    skip_word = [" ",".",",",";","'","-","?","’"]
    row_limit_word = 60
    hint = ''
    flag_keyword = False
    flag_skip = 0
    flag_row = False
    def __init__(self,master,sentence,num):
        super().__init__(master)
        self.pack()
        self.sentence = sentence
        self.num = num
        self.master.geometry('1400x800')
        self.master.title('ディクテーション')
        self.buffer = tk.StringVar()
        self.a = tk.Label(textvariable=self.buffer,font=('',30)) 
        self.a.bind('<Key>',self.input)
        self.a.pack()
        
        self.button_function()

        self.a.focus_set()
    
    def input(self,event):
        key = event.keysym  #入力の受取
        self.output(key)
        
    def output(self,key):
        self.flag_keyword = False
        self.flag_skip = 0
        self.flag_row = False
        if key == self.sentence[self.count].lower() or key == 'hint':
            self.count += 1
            self.flag_keyword = True
        if self.sentence[self.count] in self.skip_word:
            if not self.sentence[self.count+1] in self.skip_word:
                self.count += 1
                self.flag_skip = 1
            else:
                self.count += 2
                self.flag_skip = 2
        if self.count > self.row_limit_word*self.row and self.sentence[self.count-1] == ' ':
            self.sentence.insert(self.count,'\n')
            self.count += 1
            self.row += 1
            self.flag_row = True
        
        if (self.flag_skip == 0 and self.flag_keyword == True and key == self.sentence[self.count-1].lower()) \
          or (self.flag_skip == 1 and key == self.sentence[self.count-2].lower())\
          or self.flag_row == True:
            self.a['fg'] = '#000000'
            self.buffer.set(''.join(self.sentence[:self.count]))
        elif self.flag_skip == 2:
            self.a['fg'] = '#000000'
            self.buffer.set(''.join(self.sentence[:self.count-1]))
        else:
            if key in self.true_word:
                self.a['fg'] = '#990000'
                self.buffer.set(''.join(self.sentence[:self.count])+key)
            elif key == 'space':
                self.num.value = 1
            elif key == 'Shift_L':
                self.num.value = 2
            elif key == 'Shift_R':
                self.num.value = 3
            elif key == 'hint':
                self.a['fg'] = '#008800'
                self.buffer.set(''.join(self.sentence[:self.count]))
            elif key == 'reset':
                self.buffer.set(''.join(self.sentence[:self.count]))
    
    def button_function(self):
        self.hint_b = tk.Button(text='１文字ヒント',width=10,height=1,bg='#00aaff',command=self.one_hint,font=("",15))
        self.hint_b.place(x=70,y=740)
        
        self.start_b = tk.Button(text='再生',width=10,height=1,bg='#00aaff',command=partial(self.sound_func,1),font=("",15))
        self.start_b.place(x=350,y=740)

        self.back_b = tk.Button(text='戻る',width=10,height=1,bg='#00aaff',command=partial(self.sound_func,2),font=("",15))
        self.back_b.place(x=630,y=740)

        self.next_b = tk.Button(text='進む',width=10,height=1,bg='#00aaff',command=partial(self.sound_func,3),font=("",15))
        self.next_b.place(x=910,y=740)

        self.reset_b = tk.Button(text='リセット',width=10,height=1,bg='#ff0000',command=self.reset,font=("",15))
        self.reset_b.place(x=1190,y=740)

    def one_hint(self):
        key = 'hint'
        self.output(key)

    def sound_func(self,num):
        self.num.value = num

    def reset(self):
        self.count = 0
        self.row = 1
        self.num.value = 0
        self.output('reset')
        self.sentence = [s for s in self.sentence if s != '\n']


def sound(audio_file,num):
    track = 1
    while(1):
        if track >= 1:
            subprocess.run(['aplay',audio_file[track-1]])
            track = -track
        if num.value != -1:
            if num.value == 1:  #press space and repeat start
                track = -track
            elif num.value == 2:  #press Shift_L and back track
                track += 1
                track = -track
            elif num.value == 3:  #press Shift_R and next track
                track -= 1
                track = -track
            elif num.value == 0:    #push reset button
                track = 0
            num.value = -1
        if abs(track) >= len(audio_file) or track == 0:
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