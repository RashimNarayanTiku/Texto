import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import font, colorchooser, filedialog, messagebox
import os, shutil
from tkinter.font import Font
import spell_checker
from spell_checker import correction
import pyttsx3
from time import sleep
import time
from idlelib import window
import logging
from multiprocessing.dummy import Process as Thread


main_application = themed_tk.ThemedTk()
main_application.geometry('900x600')
main_application.wm_iconbitmap('icon.ico')



#################################### MAIN-MENU ###########################################

main_menu = tk.Menu()


#MENU options
File = tk.Menu(main_menu,tearoff=False)
Edit = tk.Menu(main_menu,tearoff=False)
View = tk.Menu(main_menu,tearoff=False)
Features = tk.Menu(main_menu,tearoff=False)
Theme = tk.Menu(main_menu,tearoff=False)
About = tk.Menu(main_menu,tearoff=False)

#FILE ICONS 
new_icon = tk.PhotoImage(file=r'icons2/new.png')
open_icon = tk.PhotoImage(file=r'icons2/open.png')
save_icon = tk.PhotoImage(file=r'icons2/save.png')
save_as_icon = tk.PhotoImage(file=r'icons2/save_as.png')
exit_icon = tk.PhotoImage(file=r'icons2/exit.png')

#EDIT ICONS
copy_icon = tk.PhotoImage(file=r'icons2/copy.png')
cut_icon = tk.PhotoImage(file=r'icons2/cut.png')
paste_icon = tk.PhotoImage(file=r'icons2/paste.png')
clear_all_icon = tk.PhotoImage(file=r'icons2/clear_all.png')
find_icon = tk.PhotoImage(file=r'icons2/find_2.png')

#VIEW ICONS
tool_bar_icon = tk.PhotoImage(file=r'icons2/tool_bar.png')
status_bar_icon = tk.PhotoImage(file=r'icons2/status_bar.png')

#FEATURES ICONS
spell_check_on_icon = tk.PhotoImage(file='icons2/book_non_trans.png')
spell_check_off_icon = tk.PhotoImage(file='icons2/book_trans.png')
tts_on_icon = tk.PhotoImage(file='icons2/tts2_on.png')
tts_off_icon = tk.PhotoImage(file='icons2/tts2_off.png')

#THEME ICONS
light_default_icon = tk.PhotoImage(file=r'icons2/light_default2.png')
light_plus_icon = tk.PhotoImage(file=r'icons2/light_plus2.png')
dark_icon = tk.PhotoImage(file=r'icons2/dark2.png')
red_icon = tk.PhotoImage(file=r'icons2/red2.png')
monokai_icon = tk.PhotoImage(file=r'icons2/monokai2.png')
night_blue_icon = tk.PhotoImage(file=r'icons2/night_blue2.png')


theme_choice = tk.StringVar()
color_icons = (light_default_icon,light_plus_icon,dark_icon,red_icon,monokai_icon,night_blue_icon)

color_dict ={
    "Light Theme":('#000000','#ffffff','xpnative'),
    "Light Plus Theme":('#474747','#e0e0e0','clam'),
    "Dark Theme":('#c4c4c4','#2d2d2d','black'),
    "Red Theme":('#2d2d2d','#ffe8e8','radiance'),
    "Monokai Theme":('#d3b774','#474747','ubuntu'),
    "Night Blue Theme":('#ededed','#6b9dc2','itft1')
}

#cascading the menu
main_menu.add_cascade(label='File',menu=File)
main_menu.add_cascade(label='Edit',menu=Edit)
main_menu.add_cascade(label='View',menu=View)
main_menu.add_cascade(label="Features",menu=Features)
main_menu.add_cascade(label='Theme',menu=Theme)
main_menu.add_cascade(label='About',menu=About)
#----------------------------------------------END OF MAIN-MENU -------------------------------------














# #################################### TOOLBAR ###########################################

tool_bar = ttk.Label(main_application)

## undo button/label
on_undo_icon = tk.PhotoImage(file=r'icons2/on_undo.png')
off_undo_icon = tk.PhotoImage(file=r'icons2/off_undo.png')
on_redo_icon = tk.PhotoImage(file=r'icons2/on_redo.png')
off_redo_icon = tk.PhotoImage(file=r'icons2/off_redo.png')

undo_btn = ttk.Label(tool_bar,image=off_undo_icon,cursor='hand2')
undo_btn.grid(row=0,column=0,padx=1)
redo_btn = ttk.Label(tool_bar,image=off_redo_icon,cursor='hand2')
redo_btn.grid(row=0,column=2,padx=1)

##font box
font_tuples = tk.font.families()
font_selected = tk.StringVar()
font_box = ttk.Combobox(tool_bar,width=30,textvariable=font_selected,state='readonly',cursor='hand2')
font_box['values'] = font_tuples
font_box.current(font_tuples.index('Arial'))
font_box.grid(row=0,column=5,padx=2)

##size box
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar, width=14,textvariable=size_var,state='readonly',cursor='hand2')
font_size['values'] = tuple(range(8,81,2))
font_size.current(2)
font_size.grid(row=0,column=6,padx=2)

##font size changer buttons
text_size_up_icon = tk.PhotoImage(file='icons2/resize-font-up.png')
text_size_down_icon = tk.PhotoImage(file='icons2/resize-font-down.png')

text_size_up_btn = ttk.Label(tool_bar,image=text_size_up_icon,cursor='hand2')
text_size_up_btn.grid(row=0,column=7,padx=2)
text_size_down_btn = ttk.Label(tool_bar,image=text_size_down_icon,cursor='hand2')
text_size_down_btn.grid(row=0,column=8,padx=2)

## font color button
font_color_icon = tk.PhotoImage(file='icons2/font_color.png')
font_color_btn = ttk.Label(tool_bar,image=font_color_icon,cursor='hand2')
font_color_btn.grid(row=0,column=9,padx=2)


emptytext= ttk.Label(tool_bar,text='').grid(row=0,column=10,padx=7)


##bold button
off_bold_icon = tk.PhotoImage(file='icons2/off_bold.png')
on_bold_icon = tk.PhotoImage(file='icons2/on_bold.png')
bold_btn = ttk.Label(tool_bar,image=off_bold_icon,cursor='hand2')
bold_btn.grid(row=0,column=11,padx=2)

##italic button
off_italic_icon = tk.PhotoImage(file='icons2/off_italic.png')
on_italic_icon = tk.PhotoImage(file='icons2/on_italic.png')
italic_btn = ttk.Label(tool_bar,image=off_italic_icon,cursor='hand2')
italic_btn.grid(row=0,column=12,padx=2)


##underline button
off_underline_icon = tk.PhotoImage(file='icons2/off_underline.png')
on_underline_icon = tk.PhotoImage(file='icons2/on_underline.png')
underline_btn = ttk.Label(tool_bar,image=off_underline_icon,cursor='hand2')
underline_btn.grid(row=0,column=13,padx=2)


emptytext= ttk.Label(tool_bar,text='').grid(row=0,column=14,padx=7)


##align center
on_align_center_icon = tk.PhotoImage(file='icons2/align-center-2x.png')
align_center_btn = ttk.Label(tool_bar,image=on_align_center_icon,cursor='hand2')
align_center_btn.grid(row=0,column=15,padx=2)


##align left
on_align_left_icon = tk.PhotoImage(file='icons2/align-left-2x.png')
align_left_btn = ttk.Label(tool_bar,image = on_align_left_icon,cursor='hand2')
align_left_btn.grid(row=0,column=16,padx=2)


##align right
on_align_right_icon = tk.PhotoImage(file='icons2/align-right-2x.png')
align_right_btn = ttk.Label(tool_bar,image = on_align_right_icon,cursor='hand2')
align_right_btn.grid(row=0,column=17,padx=2)

emptytext= ttk.Label(tool_bar,text='').grid(row=0,column=18,padx=7)

## find button
find_btn = ttk.Label(tool_bar,image=find_icon,cursor='hand2')
find_btn.grid(row=0, column=19, padx=2)

## find and replace labels and entry fields
find_state = 0
find_label = ttk.Label(tool_bar,text='Find',font=('InkFree',9))
find_label.grid(row=0,column=20)
find_var = tk.StringVar()
find_entry = ttk.Entry(tool_bar,textvariable=find_var,width=20)
find_entry.grid(row=0,column=21)

replace_label=ttk.Label(tool_bar,text='Replace',font=('InkFree',9))
replace_label.grid(row=0,column=22)
replace_var = tk.StringVar()
replace_entry = ttk.Entry(tool_bar,textvariable=replace_var,width=20)
replace_entry.grid(row=0,column=23)

submit_icon = tk.PhotoImage(file='icons2/enter.png')
submit_btn = ttk.Label(tool_bar,image = submit_icon)
submit_btn.grid(row = 0,column= 24)

find_label.grid_remove()
find_entry.grid_remove()
replace_label.grid_remove()
replace_entry.grid_remove()
submit_btn.grid_remove()



#----------------------------------------------END OF TOOLBAR -------------------------------------














#################################### TEXT-EDITOR ##########################################

text_editor = tk.Text(main_application)
text_editor.config(wrap='word',relief=tk.FLAT, undo=True)
text_editor.focus_set()

yscroll_bar = tk.Scrollbar(main_application)
yscroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=yscroll_bar.set)


##undo_redo functionality
def undo_func(event=None):
    undo_btn.config(image=on_undo_icon)
    text_editor.event_generate('<Control-z>')
def redo_func(event=None):
    redo_btn.config(image=on_redo_icon)
    text_editor.event_generate('<Control-y>')
def change_undo(event=None):
    undo_btn.config(image=off_undo_icon)
def change_redo(event=None):
    redo_btn.config(image=off_redo_icon)

undo_btn.bind('<Button-1>', undo_func)
undo_btn.bind('<ButtonRelease-1>', change_undo)
redo_btn.bind('<Button-1>', redo_func)
redo_btn.bind('<ButtonRelease-1>', change_redo)


## font family and font size functionality
my_font=Font(family='Arial',size=12)      
text_editor.configure(font=my_font)

## states of the formatting buttons
current_font_family = 'Arial'
current_font_size = 12
bold_state='normal'
italic_state='roman'
underline_state=0

def change_font_family(event=None):
    global current_font_family
    current_font_family = font_selected.get()
    change_formatting()
def change_font_size(event=None):
    global current_font_size
    current_font_size = size_var.get()
    change_formatting()
font_box.bind("<<ComboboxSelected>>",change_font_family)
font_size.bind("<<ComboboxSelected>>",change_font_size)

## to change formatting
def change_formatting():
    my_font.configure(family=current_font_family,size=current_font_size,weight=bold_state,slant=italic_state,underline=underline_state)


## text size up button functionality
def text_size_up(event=None):
    global current_font_size
    if current_font_size < 80:
        current_font_size += 2
        change_formatting()
        index = font_size.current()
        font_size.current(index+1)
text_size_up_btn.bind('<Button-1>',text_size_up)


## text size down button functionality
def text_size_down(event=None):
    global current_font_size
    if current_font_size > 8:
        current_font_size -= 2
        change_formatting()
        index = font_size.current()
        font_size.current(index-1)
text_size_down_btn.bind('<Button-1>',text_size_down)


## bold button functionality
def change_bold(event=None):
    global bold_state
    text_property = tk.font.Font(font=text_editor['font'])
    if my_font['weight'] == 'normal':
        bold_state='bold'
        change_formatting()
        bold_btn.config(image=on_bold_icon)
    elif my_font['weight'] == 'bold' :
        bold_state='normal'
        change_formatting()
        bold_btn.config(image=off_bold_icon)
bold_btn.bind('<Button-1>',change_bold)


## italic button functionality
def change_italic(event=None):
    global italic_state
    # text_property = tk.font.Font(font=text_editor['font'])
    if my_font['slant']=='roman':
        italic_state='italic'
        change_formatting()
        italic_btn.config(image=on_italic_icon)
    elif my_font['slant']=='italic' :
        italic_state='roman'
        change_formatting()
        italic_btn.config(image=off_italic_icon)
italic_btn.bind('<Button-1>',change_italic)


## underline button functionality
def change_underline(event=None):
    global underline_state
    # text_property = tk.font.Font(font=text_editor['font'])
    if my_font['underline']==0:
        underline_state=1
        change_formatting()
        underline_btn.config(image=on_underline_icon)

    elif my_font['underline']==1 :
        underline_state=0
        change_formatting()
        underline_btn.config(image=off_underline_icon)
underline_btn.bind('<Button-1>',change_underline)


## font color button functionality
def change_font_color(event=None):
    color_var = tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])
font_color_btn.bind('<Button-1>',change_font_color)

## align right functionality
def align_right(event=None):
    text_content = text_editor.get(1.0,'end')
    text_editor.tag_config('right',justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content,'right')
align_right_btn.bind('<Button-1>',align_right)

## align left functionality
def align_left(event=None):
    text_content = text_editor.get(1.0,'end')
    text_editor.tag_config('left',justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content,'left')
align_left_btn.bind('<Button-1>',align_left)

## align center functionality
def align_center(event=None):
    text_content = text_editor.get(1.0,'end')
    text_editor.tag_config('center',justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_content,'center')
align_center_btn.bind('<Button-1>',align_center)


# initialize the spell checking dictionary.
words=open("dict.txt").read().split("\n")
words = list(word.lower() for word in words)


def remove_widget(widget):
    widget.grid_remove()

found_list = []
def find_show_hide(event=None):
    ''' shows or hides the find/replace column '''
    
    global find_state
    find_word = find_var.get()
    if find_state:
        find_state = 0
        find_label.grid_remove()
        find_entry.grid_remove()
        replace_label.grid_remove()
        replace_entry.grid_remove()
        submit_btn.grid_remove()
        
        ##removing entry in find and replace
        find_entry.delete(0,'end')
        replace_entry.delete(0,'end')
        
        ## remove the tags from found words
        if len(found_list) == 0:
            return
        else:
            for start_pos in found_list:
                end_pos = f'{start_pos}+{len(find_word)}c'
                text_editor.tag_remove('match',start_pos,end_pos)
        
    else:
        find_state = 1
        find_label.grid()
        find_entry.grid()
        replace_label.grid()
        replace_entry.grid()
        submit_btn.grid()

find_btn.bind('<Button-1>',find_show_hide)

def find_and_replace(event=None):
    '''Finds and replaces the word '''

    global found_list
    found_list.clear()
    find_word = find_var.get()
    replace_word = replace_var.get()
    text_editor.tag_remove('match','1.0',tk.END)
    matches=0
    if find_word:
        start_pos = '1.0'
        while True:
            start_pos = text_editor.search(find_word,start_pos,stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f'{start_pos}+{len(find_word)}c'
            if replace_word:
                text_editor.delete(start_pos,end_pos)
                text_editor.insert(start_pos,replace_word)
            else:
                text_editor.tag_add('match',start_pos,end_pos)
                found_list.append(start_pos)

            start_pos = end_pos
            matches += 1
            text_editor.tag_config('match',foreground='red',background='yellow')
submit_btn.bind('<Button-1>',find_and_replace)
find_entry.bind('<Return>',find_and_replace)
replace_entry.bind('<Return>',find_and_replace)


def spell_check(event=None):
    '''spell_check the word preceeding the insertion point'''
    
    index = text_editor.search(r'\s', "insert", backwards=True, regexp=True)

    if index == "":
        index ="1.0"
    else:
        index = text_editor.index(f"{index}+1c")

    #removing special_char from word
    special_char = ('.','?',',',';',':','\'','"','[',']','{','}','>','<','/','\\','+','=','-','_','!','@','#','$','%','^')
    raw_word = text_editor.get(index, "insert")
    word = ''.join(i for i in raw_word if i not in special_char).lower()

    if(len(word) > 45):
        word = ' '
    text_editor.tag_configure("misspelled",foreground='red')
    corrected_word = correction(word)

    ## DISPLAYING spell_check 
    if corrected_word != word and corrected_word != "s":
        spell_check_label=ttk.Label(status_bar,text=f'Did you mean: {corrected_word}',font=('FreeInk',9))
        spell_check_label.grid(row = 0,column=1)
        main_application.after(2000,remove_widget,spell_check_label)

    if word in words:
        text_editor.tag_remove("misspelled", index, f"{index}+{len(word)}c")
    else:
        text_editor.tag_add("misspelled", index, f"{index}+{len(word)}c")

## Binding space with spell checking 
text_editor.bind("<space>",spell_check)

#---------------------------------------------END OF TEXT-EDITOR -------------------------------------












#################################### STATUS BAR ##########################################

status_bar = ttk.Label(main_application,compound=tk.LEFT)

## Spell check icon
spell_check_btn = ttk.Label(status_bar,image=spell_check_on_icon)
spell_check_btn.grid(row = 0,column=0)

##word and character count
words_count = 0
characters_count = 0
countLabel= ttk.Label(status_bar, width=25, text=f"Words: {words_count}  Characters: {characters_count}")
countLabel.grid(row=0,column=2,sticky='n')
emptytext= ttk.Label(tool_bar,text='')
emptytext.grid(row=0,column=1)

status_bar.grid_columnconfigure(2, weight=1)

## text to speech
tts_btn = ttk.Label(status_bar,image=tts_on_icon,cursor='hand2')
tts_btn.grid(row=0,column=2,sticky='e')

def changed(event=None):
    global is_saved
    global words_count
    global characters_count
    if text_editor.edit_modified():
        is_saved = False
        saved_state()
        words_count = len(text_editor.get(1.0,'end-1c').split())
        characters_count = len(text_editor.get(1.0,'end-1c'))
        countLabel.configure(text=f'Words: {words_count}  Characters: {characters_count}')
    text_editor.edit_modified(False)
text_editor.bind('<<Modified>>',changed)


#----------------------------------------------END OF STATUS BAR -------------------------------------















#################################### MAIN-MENU FUNCTIONALITY ###########################################

url = 'Untitled.txt'
is_saved = True

## to set * with filename
def saved_state():
    if is_saved:
        main_application.title(f'{os.path.basename(url)} - Texto')
    else:
        main_application.title(f'*{(os.path.basename(url))} - Texto')


##new functionality
def new_file(event=None):
    global url
    if not is_saved:
        choice = messagebox.askokcancel('New file','Are you sure you want to open a new file. Any unsaved changes will be lost.')
    if not choice:
        return
    url = 'Untitled.txt'
    text_editor.delete(1.0,tk.END)
File.add_command(label='New',image=new_icon,compound=tk.LEFT,accelerator='CTRL+N', command=new_file)


## open functionality
def open_file(event=None):
    global url
    global is_saved
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text Files','*.txt'),('All Files','*.*')))
    try:
        with open(url,'r') as rf:
            text_editor.delete(1.0,tk.END)
            text_editor.insert(1.0,rf.read())
    except FileNotFoundError:
        return 
    except:
        return 
    is_saved = True
    saved_state()
File.add_command(label='Open',image=open_icon,compound=tk.LEFT,accelerator='CTRL+O',command=open_file)


## Save functionality
def save_file(event=None):
    global url
    global is_saved
    try:
        if url == 'Untitled.txt':
            save_as_file()
        else:
            contents = str(text_editor.get(1.0,tk.END))
            with open(url,'r+',encoding='utf-8') as wf:
                wf.write(contents)
                is_saved = True
                saved_state()
    except:
        messagebox.showerror('Saving Error','An error occured while saving the file. The file has not been saved')
        return

File.add_command(label='Save',image=save_icon,compound=tk.LEFT,accelerator='CTRL+S',command=save_file)


##Save as functionality
def save_as_file(event=None):
    global url
    global is_saved
    file_name = filedialog.asksaveasfilename(filetypes=(('Text Files','*.txt'),('All Files','*.*')),defaultextension='.txt')
    if not file_name:
        return
    else:
        try:
            file2save = open(file_name,'w')
            text2save = str(text_editor.get(1.0,tk.END))
            file2save.write(text2save)
            file2save.close()
            url = file_name
            is_saved = True
            saved_state()
            file2save.close()
        except:
            messagebox.showerror('Saving Error','Error while saving file. File is not saved.')
File.add_command(label='Save as',image=save_as_icon,compound=tk.LEFT,accelerator='CTRL+Q',command=save_as_file)

##exit functionality
## ON EXIT
def on_closing():
    if is_saved:
        main_application.quit()
    else:
        choice = messagebox.askyesnocancel('TEXTO','Do you want to save the changes made to the file?')
        if choice:
            save_file()
            main_application.quit()
        elif choice is None:
            return
        else:
            main_application.quit()
main_application.protocol('WM_DELETE_WINDOW',on_closing)
File.add_command(label = 'Exit',image=exit_icon,compound=tk.LEFT,accelerator='CTRL+E',command=on_closing)

#adding images to EDIT menu
Edit.add_command(label='Copy',image=copy_icon,compound=tk.LEFT,accelerator='CTRL+C',command=lambda:text_editor.event_generate('<Control-c>'))

Edit.add_command(label='Cut',image=cut_icon,compound=tk.LEFT,accelerator='CTRL+X',command=lambda:text_editor.event_generate('<Control-x>'))

Edit.add_command(label='Paste',image=paste_icon,compound=tk.LEFT,accelerator='CTRL+V',command=lambda:text_editor.event_generate('<Control-v>'))

Edit.add_command(label='Clear All',image=clear_all_icon,compound=tk.LEFT,accelerator='CTRL+ALT+X',command=lambda:text_editor.delete(1.0, tk.END))



# VIEW MENU FUNCTIONALITY
tool_bar_state = tk.BooleanVar()
tool_bar_state.set(True)
status_bar_state = tk.BooleanVar()
status_bar_state.set(True)

def show_hide_toolbar():
    global tool_bar_state
    if tool_bar_state:
        tool_bar.pack_forget()
        tool_bar_state=False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP,fill=tk.X)
        text_editor.pack(fill=tk.BOTH,expand=True)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        tool_bar_state=True
def show_hide_statusbar():
    global status_bar_state
    if status_bar_state:
        status_bar.pack_forget()
        status_bar_state=False
    else:
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_bar_state=True

View.add_checkbutton(label='Tool Bar',image=tool_bar_icon,compound=tk.LEFT,variable=tool_bar_state, onvalue=True, offvalue=False, command=show_hide_toolbar)
View.add_checkbutton(label='Status Bar',image=status_bar_icon,compound=tk.LEFT, variable=status_bar_state, onvalue=True, offvalue=False,command=show_hide_statusbar)




# COLOR THEME
def theme_change():
    theme = theme_choice.get()
    color_tuple = color_dict.get(theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    text_editor.config(fg=fg_color,background = bg_color)
    main_application.set_theme(color_tuple[2])
count = 0
for i in color_dict:
    Theme.add_radiobutton(label=i,image=color_icons[count],variable=theme_choice,compound=tk.LEFT,command=theme_change)
    count+=1


# FEATURES

##spell_check button
spell_check_state = tk.BooleanVar()
spell_check_state.set(True)

def change_spell_check(event=None):
    global spell_check_state
    if spell_check_state:
        spell_check_state = False
        spell_check_btn.configure(image=spell_check_off_icon)
        text_editor.unbind("<space>")
    else:        
        spell_check_state = True
        spell_check_btn.configure(image=spell_check_on_icon)
        text_editor.bind("<space>",spell_check)
Features.add_checkbutton(label='Spell Checker',image=spell_check_on_icon,compound=tk.LEFT,variable=spell_check_state,command=change_spell_check)


## Text to Speech

logger = logging.getLogger(__name__)

## MADE A DIFFERENT CLASS TO STOP TTS MIDSENTENCE
class VoiceBox(object):
    def __init__(self):
        self.t = None
        self._running = False
        self.engine = None

    def _processSpeech(self, text):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate',120)
        self.engine.say(str(text))
        self.engine.startLoop(False)
        while self._running:
            self.engine.iterate()
        logger.debug('Thread loop stopped')

    def say(self, text, noInter=2):
        # check if thread is running
        if self.t and self._running:
            logger.debug('Interupting...')
            # stop it if it is
            self.stop()
        # iterate speech in a thread
        logger.debug('Talking: %s', text)
        self.t = Thread(target=self._processSpeech, args=(text,))
        

        self._running = True
        self.t.daemon = True
        self.t.start()
        # give the thread some space
        # without this sleep and repeatitive calls to 'say'
        # the engine may not close properly and errors will start showing up
        sleep(noInter)

    def isbusy(self):
        if self.engine == None:
            return False
        else:
           return(self.engine.isBusy)

    def stop(self):
        self._running = False
        try:
            self.engine.endLoop()
            logger.debug('Voice loop stopped')
        except:
            pass
        try:
            self.t.join()
            logger.debug('Joined Voice thread')
        except Exception as e:
            logger.exception(e)


def tts(event=None):
    ranges = text_editor.tag_ranges(tk.SEL)
    if(ranges):
        tts_engine.say(text_editor.get(*ranges))

tts_state = tk.BooleanVar()
tts_state.set(True)

def change_tts(event=None):
    global tts_state
    if tts_state:
        tts_state = False
        tts_btn.configure(image=tts_off_icon)
        tts_btn.unbind('<Button-1>')
        text_editor.unbind_all("<Control-t>")
    else:
        tts_state = True
        tts_btn.configure(image=tts_on_icon)
        tts_btn.bind('<Button-1>',tts)  
        text_editor.bind_all("<Control-t>",tts)

tts_engine = VoiceBox()
tts_btn.bind('<Button-1>',tts)
Features.add_checkbutton(label="Text to Speech",image=tts_on_icon,compound=tk.LEFT,variable=tts_state,command=change_tts)


## Binding shortcuts
text_editor.bind_all("<Control-o>",open_file)
text_editor.bind_all("<Control-O>",open_file)
text_editor.bind_all("<Control-n>",new_file)
text_editor.bind_all("<Control-N>",new_file)
text_editor.bind_all("<Control-s>",save_file)
text_editor.bind_all("<Control-S>",save_file)
text_editor.bind_all("<Control-q>",save_as_file)
text_editor.bind_all("<Control-Q>",save_as_file)
text_editor.bind_all("<Control-F>",find_show_hide)
text_editor.bind_all("<Control-f>",find_show_hide)
text_editor.bind_all("<Control-t>",tts)

about_info = '''Name: Texto
Type: Simple text editor
Creator: Rashim Narayan Tiku
Technology: Tkinter (Python)'''

def open_about():
    messagebox.showinfo('TEXTO',about_info)
About.add_command(label='About Texto',command=open_about)



#----------------------------------------------END OF MAIN-MENU FUNCTIONALITY -------------------------------------








######################################### APPLICATION PACKING #####################################################

tool_bar.pack(side=tk.TOP,fill=tk.X)
status_bar.pack(side=tk.BOTTOM,fill=tk.X)
yscroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)



main_application.state('zoomed')
main_application.config(menu=main_menu)
main_application.mainloop()