from Tkinter import *
import threading

def do(*cmd):
    root = Tk()
    for c in cmd:
        Button(root, text="Stop {}".format(c.__class__.__name__), command=c.stop).pack()
    root.mainloop()

def run_gui(*cmd):
    t = threading.Thread(target=do, args=cmd)
    t.daemon = True
    t.start()
