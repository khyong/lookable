from Tkinter import *
from PIL import Image, ImageTk


def callback(event):
  print("click - ", event.x, event.y)
  data = "click - ", event.x, event.y
  f.write(str(data[1]))
  f.write(",")
  f.write(str(data[2]))
  f.write("\n")

def callimg(filename):
  root=Tk()
  root.title("wallpaper")

  image=Image.open(filename)
  display=ImageTk.PhotoImage(image)
  label=Label(root,image=display)
  label.bind("<Button-1>",callback)
  label.pack()

  root.mainloop()

f = open("coor.txt", 'a')
for i in range(414,415):
  f.write("shoes_"+str(i)+".png\n")
  callimg("./shoes/shoes_"+str(i)+".png")

f.close()
