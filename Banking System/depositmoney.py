from tkinter import *
root = Tk()
root.geometry("50x50")
root.title("Review Orders")

value = StringVar()
valueentry = Entry(root, textvariable=value)
valueentry.pack()

def button_command():
    global value_deposit
    value_deposit = value.get()
    print(value_deposit)
    root.destroy()

submitbutton = Button(root, text="Submit", command=button_command)
submitbutton.pack()

root.mainloop()
