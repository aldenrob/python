import sqlite3
import re
import csv
import time
import sys
import datetime
from pprint import pprint
##################### NOTES SECTION ##############################
#EmpID integer
#StartDate text
#StopDate text
#Amount integer
#ROTC accounting codes 

#ROTC45 = TEXTBOOK

#ROTC12 = STIPEND (GMC)

#ROTC11 = STIPEND (POC)

#AcademicLevel	ASLevel	Monthly	    Bi-Monthly	    Daily
    #SC01	    100	    $300.00	     $150.00	    $10.00
    #SC02	    200	    $350.00	     $175.00	    $11.67
    #NS03	    300	    $450.00	     $225.00	    $15.00
    #NS04	    400	    $500.00	     $250.00	    $16.67
##################################################################

def CreateDB(Name,Flag):
        #creates DB if it doesnt exist or connects to it if it does
        with sqlite3.connect(Name) as conn:
        
            #Allows sql commands to execute
            c = conn.cursor()
            if Flag == 1:
                    #Builds Table
                    c.execute("CREATE TABLE IF NOT EXISTS CadetPay (EmpID text, StartDate text, StopDate text, Amount integer, ROTC_Code text, Row_Index integer)")
            
                    #commits the changes to reflect in db
                    conn.commit()
            if Flag == 2:
                    c.execute('''CREATE TABLE IF NOT EXISTS SMR (EmpID text, Detachment text, ASLvl text, L_Name text, F_Name text, MI text, Name text, SSAN text, DOB text, Program text, Major_Lvl text, Status text, GMC_POC text, 
                                Citizen text, FICE_Code text, Major text, DOC text, ELD text, TGPA integer, CGPA integer, FT_Stat text, FT_Fiscal_Year text, FT_Loc text, FT_Session text, FT_Ranking text, 
                                FT_Class_Size text, Schlr text, Type text, Schlr_Length text, Schlr_Activ_Dt text, Schlr_Term_Ent text, Schlr_Prog text, Schlr_Stat text, Schlr_Stat_Dt text, Enlist_Date text,
                                POC_Entry_Dt text, Security_Level text, Date_Completed text, E_Grade integer, Cat_Sel text, Height integer, Weight integer, Ht_Wt_Dt text, Phys_Type text, DoDMERB_Exp text, MRS text, 
                                AFPFT integer, AFPFT_Dt text, AFPFT_R text, AFOQT_P integer, AFOQT_N integer, AFOQT_A integer, AFOQT_V integer, AFOQT_Q integer, ACT integer, SAT_M integer, SAT_V integer,
                                Conditionals text, Priv_Pilot text, As_Of_Date text)''') 
                    conn.commit()
            if Flag == 3:
                    c.execute("CREATE TABLE IF NOT EXISTS Medical (EmpID text, Address text, City text, State text, Gender text, Zip text, Phone text, Email text)")
                    conn.commit()
#End CreateDB() 

def PopulateMedicalDB(ID, AD, CT, ST, GD, ZP, PH, EM):
    with sqlite3.connect('Medical.db') as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Medical VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ID, AD, CT, ST, GD, ZP, PH, EM))
            conn.commit()
        except Exception as ex:
            print(ex)
#End of PopulateMedicalDB()

def PopulatePayDB(ID,SD,ED,P,A,R):
    with sqlite3.connect('Cadetpay.db') as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO CadetPay VALUES (?, ?, ?, ?, ?, ?)", (ID, SD, ED, P, A, R)) #WORKS
            #c.execute("INSERT INTO CadetPay VALUES (?, ?, ?, ?, ?)", (ID, SD, ED, P, A))
            #c.execute(f"INSERT INTO CadetPay VALUES '{ID}', '{SD}', '{ED}', '{P}', '{A}', '{R}'") #SYNTAX ERROR 
            conn.commit()
        except Exception as ex:
                print(ex)       
#End PopulatePayDB()

def PopulateSMR_DB(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y,
z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx, yy, zz, aaa, bbb, ccc, ddd, eee, fff, ggg, hhh):
    #print("...............Starting SMR SQL Function................")
    with sqlite3.connect('SMR.db') as conn:
        c = conn.cursor()
        try:
            c.execute(f"""INSERT INTO SMR VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}', '{h}', '{i}', '{j}', '{k}', 
            '{l}', '{m}', '{n}', '{o}','{p}', '{q}', '{r}', '{s}', '{t}', '{u}', '{v}', '{w}', '{x}', '{y}', '{z}', '{aa}', '{bb}', 
            '{cc}', '{dd}', '{ee}', '{ff}', '{gg}', '{hh}', '{ii}', '{jj}', '{kk}', '{ll}', '{mm}', '{nn}', '{oo}', '{pp}', '{qq}', 
            '{rr}', '{ss}', '{tt}','{uu}', '{vv}', '{ww}', '{xx}', '{yy}', '{zz}', '{aaa}', '{bbb}', '{ccc}', '{ddd}', '{eee}', '{fff}', '{ggg}', '{hhh}')""")
            conn.commit()            
        except Exception as ex:
                print(ex)       
#End PopulatePayDB()

def NameConversion(ID):
    with sqlite3.connect('SMR.db') as conn:
        c = conn.cursor()
        c.execute(f"SELECT L_Name FROM SMR WHERE EmpID='{ID}'")
        pattern = re.compile(r'\[\(\'(\w.+)\'\,\)\]') #converts [('blah')] to blah 
        try:
            matches = pattern.finditer(str(c.fetchall()))
            for match in matches:
                return match.group(1)
        except Exception as ex:
            print(ex)

def StrQueryConvert(QueryStr):
    pattern = re.compile(r'(\(\')(\w+)\',\)') #converts ('blah') to blah
    matches = pattern.finditer(QueryStr)
    fixedID = []
    for match in matches:
        fixedID.append(match.group(2))
    return fixedID

def PayIndex():
     #Query DB first...
    """
    try:    
        with sqlite3.connect('CadetPay.db') as conn:
        c = conn.cursor()
        c.execute(f"SELECT MAX FROM CadetPay WHERE EmpID='{ID}'")
        return c.fetchall() #set i equal to the most recent rowindex stored in DB
    except Exception:
        return 0 #otherwise start fresh
        break"""     

def ContractDate(ID):
    with sqlite3.connect('CadetPay.db') as conn:
        c = conn.cursor()
        c.execute(f"SELECT StartDate FROM CadetPay WHERE EmpID='{ID}' ORDER BY StartDate")
        Paydates = c.fetchall()
        datetime_list = []
        newDate = []
        pattern = re.compile(r'\(\'(\d+)/(\d+)/(\d+)\'\,\)')
        for i in range(len(Paydates)):
            try:
                matches = pattern.finditer(str(Paydates[i]))
            except Exception:
                print(f"Cadet {NameConversion(ID)} has recieved {Paydates[i]}, and requires action.")
            for match in matches:
                try:
                    newDate.append(match.group(1))
                    newDate.append(match.group(2))
                    newDate.append(match.group(3))
                except Exception as ex:
                    print(ex)    
            try:
                if newDate[0][0] == '0':
                    newDate[0] = newDate[0][1]
            except Exception:
                print(f"An Error occurred for the Date calculation for Cadet {NameConversion(ID)}")
            try:    
                datetime_list.append(datetime.date(int(newDate[2]), int(newDate[0]), int(newDate[1])))
                newDate[:] = []
            except Exception:
                print(f"{NameConversion(ID)} Requires Further attention")        
                newDate[:] = []
        try:
            #print(f"{datetime_list}")    
            return min(datetime_list)
        except Exception:
            print("Could not find a start date")

def TxtBkPay(ID):
    with sqlite3.connect('CadetPay.db') as conn:
        c = conn.cursor()
        c.execute(f"SELECT sum(Amount) FROM CadetPay WHERE EmpID='{ID}' AND Rotc_Code='ROTC45' ")
        pattern = re.compile(r'\[\((\d.+)\,\)\]') 
        matches = pattern.finditer(str(c.fetchall()))
        for match in matches:
            #print(f"Cadet {NameConversion(ID)} has recieved: {int(match.group(1))/300} Semesters of textbook stipend")
            return match.group(1)

def GMCPay(ID):
    with sqlite3.connect('CadetPay.db') as conn:
        c = conn.cursor()
        c.execute(f"SELECT sum(Amount) FROM CadetPay WHERE EmpID='{ID}' AND AccountCode='ROTC12' ")
        pattern = re.compile(r'\[\((\d.+)\,\)\]') 
        matches = pattern.finditer(str(c.fetchall()))
        for match in matches:
            #print(f"Cadet {NameConversion(ID)} has recieved: ${match.group(1)} GMC Stipend")
            return match.group(1)

def POCPay(ID):
    with sqlite3.connect('CadetPay.db') as conn:
        c = conn.cursor()
        c.execute(f"SELECT sum(Amount) FROM CadetPay WHERE EmpID='{ID}' AND AccountCode='ROTC11' ")
        pattern = re.compile(r'\[\((\d.+)\,\)\]') 
        matches = pattern.finditer(str(c.fetchall()))
        for match in matches:
            #print(f"Cadet {NameConversion(ID)} has recieved: ${match.group(1)} POC Stipend")
            return match.group(1)

def AuditPay(DataBase,IDs):
     with sqlite3.connect(DataBase) as conn:
        print("Opened connection to : " + DataBase)
        c = conn.cursor()              
        for i in range (len(IDs)):
            c.execute("SELECT sum(Amount) FROM CadetPay WHERE EmpID=?", (IDs[i],))
            print('')
            print('Cadet '+ IDs[i] +' has Earned:')
            print(c.fetchall())

def AuditPay2(ID):
    def semesters():
        try:
            return int(TxtBkPay(ID))/300 #no longer applicable since txt book increase
        except Exception:
            return "Non-Scholarshipt Cadet"
    def textbook():
        if TxtBkPay(ID) == "None":
            return "N/A "
        else: 
            return f"${TxtBkPay(ID)}"


    print(f'Cadet {NameConversion(ID)} \nContracted(DOE): {ContractDate(ID)} \nTotal GMC Pay: ${GMCPay(ID)} \nTotal POC Pay: ${POCPay(ID)} \nTotal TextBook Stipen: {textbook} over the course of {semesters()}: Semesters\nTotal Amt Paid: ${CareerPay(ID)}\n')

def Overview(Name,Flag):
    with sqlite3.connect(Name) as conn:
        c = conn.cursor()
        if (Flag == 1):
            #returns Pay column only for respective cadet
            c.execute("SELECT Amount FROM Cadetpay WHERE EmpID=0208153") #why do you need this?
            print(c.fetchall())
        if (Flag == 2):
            #returns number of rows for respective cadet
            c.execute("SELECT * FROM SMR WHERE EmpID=0248535") #why do we care about this?
            print(c.fetchall())
        if (Flag == 3):
            #returns number of rows for respective cadet
            c.execute("SELECT * FROM SMR") #why do we need this?
            print(c.fetchall())
        if (Flag == 4):
            #returns PayTotal for respective cadet
            c.execute("SELECT sum(amount) FROM Cadetpay WHERE EmpID=0206539") #not needed, break down into txtbook, GMC and POC.
            print(c.fetchall())
        if (Flag == 5):
            #returns PayTotal for respective cadet
            c.execute("SELECT EmpID FROM SMR WHERE Enlist_Date <>' '")# not required 
            return c.fetchall()
        if (Flag == 6):
            #returns PayTotal for respective cadet
            c.execute("SELECT Enlist_Date FROM SMR")
            return c.fetchall()

#Overview('CadetPay.db',3)
#Overview('SMR.db',3)
#print(len(TestVar))
#Insert_SMR(TestVar)


#Grabs all Contracted Cadet EmpID's
def CadetPayIDs():
    DB_Query = Overview('SMR.db',5)
    Found = (str(DB_Query))
    pattern = re.compile(r'(\(\')(\w+)\',\)')
    matches = pattern.finditer(Found)   
    fixedID = []
    for match in matches:
        fixedID.append(match.group(2))
    return fixedID
#end CadetPayIDs

#Grabs all EmpID's for Cadets with 

#Grabs all EmpID's for Cadets with Certified DoDMERBS
def DoDmetsID():
    with sqlite3.connect("SMR.db") as conn:
        c = conn.cursor()
        c.execute("SELECT EmpID FROM SMR WHERE DoDMERB_Exp =' '")
        DB_Query = c.fetchall()
        return StrQueryConvert(str(DB_Query))
#end DoDMETS_ID

#print(CadetPayIDs())
#print("....................................")
#print(Overview('SMR.db',5))

#Test Area 
def Db_To_CSV():
    with sqlite3.connect("CadetPay.db") as conn:
        csvWriter = csv.writer(open("Output.csv", "w"))
        #columnnames = ['EmpID','Start Date','End Date','PAY']
        #thewriter = csv.DictWriter(csvWriter, fieldnames=columnnames)
        #thewriter.writeheader()
        c = conn.cursor()
        c.execute("SELECT * FROM CadetPay")
        rows = c.fetchall()
        csvWriter.writerows(rows)        
#Db_To_CSV()

if __name__ == "__main__":
    Db_To_CSV()
    #AuditPay('Cadetpay.db',CadetPayIDs())
    #GMCPay(CadetPayIDs()[6])
    
    #for i in range(len(DoDmetsID())):
        #print(DoDmetsID()[i])
        #print(i+1)
    #print(f'Memory (Before): {sys.getsizeof([])}Mb\n')
    #t1 = time.clock()        
    #for i in range(len(CadetPayIDs())):
        #AuditPay2(CadetPayIDs()[i])
    #t2 = time.clock()
    #print(f'Memory (After): {sys.getsizeof([])}Mb\n')
    #print(f'Took {t2-t1} Seconds')
    #     print(NameConversion(CadetPayIDs()[i]))
    # #ConvertDate(CadetPayIDs()[0])
    #TxtBkPay(CadetPayIDs()[])
    #GMCPay(CadetPayIDs()[7])
    #POCPay(CadetPayIDs()[30])
    #print(CadetPayIDs()[6])