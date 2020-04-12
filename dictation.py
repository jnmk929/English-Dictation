#
#機能:
# 入力:
# ○ ・大文字小文字関係なく入力できる　入力は小文字に統一
# △・スペース等はスキップ ひとまず２連続　後々固有名詞など長めでも対応できるように
# ○ ・いい感じで自動改行する 単位ごとに改行
#   ・１文字ヒント機能
# ○ ・タイプミスの効果
# 音声:
# ○ ・wavファイルが再生できる
#   ・繰り返し　一時停止
# ☓ ・数秒飛ばし戻し 3s 5s
# △    変更 -> soundファイルを空白部分で分割  分割の調整が必要
#              キーボードとマウスの入力から再生箇所を変える
#              プロセス間でのデータのやりとり
# その他:
#   ・採点機能　間違い数のカウント　
#   ・入力後に解答の表示
#   ・複数の問題に対応
#   ・入力文字を予め ＿ で伏せて見せておく

import tkinter as tk
from pydub import AudioSegment      #sound分割用
from pydub.silence import split_on_silence
import os   #分割したsoundの読み込み用
import subprocess #音楽流す aplay
from multiprocessing import Process
import glob     #すでにあるファイルの削除用

class Application(tk.Frame):
    count = 0
    row = 1
    true_word = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
    skip_word = [" ",".",",",";","'","-","?","’"]
    row_limit_word = 60
    def __init__(self,master,sentence):
        super().__init__(master)
        self.pack()
        self.sentence = sentence
        
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

        if self.count == 0 and key in self.true_word:     #一文字目
            self.buffer.set(key)
        elif (flag_skip == 0 and flag_keyword == True and key == self.sentence[self.count-1].lower()) \
          or (flag_skip == 1 and key == self.sentence[self.count-2].lower())\
          or flag_row == True:
            self.buffer.set(''.join(self.sentence[:self.count]))
        elif flag_skip == 2:
            self.buffer.set(''.join(self.sentence[:self.count-1]))
        elif key in self.true_word:
            self.a['fg'] = '#ff0000'
            self.buffer.set(''.join(self.sentence[:self.count])+key)

def sound(audio_file):
    track = 1
    while(1):
        if track >= 0:
            for i in range(5):
                subprocess.run(['aplay',audio_file[track]])
            track += 1
        if track == len(audio_file):
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
    chunks = split_on_silence(origin_sound, min_silence_len=50, silence_thresh=-60, keep_silence=6)
    for i, chunk in enumerate(chunks):
        chunk.export(split_sound_dir+'output' + str(i) +'.wav', format='wav')
    
    audio_file = []
    for f in os.listdir(split_sound_dir):
        file_name = split_sound_dir+f
        audio_file.append(file_name)
    audio_file.sort()
    p = Process(target=sound,args=(audio_file,))
    p.start()

    root = tk.Tk()
    app = Application(master=root,sentence=sentence)#Inherit
    app.mainloop()

if __name__ == "__main__":
    main()