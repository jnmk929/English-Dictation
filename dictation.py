#
#機能:
# 入力:
# ○ ・大文字小文字関係なく入力できる　入力は小文字に統一
# △・スペース等はスキップ ひとまず２連続　後々固有名詞など長めでも対応できるように
#   ・いい感じで自動改行する 単位ごとに改行
#   ・１文字ヒント機能
#   ・タイプミスの効果
# 音声:
#   ・wavファイルが再生できる
#   ・繰り返し　一時停止
#   ・数秒飛ばし戻し 3s 5s
# その他:
#   ・採点機能　間違い数のカウント　
#   ・入力後に解答の表示
#   ・複数の問題に対応
#   ・入力文字を予め ＿ で伏せて見せておく

import tkinter as tk

class Application(tk.Frame):
    count = 0
    skip_word = [" ",".",",",";","'","-","?","’"]
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
        #flag_keyword = False
        #flag_skip = 0
        key = event.keysym  #入力の受取
        self.buffer.set(key)
        '''
        if key == self.sentence[self.count].lower():    #
            self.count += 1
            flag_keyword = True
        if self.sentence[self.count] in self.skip_word:
            if not self.sentence[self.count+1] in self.skip_word:
                self.count += 1
                flag_skip = 1
            else:
                self.count += 2
                flag_skip = 2

        if self.count == 0:     #一文字目
            self.buffer.set(key)
        elif (flag_skip == 0 and flag_keyword == True and key == self.sentence[self.count-1].lower()) \
          or (flag_skip == 1 and key == self.sentence[self.count-2].lower()):
            self.buffer.set(''.join(self.sentence[:self.count]))
        elif flag_skip == 2:
            self.buffer.set(''.join(self.sentence[:self.count-1]))
        else:
            self.buffer.set(''.join(self.sentence[:self.count])+key)
        '''
textfile = './data/part4.txt'

def main():
    with open(textfile,'r') as f:
        line = f.readlines()
    sentence = list(line[0])    #ファイルには1行の文章の予定
    root = tk.Tk()
    app = Application(master=root,sentence=sentence)#Inherit
    app.mainloop()

if __name__ == "__main__":
    main()