import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import font, colorchooser, filedialog, messagebox
import os, shutil
from tkinter.font import Font
from time import sleep
import time
from idlelib import window

import pyttsx3
import enchant  
from SpellCheckMenu import SpellCheckMenu
from ToolTip import createToolTip
from Editor import Editor

main_application = themed_tk.ThemedTk()
main_application.geometry('900x600')
main_application.wm_iconbitmap('icon.ico')



# //////////////////////////////////////////////  MAIN-MENU  /////////////////////////////////////////////////////

main_menu = tk.Menu(tearoff=False)


#MENU options
File = tk.Menu(main_menu,tearoff=False)
Edit = tk.Menu(main_menu,tearoff=False)
View = tk.Menu(main_menu,tearoff=False)
Tools = tk.Menu(main_menu,tearoff=False)
Theme = tk.Menu(main_menu,tearoff=False)
About = tk.Menu(main_menu,tearoff=False)

#FILE ICONS 
new_icon = tk.PhotoImage(file=r'icons/new.png')
open_icon = tk.PhotoImage(file=r'icons/open.png')
save_icon = tk.PhotoImage(file=r'icons/save.png')
save_as_icon = tk.PhotoImage(file=r'icons/save_as.png')
exit_icon = tk.PhotoImage(file=r'icons/exit.png')

#EDIT ICONS
copy_icon = tk.PhotoImage(file=r'icons/copy.png')
cut_icon = tk.PhotoImage(file=r'icons/cut.png')
paste_icon = tk.PhotoImage(file=r'icons/paste.png')
clear_all_icon = tk.PhotoImage(file=r'icons/clear_all.png')
find_icon = tk.PhotoImage(file=r'icons/find_2.png')

#VIEW ICONS
tool_bar_icon = tk.PhotoImage(file=r'icons/tool_bar.png')
status_bar_icon = tk.PhotoImage(file=r'icons/status_bar.png')

#FEATURES ICONS
spell_check_on_icon = tk.PhotoImage(file='icons/book_non_trans.png')
spell_check_off_icon = tk.PhotoImage(file='icons/book_trans.png')
tts_on_icon = tk.PhotoImage(file='icons/tts_on.png')
tts_off_icon = tk.PhotoImage(file='icons/tts_off.png')

#THEME ICONS
xpnative = tk.PhotoImage(file=r'icons/light_default2.png')
clam = tk.PhotoImage(file=r'icons/light_plus2.png')
black = tk.PhotoImage(file=r'icons/dark.png')
radiance = tk.PhotoImage(file=r'icons/red2.png')
ubuntu = tk.PhotoImage(file=r'icons/monokai2.png')
itft1 = tk.PhotoImage(file=r'icons/night_blue2.png')

fullscreen_icon = tk.PhotoImage(file=r'icons/001-fullscreen.png')


theme_choice = tk.StringVar()
color_icons = {
    "Light Theme":xpnative,
    "Light Plus Theme":clam,
    "Dark Theme":black,
    "Red Theme":radiance,
    "Monokai Theme":ubuntu,
    "Night Blue Theme":itft1
}   

color_dict ={
    "Light Theme":('#000000','#ffffff','#000000','xpnative'),
    "Light Plus Theme":('#474747','#e0e0e0','#000000','clam'),
    "Dark Theme":('#c4c4c4','#2d2d2d','#ffffff','black'),
    "Red Theme":('#2d2d2d','#ffe8e8','#000000','radiance'),
    "Monokai Theme":('#d3b774','#474747','#000000','ubuntu'),
    "Night Blue Theme":('#ededed','#6b9dc2','#000000','itft1')
}

#cascading the menu
main_menu.add_cascade(label='File',menu=File)
main_menu.add_cascade(label='Edit',menu=Edit)
main_menu.add_cascade(label='View',menu=View)
main_menu.add_cascade(label="Tools",menu=Tools)


about_info = '''Name: Texto
Type: Simple text editor
Creator: Rashim Narayan Tiku
Technology: Tkinter (Python)'''

def open_about():
    messagebox.showinfo('TEXTO',about_info)
main_menu.add_command(label='About',command=open_about)



# ///////////////////////////////////// CONTEXTUAL MENU (Right click menu) ///////////////////////////////////////

def do_popup(event): 
    try: 
        main_menu.tk_popup(event.x_root, event.y_root) 
    finally: 
        main_menu.grab_release() 
main_application.bind("<Button-3>", do_popup) 
  




# /////////////////////////////////////////////// TOOLBAR /////////////////////////////////////////////// 

tool_bar = ttk.Label(main_application)


## COLOR THEME
def theme_change():
    ''' For changing themes '''
    theme = theme_choice.get()
    color_tuple = color_dict.get(theme)
    fg_color,bg_color,ins_color = color_tuple[0],color_tuple[1],color_tuple[2]
    text_area.config(fg=fg_color,background = bg_color,insertbackground=ins_color)
    number_line.config(background=bg_color)
    
    theme_btn.config(image=color_icons[theme])
    main_application.set_theme(color_tuple[3])

theme_btn = tk.Menubutton(tool_bar,image=color_icons['Light Theme'])
theme_btn_menu = tk.Menu(theme_btn,tearoff=False)
theme_btn.config(menu=theme_btn_menu)
for i in color_dict:
    theme_btn_menu.add_radiobutton(label=i,image=color_icons[i],variable=theme_choice,compound=tk.LEFT,command=theme_change)

theme_btn.grid(row=0,column=0)
createToolTip(theme_btn,text="Theme")

##font box
font_tuples = tk.font.families()
font_selected = tk.StringVar()
font_box = ttk.Combobox(tool_bar,width=30,textvariable=font_selected,state='readonly',cursor='hand2')
font_box['values'] = font_tuples
font_box.current(font_tuples.index('Arial'))
font_box.grid(row=0,column=1,padx=2)

##size box
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar, width=14,textvariable=size_var,state='readonly',cursor='hand2')
font_size['values'] = tuple(range(8,81,2))
font_size.current(2)
font_size.grid(row=0,column=4,padx=2)

## undo button/label
on_undo_icon = tk.PhotoImage(file=r'icons/on_undo.png')
off_undo_icon = tk.PhotoImage(file=r'icons/off_undo.png')
on_redo_icon = tk.PhotoImage(file=r'icons/on_redo.png')
off_redo_icon = tk.PhotoImage(file=r'icons/off_redo.png')

undo_btn = ttk.Label(tool_bar,image=off_undo_icon,cursor='hand2')
undo_btn.grid(row=0,column=5,padx=1)
createToolTip(undo_btn,"Undo")
redo_btn = ttk.Label(tool_bar,image=off_redo_icon,cursor='hand2')
redo_btn.grid(row=0,column=6,padx=1)
createToolTip(redo_btn,"Redo")

separator = ttk.Separator(tool_bar, orient=tk.VERTICAL).grid(row=0,column=7,padx=6,sticky="sn")

##font size changer buttons
text_size_up_icon = tk.PhotoImage(file='icons/resize-font-up.png')
text_size_down_icon = tk.PhotoImage(file='icons/resize-font-down.png')

text_size_up_btn = ttk.Label(tool_bar,image=text_size_up_icon,cursor='hand2')
text_size_up_btn.grid(row=0,column=9,padx=2)
createToolTip(text_size_up_btn,"Bigger Text")
text_size_down_btn = ttk.Label(tool_bar,image=text_size_down_icon,cursor='hand2')
text_size_down_btn.grid(row=0,column=10,padx=2)
createToolTip(text_size_down_btn,"Smaller Text")

## font color button
font_color_icon = tk.PhotoImage(file='icons/font_color.png')
font_color_btn = ttk.Label(tool_bar,image=font_color_icon,cursor='hand2')
font_color_btn.grid(row=0,column=11,padx=2)
createToolTip(font_color_btn,"Color Palette")

separator = ttk.Separator(tool_bar, orient=tk.VERTICAL).grid(row=0,column=12,padx=6,sticky="sn")

##bold button
off_bold_icon = tk.PhotoImage(file='icons/off_bold.png')
on_bold_icon = tk.PhotoImage(file='icons/on_bold.png')
bold_btn = ttk.Label(tool_bar,image=off_bold_icon,cursor='hand2')
bold_btn.grid(row=0,column=13,padx=2)
createToolTip(bold_btn,"Bold")

##italic button
off_italic_icon = tk.PhotoImage(file='icons/off_italic.png')
on_italic_icon = tk.PhotoImage(file='icons/on_italic.png')
italic_btn = ttk.Label(tool_bar,image=off_italic_icon,cursor='hand2')
italic_btn.grid(row=0,column=14,padx=2)
createToolTip(italic_btn,"Italics")

##underline button
off_underline_icon = tk.PhotoImage(file='icons/off_underline.png')
on_underline_icon = tk.PhotoImage(file='icons/on_underline.png')
underline_btn = ttk.Label(tool_bar,image=off_underline_icon,cursor='hand2')
underline_btn.grid(row=0,column=15,padx=2)
createToolTip(underline_btn,"Underline")

separator = ttk.Separator(tool_bar, orient=tk.VERTICAL).grid(row=0,column=16,padx=6,sticky="sn")

##align left
on_align_left_icon = tk.PhotoImage(file='icons/align-left-2x.png')
align_left_btn = ttk.Label(tool_bar,image = on_align_left_icon,cursor='hand2')
align_left_btn.grid(row=0,column=17,padx=2)
createToolTip(align_left_btn,"Align Left")

##align center
on_align_center_icon = tk.PhotoImage(file='icons/align-center-2x.png')
align_center_btn = ttk.Label(tool_bar,image=on_align_center_icon,cursor='hand2')
align_center_btn.grid(row=0,column=18,padx=5)
createToolTip(align_center_btn,"Align Center")

##align right
on_align_right_icon = tk.PhotoImage(file='icons/align-right-2x.png')
align_right_btn = ttk.Label(tool_bar,image = on_align_right_icon,cursor='hand2')
align_right_btn.grid(row=0,column=19,padx=2)
createToolTip(align_right_btn,"Align Right")

separator = ttk.Separator(tool_bar, orient=tk.VERTICAL).grid(row=0,column=20,padx=6,sticky="sn")

## text to speech
tts_btn = ttk.Label(tool_bar,image=tts_on_icon,cursor='hand2')
tts_btn.grid(row=0,column=21, padx=2)
createToolTip(tts_btn,"Text To Speech")


## Spell check icon
dictionary = enchant.Dict("en_US")
spell_check_btn = ttk.Label(tool_bar,image=spell_check_on_icon,cursor='hand2')
spell_check_btn.grid(row=0,column=22,padx=2)
createToolTip(spell_check_btn,"Spell checker")

separator = ttk.Separator(tool_bar, orient=tk.VERTICAL).grid(row=0,column=23,padx=6,sticky="sn")

## find button
find_btn = ttk.Label(tool_bar,image=find_icon,cursor='hand2')
find_btn.grid(row=0, column=24, padx=2)
createToolTip(find_btn, "Find and Replace")


## find and replace labels and entry fields
find_state = 0
find_label = ttk.Label(tool_bar,text='Find',font=('InkFree',9))
find_label.grid(row=0,column=25)
find_var = tk.StringVar()
find_entry = ttk.Entry(tool_bar,textvariable=find_var,width=20)
find_entry.grid(row=0,column=26)

replace_label=ttk.Label(tool_bar,text='Replace',font=('InkFree',9))
replace_label.grid(row=0,column=27)
replace_var = tk.StringVar()
replace_entry = ttk.Entry(tool_bar,textvariable=replace_var,width=20)
replace_entry.grid(row=0,column=28)

submit_icon = tk.PhotoImage(file='icons/enter.png')
submit_btn = ttk.Label(tool_bar,image = submit_icon)
submit_btn.grid(row=0,column=29)

find_label.grid_remove()
find_entry.grid_remove()
replace_label.grid_remove()
replace_entry.grid_remove()
submit_btn.grid_remove()



# /////////////////////////////////////////////////////  TEXT-EDITOR /////////////////////////////////////////////////////

text_editor = Editor(main_application)
text_area = text_editor.text
number_line = text_editor.numberLine

## Number Line Hide Show
numLineVisible = True


def hide_show_number_line():
    if numLineVisible == True:
        self.numberLine.pack_forget()
    else:
        self.numberLine.pack(side=tk.LEFT,fill=tk.Y)




##undo_redo functionality
def undo_func(event=None):
    undo_btn.config(image=on_undo_icon)
    text_area.event_generate('<<Undo>>')
def redo_func(event=None):
    redo_btn.config(image=on_redo_icon)
    text_area.event_generate('<<Redo>>')
def change_undo(event=None):
    undo_btn.config(image=off_undo_icon)
def change_redo(event=None):
    redo_btn.config(image=off_redo_icon)

undo_btn.bind('<Button-1>', undo_func)
undo_btn.bind('<ButtonRelease-1>', change_undo)
redo_btn.bind('<Button-1>', redo_func)
redo_btn.bind('<ButtonRelease-1>', change_redo)


## font family and font size functionality
my_font = Font(family='Arial',size=12)      
text_area.configure(font=my_font)

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
    text_property = tk.font.Font(font=text_area['font'])
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
    # text_property = tk.font.Font(font=text_area['font'])
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
    # text_property = tk.font.Font(font=text_area['font'])
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
    text_area.configure(fg=color_var[1])
font_color_btn.bind('<Button-1>',change_font_color)


## align right functionality
def align_right(event=None):
    text_content = text_area.get(1.0,'end')
    text_area.tag_config('right',justify=tk.RIGHT)
    text_area.delete(1.0,tk.END)
    text_area.insert(tk.INSERT,text_content,'right')
align_right_btn.bind('<Button-1>',align_right)

## align left functionality
def align_left(event=None):
    text_content = text_area.get(1.0,'end')
    text_area.tag_config('left',justify=tk.LEFT)
    text_area.delete(1.0,tk.END)
    text_area.insert(tk.INSERT,text_content,'left')
align_left_btn.bind('<Button-1>',align_left)

## align center functionality
def align_center(event=None):
    text_content = text_area.get(1.0,'end')
    text_area.tag_config('center',justify=tk.CENTER)
    text_area.delete(1.0,tk.END)
    text_area.insert(tk.INSERT,text_content,'center')
align_center_btn.bind('<Button-1>',align_center)


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
                text_area.tag_remove('match',start_pos,end_pos)
        
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
    text_area.tag_remove('match','1.0',tk.END)
    matches=0
    if find_word:
        start_pos = '1.0'
        while True:
            start_pos = text_area.search(find_word,start_pos,stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f'{start_pos}+{len(find_word)}c'
            if replace_word:
                text_area.delete(start_pos,end_pos)
                text_area.insert(start_pos,replace_word)
            else:
                text_area.tag_add('match',start_pos,end_pos)
                found_list.append(start_pos)

            start_pos = end_pos
            matches += 1
            text_area.tag_config('match',foreground='red',background='yellow')
submit_btn.bind('<Button-1>',find_and_replace)
find_entry.bind('<Return>',find_and_replace)
replace_entry.bind('<Return>',find_and_replace)



def spell_check(event=None):
    '''spell_check the word preceeding the insertion point'''
    
    index = text_area.search(r'\s', "insert",stopindex="1.0",backwards=True, regexp=True)

    if not index:
        index = "1.0"
    else:
        index = text_area.index(f"{index}+1c")

    #removing special_char from word
    special_char = ('.','?',',',';',':','\'','"','[',']','{','}','>','<','/','\\','+','=','-','_','!','@','#','$','%','^')
    raw_word = text_area.get(index, "insert")
    word = ''.join(i for i in raw_word if i not in special_char).lower()

    if raw_word=='':
        return
    text_area.tag_configure("misspelled",foreground='red')

    correct = dictionary.check(word)
    candidate_words = dictionary.suggest(word)

    ## DISPLAYING spell_check 
    if correct:
        text_area.tag_remove("misspelled", index, f"{index}+{len(word)}c")
    elif not correct and len(candidate_words)==0:
        text_area.tag_add("misspelled", index, f"{index}+{len(word)}c")
    else:
        spell_check_menu = SpellCheckMenu(text_area,index,len(word),candidate_words,tearoff=False)
        spell_check_menu.popup(event)
        text_area.tag_add("misspelled", index, f"{index}+{len(word)}c")

text_area.bind("<space>",spell_check)






# ///////////////////////////////////////////////  STATUS BAR ///////////////////////////////////////////////

status_bar = ttk.Label(main_application)
status_bar.grid_columnconfigure(3, weight=1)


def changed(event=None):
    global is_saved
    if text_area.edit_modified():
        is_saved = False
        saved_state()
    text_area.edit_modified(False)

    words_count = len(text_area.get(1.0,'end-1c').split())
    countLabel.configure(text=f'{words_count} words')
    if words_count > 1000:
        countLabel.configure(width=35)

    index = text_area.index(tk.INSERT)
    dot_pos = index.find('.')
    line_no = index[:dot_pos]
    column_no = index[dot_pos+1:]
    lineNumberLabel.configure(text=f"Ln: {line_no}  Col: {column_no}")
    if int(line_no)>10000 or int(column_no)>10000: lineNumberLabel.configure(width=20)
    elif int(line_no)>1000 or int(column_no)>1000: lineNumberLabel.configure(width=14)
    else: lineNumberLabel.configure(width=10)

text_area.bind('<<Modified>>',changed)


##Line and Column counter
lineNumberLabel = ttk.Label(status_bar,width=10, text=f"Ln: {1}  Col: {0}")
lineNumberLabel.config(font=("Calibri",8))
lineNumberLabel.grid(row=0,column=0,padx=4)

separator = ttk.Separator(status_bar, orient=tk.VERTICAL).grid(row=0,column=1,padx=6,sticky="sn")

##word and character counter
countLabel = ttk.Label(status_bar, width=30, text=f"0 words")
countLabel.config(font=("Calibri",8))
countLabel.grid(row=0,column=2)



## FullScreen 
full_screen_state = False

def toggle_full_screen(event):
    global full_screen_state
    full_screen_state = not full_screen_state
    main_application.attributes("-fullscreen", full_screen_state)

def quit_full_screen(event):
    global full_screen_state
    full_screen_state = False
    main_application.attributes("-fullscreen", full_screen_state)

main_application.attributes('-fullscreen', False)  
main_application.bind("<F11>", toggle_full_screen)
main_application.bind("<Escape>", quit_full_screen)

fullscreen_btn = ttk.Label(status_bar,image=fullscreen_icon,cursor='hand2')
fullscreen_btn.bind('<ButtonRelease-1>',toggle_full_screen)

fullscreen_btn.grid(row=0,column=30,sticky='e')
createToolTip(fullscreen_btn,text="Full Screen")




# ///////////////////////////////////////////////  MAIN-MENU FUNCTIONALITY ///////////////////////////////////////////////

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
    if is_saved or not choice:
        return
    url = 'Untitled.txt'
    text_area.delete(1.0,tk.END)
File.add_command(label='New',compound=tk.LEFT,accelerator='CTRL+N', command=new_file)


## open functionality
def open_file(event=None):
    global url
    global is_saved
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text Files','*.txt'),('All Files','*.*')))
    try:
        with open(url,'r') as rf:
            text_area.delete(1.0,tk.END)
            text_area.insert(1.0,rf.read())
    except FileNotFoundError:
        return 
    except:
        return 
    is_saved = True
    saved_state()
File.add_command(label='Open',compound=tk.LEFT,accelerator='CTRL+O',command=open_file)


## Save functionality
def save_file(event=None):
    global url
    global is_saved
    try:
        if url == 'Untitled.txt':
            save_as_file()
        else:
            contents = str(text_area.get(1.0,tk.END))
            with open(url,'r+',encoding='utf-8') as wf:
                wf.write(contents)
                is_saved = True
                saved_state()
    except:
        messagebox.showerror('Saving Error','An error occured while saving the file. The file has not been saved')
        return

File.add_command(label='Save',compound=tk.LEFT,accelerator='CTRL+S',command=save_file)


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
            text2save = str(text_area.get(1.0,tk.END))
            file2save.write(text2save)
            file2save.close()
            url = file_name
            is_saved = True
            saved_state()
            file2save.close()
        except:
            messagebox.showerror('Saving Error','Error while saving file. File is not saved.')
File.add_command(label='Save as',compound=tk.LEFT,accelerator='CTRL+Q',command=save_as_file)

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
File.add_command(label = 'Exit',compound=tk.LEFT,accelerator='CTRL+E',command=on_closing)


#adding images to EDIT menu
Edit.add_command(label='Copy',image=copy_icon,compound=tk.LEFT,command=lambda:text_area.event_generate('<Control-c>'))

Edit.add_command(label='Cut',image=cut_icon,compound=tk.LEFT,command=lambda:text_area.event_generate('<Control-x>'))

Edit.add_command(label='Paste',image=paste_icon,compound=tk.LEFT,command=lambda:text_area.event_generate('<Control-v>'))

Edit.add_command(label='Clear All',image=clear_all_icon,compound=tk.LEFT,command=lambda:text_area.delete(1.0, tk.END))


# VIEW MENU FUNCTIONALITY
tool_bar_state = tk.BooleanVar()
tool_bar_state.set(True)
status_bar_state = tk.BooleanVar()
status_bar_state.set(True)
line_bar_state = tk.BooleanVar()
line_bar_state.set(True)

def show_hide_toolbar():
    global tool_bar_state,status_bar_state
    if tool_bar_state:
        tool_bar.pack_forget()
        tool_bar_state=False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP,fill=tk.X)
        text_editor.pack(fill=tk.BOTH,expand=1)

        if status_bar_state:
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

def show_hide_linebar():
    global line_bar_state
    if line_bar_state:
        text_editor.numberLine.pack_forget()
        line_bar_state=False
    else:
        text_editor.scrollbar.pack_forget()
        text_editor.text.pack_forget()
        text_editor.numberLine.pack(side=tk.LEFT, fill=tk.Y)
        text_editor.text.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)
        text_editor.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        line_bar_state=True
View.add_checkbutton(label='Tool Bar',compound=tk.LEFT,variable=tool_bar_state, onvalue=True, offvalue=False, command=show_hide_toolbar)
View.add_checkbutton(label='Status Bar',compound=tk.LEFT, variable=status_bar_state, onvalue=True, offvalue=False,command=show_hide_statusbar)
View.add_checkbutton(label='Line Number Bar',compound=tk.LEFT, variable=line_bar_state, onvalue=True, offvalue=False,command=show_hide_linebar)


##spell_check button
spell_check_state = tk.BooleanVar()
spell_check_state.set(True)

def change_spell_check(event=None):
    global spell_check_state
    if spell_check_state:
        spell_check_state = False
        spell_check_btn.configure(image=spell_check_off_icon)
        text_area.unbind("<space>")
    else:        
        spell_check_state = True
        spell_check_btn.configure(image=spell_check_on_icon)
        text_area.bind("<space>",spell_check)
Tools.add_checkbutton(label='Spell Checker',image=spell_check_on_icon,compound=tk.LEFT,variable=spell_check_state,command=change_spell_check)


## Text to Speech

def tts(event=None):
    ranges = text_area.tag_ranges(tk.SEL)
    if(ranges):
        tts_engine.say(text_area.get(*ranges))
        tts_engine.runAndWait()

tts_state = tk.BooleanVar()
tts_state.set(True)

def change_tts(event=None):
    global tts_state
    if tts_state:
        tts_state = False
        tts_btn.configure(image=tts_off_icon)
        tts_btn.unbind('<<Invoke>>')
        text_area.unbind_all("<Control-t>")
    else:
        tts_state = True
        tts_btn.configure(image=tts_on_icon)
        tts_btn.bind('<Button-1>',tts)  
        text_area.bind_all("<Control-t>",tts)

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate',120)

tts_btn.bind('<Button-1>',tts)
Tools.add_checkbutton(label="Text to Speech",image=tts_on_icon,compound=tk.LEFT,variable=tts_state,command=change_tts)


## Binding shortcuts
text_area.bind_all("<Control-o>",open_file)
text_area.bind_all("<Control-O>",open_file)
text_area.bind_all("<Control-n>",new_file)
text_area.bind_all("<Control-N>",new_file)
text_area.bind_all("<Control-s>",save_file)
text_area.bind_all("<Control-S>",save_file)
text_area.bind_all("<Control-q>",save_as_file)
text_area.bind_all("<Control-Q>",save_as_file)
text_area.bind_all("<Control-F>",find_show_hide)
text_area.bind_all("<Control-f>",find_show_hide)
text_area.bind_all("<Control-t>",tts)





# ///////////////////////////////////////////////  APPLICATION  /////////////////////////////////////////////// 
 
tool_bar.pack(side=tk.TOP,fill=tk.X)
status_bar.pack(side=tk.BOTTOM,fill=tk.X)
text_editor.pack(fill=tk.BOTH,expand=1)
text_area.focus_set()

# for paste command glitch in line_number_bar
main_application.after(200, text_editor.redraw())

main_application.state('zoomed')
main_application.config(menu=main_menu)

main_application.mainloop()