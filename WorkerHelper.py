import win32clipboard 
import time , os
from googletrans import Translator
from tkinter import Tk
from threading import Lock , Event,Thread
from tkinter import Button

translator = Translator()
mutex = Lock()
runStoper = True


def getCurrentText():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    clearedText = data.replace("\n"," ").replace("\r"," ").strip()
    return clearedText

def translateOk(textT):
    return translator.translate(textT, dest='tr').text

class Controller(object):
    def __init__(self):
        self.thread1 = None
        self.stop_threads = Event()

    def RunThreadApp(self):
        
        lastText = ""
        currentText = ""
        while not self.stop_threads.is_set():
           
            currentText = getCurrentText()
            if currentText != lastText and currentText !="":
                res = translateOk(currentText)
                print("res : " , res , " last : " ,lastText," current = " , currentText)
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(res) 
                win32clipboard.CloseClipboard()
                lastText= res
                currentText=res
            time.sleep(1)

    def combine(self):
        self.stop_threads.clear()
        self.thread1 = Thread(target = self.RunThreadApp)
        self.thread1.start()

    def stop(self):
        self.stop_threads.set()
        self.thread1.join()
        self.thread1 = None


control = Controller()
control.combine()


window = Tk()
im = (str(os.getcwd())+"\\"+"st.ico")
window.iconbitmap(im)
window.title("Welcome to EBB Work Helper App")
btn1 = Button(window, text ="Stop Working", command=control.stop)
btn1.pack()

window.geometry ('350x40')
window.attributes ("-topmost",1)
window.resizable(False, False)
window.mainloop()

if control.thread1 != None:
    command=control.stop()


