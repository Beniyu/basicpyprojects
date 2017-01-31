import random as r
import tkinter as tk

def remove_letters(string):
    complete=[x for x in string if x.isdigit()]
    if len(complete)!=0:
        return int(''.join(complete))
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
    global delay
    pop_up=tk.Toplevel()
    pop_up.title('')
    pop_up.overrideredirect(1)
    message_pop_up=tk.Label(pop_up)
    if type_of_message=='correct':
        message_pop_up.config(text='Correct!',background='green',foreground='white',font=('Times','340'),pady=180,padx=42)
    if type_of_message=='incorrect':
        message_pop_up.config(text='Incorrect',background='red',foreground='white',font=('Times','300'),pady=240,padx=78)
    message_pop_up.pack(fill='both',expand='yes')
    pop_up.after(int(delay*1000),lambda: pop_up.destroy())

def change_button_1(text):
    button1.config(text=text)

def create_setting_visual(window,setting,name,row,column,*options):
    tk.Label(window,text=name,font='Bold').grid(row=row,column=column)
    tk.OptionMenu(window,setting,*options).grid(row=row+1,column=column)

def finish_setting(settings,delay_temp):
    global delay
    delay=delay_temp
    settings.destroy()
    
def settings_menu():
    global difficulty,mode,setting_count,delay
    settings=tk.Toplevel()
    create_setting_visual(settings,difficulty,'Difficulty',0,0,'Easy','Normal','Hard')
    create_setting_visual(settings,mode,'Mode',0,1,'Regular','Unlimited')
    delay_var=tk.DoubleVar()
    delay_var.set(delay)
    tk.Label(settings,text='Popup delay (s)',font='Bold').grid(row=2,column=0)
    delay_temp=tk.Scale(settings,from_=0,to=2,resolution=0.1,orient='horizontal',variable=delay_var).grid(row=3,column=0)
    tk.Button(settings,text='Close',command=lambda: finish_setting(settings,delay_var.get())).grid(row=4,column=0,columnspan=2,sticky='n',ipadx=70)
    
def check_answer():
    global computer_answer,user_input_raw,attempts
    user_answer=remove_letters(user_input_raw.get())
    user_input_raw.set('')
    if attempts['total']==-1:
        change_button_1('Confirm')
    elif computer_answer==user_answer:
        attempts['correct']+=1
        pop_up('correct')
    else:
        pop_up('incorrect')
    attempts['total']+=1
    
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

def confirm():
    global computer_answer
    check_answer()
    correct_counter.config(text="Correct: {}".format(attempts['correct']))
    computer_answer=arithmetic_question_generation()

def arithmetic_question_generation():
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

attempts={'total':-1,'correct':0}
correct_attempts=0
total_attempts=-1
computer_answer=0

operations={'times':{'display':'x','boundary':[1,12]},
    'plus':{'display':'+','boundary':[1,100]},
    'minus':{'display':'-','boundary':[1,100]},
    'divide':{'display':'÷','boundary':[1,12]}}

root=tk.Tk()
delay=1
difficulty=tk.StringVar()
difficulty.set('Normal')
mode=tk.StringVar()
mode.set('Regular')

monitor_width=root.winfo_screenwidth()
monitor_height=root.winfo_screenheight()
screen_width=800
screen_height=291
root.geometry('{}x{}+{}+{}'.format(screen_width,screen_height,window_calculation(monitor_width,screen_width),window_calculation(monitor_height,screen_height)))
root.title('Arithmetic program')

menu=tk.Menu(root)
root.config(menu=menu)
menuFont=('Times',9)

dropdownMenu=tk.Menu(menu,tearoff=0)
menu.add_cascade(label='Mode',menu=dropdownMenu)
dropdownMenu.add_command(label='Type:',font=('Times',9,'bold'))
dropdownMenu.add_command(label='Regular',font=menuFont,command=lambda:set_mode('regular'))
dropdownMenu.add_command(label='Unlimited',font=menuFont,command=lambda:set_mode('unlimited'))
dropdownMenu.add_separator()
dropdownMenu.add_command(label='Difficulty:',font=('Times',9,'bold'))
dropdownMenu.add_command(label='Level 1: Easy',font=menuFont,command=lambda:set_difficulty('easy'))
dropdownMenu.add_command(label='Level 2: Normal',font=menuFont,command=lambda:set_difficulty('normal'))
dropdownMenu.add_command(label='Level 3: Difficult',font=menuFont,command=lambda:set_difficulty('hard'))
dropdownMenu.add_command(label='Custom Difficulty',font=menuFont,command=lambda:set_difficulty('custom'))

settingsMenuButton=tk.Menu(menu,tearoff=0)
menu.add_cascade(label='Extra',menu=settingsMenuButton)
settingsMenuButton.add_command(label='Full Settings Panel',font=menuFont,command=settings_menu)

questionWindow=tk.Label(root,text="Welcome!",relief='raised',font=('Times',72))
questionWindow.pack()

user_input_raw=tk.StringVar()
answerWindow=tk.Entry(root,textvariable=user_input_raw,font=('Times',36))
answerWindow.pack(fill='x',expand='yes')

buttonFrame=tk.Frame(root)
buttonFrame.pack(fill='x',expand='yes')
button1=tk.Button(buttonFrame,text='Begin',font=('Times',36),command=confirm)
button1.pack(side='left',fill='x',expand='yes')
root.bind('<Return>',lambda x: confirm())
tk.Button(buttonFrame,text='End',font=('Times',36),command=finish_program).pack(side='right',expand='no')

correct_counter=tk.Label(root,text="Correct: 0",font=('Times',10,'bold'))
correct_counter.pack()

root.mainloop()



