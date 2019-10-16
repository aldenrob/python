from tkinter import *

class FormApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Detachment 560 Application Dashboard')
        self.geometry('600x500')
        container = Frame(self)
        self.frames = {
            'Dash': DashBoard(self),
            'AuditPay': CadetPaySURF(self)
        }

        self.App_Dash_Frame()
        container.config(bg='#f1f1f1')
        container.pack(fill=BOTH, expand=True, padx=20, pady=20)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.config(borderwidth=2, relief="groove", bg='#f1f1f1')
        frame.place(width=500, height=400, relx=0.5, rely=0.5, anchor=CENTER)
        frame.tkraise()

    def Audit_Pay_Frame(self):
        self.show_frame('AuditPay')

    def App_Dash_Frame(self):
        self.show_frame('Dash')                   

class DashBoard(Frame):
    def __init__(self, form):
        Frame.__init__(self, form)

        frame = Frame(self, bg='#f1f1f1')
        self.tstlbl=Label(frame, text='App Dash', font=('Arial Bold', 20), pady=20, bg='#f1f1f1')\
            .grid(row=0, column=0, columnspan=2)

        Label(frame, text='Username', bg='#f1f1f1').grid(row=1, column=0)
        Entry(frame).grid(row=1, column=1)

        Label(frame, text='Password', bg='#f1f1f1').grid(row=2, column=0)
        Entry(frame).grid(row=2, column=1)

        #DropDown Menu
        Label(frame, text='Select App:', bg='#f1f1f1')\
            .grid(row=4, column=2)
        choices = {'Initiate SMR DB', 'Initiate Cadet Pay DB','Audit Cadet Pay','Initiate Cadet DoDMETS'}
        tk_var = StringVar(frame)
        tk_var.set('Initiate SMR Database')
        OptionMenu(frame, tk_var, *choices) \
            .grid(row=4, column=3, sticky=W)
        
        #Checkboxes
        self.Stealth_var = IntVar()
        self.Stealth_bx = Checkbutton(frame, text='Background Mode', state=DISABLED, variable=self.Stealth_var, bg='#f1f1f1',)
        self.Stealth_bx.grid(row=1, column=3, columnspan=2, sticky=W)
        
        self.Chrome_var = IntVar()
        Checkbutton(frame, text='Chrome Browser',
                    variable=self.Chrome_var, bg='#f1f1f1',
                    command=self.check_status)\
            .grid(row=2, column=3, columnspan=2, sticky=W)
        
        self.IE_var = IntVar()
        Checkbutton(frame, text='Internet Explorer Browser',
                    variable=self.IE_var, bg='#f1f1f1',
                    command=self.check_status)\
            .grid(row=3, column=3, columnspan=2, sticky=W)

        #RadioButtons
        self.login_btn = Button(frame, width=15, text='Enter App Credentials', state=DISABLED, command=form.Audit_Pay_Frame)
        self.login_btn.grid(row=1, column=2, sticky=W)

        self.exit_btn = Button(frame, width=15,text=' Exit Program ', command=self.quit)
        self.exit_btn.grid(row=2, column=2, sticky=W)
        
        # Button(frame, text='New User ! Sign me up',
        #        command=form.Audit_Pay_Frame)\
        #     .grid(row=4, column=1, sticky=W)

        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def check_status(self):
        #Enables or Disables Headless Mode (Chrome Only Feature)        
        if self.Chrome_var.get() > self.IE_var.get():
            self.Stealth_bx.config(state=NORMAL)            
        else:
            self.Stealth_bx.config(state=DISABLED)
            self.Stealth_var.set(0)
        #Enables or Disables Application Login (Browser Selection Required)
        if self.Chrome_var.get() != self.IE_var.get():
            self.login_btn.config(state=NORMAL)
        elif self.Chrome_var.get() == self.IE_var.get():
            self.login_btn.config(state=DISABLED)    


class CadetPaySURF(Frame):
    def __init__(self, form):
        Frame.__init__(self, form)

        frame = Frame(self, bg='#f1f1f1')
        
        Label(frame, text='Cadet Pay Query', font=('Arial Bold', 20), pady=20, bg='#f1f1f1')\
            .grid(row=0, column=0, columnspan=2)        

        self.EmplID = StringVar()
        Label(frame, text='Employee ID', bg='#f1f1f1').grid(row=1, column=0)
        Entry(frame, textvariable=self.EmplID,).grid(row=1, column=1)

        Label(frame, text='Last Name', bg='#f1f1f1').grid(row=2, column=0)
        Entry(frame).grid(row=2, column=1)        

        Button(frame, text='Sign Up !') \
            .grid(row=4, column=1, sticky=W)

        Button(frame, text='Back to Main Screen',
               command=form.App_Dash_Frame) \
            .grid(row=4, column=0, sticky=W)

        frame.place(relx=0.5, rely=0.5, anchor=CENTER)


if __name__ == "__main__":
    app = FormApp()
    app.mainloop()
