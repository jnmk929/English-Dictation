import tkinter as tk

root = tk.Tk()
root.geometry('300x200')
root.title('サンプルプログラム')

buffer = tk.StringVar() # ①   入力情報を変数に代入
#buffer.set('')

# キーの表示
def print_key(event): # ③
    key = event.keysym  #キーの識別番号
    buffer.set(key)

# ラベルの設定
tk.Label(text='何か入力してください。').pack()
a = tk.Label(textvariable=buffer) # ②   表示用ラベルに紐付ける
a.pack()
a.bind('<Key>', print_key) # ④ ボタンが押されたときに実行
a.focus_set() # ⑤ キー入力のおまじない

root.mainloop()