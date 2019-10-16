import csv
import pandas as pd

# Web automation imports
from selenium import webdriver
from selenium.webD.common.by import By

from selenium.webD.support.ui import WebDriverWait
from selenium.webD.common.keys import Keys
from selenium.webD.support import expected_conditions as EC
from selenium.webD.support.select import Select

import time

def DoDMETS_Data_Grab(D):
    #Check SSSS for required Cadets to be Updated
    SSSS_Db = pd.read_csv('./SSSS.csv')
    EmpID_df = SSSS_Db.loc[: , 'EmplID'].values
       
    #nested function in order to accurately reference driver variable
    def FrameSwitch(FrameName):
        D.switch_to.frame(D.find_element_by_name(FrameName))
    
        D.get("https://wingsuid.holmcenter.com/psp/wings/WINGS/WINGS_LOCAL/c/W_CADET_PERSONNEL.W_PERSON_ROTC.GBL?PORTALPARAM_PTCNAV=W_PERSON_ROTC&EOPP.SCNode=WINGS_LOCAL&EOPP.SCPortal=WINGS&EOPP.SCName=PERSON_ROTC&EOPP.SCLabel=Bio%2fDemo&EOPP.SCFName=BIO_DEMO&EOPP.SCSecondary=true&EOPP.SCPTfname=BIO_DEMO&FolderPath=PORTAL_ROOT_OBJECT.PERSON_ROTC.W_PERSONNEL.BIO_DEMO.W_PERSON_ROTC&IsFolder=false")
         
    time.sleep(2)
    alert = D.switch_to_alert()
    alert.accept()
       
    #to be populated
    SSN_DB = []
    Address_DB = []
    City_DB = []
    State_DB = []
    Phone_DB = []
    Email_DB = []
    Zip_DB = []
    Gender_DB = []
    
    ###
    FName_DB = []
    LName_DB = []
    MName_DB = []
    DOB_DB = []

    for i in range(len(EmpID_df)):
        time.sleep(3.5)#3.5 Seconds Works, Will try to lower this for faster results in the future
        FrameSwitch('TargetContent')
        #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, 'UserID')))
        EmpID = WebDriverWait(D, 5).until(EC.presence_of_element_located((By.XPATH,'//input[@id="W_ROTC_XSRCH_EMPLID" and @maxlength="11"]')))
        Fixed_EMPID = ''.join(('0',str(EmpID_df[i])))
        EmpID.send_keys(Fixed_EMPID)
        EmpSrc = D.find_element_by_id('#ICSearch')
        EmpSrc.click()
        #time.sleep(1.5)   
        #Begin WINGS Scrape for required Data
        SSN_DB.append(WebDriverWait(D, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="W_PERSON_W_SSN"]'))).text) 
        #SSN_DB.append(D.find_element_by_xpath('//*[@id="W_PERSON_W_SSN"]').text)
    
        Personal_Tab = D.find_element_by_id('ICTAB_2')
        Personal_Tab.click()

        Address_DB.append(WebDriverWait(D, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="W_ADDRESS_ADDRESS1$0"]'))).text) 
        FName_DB.append(D.find_element_by_xpath('//*[@id="W_PERSON_W_FIRST_NAME"]').get_attribute('value')) #grabs textbox inputs
        LName_DB.append(D.find_element_by_xpath('//*[@id="W_PERSON_W_LAST_NAME"]').get_attribute('value')) #grabs textbox inputs
        MName_DB.append(D.find_element_by_xpath('//*[@id="W_PERSON_W_MIDDLE_NAME"]').get_attribute('value')) #grabs textbox inputs
        DOB_DB.append(D.find_element_by_xpath('//*[@id="W_PERSON_W_BIRTHDATE"]').get_attribute('value')) #grabs textbox inputs
        City_DB.append(D.find_element_by_xpath('//*[@id="W_ADDRESS_CITY$0"]').text) 
        State_DB.append(D.find_element_by_xpath('//*[@id="W_ADDRESS_W_STATE$0"]').text) 
        Gender_DB.append((Select(D.find_element_by_id('W_PERSON_W_GENDER')).first_selected_option).text) 
        Zip_DB.append(D.find_element_by_xpath('//*[@id="W_ADDRESS_POSTAL$0"]').text) 
        Phone_DB.append(D.find_element_by_xpath('//*[@id="W_PHONE_W_PHONE$0"]').text) 
        Email_DB.append(D.find_element_by_xpath('//*[@id="W_EMAIL_W_EMAIL$0"]').text)
        D.get("https://wingsuid.holmcenter.com/psp/wings/WINGS/WINGS_LOCAL/c/W_CADET_PERSONNEL.W_PERSON_ROTC.GBL?PORTALPARAM_PTCNAV=W_PERSON_ROTC&EOPP.SCNode=WINGS_LOCAL&EOPP.SCPortal=WINGS&EOPP.SCName=PERSON_ROTC&EOPP.SCLabel=Bio%2fDemo&EOPP.SCFName=BIO_DEMO&EOPP.SCSecondary=true&EOPP.SCPTfname=BIO_DEMO&FolderPath=PORTAL_ROOT_OBJECT.PERSON_ROTC.W_PERSONNEL.BIO_DEMO.W_PERSON_ROTC&IsFolder=false")
    
    #Create DoDMets.CSV with gathered information for User Review/Vetting, Will migrate this to Sqlite DB for Spring 19            
    with open('DoDMets.csv','w', newline='') as ws:
        columnnames = ['Last Name','First Name','MI','SSN','BDay','Gender','Address','City','State','ZIP','Email','Phone']
        thewriter = csv.DictWriter(ws, fieldnames=columnnames)
        
        thewriter.writeheader()
        for i in range(len(EmpID_df)):
            thewriter.writerow({'Last Name' : LName_DB[i],'First Name' : FName_DB[i],'MI' : MISC.CleanUpNaN(MName_DB[i]),'SSN' : SSN_DB[i],'BDay' : DOB_DB[i],'Gender' : Gender_DB[i],'Address' : Address_DB[i],'City' : City_DB[i],'State' : DMETS.StateFix[State_DB[i]],'ZIP' : str(Zip_DB[i]),'Email' : Email_DB[i],'Phone' : Phone_DB[i]})
            
 
    
def DoDMets_Execute(D):
    
    #Collect DodMets
    df = pd.read_csv('./DoDMets.csv')
    
    # created a df for each variable
    df_LastName = df["Last Name"]
    df_FirstName = df["First Name"]
    df_MI = df["MI"]
    df_SSN = df["SSN"]
    df_DoB = df["BDay"]
    df_Email = df["Email"]
    df_Gender = df["Gender"]
    df_Address = df["Address"]
    df_City = df["City"]
    df_State = df["State"]
    df_Zip = df["ZIP"]
    df_Phone = df["Phone"]
    
    #driver = webD.Ie() #Opens Browser
    driver = webdriver.Chrome()
    D.maximize_window()

    D.get("https://www.dodmets.com/Login.aspx") #Navigates to URL
    
    #Automates actions
    Usr_Login = D.find_element_by_id('MasterContentBody_contentPlaceHolderContent_UserName')
    #Usr_Login.send_keys("560")
    Usr_Login.send_keys(ssss.Mets_usr)
        
    Pwd_Login = D.find_element_by_id('MasterContentBody_contentPlaceHolderContent_UserPassword')
    #Pwd_Login.send_keys("Det560ny30")
    Pwd_Login.send_keys(ssss.Mets_pwd)

    Login = D.find_element_by_id('MasterContentBody_contentPlaceHolderContent_buttonlogin')
    Login.click()  
    D.get("https://www.dodmets.com/Dashboard/Applicant/Add.aspx")
   
    for i in range(len(df_LastName)):
        ssn= D.find_element_by_id('ApplicantSSN')
        ssn.send_keys(df_SSN[i])
    
        Confirm_ssn = D.find_element_by_id('ApplicantSSNConfirm')
        Confirm_ssn.send_keys(df_SSN[i])
    
        F_name = D.find_element_by_id('ApplicantFirstName')
        F_name.send_keys(df_FirstName[i])
        
        if(df_MI[i] != "-"):
            M_Name = D.find_element_by_id('ApplicantMiddleName') #optional
            M_Name.send_keys(str(df_MI[i]))
    
        L_Name = D.find_element_by_id('ApplicantLastName')
        L_Name.send_keys(df_LastName[i])
    
        Bday = D.find_element_by_id('ApplicantBirthDate') ##/##/####
        Bday.send_keys(df_DoB[i])

        Confirm_Bday = D.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[2]/button[2]')
        Confirm_Bday.click()
    
        Gender = D.find_element_by_id('ApplicantSexInitial') #dropdown
        for option in Gender.find_elements_by_tag_name('option'):
            if option.text == str(df_Gender[i]).upper():
                option.click()
                break
    
        Address = D.find_element_by_id('ApplicantAddress1')
        Address.send_keys(df_Address[i])
    
        City = D.find_element_by_id('ApplicantCity')
        City.send_keys(df_City[i])
    
        State = D.find_element_by_id('ApplicantState') #dropDown
        for option in State.find_elements_by_tag_name('option'):
            if option.text == df_State[i]:
                option.click()
                break

        Zip = D.find_element_by_id('ApplicantZip1') #5 Digits Max
        if(len(str(df_Zip[i])) < 5):
            NewZip = "0" + str(df_Zip[i])
            Zip.send_keys(str(NewZip))
        else:
            Zip.send_keys(str(df_Zip[i]))
    
        Email = D.find_element_by_id('ApplicantEmail')
        Email.send_keys(df_Email[i])
    
        Confirm_Email = D.find_element_by_id('ApplicantEmailConfirm')
        Confirm_Email.send_keys(df_Email[i])
    
        H_Phone = D.find_element_by_id('ApplicantPhone1')
        H_Phone.send_keys(df_Phone[i])

        C_Phone = D.find_element_by_id('ApplicantPhone2')
        C_Phone.send_keys(df_Phone[i])
    
        AppZip = D.find_element_by_id('centerselectby_detachmentcenter')
        AppZip.click()

        
        #AddCadet = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'buttonApplicantAdd')), 'Did not find add Applicant Button by ID')
        #AddCadet = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="buttonApplicantAdd"]')))
        #AddCadet.click() #Works in IE
        #Need to Add Toggle for execute & dry run
        #AddCadet = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="buttonApplicantAdd"]')))        
        #AddCadet.send_keys('\n') #Solution to the unclickable element error in Chrome Driver

        time.sleep(.5)
        D.get("https://www.dodmets.com/Dashboard/Applicant/Add.aspx")
    D.get("https://www.dodmets.com/Dashboard/")

#DoDMETS_Data_Grab()
DoDMets_Execute()


