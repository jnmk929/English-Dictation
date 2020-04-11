import tkinter as tk

class Application(tk.Frame):
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
        key = event.keysym  #入力の受取
        self.buffer.set(key)

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