import tkinter as tk
import maze_maker as mm
import tkinter.messagebox as tkm

def count_up(): # ゲームを始めてから時間を数える
  global tmr
  global jid
  label["text"] = tmr
  tmr += 1
  jid = root.after(1000, count_up)

def key_down(event):
  global key 
  key = event.keysym

def key_up(event):
  global key
  key = ""

def main_proc():
  global cx, cy, mx, my
  if key == "Up":
    my -= 1
  if key == "Down":
    my += 1
  if key == "Left":
    mx -= 1
  if key =="Right":
    mx += 1

  # if key == "r":
  #   mm.show_maze(canvas, maze_lst)

  if maze_lst[mx][my] == 1: #移動先が壁だったら  
    if key == "Up":
      my += 1
    if key == "Down":
      my -= 1
    if key == "Left":
      mx += 1
    if key =="Right":
      mx -= 1
    canvas.coords("kokaton2", cx, cy)
  # else:
  #   canvas.coords("kokaton", cx, cy)


  cx, cy = mx*100+50, my*100+50
  # canvas.coords("kokaton", cx, cy)
  root.after(100, main_proc)


if __name__ == "__main__":
  root = tk.Tk()
  root.title("迷えるこうかとん")

  label = tk.Label(root, text="Redy?", font=("", 30))

  label.pack()
  tmr = 0
  jid = None
  count_up()
  
  canvas = tk.Canvas(root, width=1500, height=900, bg="black")
  canvas.pack()

  maze_lst = mm.make_maze(15, 9)
  # print(maze_lst)
  mm.show_maze(canvas, maze_lst)


  kokaton = tk.PhotoImage(file="fig/4.png")
  kokaton2 = tk.PhotoImage(file="fig/1.png")
  mx, my = 1, 1
  cx, cy = mx*100+50, my*100+50

  
  canvas.create_rectangle(cx-50, cy-50, cx+50, cy+50, fill="red")
  # canvas.create_rectangle(fill="blue") ゴールを作りたかった
  canvas.create_image(cx, cy, image=kokaton, tag="kokaton")

  key = ""
  root.bind("<KeyPress>", key_down)
  root.bind("<KeyRelease>", key_up)
  main_proc()

  root.mainloop() 