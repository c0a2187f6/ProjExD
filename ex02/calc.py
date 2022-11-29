import tkinter as tk
import tkinter.messagebox as tkm

#ボタンの配置
BUTTON = [
  ['', 'AC', 'C', '='],
  ['7', '8', '9', '/'],
  ['4', '5', '6', '*'],
  ['1', '2', '3', '-'],
  ['00', '0', '.', '+'],
]

#ポインタを当てる
def mouse_over(event):
  btn = event.widget
  btn["bg"] = "#808080"

#ポインタを外す
def mouse_leave(event):
  btn = event.widget
  btn['bg'] = '#ffffff'


#練習3
def button_click(event):
  btn = event.widget
  num = btn["text"]


  #練習7
  if num == "=":
    siki = entry.get() #数式の文字列
    res = eval(siki) #数式文字列の評価
    entry.delete(0, tk.END) #表示文字列の削除
    entry.insert(tk.END, res) #結果の挿入
  elif num == "AC":
    entry.delete(0, tk.END) #オールクリア
  elif num == "C":
    entry.delete(len(entry.get())-1, tk.END) #1文字クリア
  else:
    # tkm.showinfo("", f"{num}ボタンが押されました")
    #練習6
    entry.insert(tk.END, num)

#練習1
root = tk.Tk()
root.geometry("300x500")

#練習4
entry = tk.Entry(root, justify="right", width=10, font=("", 20))
entry.grid(row=0, column=0, columnspan=3)


for r, row in enumerate(BUTTON, 1):
  for c, num in enumerate(row):
    button = tk.Button(root, text=num, font=('', 15), width=6, height=3, bg='#ffffff')
    button.grid(row=r, column=c)
    button.bind("<Enter>", mouse_over)
    button.bind("<Leave>", mouse_leave)
    button.bind("<1>", button_click)
    

root.mainloop()
