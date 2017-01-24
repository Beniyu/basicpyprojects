import random as r
import tkinter as tk
from time import sleep
import time

def remove_letters(string):
    result1=[]
    valid='false'
    for i in range(len(string)):
        if string[i].isdigit():
            result1.append(string[i])
            valid='true'
    if valid=='true':
        return int(''.join(result1))
    else:
        return 0

def prime_check(number):
    for possible_factor in range(number/2):
        if number%possible_factor==0:
            return True
    else:
        return False

def window_calculation(monitor_dimension,window_dimension):
    return int((monitor_dimension/2)-(window_dimension/2))

def pop_up(type_of_message):
    pop_up=tk.Toplevel()
    pop_up.title('')
    pop_up.overrideredirect(1)
    message_pop_up=tk.Label(pop_up)
    if type_of_message=='correct':
        message_pop_up.config(text='Correct!',background='green',foreground='white',font=('Times','340'),pady=180,padx=42)
    if type_of_message=='incorrect':
        message_pop_up.config(text='Incorrect',background='red',foreground='white',font=('Times','300'),pady=240,padx=78)
    message_pop_up.pack(fill='both',expand='yes')
    pop_up.after(1000,lambda: pop_up.destroy())
    
def finish_program():
    root.destroy()
    quit()

def calculation(number1,number2,operation):
    if operation=='times':
        return number1*number2
    if operation=='plus':
        return number1+number2
    if operation=='minus':
        return number1-number2
    if operation=='divide':
        return number1*number2

def confirm(user_input):
    if total_attempts!=-1 and computer_answer==remove_letters(user_input):
        correct_attempts+=1
        pop_up('correct')
    else:
        pop_up('incorrect')
    total_attempts+=1
    correct_counter.config(text="Correct: {}".format(correct_attempts))
    computer_answer=arithmetic_question()
    return total_attempts,correct_attempts,computer_answer

def arithmetic_question():
    typeofproblem=r.choice(['times','plus','minus','divide'])
    number1,number2=r.randint(*operations[typeofproblem]['boundary']),r.randint(*operations[typeofproblem]['boundary'])
    if typeofproblem=='minus':
        number2=r.randint(1,number1)
    computer_answer=calculation(number1,number2,typeofproblem)
    if typeofproblem=='divide':
        computer_answer,number1=number1,computer_answer
    questionWindow.config(text='What is {} {} {}? '.format(number1,operations[typeofproblem]['display'],number2))
    return computer_answer

##try:
##    options_file=open('options.txt','r')
##    for line in options_file:
##        name,value=line.split(',')
##    print('Option file loaded in.\n')
##except:
##    print('Loading in with no options file.\n')

##if settings['mode']=='unlimited':
##    total=0

settings={'mode':'regular'}
correct_attempts=0
total_attempts=-1
computer_answer=0
operations={'times':{'display':'x','boundary':[1,12]},
    'plus':{'display':'+','boundary':[1,100]},
    'minus':{'display':'-','boundary':[1,100]},
    'divide':{'display':'÷','boundary':[1,12]}}
root=tk.Tk()
monitor_width=root.winfo_screenwidth()
monitor_height=root.winfo_screenheight()
screen_width=800
screen_height=291
root.geometry('{}x{}+{}+{}'.format(screen_width,screen_height,window_calculation(monitor_width,screen_width),window_calculation(monitor_height,screen_height)))
root.title('Arithmetic program')
questionWindow=tk.Label(root,text="Welcome!",relief='raised',font=('Times',72))
questionWindow.pack()
user_input=tk.StringVar()
answerWindow=tk.Entry(root,textvariable=user_input,font=('Times',36))
answerWindow.pack(fill='x',expand='yes')
buttonFrame=tk.Frame(root)
buttonFrame.pack(fill='x',expand='yes')
tk.Button(buttonFrame,text='Confirm',font=('Times',36),command=lambda: confirm(user_input.get(),correct_attempts,total_attempts,computer_answer)).pack(side='left',fill='x',expand='yes')
tk.Button(buttonFrame,text='End',font=('Times',36),command=finish_program).pack(side='right',expand='no')
correct_counter=tk.Label(root,text="Correct: 0")
correct_counter.pack()

#print('Welcome to the Under 11 Arithmetic program.\nOtherwise, type in the correct answer.\n')

##if settings['mode']=='regular':
##    for attempt in range(10):
##        correct,total=arithmetic(correct,total)
##if settings['unlimited']=='unlimited':
##    while True:
##        
##print('You got {}/{} correct.'.format(correct,total))

root.mainloop()
