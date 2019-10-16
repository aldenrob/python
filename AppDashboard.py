# Data Storage Imports
import csv
import pandas as pd
import SQL_Functions as SQLF
import MISC_Functions as MISC

# GUI imports
from tkinter import *
from tkinter import messagebox
from tkinter import Tk, Checkbutton, DISABLED

# Web automation imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

# MISC 
import time

# Time Tracking import
import timeit

# Scrape WINGS SMR
def SMR_DB(D):
    toc = time.time()    
    D.get("https://tinyurl.com/SMRDB")# Load WINGS SMR URL
    time.sleep(2)    
    try:      
       alert = D.switch_to_alert()
       alert.accept()
    except Exception as ex:
       print(ex)        
    time.sleep(3)
    D.switch_to.frame(0)    
    MISC.Find_ID('#ICOK',"C","","Search for SMR",D) # Pulls up SMR Data        
    # Create SMR DB
    SQLF.CreateDB('SMR.db',2)
    try:
        WebDriverWait(D, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="win0divQUERYRESULT"]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/a/span'))).click()
    except Exception as ex:
       print(ex)
    time.sleep(3) 
    ID = []
    i = 2
    while(i < 999):
        for j in range(2,62):
            try:
                ID.append(WebDriverWait(D, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="win0divQUERYRESULT"]/table/tbody/tr[2]/td/table/tbody/tr[{str(i)}]/td[{str(j)}]'))).text)            
                #print(f"Column {str(j)}: {ID[j-2]}")                 
            except Exception as ex:
                print("Database Closed")                                 
                break
        try:
            #print(f".....Preparing to INSERT C/{ID[3]}")
            SQLF.PopulateSMR_DB(ID[0], ID[1], ID[2], ID[3], ID[4], ID[5], ID[6], ID[7], ID[8], ID[9], ID[10], ID[11], ID[12], ID[13], ID[14], ID[15], ID[16], ID[17], ID[18], ID[19], ID[20], ID[21], ID[22], ID[23], ID[24], ID[25], ID[26], ID[27], ID[28], ID[29], ID[30], ID[31], ID[32], ID[33], ID[34], ID[35], ID[36], ID[37], ID[38], ID[39], ID[40], ID[41], ID[42], ID[43], ID[44], ID[45], ID[46], ID[47], ID[48], ID[49], ID[50], ID[51], ID[52], ID[53], ID[54], ID[55], ID[56], ID[57], ID[58], ID[59])
            ID[:]=[]
        except Exception:
            #print(f"{i} Cadets gathered. SMR DB population Complete")
            i += 999
        i += 1
        # End of for loop
   # End while loop    
    tic = time.time()
    D.quit()    
    print(f"The SMR DB took {(tic-toc)/60} minutes to complete")    
#End of SMR DB Function

# Creates SQL DB to sort and manipulate data            
def CadetPayDB(EmpID,D):
    toc = time.time()
    html = ["DATE$","VOU_STOP_DATE$","VOU_AMNT$","APC$"]   
    Data = []    
    i = 0 
    while(i < 999):
        for j in range(0,4):
            try:
                #time.sleep(.25)#TESTESTESTEST                
                Scraper = WebDriverWait(D, .5).until(EC.presence_of_element_located((By.ID, f'W_DFAS_VOUCH_IN_W_{html[j]}{str(i)}')))#Scrapes data
                Data.append(Scraper.text)#Stores Data
                print(Scraper.text) #Visual Aid
                if j == 3:
                    RowIndex = WebDriverWait(D, .5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="trW_DFAS_VOUCH_IN$0_row{i+1}"]/td[1]')))#Scrapes row data
                    Data.append(RowIndex.text)#Stores Data
                    print(RowIndex.text) #Visual Aid
            except Exception:
                break
        try:
            SQLF.PopulatePayDB(EmpID,Data[0],Data[1],Data[2],Data[3],Data[4])
            Data[:]=[]#Resets list
        except Exception:
            break    
        i += 1
    tic = time.time()    
    D.quit()
    print(f"The SMR DB took {(tic-toc)/60} minutes to complete")       
# End of CadetPayDB()

def Financial(D):
    # Create Cadet Pay Database 
    SQLF.CreateDB('CadetPay.db',1)
    # Insert All Contracted Cadet Pay data into CadetPay DB
    for i in range (0,len(SQLF.CadetPayIDs())):
        D.get("https://tinyurl.com/CadetPay")
        time.sleep(.5)
        try:
            alert = D.switch_to_alert()
            alert.accept()
        except Exception:
            print("No Alert Button Present")
        print(f"Scraping WINGS for EmpID: {SQLF.CadetPayIDs()[i]}")                
        MISC.Find_ID("W_PSN_SCRTY_VW_EMPLID","K",SQLF.CadetPayIDs()[i],'EmpID',D)# Enter EmpID        
        MISC.Find_Xpath('//*[@id="#ICSearch"]',"C","","Search Button","#ICSearch",D)# Search        
        MISC.Find_Xpath('//*[@id="W_DFAS_VOUCH_IN$hviewall$0"]',"C","","View All Link","W_DFAS_VOUCH_IN$hviewall$0",D)# View All
        MISC.Find_Xpath('//*[@id="W_DFAS_VOUCH_IN$srt0$0"]',"C","","Sort by Date","W_DFAS_VOUCH_IN$srt0$0",D)# Sort Index Decending
        time.sleep(.5)
        # Insert Cadet Financial Data to DB
        CadetPayDB(SQLF.CadetPayIDs()[i],D)                  
    # END FOR LOOP ADDING CADET TO DB
    print("Cadet Pay Database Complete")      

def AppDashboard():
    # Ensures Username and Password are entered prior to proceeding     
    if Username.get() and Password.get():                   
        # Ensures only One browser is selected
        if ChromeMode.get() == ExplorerMode.get():
            messagebox.showerror('Browser error', 'Browser mode selection is MANDATORY, Please ensure only ONE browser mode is selected.')
        # Proceeds when browser selection condition is met
        if ChromeMode.get() != ExplorerMode.get():
            # Determines Which Browser was chosen
            if ChromeMode.get() > ExplorerMode.get():
                # Checks to see if Headless Mode was selected
                if StealthMode.get() > 0 and ChromeMode.get() > 0:                    
                    options = Options()
                    options.set_headless(headless=True)
                    driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver.exe')
                # If Headless Mode is not selected Open Chrome
                if StealthMode.get() < 1:                   
                    driver = webdriver.Chrome()
                    driver.maximize_window()
            # Open Internet Explorer    
            if ExplorerMode.get() > ChromeMode.get():
                driver = webdriver.Ie()
                driver.maximize_window()                    
            # WINGS Sign In Page
            driver.get("https://wings.holmcenter.com/psc/hcp/LANDING/PORT_HCP/s/WEBLIB_PTSIGNIN.ISCRIPT1.FieldFormula.IScript_SignIn")                   
            # User login
            MISC.Find_Xpath('//*[@id="userid"]',"K",Username.get(), "UserName","userid",driver)
            MISC.Find_Xpath('//*[@id="pwd"]',"K",Password.get(), "Password","pwd",driver)
            MISC.Find_Xpath('//*[@id="login"]/div[2]/div[6]/span/a',"C","", "Submit button for Username and Password","login",driver)
            # Check for Program Selection
            Prgm = v.get()
            # Run the Selected Program            
            if Prgm == 1:        
                SMR_DB(driver)
            if Prgm == 4:
                Financial(driver)            
    else:
        messagebox.showerror('Username and Password Error', 'Username and Password is MANDATORY, Please enter both and try again.')            

# Create GUI for App Dashboard
win = Tk()
win.title("Detachment 560 Application Dashboard")

#BackGround Image
img = PhotoImage(file="DET560BG.gif")
img = img.subsample(2, 2)
background = Label(win, image=img, bd=0)
background.place(relx=.5, rely=.5, anchor="center")
background.lower()
background.image = img

# Centers App on Screen
screen_w = win.winfo_screenwidth()
screen_h = win.winfo_screenheight()
x_cord = (screen_w/2) - 200
y_cord = (screen_h/2) - 100
win.geometry("%dx%d+%d+%d" % (550, 300, x_cord, y_cord))

# Username and Password Textboxes
Username = StringVar()
Label(win, text="Username:").grid(column=0, row=0)
UsernameTextbox = Entry(win, width=20, textvariable=Username,)
UsernameTextbox.grid(column=1, row=0)

Password = StringVar()
Label(win, text="Password:").grid(column=0, row=1)
PasswordTextbox = Entry(win, width=20, textvariable=Password,)
PasswordTextbox.config(show="*")
PasswordTextbox.grid(column=1, row=1)

# Buttons
Log_In = Button(win, width=15, text="Execute Application", command=AppDashboard).grid(column=2, row=0)
Button(win, width=15, text="Exit Program", command=win.quit).grid(column=2, row=1)

# Checkbox
StealthMode = IntVar()
ChromeMode = IntVar()
ExplorerMode = IntVar()

Checkbutton(win,text="S-Mode        ",variable=StealthMode).grid(column=3,row=0, sticky=W)
Checkbutton(win,text="IE-Browser    ",variable=ExplorerMode).grid(column=3,row=1, sticky=W)
Checkbutton(win,text="Chrome-Browser",variable=ChromeMode).grid(column=3,row=2, sticky=W)

# RadioButtons
v = IntVar()
Radiobutton(win, variable=v, value=1, state='normal', text="Create SMR DB         ").grid(column=0, row=2) #Space added for manual alignment of buttons
Radiobutton(win, variable=v, value=2, state='disabled', text="Audit Cadet Pay       ").grid(column=1, row=3) #Space added for manual alignment of buttons
Radiobutton(win, variable=v, value=3, state='disabled', text="Upload PFA's             ").grid(column=1, row=2) #Space added for manual alignment of buttons
Radiobutton(win, variable=v, value=4, state='normal', text="Create CadetPay DB").grid(column=0, row=3)
Radiobutton(win, variable=v, value=5, state='disabled', text="Collect DoDMETS Data      ").grid(column=2, row=2)
Radiobutton(win, variable=v, value=6, state='disabled', text="Populate DoDMETS      ").grid(column=2, row=3)

if __name__ == "__main__":    
    # Keeps GUI open
    win.mainloop()