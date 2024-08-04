from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from os import *
import sys
import sqlite3
from xlsxwriter import *
from xlrd import *

import random
import smtplib
from email.message import EmailMessage
import ssl



import datetime
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui #pyqt stuff
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

from main import Ui_MainWindow
MAIN_UI,_= loadUiType("main.ui")

# gettig id and branch from the user who just login
#Giving a default values
employee_id = 0
employee_branch = 0
#generate a rando number for password recovery
password_code = random.randint(1000, 9999)


class MainApp(QMainWindow, MAIN_UI):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.db_connect()

        self.Handel_Buttons()

        self.Ui_Changes()
        #to open in this tab
        #self.Open_Daily_Movements_tab()
        self.Open_Login_tab()
        
        self.Show_All_categories()
        self.Show_All_branchies()
        self.Show_All_Authors()
        self.Show_All_Publishers()
        self.Show_All_Clients()
        self.Show_All_Books()
        self.Show_All_Employees()
        self.Show_History()
        
        self.Retrive_Today_Work()
        # self.Show_All_Status()
        
        self.Get_Dashboard_Data()
#######################################(##########################################################    
    
    def Ui_Changes(self):
        #Type here the ui changes
        #Tp hide the main tab bar
        self.tabWidget.tabBar().setVisible(False)


    def db_connect(self):
        self.db = sqlite3.connect('library.db')
        self.cur = self.db.cursor()
        print("db connected")


    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Open_Daily_Movements_tab)
        self.pushButton_2.clicked.connect(self.Open_Books_tab)
        self.pushButton_3.clicked.connect(self.Open_Clients_tab)
        self.pushButton_4.clicked.connect(self.Open_Dashboeard_tab)
        self.pushButton_5.clicked.connect(self.Open_History_tab)
        self.pushButton_6.clicked.connect(self.Open_Reports_tab)
        self.pushButton_7.clicked.connect(self.Open_Settings_tab)
        self.pushButton_46.clicked.connect(self.Open_Login_tab)
        self.pushButton_14.clicked.connect(self.Edit_Book_Search)
        self.pushButton_19.clicked.connect(self.Edit_Client_Search)
        self.pushButton_9.clicked.connect(self.All_Books_Filter)
        self.pushButton_13.clicked.connect(self.All_Clients_Filter)
        

        self.pushButton_8.clicked.connect(self.Handel_Today_work)
        self.pushButton_21.clicked.connect(self.Add_New_branch)
        self.pushButton_22.clicked.connect(self.Add_New_publisher)
        self.pushButton_23.clicked.connect(self.Add_New_Author)
        self.pushButton_25.clicked.connect(self.Add_New_catigory)
        self.pushButton_27.clicked.connect(self.Add_New_Employee)
        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_17.clicked.connect(self.Add_New_Client)
        self.pushButton_15.clicked.connect(self.Edit_Book)
        self.pushButton_13.clicked.connect(self.Delete_Book)
        self.pushButton_16.clicked.connect(self.All_Clients_Filter)
        self.pushButton_18.clicked.connect(self.Edit_Client)
        self.pushButton_35.clicked.connect(self.Export_Books)
        self.pushButton_20.clicked.connect(self.Delete_Client)
        self.pushButton_32.clicked.connect(self.check_employee)
        self.pushButton_28.clicked.connect(self.Edit_Employee)
        self.pushButton_30.clicked.connect(self.Add_Employee_Permissions)
        self.pushButton_37.clicked.connect(self.Export_Clients)
        self.pushButton_39.clicked.connect(self.Export_History)
        ###### LOGIN
        self.pushButton_38.clicked.connect(self.Handel_Login)
        self.pushButton_44.clicked.connect(self.Open_Rest_Password_Tab)
        self.pushButton_47.clicked.connect(self.Handel_Reset_Password)
        self.pushButton_50.clicked.connect(self.check_the_code)
        self.pushButton_51.clicked.connect(self.Save_New_Password)
        #### Refresh
        # self.pushButton_49.clicked.connect(self.Refresh)
        
        
    # def Refresh(self):
    #     self.Show_All_Authors()
    #     self.Show_All_Books()
    #     self.Show_All_categories()
    #     self.Show_All_Clients()
    #     self.Show_All_Employees()
    #     self.Show_All_Publishers()
    #     self.Show_History()
        
        
    def Handel_Login(self):
        username = self.lineEdit_11.text()
        password = self.lineEdit_49.text()
        self.cur.execute('''
            SELECT name , password , id , branch FROM Employees             
            ''')
        data = self.cur.fetchall()
        for row in data:
            if row[0] == username and row[1] == password:
              ##########################################
                global employee_id , employee_branch
                employee_id = row[2]
                employee_branch = row[3]
                
                print(employee_id)
              ########################################
                self.groupBox_15.setEnabled(True)
                ## load user permissions
                self.cur.execute('''
                    SELECT * FROM EmployeePermissions WHERE employee_name=?
                    ''',(username,))
                permissions = self.cur.fetchone()
                print(permissions)
                
                if permissions[2] == 1 :
                    self.pushButton_2.setEnabled(True)
                if permissions[3] == 1 :
                    self.pushButton_3.setEnabled(True)
                if permissions[4] == 1 :
                    self.pushButton_4.setEnabled(True)
                if permissions[5] == 1 :
                    self.pushButton_5.setEnabled(True)
                if permissions[6] == 1 :
                    self.pushButton_6.setEnabled(True)
                if permissions[7] == 1 :
                    self.pushButton_7.setEnabled(True)
                #Add book    
                if permissions[8] == 1 :
                    self.pushButton_10.setEnabled(True)
                #Edit book   
                if permissions[9] == 1 :
                    self.pushButton_15.setEnabled(True)
                #Delete Book   
                if permissions[10] == 1 :
                    self.pushButton_13.setEnabled(True)
                 #import book   
                if permissions[9] == 1 :
                    self.pushButton_34.setEnabled(True)
                #Exporte Book   
                if permissions[10] == 1 :
                    self.pushButton_35.setEnabled(True)
                    
                 #Add client    
                if permissions[11] == 1 :
                    self.pushButton_17.setEnabled(True)
                #Edit client    
                if permissions[12] == 1 :
                    self.pushButton_18.setEnabled(True)
                #Delete client   
                if permissions[13] == 1 :
                    self.pushButton_20.setEnabled(True)
                 #import client    
                if permissions[14] == 1 :
                    self.pushButton_36.setEnabled(True)
                #Exporte client    
                if permissions[15] == 1 :
                    self.pushButton_37.setEnabled(True)
                    
                 #add branch   
                if permissions[16] == 1 :
                    self.pushButton_21.setEnabled(True)
                 #add publisher   
                if permissions[17] == 1 :
                    self.pushButton_22.setEnabled(True)
                 #add author 
                if permissions[18] == 1 :
                    self.pushButton_23.setEnabled(True)
                 #add catigory    
                if permissions[19] == 1 :
                    self.pushButton_25.setEnabled(True)
                 #add employee  
                if permissions[20] == 1 :
                    self.pushButton_27.setEnabled(True)
                    
                self.Open_Daily_Movements_tab()
            else:
                self.groupBox_7.setEnabled(True)
       




      
               
    def Handel_Reset_Password(self):
        receiver_email = self.lineEdit_50.text()
        
        #check if the email exists
        self.cur.execute('''
            SELECT name FROM employees WHERE email=?    
        ''',(receiver_email,))    
        data = self.cur.fetchone()
          
        if data:
            print(data[0]) 
            #sendig the code via email
            sender_email = 'techameur@gmail.com'
            email_password = 'bcsg bhcv kfnf cjxw'
            subject = 'Reset Password Library management'
            message = f'this is your reset password code : {password_code}'
            print(f'password_code is {password_code}')
            em= EmailMessage()
            em['From'] = sender_email
            em['To'] = receiver_email
            em['Subject'] = subject
            em.set_content(message)
            #crypting
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(sender_email,email_password)
                smtp.sendmail(sender_email,receiver_email,em.as_string())

            self.statusBar().showMessage('Code has been sent')
            #Enable the code line edit
            self.lineEdit_52.setEnabled(True)
            self.pushButton_50.setEnabled(True)
            
        if data == None:
            self.statusBar().showMessage('Email does not exist')

    #cheking if the codes are the same
    def check_the_code(self):
        code = int(self.lineEdit_52.text())
        if code == password_code:
            self.lineEdit_53.setEnabled(True)
            self.lineEdit_54.setEnabled(True)
            self.pushButton_51.setEnabled(True)
            
        else:
            self.statusBar().showMessage('Code is wrong') 

    # save the new password to db
    def Save_New_Password(self):
        email = self.lineEdit_50.text()
        password1 = self.lineEdit_53.text()
        password2 = self.lineEdit_54.text()
        if password1 == password2:
            self.cur.execute('''
                UPDATE Employees SET password=? 
                WHERE email=?
            ''',(password1,email))
            self.db.commit()
            self.statusBar().showMessage('Password changed')
        else:
            self.statusBar().showMessage('Please retype the passwords correctly')


    def Handel_Today_work(self):
        book_barcode = self.lineEdit.text()
        type = self.comboBox.currentIndex()
        client_national_id = self.lineEdit_51.text()
        #to_date = self.dateEdit_6.date()
        to_date = datetime.date.today()
        from_date = datetime.date.today()
        date = datetime.datetime.now()
        branch_id = 1 #just for testing
        # still branch and employee!!!!!
        self.cur.execute('''
            INSERT INTO DailyMovements (book_barcode , client_national_id , type , book_from , book_to ,branch_id, date)             
            VALUES (? , ? , ? , ? , ? ,?,?)
            ''',(book_barcode,client_national_id,type,from_date,to_date, branch_id ,date))
        self.db.commit()
        print("done")
        self.Retrive_Today_Work()
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(3) 
        table = str(9) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        
        
    def Retrive_Today_Work(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        self.cur.execute('''
            SELECT book_barcode , client_national_id , type, book_from, book_to FROM DailyMovements                 
        ''')
        data = self.cur.fetchall()
          # creating the table
        for row,form in enumerate(data):
            for col , item in enumerate(form):
                if col == 2 :
                    if item == 0:
                        self.tableWidget.setItem(row,col,QTableWidgetItem(str("Rent")))
                    else:
                        self.tableWidget.setItem(row,col,QTableWidgetItem(str("Rtrive")))
                elif col == 1:
                    self.cur.execute('''
                        SELECT name from Clients WHERE national_id=?          
                                     ''',(item,))
                    name = self.cur.fetchone()
                    self.tableWidget.setItem(row,col,QTableWidgetItem(str(name[0])))
                else:   
                    self.tableWidget.setItem(row,col,QTableWidgetItem(str(item)))
                col+=1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
        
        
        
        
    ################## OPEN TABS ############################   
    def Open_Login_tab(self):
        self.tabWidget.setCurrentIndex(0)


    def Open_Password_tab(self):
        self.tabWidget.setCurrentIndex(1)


    def Open_Daily_Movements_tab(self):
        self.tabWidget.setCurrentIndex(2)


    def Open_Books_tab(self):
        self.tabWidget.setCurrentIndex(3)
        #To open it in the first tab
        self.tabWidget_2.setCurrentIndex(0)
     


    def Open_Clients_tab(self):
        self.tabWidget.setCurrentIndex(4)
        #To open it in the first tab
        self.tabWidget_3.setCurrentIndex(0)
      


    def Open_Dashboeard_tab(self):
        self.Get_Dashboard_Data()
        self.tabWidget.setCurrentIndex(5)
        


    def Open_History_tab(self):
        self.tabWidget.setCurrentIndex(6)


    def Open_Reports_tab(self):
        self.tabWidget.setCurrentIndex(7)
        #To open it in the first tab
        self.tabWidget_5.setCurrentIndex(0)


    def Open_Settings_tab(self):
        self.tabWidget.setCurrentIndex(8)
        #To open it in the first tab
        self.tabWidget_4.setCurrentIndex(0)

    def Open_Rest_Password_Tab(self):
        self.tabWidget.setCurrentIndex(1)



    #######################################  BOOKS #################################################

    def Show_All_Books(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        # Get data from db
        self.cur.execute('''
            SELECT barcode , title , catigory_id , author_id , price FROM Books
        ''')
        data = self.cur.fetchall()
        # creating the table
        for row,form in enumerate(data):
            for col , item in enumerate(form):
                if col == 2:
                    self.cur.execute('''
                        SELECT name FROM catigory WHERE id=?             
                        ''',(item+1,))
                    catigory_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(catigory_name[0])))
                elif col==3:
                    self.cur.execute('''
                        SELECT name FROM Authors WHERE id=?             
                        ''',(item+1,)) #زائد واحد لانو مكانش اي دي صفر
                    author_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(author_name[0])))
                else:
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(item)))
                col+=1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)

    def Add_New_Book(self):
        title = self.lineEdit_3.text()
        desc = self.textEdit.toPlainText()
        catigory = self.comboBox_3.currentIndex()
        price = self.lineEdit_4.text()
        barcode = self.lineEdit_5.text()
        publisher = self.comboBox_4.currentIndex()
        author = self.comboBox_5.currentIndex()
        partorder = self.lineEdit_6.text()
        status = self.comboBox_6.currentIndex()
        date = datetime.datetime.now()

        self.cur.execute('''
            INSERT INTO Books (title,desc,catigory_id,barcode,price,publisher_id,author_id,partorder,date,status)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        ''' , (title,desc,catigory,barcode,price,publisher,author,partorder,date,status))
        self.db.commit()
        print("Book Added")
        self.statusBar().showMessage("Book Added")
        
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(3) # add on the combobox
        table = str(1) #books on the combobox
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,branch,date)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,employee_branch,date))
        self.db.commit()
        self.Show_History()
        
    def All_Books_Filter(self):
        book_barcode = self.lineEdit_2.text()    
        self.cur.execute('''
            SELECT barcode,title,catigory_id,author_id,price FROM Books
            WHERE barcode=? 
            ''',(book_barcode,))
        
        data = self.cur.fetchall()
         # creating the table
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        for row,form in enumerate(data):
            for col , item in enumerate(form):
                if col == 2:
                    self.cur.execute('''
                        SELECT name FROM catigory WHERE id=?             
                        ''',(item+1,))
                    catigory_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(catigory_name[0])))
                elif col==3:
                    self.cur.execute('''
                        SELECT name FROM Authors WHERE id=?             
                        ''',(item+1,)) #زائد واحد لانو مكانش اي دي صفر
                    author_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(author_name[0])))
                else:
                    self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(item)))
                col+=1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
        print(data)

    def Edit_Book_Search(self):   #Delete book from db
        code = self.lineEdit_15.text()
        #getting the data
        self.cur.execute('''
            SELECT * FROM Books WHERE barcode = ?
        ''',(code,))
        book = self.cur.fetchall()
        
        #setting the data
        self.lineEdit_14.setText(book[0][1])
        self.lineEdit_12.setText(str(book[0][6]))
        self.lineEdit_13.setText(str(book[0][5]))
        self.comboBox_15.setCurrentIndex(book[0][3])
        self.comboBox_12.setCurrentIndex(book[0][7])
        self.comboBox_14.setCurrentIndex(book[0][8])
        self.textEdit_3.setPlainText(book[0][2])

    def Edit_Book(self):
        #Getting the new data
        title = self.lineEdit_14.text()
        desc = self.textEdit_3.toPlainText()
        catigory = self.comboBox_15.currentIndex()
        price = self.lineEdit_12.text()
        publisher = self.comboBox_12.currentIndex()
        author = self.comboBox_14.currentIndex()
        partorder = self.lineEdit_13.text()
        status = self.comboBox_13.currentIndex()
        date = datetime.datetime.now()
        code = self.lineEdit_15.text()

        self.cur.execute('''
            UPDATE Books SET title=? , desc=? ,catigory_id=? , price=? , publisher_id=? , author_id=? , partorder=? , status=? , date=? 
            WHERE barcode=?             
        ''',(title,desc,catigory,price,publisher,author,partorder,status,date,code))
        self.db.commit()
        #Show a message
        self.statusBar().showMessage("Book Updated")
        #to reload the new data
        self.Show_All_Books()
        
         ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(4) # add on the combobox
        table = str(1) #books on the combobox
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()


    def Delete_Book(self):
        code = self.lineEdit_15.text()
        self.cur.execute('''
            DELETE FROM Books WHERE barcode=?
        ''',(code,))
        self.db.commit()
        self.statusBar().showMessage('Book Deleted')
        #to reload the new data
        self.Show_All_Books()
        date =datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(5) 
        table = str(1) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()
        
    def Export_Books(self):
        # Get data from db
        self.cur.execute('''
            SELECT barcode , title , catigory_id , author_id , price FROM Books
        ''')
        data = self.cur.fetchall()
       
         #Create exel file
        file = Workbook('Reports/books.xlsx')
        sheet_1 = file.add_worksheet()
        #Add format
        bold = file.add_format({'bold':1})
        date = file.add_format({'num_format':"mmmm d yyyy"})
        border = file.add_format({'border':True})
        header = file.add_format({'bold':1 ,
                                  'border':True ,
                                  "align": "center",})
        main_title = file.add_format({'bold':True,
                                      'font_size':20,
                                      "align": "center",
                                      "valign": "vcenter",
                                      })
        sub_title = file.add_format({'bold':True,
                                      "align": "center",
                                      "valign": "vcenter",
                                      })
        
        price = file.add_format({'num_format' :'$#,##0'})
        #Creating a title
        sheet_1.merge_range('C3:F3','Clients Report',main_title)

        sheet_1.merge_range('A5:C5' , 'Habib for library management',sub_title)

        sheet_1.merge_range('D5:F5' , 'Phone : 0778111137' , sub_title)

        #Creating Headers
        sheet_1.write('A9','Code', header)
        sheet_1.write('B9','Title', header)
        sheet_1.write('C9','Catigory', header)
        sheet_1.write('D9','Author', header)
        sheet_1.write('E9','Price', header)

        sheet_1.set_column(0,4,12)
        # insert the data to the table
        row_number=9
        for row in data:
            col_number = 0
            for item in row:
                sheet_1.write(row_number,col_number,str(item),border)
                col_number+=1
            row_number+=1
        file.close()
        self.statusBar().showMessage("Books Exported")
        

    ##########################################  CLIENTS  #############################################

    def Show_All_Clients(self):
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        # Get data from db
        self.cur.execute('''
            SELECT name , email, phone , national_id , date FROM Clients
        ''')
        data = self.cur.fetchall()
        # creating the table
        for row,form in enumerate(data):
            for col , item in enumerate(form):
                self.tableWidget_4.setItem(row,col,QTableWidgetItem(str(item)))
            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)
        
    def All_Clients_Filter(self):
        #getting the data from user
        employee_data = self.lineEdit_16.text()
        
        if self.comboBox_17.currentIndex () == 0:
            print('name')
            self.cur.execute('''
            SELECT name,email,phone,national_id,date FROM Clients WHERE name=?
            ''',(employee_data,))
            data = self.cur.fetchall()
            print(data)
        if self.comboBox_17.currentIndex() == 1:
            self.cur.execute('''
            SELECT name,email,phone,national_id,date FROM Clients WHERE email=?
            ''',(employee_data,))
            data = self.cur.fetchall()
            print(data)
        if self.comboBox_17.currentIndex() == 2:
            self.cur.execute('''
            SELECT name,email,phone,national_id,date FROM Clients WHERE phone=?
            ''',(employee_data,))
            data = self.cur.fetchall()
            print(data)
        if self.comboBox_17.currentIndex() == 3:
            self.cur.execute('''
            SELECT name,email,phone,national_id,date FROM Clients WHERE national_id=?
            ''',(employee_data,))
            data = self.cur.fetchall()
            print(data)

        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        for row,form in enumerate(data):
            for col,item in enumerate(form):
                self.tableWidget_4.setItem(row,col,QTableWidgetItem(str(item)))
        row_position = self.tableWidget_4.rowCount()
        self.tableWidget_4.insertRow(row_position)


    def Add_New_Client(self):
        name = self.lineEdit_17.text()
        phone = self.lineEdit_19.text()
        national_id = self.lineEdit_20.text()
        email = self.lineEdit_18.text()
        date = datetime.datetime.now()
        self.cur.execute('''
            INSERT INTO Clients (name , phone , national_id , email , date)
            VALUES (? , ? , ? , ? , ?)
        ''', (name,phone,national_id,email , date))

        self.db.commit()
        print("client")
        self.statusBar().showMessage("Clieent Added")
        
        
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(3) 
        table = str(2) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()

    def Edit_Client_Search(self):   #Delete Client from db
        client_data = self.lineEdit_21.text()
        #name
        if self.comboBox_16.currentIndex() == 0:
            self.cur.execute('''
                SELECT * FROM Clients WHERE name=?
            ''',(client_data,))
            client = self.cur.fetchone()
            print(client)
        #email
        if self.comboBox_16.currentIndex() == 1:
            self.cur.execute('''
            SELECT * FROM Clients WHERE email=?
            ''',(client_data,))
            client = self.cur.fetchone()
            print(client)
        #phone
        if self.comboBox_16.currentIndex() == 2:
            self.cur.execute('''
            SELECT * FROM Clients WHERE phone=?
            ''',(client_data,))
            client = self.cur.fetchone()
            print(client)
        #national id
        if self.comboBox_16.currentIndex() == 3:
            self.cur.execute('''
            SELECT * FROM Clients WHERE national_id=?
            ''',(client_data,))
            client = self.cur.fetchone()
            print(client)

        # Setting up Data
        #name
        self.lineEdit_25.setText(client[1])
        #email
        self.lineEdit_22.setText(client[2])
        #phone
        self.lineEdit_24.setText(client[3])
        #national id
        self.lineEdit_23.setText(str(client[5]))
           

    def Export_Clients(self):
        #Getting data
        self.cur.execute('''
            SELECT name,email,phone,national_id,date FROM Clients
        ''')
        data = self.cur.fetchall()
        print(data)
        #Create exel file
        file = Workbook('Reports/clients.xlsx')
        sheet_1 = file.add_worksheet()
        #Add format
        bold = file.add_format({'bold':1})
        date = file.add_format({'num_format':"mmmm d yyyy"})
        border = file.add_format({'border':True})
        header = file.add_format({'bold':1 ,
                                  'border':True ,
                                  "align": "center",})
        main_title = file.add_format({'bold':True,
                                      'font_size':20,
                                      "align": "center",
                                      "valign": "vcenter",
                                      })
        sub_title = file.add_format({'bold':True,
                                      "align": "center",
                                      "valign": "vcenter",
                                      })
        #Creating a title
        sheet_1.merge_range('C3:D3','Clients Report',main_title)

        sheet_1.merge_range('A5:B5' , 'Habib for library management',sub_title)

        sheet_1.merge_range('D5:E5' , 'Phone : 0778111137' , sub_title)
        #Creating Headers
        sheet_1.write('A9','Name', header)
        sheet_1.write('B9','Email', header)
        sheet_1.write('C9','Phone', header)
        sheet_1.write('D9','National ID', header)
        sheet_1.write('E9','Date', header)

        # insert the data to the table
        row_count=9
        for row in data:
            col_count = 0
            for item in row: 
                # توسعة الاعمدة
                if col_count == 4:
                    sheet_1.set_column(
                        col_count, #Starting column
                        col_count , #Ending column
                        30 , #width
                    )
                else:
                    sheet_1.set_column(
                        0 , #starting column
                        3 , #end column
                        15,
                    )
                sheet_1.write(row_count,col_count,str(item),border)
                col_count+=1
            row_count+=1
        file.close()
        self.statusBar().showMessage("Clients Exported")


    def Edit_Client(self):
        name = self.lineEdit_25.text()
        phone = self.lineEdit_24.text()
        national_id = self.lineEdit_23.text()
        email = self.lineEdit_22.text()
       
        self.cur.execute('''
            UPDATE or IGNORE Clients SET name=? , phone=? , national_id=? , email=? 
        ''',(name,phone,national_id,email))
        self.db.commit()
        self.statusBar().showMessage("Client Edited")
        #to reload the new data
        self.Show_All_Clients()
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(4) 
        table = str(2) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()

    def Delete_Client(self):
        client_data = self.lineEdit_21.text()
        #name
        if self.comboBox_16.currentIndex() == 0:
            self.cur.execute('''
                DELETE FROM Clients WHERE name=?
            ''',(client_data,))
        #email
        if self.comboBox_16.currentIndex() == 1:
            self.cur.execute('''
            DELETE FROM Clients WHERE email=?
            ''',(client_data,))
        #phone
        if self.comboBox_16.currentIndex() == 2:
            self.cur.execute('''
            DELETE FROM Clients WHERE phone=?
            ''',(client_data,))
        #national id
        if self.comboBox_16.currentIndex() == 3:
            self.cur.execute('''
            DELETE FROM Clients WHERE national_id=?
            ''',(client_data,))
        self.db.commit()
        self.statusBar().showMessage('Client Deleted')
        #to reload the new data
        self.Show_All_Clients()
        
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(5) 
        table = str(2) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()
  
        # Get data from db
        self.cur.execute('''
            SELECT name , email, phone , national_id  FROM Clients
        ''')
        data = self.cur.fetchall()
        
         #create exel file
        excel_file = Workbook('clients_report.xlsx')
        sheet_1 = excel_file.add_worksheet()
        # wtrite data on the file
        sheet_1.write(0,0,"Name")
        sheet_1.write(0,1,"Email")
        sheet_1.write(0,2,"Phone")
        sheet_1.write(0,3,"National id")
        
        row_number=1
        for row in data:
            col_number = 0
            for item in row:
                sheet_1.write(row_number,col_number,str(item))
                col_number+=1
            row_number+=1
        excel_file.close()
        self.statusBar().showMessage("Clients Exported")
        
        
    ##########################################  DASHBORAD #################################################
    
    def Get_Dashboard_Data(self):
        year_filter = self.dateEdit_7.date()
        year_filter = year_filter.toPyDate()  #convert it to a python date
        year = str(year_filter).split('-')[0]  # Getting the year
        #Getting data from db
        #strftime('%m', book_from) is just like extract in my sql
        
        #This need year filter
        self.cur.execute('''
            SELECT COUNT(book_barcode), strftime('%m', book_from) as month 
            FROM DailyMovements
            GROUP BY month          
            ''')
        data = self.cur.fetchall()
        print(data)
        book_count = []
        rent_count = []
        for row in data:
            book_count.append(row[0])
            rent_count.append(int(row[1]))
           
        # Creating a bar chart
        bar_graph = pg.BarGraphItem(x=rent_count , height=book_count , width=.2 )
        self.widget.addItem(bar_graph)
        #self.widget.plot(book_count,rent_count)
        self.widget.setTitle('sales')
        self.widget.setLabel('left','Quantity')
        self.widget.setLabel('bottom','Books')
    ##########################################  HISTORY  #############################################

    def Show_History(self):
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)
        
        self.cur.execute('''
            SELECT employee , db_table , action , branch , date FROM History             
            ''')
        data = self.cur.fetchall()
        for row,form in enumerate(data):
            for col , item in enumerate(form):
                if col == 0:
                    self.cur.execute('''
                        SELECT name FROM Employees WHERE id=?
                        ''',(item,))
                    employee = self.cur.fetchone()
                    self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(employee[0])))
                elif col == 1:
                    if item == 1:
                        table = 'Books'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    if item == 2:
                        table = 'Clients'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    if item == 3:
                        table = 'History'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    if item == 4:
                        table = 'Employees'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    if item == 5:
                        table = 'Branch'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    if item == 6:
                        table = 'Author'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    if item == 7:
                        table = 'Catigory'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    if item == 8:
                        table = 'Publisher'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    if item == 9:
                        table = 'Daily movements'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(table)))
                    
                elif col == 2:
                    if item == 1:
                        action = 'Login'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(action)))
                    if item == 2:
                        action = 'Logout'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(action)))
                    if item == 3:
                        action = 'Add'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(action)))
                    if item == 4:
                        action = 'Edit'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(action)))
                    if item == 5:
                        action = 'Delete'
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(action)))
                elif col == 3:
                    self.cur.execute('''
                        SELECT name FROM Branch WHERE id=?
                        ''',(item+1,))
                    branch = self.cur.fetchone()
                    self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(branch[0])))
                else:
                    self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(item)))
            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)
        
    def Export_History(self):
        #Getting data
        self.cur.execute('''
        SELECT employee , db_table , branch , action , date FROM  history
    ''')
        data = self.cur.fetchall()
        #Create Ewel file
        file = Workbook('Reports/history.xlsx')
        sheet_1 = file.add_worksheet()
        #Add format
        bold = file.add_format({'bold':1})
        date = file.add_format({'num_format':"mmmm d yyyy"})
        border = file.add_format({'border':True})
        header = file.add_format({'bold':1 ,
                                  'border':True ,
                                  "align": "center",})
        main_title = file.add_format({'bold':True,
                                      'font_size':20,
                                      "align": "center",
                                      "valign": "vcenter",
                                      })
        sub_title = file.add_format({'bold':True,
                                      "align": "center",
                                      "valign": "vcenter",
                                      })
        #Creating a title
        sheet_1.merge_range('C3:E3','Clients Report',main_title)

        sheet_1.merge_range('A5:C5' , 'Habib for library management',sub_title)

        sheet_1.merge_range('D5:E5' , 'Phone : 0778111137' , sub_title)
        #Creating Headers
        sheet_1.write('A9','Employee', header)
        sheet_1.write('B9','Table', header)
        sheet_1.write('C9','Branch', header)
        sheet_1.write('D9','Action', header)
        sheet_1.write('E9','Date', header)

        # insert the data to the table
        row_count=9
        for row in data:
            col_count = 0
            for item in row:
                if col_count == 0:
                    self.cur.execute('''
                        SELECT name FROM Employees WHERE id=?
                        ''',(item,))
                    employee = self.cur.fetchone()
                    sheet_1.write(row_count,col_count,str(employee[0]),border)
                elif col_count == 4:
                    sheet_1.set_column(col_count,col_count,30)
                    sheet_1.write(row_count,col_count,str(item),border)
                elif col_count == 1:
                    if item == 1:
                        table = 'Books'
                        sheet_1.write(row_count,col_count,str(table),border)
                    if item == 2:
                        table = 'Clients'
                        sheet_1.write(row_count,col_count,str(table),border)
                    if item == 3:
                        table = 'History'
                        sheet_1.write(row_count,col_count,str(table),border)
                    if item == 4:
                        table = 'Employees'
                        sheet_1.write(row_count,col_count,str(table),border)
                    if item == 5:
                        table = 'Branch'
                        sheet_1.write(row_count,col_count,str(table),border)
                    if item == 6:
                        table = 'Author'
                        sheet_1.write(row_count,col_count,str(table),border)
                    if item == 7:
                        table = 'Catigory'
                        sheet_1.write(row_count,col_count,str(table),border)
                    if item == 8:
                        table = 'Publisher'
                        sheet_1.write(row_count,col_count,str(table),border)
                    if item == 9:
                        table = 'Daily movements'
                        sheet_1.write(row_count,col_count,str(table),border)
                elif col_count == 2:
                    self.cur.execute('''
                        SELECT name FROM Branch WHERE id=?
                        ''',(item+1,))
                    branch = self.cur.fetchone()
                    sheet_1.write(row_count,col_count,str(branch[0]),border)
                elif col_count == 3:
                    if item == 1:
                        action = 'Login'
                        sheet_1.write(row_count,col_count,str(action),border)
                    if item == 2:
                        action = 'Logout'
                        sheet_1.write(row_count,col_count,str(action),border)
                    if item == 3:
                        action = 'Add'
                        sheet_1.write(row_count,col_count,str(action),border)
                    if item == 4:
                        action = 'Edit'
                        sheet_1.write(row_count,col_count,str(action),border)
                    if item == 5:
                        action = 'Delete'
                        sheet_1.write(row_count,col_count,str(action),border)
                else:
                    sheet_1.write(row_count,col_count,str(item),border)
                col_count+=1
            row_count+=1
        file.close()
        self.statusBar().showMessage("History Exported")



    ##########################################  Reports  #############################################
    ######################## Books
    def All_Books_Report(self):
        pass

    def Books_Filter_Report(self):
        pass

    def Export_Books_report(self):
        pass
    
    ######################## Client
    def All_Clients_Report(self):
        pass

    def Clients_Filter_Report(self):
        pass

    def Export_Clients_report(self):
        pass

    ######################## Monthly

    def Monthly_report(self):
        pass

    def Export_Monthly_Report(self):
        pass

    #################### SHOW ######################################################
    def Show_All_categories(self):
        self.cur.execute('''
            SELECT name FROM Catigory
        ''')
        #Getting all categories
        categories = self.cur.fetchall()
        # convert it from tupel to string and add it to combo box
        for category in categories:
            c = category[0]
            self.comboBox_7.addItem(c)     
            # ADD new Book
            self.comboBox_3.addItem(c)    
            # Edit or delete Book
            self.comboBox_15.addItem(c)  

    def Show_All_branchies(self):
        self.cur.execute('''
            SELECT name FROM Branch               
        ''')

        branchies = self.cur.fetchall()
        for branch in branchies:
            b = branch[0]
            # Add items to add employee
            self.comboBox_22.addItem(b)
            #History
            #self.comboBox_9.addItem(b)

    def Show_All_Publishers(self):
        self.cur.execute('''
            SELECT name FROM Publisher               
        ''')

        publishers = self.cur.fetchall()
        for publisher in publishers:
            p = publisher[0]
            #add new book
            self.comboBox_4.addItem(p)
            #edit or delete book
            self.comboBox_12.addItem(p)

    def Show_All_Authors(self):
        self.cur.execute('''
            SELECT name FROM Authors              
        ''')

        authors = self.cur.fetchall()
        for author in authors:
            a = author[0]
            #add new book
            self.comboBox_5.addItem(a)
            #Edit or delete book
            self.comboBox_14.addItem(a)
    
    # def Show_All_Status(self):
    #     self.cur.execute('''
    #     SELECT status FROM Books
    # ''')
    #     book_status = self.cur.fetchall()
    #     for s in book_status:
    #         s = s[0]
    #         #add new book
    #         self.comboBox_13.addItem(s)
    
    def Show_All_Employees(self):
        self.cur.execute('''
            SELECT name FROM Employees
            ''')
        employees = self.cur.fetchall()
        for employee in employees:
            e = employee[0]
            # To employee permissions tab
            self.comboBox_19.addItem(e)
            # to history
            self.comboBox_21.addItem(e)
    ##########################################  Settings  #############################################
    def Add_New_branch(self):
        branch_name = self.lineEdit_26.text()
        branch_code = self.lineEdit_27.text()
        branch_location = self.lineEdit_28.text()

        self.cur.execute(''' 
            INSERT INTO Branch (name , code , location)
            VALUES (? , ? , ?)    
        ''', (branch_name , branch_code , branch_location))
        self.db.commit()
        print("Branch Added")
        
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(3) 
        table = str(5) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()
        
    def Add_New_catigory(self):
        self.comboBox_7.clear()
        category_name = self.lineEdit_36.text()
        parent_category = self.comboBox_7.currentIndex() + 1

        self.cur.execute('''
            INSERT INTO Catigory (name,parent_category)
            VALUES (?,?)
        ''',(category_name,parent_category))
        self.db.commit()
        print('category added')
        self.lineEdit_36.setText('')
        self.Show_All_categories()
        
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(3) 
        table = str(7) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()
    
    

    def Add_New_publisher(self):
        publisher_name = self.lineEdit_26.text()
        publisher_code = self.lineEdit_27.text()
        publisher_location = self.lineEdit_28.text()

        self.cur.execute(''' 
            INSERT INTO Publisher (name , code , location)
            VALUES (? , ? , ?)    
        ''', (publisher_name , publisher_code , publisher_location))
        self.db.commit()
        print("Publisher Added")
        
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(3) 
        table = str(8) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()

    def Add_New_Author(self):
        author_name = self.lineEdit_32.text()
        author_email = self.lineEdit_33.text()
        
        self.cur.execute(''' 
            INSERT INTO Authors (name , email)
            VALUES (? , ?)    
        ''', (author_name , author_email))
        self.db.commit()
        print("Author Added")
        
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(3) 
        table = str(6) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()


    ######################## Employee
    def Add_New_Employee(self):
        employee_name = self.lineEdit_34.text()
        employee_email = self.lineEdit_35.text()
        employee_phone = self.lineEdit_38.text()
        employee_nationalid = self.lineEdit_37.text()
        employee_preority = self.lineEdit_47.text()
        employeebranch= self.comboBox_22.currentText()
        employee_password = self.lineEdit_39.text()
        confirm_password = self.lineEdit_40.text()
        date = datetime.datetime.now()
        if employee_password == confirm_password:
            self.cur.execute('''
                INSERT INTO Employees (name,email,phone,national_id,preority,password,branch,date)
                VALUES (?,?,?,?,?,?,?,?)
            ''', (employee_name,employee_email,employee_phone,employee_nationalid,employee_preority,employee_password,employeebranch,date))
            self.db.commit()
            self.statusBar().showMessage("Employee Added")
        else:
            self.statusBar().showMessage("Wrong password")
        #clean data
        self.lineEdit_34.setText("")
        self.lineEdit_35.setText("")
        self.lineEdit_38.setText("")
        self.lineEdit_37.setText("")
        self.lineEdit_47.setText("")
        self.comboBox_22.currentText()
        self.lineEdit_39.setText("")
        self.lineEdit_40.setText("")
        
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(3) 
        table = str(4) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()
        
    def check_employee(self):
        name = self.lineEdit_42.text()
        password = self.lineEdit_45.text()
        
        self.cur.execute('''
            SELECT * FROM Employees             
            ''')
        data = self.cur.fetchall()
        for row in data:
            if row[7] == password and row[1] == name :
                self.groupBox_9.setEnabled(True)
                self.lineEdit_44.setText(str(row[3]))
                self.lineEdit_41.setText(str(row[5]))
                self.lineEdit_43.setText(str(row[2]))
                self.lineEdit_48.setText(str(row[6]))
                self.lineEdit_46.setText(str(row[7]))
        else : 
            self.statusBar().showMessage("Wrong Password")
            
            
    def Edit_Employee(self):
        phone =  self.lineEdit_44.text()
        national_id = self.lineEdit_41.text()
        email = self.lineEdit_43.text()
        preority = self.lineEdit_48.text()
        new_password= self.lineEdit_46.text()
        
        self.cur.execute('''
            UPDATE Employees SET phone=? , national_id=? , email=? , preority=? , password=?
            WHERE national_id=?
        ''',(phone,national_id,email,preority,new_password,national_id))
        self.db.commit()
        #cleaning data
        self.lineEdit_44.setText("")
        self.lineEdit_41.setText("")
        self.lineEdit_43.setText("")
        self.lineEdit_48.setText("")
        self.lineEdit_46.setText("")
        self.groupBox_9.setEnabled(False)
        self.statusBar().showMessage("Employee Edited")
        
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(4) 
        table = str(4) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()
        
    def Add_Employee_Permissions(self):
        employee_name = self.comboBox_19.currentText()
        #Admin
        if self.checkBox_20.isChecked():
            books_tab= True
            clients_tab= True
            dashboard_tab= True
            history_tab= True
            settings_tab= True
            reports_tab = True
            add_book = True
            edit_book = True
            delete_book = True
            import_book = True
            export_book = True
            add_client = True
            edit_client = True
            delete_client = True
            import_client = True
            export_client = True
            add_branch = True
            add_publisher = True
            add_author = True
            add_catigory =True
            add_employee = True
            self.cur.execute('''
                INSERT INTO EmployeePermissions (employee_name,books_tab,clients_tab,dashboard_tab,history_tab,reports_tab,settings_tab,add_book,edit_book,delete_book,import_book,export_book,add_client,edit_client,delete_client,import_client,export_client,add_branch,add_publisher,add_author,add_catigory,add_employee,add_branch) 
                VALUES   (? , ? , ? , ? , ? , ? , ?, ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?,?,? )          
                ''',(employee_name,books_tab,clients_tab,dashboard_tab,history_tab,reports_tab,settings_tab,add_book,edit_book,delete_book,import_book,export_book,add_client,edit_client,delete_client,import_client,export_client,add_branch,add_publisher,add_author,add_catigory,add_employee,add_branch))
            self.db.commit()
            self.statusBar().showMessage("Employee Edited")
        else:
            books_tab= False
            clients_tab= False
            dashboard_tab= False
            history_tab= False
            settings_tab= False
            reports_tab = False
            add_book = False
            edit_book = False
            delete_book = False
            import_book = False
            export_book = False
            add_client = False
            edit_client = False
            delete_client = False
            import_client = False
            export_client = False
            add_branch = False
            add_publisher = False
            add_author = False
            add_catigory =False
            add_employee = False
            
            
            if self.checkBox_7.isChecked():
                books_tab=True
            if self.checkBox_11.isChecked():
                clients_tab=True
            if self.checkBox_8.isChecked():
                dashboard_tab=True
            if self.checkBox_10.isChecked():
                history_tab=True
            if self.checkBox_9.isChecked():
                reports_tab=True
            if self.checkBox_12.isChecked():
                settings_tab=True
            #Books     
            if self.checkBox.isChecked():
                add_book=True
            if self.checkBox_2.isChecked():
                edit_book=True
            if self.checkBox_3.isChecked():
                delete_book=True
            if self.checkBox_13.isChecked():
                import_book=True
            if self.checkBox_14.isChecked():
                export_book=True
            #Clients
            if self.checkBox_4.isChecked():
                add_client=True
            if self.checkBox_5.isChecked():
                edit_client=True
            if self.checkBox_6.isChecked():
                delete_client=True
            if self.checkBox_15.isChecked():
                import_client=True
            if self.checkBox_16.isChecked():
                export_client=True
            #Settings
            if self.checkBox_18.isChecked():
                add_publisher=True
            if self.checkBox_19.isChecked():
                add_author=True
            if self.checkBox_17.isChecked():
                add_catigory=True
            if self.checkBox_21.isChecked():
                add_employee=True
            if self.checkBox_22.isChecked():
                add_branch=True
        
            
            self.cur.execute('''
                INSERT INTO EmployeePermissions (employee_name,books_tab,clients_tab,dashboard_tab,history_tab,reports_tab,settings_tab,add_book,edit_book,delete_book,import_book,export_book,add_client,edit_client,delete_client,import_client,export_client,add_branch,add_publisher,add_author,add_catigory,add_employee,add_branch) 
                VALUES   (? , ? , ? , ? , ? , ? , ?, ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?,?,? )          
                ''',(employee_name,books_tab,clients_tab,dashboard_tab,history_tab,reports_tab,settings_tab,add_book,edit_book,delete_book,import_book,export_book,add_client,edit_client,delete_client,import_client,export_client,add_branch,add_publisher,add_author,add_catigory,add_employee,add_branch))
            self.db.commit()
        self.statusBar().showMessage("Employee Edited")
        
        date = datetime.datetime.now()
        ###################### Save to the history ###########################
        global employee_id , employee_branch
        action = str(4) 
        table = str(4) 
        self.cur.execute('''
            INSERT INTO History (employee,action,db_table,date,branch)  
            VALUES (?,?,?,?,?)           
            ''',(employee_id,action,table,date,employee_branch))
        self.db.commit()
        self.Show_History()
    def Add_Admin_Report(self):
        # sent report to the admin   
        pass




def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__== '__main__':
    main()