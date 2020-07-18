# Author: Kalana Abeywardena
# Created on: 17/06/2020

# This is a simple calculator design with the following functionalities
# Addition | Subtraction | Multiplication | Division | Power of 2 | Square Root

from tkinter import *
from tkinter import messagebox, Button
from time import *

cal=Tk()
numpad = Frame(cal, bg = 'Black')
screen = Frame(cal)

cal.geometry("354x460")
cal.title("Project Calculator")                 # can change to anything the user want
melabel = Label(cal,text="cal2345",bg='black', foreground='White',font=("Helvetica",10,'bold','italic')) # edit text field to give a name to yout calculator
melabel.place(x=294,y=2)
cal.configure(background="black")

screen.place(x=10, y = 24, width = 332, height = 60)
screen_1 = Entry(screen, background="White", foreground="black")     # setting the screen_1 to display intermediate valueif multiple operations are performed pair-wise
screen_1.insert(0,"")
screen_1.grid(row=0, column=0, ipadx=102, ipady=3, padx=2, pady=2)

screen_2 = Entry(screen, background="White", foreground="black")     # main screen one number at a time
screen_2.insert(0,"0")
screen_2.grid(row=1, column=0, ipadx=102, ipady=3, padx=2, pady=2)


calc = 0.0
math_op = ''
result = 0.0
last_equal = False

def numbtn(value):                          # display numbers in the screen
    if value != 'AC':
        val_screen = screen_2.get()
        if val_screen == '0':
            content = '' + value
        else:
            content = val_screen + value
        screen_2.delete(0,END) 
        screen_2.insert(0,content)            # update the new value

    elif value == '.':
        decimal = str(screen_2.get()) + '.'
        screen_2.insert(0,decimal)

    else:                                   # when AC is clicked the screen gets cleared (to do a new calculation should always press AC)
        screen_2.delete(0,END)
        screen_2.insert(0,'0')
        screen_1.delete(0,END)
        screen_1.insert(0,'')

def reverse(value):                             # function to make the numbers negative, squared and square root
    global result 
    global math_op

    if value == '-':                            # negating the value on screen
        scr_value = float(screen_2.get())
        sub = str(-1*scr_value)
        screen_2.delete(0, END)
        screen_2.insert(0, sub)

    elif value == '^2':                         # raising to power 2
        scr_value = float(screen_2.get())
        squared_content = screen_1.get() 
        screen_1.delete(0,END)
        screen_1.insert(0,squared_content + screen_2.get() + '\u00B2')
        screen_2.delete(0,END)
        screen_2.insert(0, "{:.3f}".format(scr_value**2))
        screen_1.delete(0,END)
        screen_1.insert(0,squared_content)
        result = scr_value**2

    elif value == '^0.5':                       # finding the square root
        scr_value = float(screen_2.get())
        sqrt_content = screen_1.get() 
        screen_1.delete(0,END)
        screen_1.insert(0,sqrt_content+'\u221A' + screen_2.get())
        screen_2.delete(0,END)
        screen_2.insert(0, "{:.3f}".format(scr_value**0.5))
        screen_1.delete(0,END)
        screen_1.insert(0,sqrt_content)
        result = scr_value**0.5

def calculation(condition):                 # perform calculations (can only do the operations pair-wise)
    ''' 
    This function supports the following calculations
        1. Addition
        2. Subtraction
        3. Division
        4. Multiplication
        
    Returns the result as a decimal number on to the screen
    '''
    global calc
    global math_op
    global result 
    global last_equal

    if condition != '=':
        calc = float(screen_2.get())
        screen_2.delete(0,END)

    if condition == '+':
        add_content = str(calc) + condition
        screen_1.delete(0,END)
        screen_1.insert(0,add_content)
        math_op = '+'
        last_equal = False

    elif condition == '-':
        sub_content = str(calc) + condition
        screen_1.delete(0,END)
        screen_1.insert(0,sub_content)
        math_op = '-'
        last_equal = False

    elif condition == 'x':
        mult_content = str(calc) + condition
        screen_1.delete(0,END)
        screen_1.insert(0,mult_content)
        math_op = 'x'
        last_equal = False

    elif condition == '/':
        div_content = str(calc) + condition
        screen_1.delete(0,END)
        screen_1.insert(0,div_content)
        math_op = '/'
        last_equal = False

    elif condition == '=':
        value_screen = screen_2.get()
        
        if last_equal:
            screen_1.delete(0,END)
            
        if math_op == '+':
            result = calc + float(value_screen)
        elif math_op == '-':
            result = calc - float(value_screen)
        elif math_op == 'x':
            result = calc * float(value_screen)
        elif math_op == '/':
            result = calc / float(value_screen)

        sc1_content = screen_1.get() 
        screen_1.delete(0,END)
        screen_1.insert(0,sc1_content + value_screen)

        screen_2.delete(0, "end")

        if (math_op != '') and (not last_equal):
            screen_2.insert(0, "{:.3f}".format(result))
            calc = float(value_screen)
            last_equal = True

        elif math_op != '' and last_equal:
            sc1_content = screen_1.get() 
            screen_1.delete(0,END)
            screen_1.insert(0,sc1_content + math_op + str(calc))
            screen_2.insert(0, "{:.3f}".format(result))

numpad.place(x=10, y = 90)

# number buttons
btn1 = Button(numpad, text="1",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('1'))
btn1.grid(row=1,column=0)

btn2 = Button(numpad,text="2",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('2'))
btn2.grid(row=1,column=1)

btn3 = Button(numpad,text="3",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('3'))
btn3.grid(row=1,column=2)

btn4 = Button(numpad,text="4",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('4'))
btn4.grid(row=2,column=0)

btn5 = Button(numpad,text="5",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('5'))
btn5.grid(row=2,column=1)

btn6 = Button(numpad,text="6",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('6'))
btn6.grid(row=2,column=2)

btn7 = Button(numpad, text="7",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('7'))
btn7.grid(row=3,column=0)

btn8 = Button(numpad, text="8",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('8'))
btn8.grid(row=3,column=1)

btn9 = Button(numpad, text="9",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('9'))
btn9.grid(row=3,column=2)

btn0 = Button(numpad,text="0",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('0'))
btn0.grid(row=4,column=0)

# operation buttons

btnadd = Button(numpad, text="+",font="Helvetica 12 bold",height="3",width="6",background="#E39F29",command=lambda: calculation("+"))
btnadd.grid(row=2,column=3)

btnSub = Button(numpad, text="-",font="Helvetica 12 bold",height="3",width="6",background="#E39F29",command=lambda: calculation(str('-')))
btnSub.grid(row=3,column=3)

btnMult = Button(numpad, text="x",font="Helvetica 12 bold",height="3",width="6",background="#E39F29",command=lambda: calculation(str('x')))
btnMult.grid(row=1,column=3)

btnDiv = Button(numpad, text="/",font="Helvetica 12 bold",height="3",width="6",background="#E39F29",command=lambda: calculation(str('/')))
btnDiv.grid(row=0,column=3)

btnEqual = Button(numpad,text="=",font="Helvetica 12 bold",height="3",width="6",background="#E39F29",command=lambda: calculation('='))
btnEqual.grid(row=4,column=3)

btnsqd = Button(numpad, text="x\u00B2",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#495438",command=lambda: reverse("^2"))
btnsqd.grid(row=0,column=2)

btnsqrt = Button(numpad, text="\u221Ax",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#495438",command=lambda: reverse("^0.5"))
btnsqrt.grid(row=0,column=1)

# Special function buttons
btnClear = Button(numpad,text="AC",fg="white",font="Helvetica 12 bold",height="3",width="6",background="Red",command=lambda: numbtn('AC'))
btnClear.grid(row=0,column=0)

btnDot = Button(numpad, text=".",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#4D4D4D",command=lambda: numbtn('.'))
btnDot.grid(row=4,column=1)

btnpm = Button(numpad, text="+/-",fg="white",font="Helvetica 12 bold",height="3",width="6",background="#495438",command=lambda: reverse("-"))
btnpm.grid(row=4,column=2)

btnexit = Button(numpad, text="OFF", fg="white",font="Helvetica 12 bold",height="7",width="5",background="Red", command=cal.destroy)
btnexit.grid(row=0,column=4, rowspan=2)

cal.mainloop()