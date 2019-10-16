# Web automation imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


#Handles element locations and potential errors
def Find_Xpath(location,Flag,Txt,Package,alt,D):
    if (Flag == "C"):
        try: 
            Clickme = WebDriverWait(D, 5).until(EC.presence_of_element_located((By.XPATH, location)))
            Clickme.click()
        except Exception as ex:
            print("Could not Find "+ Package +" Element By XPATH")
            Find_ID(alt,Flag,Txt,Package,D)
    elif (Flag == "K"):
        try: 
            Textme = WebDriverWait(D, 5).until(EC.presence_of_element_located((By.XPATH, location)))
            Textme.clear()#TESTESTESTESTEST
            Textme.send_keys(Txt)
        except Exception as ex:
            print("Could not Find "+ Package +" Element by XPATH")
            if (Package == "EmpID"):
                D.switch_to.frame(0)
                Find_ID(alt,Flag,Txt,Package,D)
            else:
                Find_ID(alt,Flag,Txt,Package,D)
 #End Find_Xpath()

#Additional Element Location Handling Function            
def Find_ID(location,Flag,Txt,Package,D):
    if (Flag == "C"):
        try:
            Clickme = WebDriverWait(D, 5).until(EC.presence_of_element_located((By.ID, location)))
            Clickme.click()
        except Exception as ex:
            print("Could not Find "+ Package +" Location By ID")
    elif (Flag == "K"):
        if (Package == "EmpID"):
                D.switch_to.frame(0)
        try:
            Textme = WebDriverWait(D, 5).until(EC.presence_of_element_located((By.ID, location)))
            Textme.send_keys(Txt)
        except Exception as ex:
            print("Could not Find "+ Package +" Element by ID")
#End Find_ID()

def CleanUpNaN(Input):
    if(str(Input) == "nan"):
        return "-"
    else:
        return Input

StateFix = {
    'AL': 'Alabama','AK': 'Alaska','AZ': 'Arizona','AR': 'Arkansas','CA': 'California','CO': 'Colorado','CT': 'Connecticut','DC': 'District of Columbia','DE': 'Delaware',
    'FL': 'Florida','GA': 'Georgia','HI': 'Hawaii','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','IA': 'Iowa','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','ME': 'Maine',
    'MD': 'Maryland','MA': 'Massachusetts','MI': 'Michigan','MN': 'Minnesota','MS': 'Mississippi','MO': 'Missouri','MT': 'Montana','NE': 'Nebraska','NV': 'Nevada','NH': 'New Hampshire',
    'NJ': 'New Jersey','NM': 'New Mexico','NY': 'New York','NC': 'North Carolina','ND': 'North Dakota','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VI': 'US Virgin Islands','VT': 'Vermont','VA': 'Virginia','WA': 'Washington','WV': 'West Virginia',
    'WI': 'Wisconsin','WY': 'Wyoming',}
