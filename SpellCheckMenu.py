import tkinter as tk

class SpellCheckMenu(tk.Menu):
    def __init__(self,master,index,length,candidate_words,*args, **kwargs):
        tk.Menu.__init__(self, *args, **kwargs)
        self.length = length
        self.index = index
        self.master = master
        self.candidate_words = candidate_words[:6]
        self.spell_choice = tk.StringVar()
        for i in self.candidate_words:
            self.add_radiobutton(label=i,variable=self.spell_choice,compound=tk.LEFT,command=lambda: self.spell_change(self.index,self.length))
        self.add_separator()
        self.add_command(label='Up/Down to select',command=lambda: print("pass"))  
        self.add_command(label='Press Enter to Exit',command=lambda: print("pass"))  
        
        self.bind("<Button-3>", self.popup) 


    def spell_change(self,index,length):
        new_word = self.spell_choice.get()
        end_index = f"{index}+{length}c"
        self.master.delete(index,end_index)
        self.master.insert(index,f'{new_word}')


    def popup(self, event):
        try:
            self.tk_popup(748,75, 0)
        finally:
            self.grab_release()