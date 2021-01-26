import tkinter as tk


# This is a scrollable text editor

'''THIS CODE IS CREDIT OF Willmish and Bryan Oakley'''

class Editor(tk.Frame):
    """ 
    It is basically a Text widget along with a sidebar showing line number and a scrollbar.
    This is a Frame widget having Text widget, TextLineNumber(Canvas widget) and Scrollbar widget and other supporting functions.
    """
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.text = CustomText(self, wrap="word", bg='#ffffff', foreground="#000000", relief='flat',
                            insertbackground='black',
                            selectbackground="blue", width=10, height=25,undo=True)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLine = TextLineNumbers(self, width=20, bg='#eeede7')
        self.numberLine.attach(self.text)

        # this is where we tell the custom widget what to call
        self.text.set_callback(self.callback)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLine.pack(side=tk.LEFT, fill=tk.Y)
        self.text.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.on_press_delay)
        self.text.bind("<Button-1>", self.numberLine.redraw)
        self.scrollbar.bind("<Button-1>", self.on_scroll_press)
        self.text.bind("<MouseWheel>", self.on_press_delay)

    def callback(self, result, *args):
        ''' Generate `Modified` event of Editor '''

        child_list = self.master.winfo_children()
        child_list[2].text.event_generate("<<Modified>>")
        

    def on_scroll_press(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLine.redraw)

    def on_scroll_release(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLine.redraw)

    def on_press_delay(self, *args):
        self.after(2, self.numberLine.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLine.redraw()

'''END OF Willmish's CODE'''


'''THIS CODE IS CREDIT OF Bryan Oakley (With minor visual modifications from Willmish): 
https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget'''


class CustomText(tk.Text):
    '''
    It is Text object with added callback when cursor moves to another position without modifying anything (which is not natively present in tk/tcl)
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # Danger Will Robinson!
        # Heavy voodoo here. All widget changes happen via
        # an internal Tcl command with the same name as the 
        # widget:  all inserts, deletes, cursor changes, etc
        #
        # The beauty of Tcl is that we can replace that command
        # with our own command. The following code does just
        # that: replace the code with a proxy that calls the
        # original command and then calls a callback. We
        # can then do whatever we want in the callback. 
        private_callback = self.register(self._callback)
        self.tk.eval('''
            proc widget_proxy {actual_widget callback args} {

                # this prevents recursion if the widget is called
                # during the callback
                set flag ::dont_recurse(actual_widget)

                # call the real tk widget with the real args
                set result [uplevel [linsert $args 0 $actual_widget]]

                # call the callback and ignore errors, but only
                # do so on inserts, deletes, and changes in the 
                # mark. Otherwise we'll call the callback way too 
                # often.
                if {! [info exists $flag]} {
                    if {([lindex $args 0] in {insert replace delete}) ||
                        ([lrange $args 0 2] == {mark set insert})} {
                        # the flag makes sure that whatever happens in the
                        # callback doesn't cause the callbacks to be called again.
                        set $flag 1
                        catch {$callback $result {*}$args } callback_result
                        unset -nocomplain $flag
                    }
                }

                # return the result from the real widget command
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy _{widget} {callback}
        '''.format(widget=str(self), callback=private_callback))

    def _callback(self, result, *args):
        self.callback(result, *args)

    def set_callback(self, callable):
        self.callback = callable


class TextLineNumbers(tk.Canvas):
    """
    This is a Canvas widget to show Line numbers at along with Text widget
    """
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#606366",font=("Calibri",10))
            i = self.textwidget.index("%s+1line" % i)   

# END OF Bryan Oakley's CODE
            
            num_i = float(i)
            if num_i>100000.0:
                self.config(width=50)
            elif num_i>10000.0:
                self.config(width=40)
            elif num_i>1000.0:
                self.config(width=35)
            elif num_i>100.0:
                self.config(width=30)
            elif num_i>10.0:
                self.config(width=25)
            else:
                self.config(width=20)


