from PyQt5 import QtWidgets, QtGui, uic
import sys
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import re

db = sqlite3.connect('NewhopeGUIproject.db')
cur = db.cursor()


#-----Login interface----------

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        uic.loadUi("Newhope_login.ui", self)

        self.login_btn = self.findChild(QtWidgets.QPushButton, "Loginbutton")
        self.email = self.findChild(QtWidgets.QLineEdit, "emailField")
        self.password = self.findChild(QtWidgets.QLineEdit, "psw")
        self.Login_as = self.findChild(QtWidgets.QComboBox, "dropdown_btn")

        self.login_btn.clicked.connect(self.loginAddress)
        self.show()

    # function for login as drop down button
    def loginAddress(self):
        Loginadd = self.Login_as.currentText()
        if Loginadd == 'Admin':
            self.validationAdmin()
        elif Loginadd == 'Staff':
            self.validationStaff()

    # ---------Admin login validation function----
    def validationAdmin(self):
        try:
            email_ = self.email.text()
            pwd_ = self.password.text()
            query = cur.execute('select * from Admin where Email="' + email_ + '" and password="' + pwd_ + '"')

            if query.fetchall() != []:
                self.hide()
                admin = AdminInterface(self)
                admin.show()

                msgbox = QMessageBox()
                msgbox.setFixedSize(800, 800)
                msgbox.setIcon(QMessageBox.Information)

                msgbox.setText("login successful")
                msgbox.exec_()


            else:
                msgbox = QMessageBox()
                msgbox.setFixedSize(800, 800)
                msgbox.setIcon(QMessageBox.Warning)

                msgbox.setText("Invalid login details")
                msgbox.exec_()

        except Exception as e:
            print(e)

    # ---------Staff Login validation function----
    def validationStaff(self):
        try:
            email_ = self.email.text()
            pwd_ = self.password.text()
            query = cur.execute('select * from Staff where Email="' + email_ + '" and password="' + pwd_ + '"')

            if query.fetchall() != []:
                self.hide()
                staff = StaffInterface(self)
                staff.show()

                msgbox = QMessageBox()
                msgbox.setFixedSize(800, 800)
                msgbox.setIcon(QMessageBox.Information)

                msgbox.setText("login successful")
                msgbox.exec_()


            else:
                msgbox = QMessageBox()
                msgbox.setFixedSize(800, 800)
                msgbox.setIcon(QMessageBox.Warning)

                msgbox.setText("Invalid login details")
                msgbox.exec_()

        except Exception as e:
            print(e)

        self.show()


# ---- Admin interface class
class AdminInterface(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AdminInterface, self).__init__(parent)
        uic.loadUi("NewHope_Admin_interface.ui", self)

        self.viewstaff = self.findChild(QtWidgets.QPushButton, "viewstaff_btn")
        self.addstaff = self.findChild(QtWidgets.QPushButton, "addstaff_btn")
        self.deletestaff = self.findChild(QtWidgets.QPushButton, "deletestaff_btn")
        self.updatestaff = self.findChild(QtWidgets.QPushButton, "updatestaff_btn")
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn_1')

        self.viewstaff.clicked.connect(self.popup_view)
        self.addstaff.clicked.connect(self.popup_add)
        self.deletestaff.clicked.connect(self.popup_delete)
        self.updatestaff.clicked.connect(self.popup_update)
        self.back.clicked.connect(self.go_back)
        self.open()

    # -------- function to show veiw staff Interface
    def popup_view(self):
        self.hide()
        view = ViewStaff(self)
        view.show()

    # ----------function to Show add staff Interface
    def popup_add(self):
        self.hide()
        add = AddStaff(self)
        add.show()
    # function to show delete staff interface
    def popup_delete(self):
        delete_ = DeleteStaff(self)
        delete_.show()

    #function to show update staff interface
    def popup_update(self):
        self.hide()
        update_ = UpdateStaff(self)
        update_.show()

    #-----------function to go back to login interface
    def go_back(self):
        self.hide()
        login = Login(self)
        login.show()


#----------View staff interface
class ViewStaff(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ViewStaff, self).__init__(parent)
        uic.loadUi("ViewStaffDetails.ui", self)

        self.populateButton = self.findChild(QtWidgets.QPushButton,'PopulateBtn')
        self.table = self.findChild(QtWidgets.QTableWidget,'tableDisplayWidget')
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn_1')
        self.searchline = self.findChild(QtWidgets.QLineEdit, 'search')
        self.search = self.findChild(QtWidgets.QPushButton, 'searchbtn')

        self.populateButton.clicked.connect(self.getData)
        self.back.clicked.connect(self.go_back)
        self.search.clicked.connect(self.searchData)
        self.getData()
        self.show()

    # function to populate the views table
    def getData(self):
      try:
        query = cur.execute(f'select * from Staff')
        myresult = query.fetchall()

        row = 0
        self.table.setRowCount(len(myresult))
        for staff in myresult:
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(staff[0])))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem((staff[1])))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(staff[2]))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(staff[3]))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(staff[4]))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(staff[5]))

            row = row + 1

      except Exception as e:
          print(e)

    # function to seearch for data in the database
    def searchData(self):
      try:
        word = self.searchline.text()
        query = cur.execute(f'select * from Staff where FirstName like "' + word + '%"')
        myresult_ = query.fetchall()


        row = 0
        self.table.setRowCount(len(myresult_))
        for staff in myresult_:
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(staff[0])))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem((staff[1])))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(staff[2]))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(staff[3]))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(staff[4]))
                self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(staff[5]))

                row = row + 1
      except Exception as e:
          print(e)


    #function to go back to Admin interface
    def go_back(self):
        self.hide()
        admin = AdminInterface(self)
        admin.show()

#-----------Add staff interface
class AddStaff(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddStaff, self).__init__(parent)
        uic.loadUi("AddStaffDetails.ui", self)

        self.firstname = self.findChild(QtWidgets.QLineEdit, 'FirstName')
        self.lastname = self.findChild(QtWidgets.QLineEdit, 'LastName')
        self.email = self.findChild(QtWidgets.QLineEdit, 'Email')
        self.phoneno = self.findChild(QtWidgets.QLineEdit, 'PhoneNo')
        self.password = self.findChild(QtWidgets.QLineEdit, 'Password')
        self.addDetails = self.findChild(QtWidgets.QPushButton, 'AddStaffbtn')
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn_2')


        self.addDetails.clicked.connect(self.addNewstaffDetail)
        self.back.clicked.connect(self.go_back)
        self.show()

    # function for validating add staff details
    def addNewstaffDetail(self):
        try:
         fname_ = self.firstname.text()
         lname_ = self.lastname.text()
         email = self.email.text()
         phoneno = self.phoneno.text()
         password = self.password.text()

         if len(fname_) > 1 and len(lname_) > 1 :

             if len(phoneno) >= 11:

                if re.findall('[a-zA-Z]', phoneno) == [] and re.findall('^080|^081|^090|^070|^091', phoneno):

                    if len(password) >= 5:

                        if '@gmail.com' in email or '@yahoo.com' in email:
                            cur.execute('INSERT INTO Staff (FirstName,LastName,Email,PhoneNo,Password)VALUES(?,?,?,?,?)',
                                       (fname_, lname_, email, phoneno, password))

                            db.commit()

                            msgbox = QMessageBox()
                            msgbox.setFixedSize(800, 800)
                            msgbox.setIcon(QMessageBox.Information)

                            msgbox.setText("Staff successfully added")
                            msgbox.exec_()


                        else:
                            msgbox = QMessageBox()
                            msgbox.setFixedSize(800, 800)
                            msgbox.setIcon(QMessageBox.Warning)

                            msgbox.setText("your data is incomplete or not in the formate required")
                            msgbox.exec_()
                    else:
                        msgbox = QMessageBox()
                        msgbox.setFixedSize(800, 800)
                        msgbox.setIcon(QMessageBox.Warning)

                        msgbox.setText("password is less than 5")
                        msgbox.exec_()


                else:
                  msgbox = QMessageBox()
                  msgbox.setFixedSize(800, 800)
                  msgbox.setIcon(QMessageBox.Warning)

                  msgbox.setText("Should not contain a-z, number formates are 080,081,091,070,090 as first numbers")
                  msgbox.exec_()
             else:
                 msgbox = QMessageBox()
                 msgbox.setFixedSize(800, 800)
                 msgbox.setIcon(QMessageBox.Warning)

                 msgbox.setText("your phone no is less than 11")
                 msgbox.exec_()
         else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Warning)

            msgbox.setText("insert values into the column.\n lenght of name must be greater than one.\n")
            msgbox.exec_()

        except Exception as e:
            print(e)

     #---- function to go Back to the  Admin interface
    def go_back(self):
        self.hide()
        admin = AdminInterface(self)
        admin.show()

#------------Delete Staff Interface---
class DeleteStaff(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DeleteStaff, self).__init__(parent)
        uic.loadUi("DeleteStaff.ui", self)

        self.dropdown = self.findChild(QtWidgets.QComboBox, 'DropDownbtn')
        self.deleteWrd = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.delete = self.findChild(QtWidgets.QPushButton, 'Deletebtn')
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn')

        self.delete.clicked.connect(self.deleteclicked)
        self.back.clicked.connect(self.go_back)
        self.show()
    # function for when you click delete button
    def deleteclicked(self):
      deleteusing = self.dropdown.currentText()

      if deleteusing =="Staff ID":
        self.usingStaffId()
        msgbox = QMessageBox()
        msgbox.setFixedSize(800, 800)
        msgbox.setIcon(QMessageBox.Information)

        msgbox.setText("Staff successfully Deleted")
        msgbox.exec_()

      elif deleteusing =="Email":
          self.usingStaffEmail()

          msgbox = QMessageBox()
          msgbox.setFixedSize(800, 800)
          msgbox.setIcon(QMessageBox.Information)

          msgbox.setText("Staff successfully Deleted")
          msgbox.exec_()

      else:
        msgbox = QMessageBox()
        msgbox.setFixedSize(800, 800)
        msgbox.setIcon(QMessageBox.Warning)

        msgbox.setText(" incorrect staff details or staff not deleted ")
        msgbox.exec_()

   # function to delete using staffId
    def usingStaffId(self):
        staffid =self.deleteWrd.text()
        cur.execute('Delete from Staff where StaffId="' + staffid + '"')
        db.commit()


    #function to delete using Email Name
    def usingStaffEmail(self):
        staffemail=self.deleteWrd.text()
        cur.execute('Delete from Staff where Email="' + staffemail + '"')

    # function to go back to admin interface
    def go_back(self):
        self.hide()
        admin = AdminInterface(self)
        admin.show()

# update staff details
class UpdateStaff(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UpdateStaff, self).__init__(parent)
        uic.loadUi("UpdateStaffDetails.ui", self)

        self.email = self.findChild(QtWidgets.QLineEdit, "Email")
        self.column = self.findChild(QtWidgets.QComboBox, "Dropdownbtn")
        self.newvalue = self.findChild(QtWidgets.QLineEdit, "NewValue")
        self.updatebtn = self.findChild(QtWidgets.QPushButton, "updatebtn")
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn')

        self.updatebtn.clicked.connect(self.emailvalidation)
        self.back.clicked.connect(self.go_back)
        self.show()

    # function to validate if email inouted is in the database
    def emailvalidation(self):
        email = self.email.text()
        query = cur.execute('select * from Staff where Email="' + email + '"')

        if query.fetchall() != []:
            self.columnName()
        else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Warning)

            msgbox.setText(" Email does not exist ")
            msgbox.exec_()

    # function to update column selected
    def columnName(self):
        column = self.column.currentText()
        if column == 'FirstName':
            self.firstname()
        elif column == 'LastName':
            self.lastname()
        elif column == 'Email':
            self.email_()
        elif column == 'PhoneNo':
            self.phoneno()
        elif column == 'Password':
            self.password()

    # ------function to update firstname column
    def firstname(self):
        new_value = self.newvalue.text()
        email_ = self.email.text()
        cur.execute('Update Staff set FirstName="'+new_value+'" where Email="'+email_+'"')
        db.commit()

        msgbox = QMessageBox()
        msgbox.setFixedSize(800, 800)
        msgbox.setIcon(QMessageBox.Information)

        msgbox.setText("Staff record successfully updated")
        msgbox.exec_()

    #--------- function to update lastname column
    def lastname(self):
        new_value = self.newvalue.text()
        email_ = self.email.text()

        cur.execute('Update Staff set LastName ="' + new_value + '" where Email="' + email_ + '"')
        db.commit()

        msgbox = QMessageBox()
        msgbox.setFixedSize(800, 800)
        msgbox.setIcon(QMessageBox.Information)

        msgbox.setText("Staff record successfully updated")
        msgbox.exec_()

    #--------- function to update email
    def email_(self):
        new_value= self.newvalue.text()
        email_ = self.email.text()

        cur.execute('Update Staff set Email="' + new_value + '" where Email="' + email_ + '"')
        db.commit()

        msgbox = QMessageBox()
        msgbox.setFixedSize(800, 800)
        msgbox.setIcon(QMessageBox.Information)

        msgbox.setText("Staff record successfully updated")
        msgbox.exec_()
    #--------  function to updated phone number
    def phoneno(self):
       new_value = self.newvalue.text()
       email_ = self.email.text()
       if len(new_value) >=11:

           if re.findall('[a-zA-Z]', new_value) == [] and re.findall('^080|^081|^090|^070|^091', new_value):
                cur.execute('Update Staff set PhoneNo="' + new_value + '" where Email="' + email_ + '"')
                db.commit()

                msgbox = QMessageBox()
                msgbox.setFixedSize(800, 800)
                msgbox.setIcon(QMessageBox.Information)

                msgbox.setText("Staff record successfully updated")
                msgbox.exec_()
           else:
                msgbox = QMessageBox()
                msgbox.setFixedSize(800, 800)
                msgbox.setIcon(QMessageBox.Warning)

                msgbox.setText("The number format you imputed is incorrect\n formates are:\n080, 090,070,081,091")
                msgbox.exec_()
       else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Warning)

            msgbox.setText("The number is less < 11")
            msgbox.exec_()
    # ----------function to update password column
    def password(self):
        new_value = self.newvalue.text()
        email_ = self.email.text()
        if len(new_value) > 5:
            cur.execute('Update Staff set Password="' + new_value + '" where Email="' + email_ + '"')
            db.commit()

            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Information)

            msgbox.setText("Staff record successfully updated")
            msgbox.exec_()
        else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Warning)

            msgbox.setText("password lenght must be > 5")
            msgbox.exec_()

    # ----------function to go back to admin interface
    def go_back(self):
        self.hide()
        admin = AdminInterface(self)
        admin.show()

#------Staff Interface class
class StaffInterface(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(StaffInterface, self).__init__(parent)
        uic.loadUi("NewHope_Staff_interface.ui", self)

        self.viewdrugs = self.findChild(QtWidgets.QPushButton, "view_drugs")
        self.adddrugs = self.findChild(QtWidgets.QPushButton, "Add_drugs")
        self.deletedrugs = self.findChild(QtWidgets.QPushButton, "Delete_drugs")
        self.updatedrugs = self.findChild(QtWidgets.QPushButton, "Update_drugs")
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn_1')
        self.viewdrugs.clicked.connect(self.popup_view)

        self.adddrugs.clicked.connect(self.popup_add)
        self.deletedrugs.clicked.connect(self.popup_delete)
        self.updatedrugs.clicked.connect(self.popup_update)
        self.back.clicked.connect(self.go_back)
        self.open()

   # -------- function to show view drugs  Interface

    def popup_view(self):
        self.hide()
        view = ViewDrugsDetails(self)
        view.show()

    # ----------functions  to show add drugs interface

    def popup_add(self):
        self.hide()
        add = AddDrugsDetails(self)
        add.show()

    # function to show delete drugs interface
    def popup_delete(self):
        delete_ = DeleteDrug(self)
        delete_.show()

    #function to show  update drugs interface
    def popup_update(self):
        update= UpdateDrugs(self)
        update.show()



    # -----------function to go back to login interface

    def go_back(self):
        self.hide()
        login = Login(self)
        login.show()

#---------view drugs interface----
class ViewDrugsDetails(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ViewDrugsDetails, self).__init__(parent)
        uic.loadUi("ViewDrugs.ui", self)

        self.populateButton = self.findChild(QtWidgets.QPushButton, 'PopulateBtn')
        self.table = self.findChild(QtWidgets.QTableWidget, 'tableDisplayWidget')
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn_1')
        self.searchline = self.findChild(QtWidgets.QLineEdit, 'search')
        self.search = self.findChild(QtWidgets.QPushButton, 'searchbtn')

        self.populateButton.clicked.connect(self.getData)
        self.back.clicked.connect(self.go_back)
        self.search.clicked.connect(self.searchData)
        self.getData()


        self.show()

#function to populate table
    def getData(self):
        try:
            query = cur.execute(f'select * from Drugs')
            myresult = query.fetchall()

            row = 0
            self.table.setRowCount(len(myresult))
            for drug in myresult:
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(drug[0])))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem((drug[1])))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(drug[2])))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(drug[3]))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(drug[4])))


                row = row + 1
                print(drug)
        except Exception as e:
            print(e)

    #function to search for a data on the table
    def searchData(self):
      try:
        word = self.searchline.text()
        query = cur.execute(f'select * from Drugs where DrugName like "' + word + '%"')
        myresult_ = query.fetchall()


        row = 0
        self.table.setRowCount(len(myresult_))
        for staff in myresult_:
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(staff[0])))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem((staff[1])))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(staff[2]))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(staff[3]))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(staff[4]))
                self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(staff[5]))

                row = row + 1
      except Exception as e:
          print(e)

    #function to go back to staff interface
    def go_back(self):
        self.hide()
        staffint = StaffInterface(self)
        staffint.show()

# ----------- Add drugs interface
class AddDrugsDetails(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddDrugsDetails, self).__init__(parent)
        uic.loadUi("AddDrugs.ui", self)

        self.Drugname = self.findChild(QtWidgets.QLineEdit, 'DrugName')
        self.Druggrammes = self.findChild(QtWidgets.QLineEdit, 'DrugGrammes')
        self.Drug_exp_date = self.findChild(QtWidgets.QLineEdit, 'Drug_exp_Date')
        self.Drugprice = self.findChild(QtWidgets.QLineEdit, 'DrugPrice')
        self.addDrug = self.findChild(QtWidgets.QPushButton, 'AddDrugbtn')
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn')

        self.addDrug.clicked.connect(self.addNewDrugs)
        self.back.clicked.connect(self.go_back)

        self.show()

    #----------function to add new drugs
    def addNewDrugs(self):
        try:
           drugname = self.Drugname.text()
           drugrammes = self.Druggrammes.text()
           drug_exp_date = self.Drug_exp_date.text()
           drugprice =self.Drugprice.text()
           if len(drugname) > 1:

            cur.execute('INSERT INTO Drugs'
                        '(DrugName,Drug_grammes,Drugs_Exp_Date,DrugsPrice)VALUES(?,?,?,?)',
                        (drugname, int(drugrammes), drug_exp_date,int(drugprice)))

            db.commit()

            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Information)

            msgbox.setText("Drugs successful Added ")
            msgbox.exec_()

           else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Warning)

            msgbox.setText("Invalid login details")
            msgbox.exec_()
        except Exception as error:
            print(error)
    #function to go back to staff interface
    def go_back(self):
        self.hide()
        staffint = StaffInterface(self)
        staffint.show()

# --------Delete drug interface
class DeleteDrug(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DeleteDrug, self).__init__(parent)
        uic.loadUi("DeleteDrugs.ui", self)

        self.deleteWrd = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.delete = self.findChild(QtWidgets.QPushButton, 'Deletebtn')
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn')

        self.delete.clicked.connect(self.deleteclicked)
        self.back.clicked.connect(self.go_back)

        self.show()
    #function for when delete button is clicked
    def deleteclicked(self):
        drugid = self.deleteWrd.text()
        query = cur.execute('select * from Drugs where DrugId="' + drugid + '"')

        if query.fetchall() != []:
            cur.execute('Delete from Drugs where DrugId="' + drugid + '"')
            db.commit()

            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Information)

            msgbox.setText(" Delete succesful ")
            msgbox.exec_()

        else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Warning)

            msgbox.setText(" Email does not exist ")
            msgbox.exec_()
    #function to go back to staff interface
    def go_back(self):
        self.hide()
        staffint = StaffInterface(self)
        staffint.show()


#--------------- update drug details
class UpdateDrugs(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UpdateDrugs, self).__init__(parent)
        uic.loadUi("UpdateDrugs.ui", self)

        self.drugId = self.findChild(QtWidgets.QLineEdit, "Email")
        self.column = self.findChild(QtWidgets.QComboBox, "Dropdownbtn")
        self.newvalue = self.findChild(QtWidgets.QLineEdit, "NewValue")
        self.updatebtn = self.findChild(QtWidgets.QPushButton, "updatebtn")
        self.back = self.findChild(QtWidgets.QPushButton, 'Backtbtn')

        self.updatebtn.clicked.connect(self.drugIdvalidation)
        self.back.clicked.connect(self.go_back)
        self.show()
    # function to check if the drugs to be updated is in the database
    def drugIdvalidation(self):
        drugid = self.drugId.text()
        query = cur.execute('select * from Drugs where DrugId="' + drugid + '"')

        if query.fetchall() != []:
            self.columnName()
        else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Warning)

            msgbox.setText(" Drug ID does not exist ")
            msgbox.exec_()

    # function to update column selected
    def columnName(self):
        try:
            column = self.column.currentText()
            if column == 'DrugName':
                self.drugname()
            elif column == 'Drug_grammes':
                self.drug_grammes()
            elif column == 'Drugs_Exp_Date':
                self.Drugs_Exp_Date()
            elif column == 'DrugPrice':
                self.drugprice()
        except Exception as e:
            print(e)

    # --------Function to update drugname
    def drugname(self):
        new_value = self.newvalue.text()
        drugid_ = self.drugId.text()

        if len(new_value) > 1:
            cur.execute('Update Drugs set DrugName="'+new_value+'" where DrugId="'+drugid_+'"')
            db.commit()

            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Information)

            msgbox.setText("Staff record successfully updated")
            msgbox.exec_()
        else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Warning)

            msgbox.setText("Drug name should be greater than one")
            msgbox.exec_()

    #--------- function to update drug_grammes
    def drug_grammes(self):
        new_value_ = self.newvalue.text()
        drugid_ = self.drugId.text()

        if len(new_value_) > 1:
            cur.execute('Update Staff set Drug_grammes ="' + int(new_value_) + '" where DrugId="' + drugid_ + '"')
            db.commit()

            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Information)

            msgbox.setText("Drug grammes record successfully updated")
            msgbox.exec_()

        else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Information)

            msgbox.setText(" lenght of Drug grammes should be greater than one ")
            msgbox.exec_()

    #--------- function to update Drugs_Exp_Date
    def Drugs_Exp_Date(self):
        new_value = self.newvalue.text()
        drugid_ = self.drugId.text()
        if len(new_value) > 1:
            cur.execute('Update Drugs set Drugs_Exp_Date="' + new_value + '" where DrugId="' + drugid_ + '"')
            db.commit()

            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Information)

            msgbox.setText("Drugs Expiry Date successfully updated")
            msgbox.exec_()
        else:
            msgbox = QMessageBox()
            msgbox.setFixedSize(800, 800)
            msgbox.setIcon(QMessageBox.Information)

            msgbox.setText(" Lenght of Drug Expiry Date must be greater than one ")
            msgbox.exec_()

    #--------  function to updated Drug price
    def drugprice(self):
           new_value = self.newvalue.text()
           drugid_ = self.email.text()

           if int(new_value) >= 500:

                cur.execute('Update Staff set DrugPrice ="' + int(new_value) + '" where DrugId="' + drugid_ + '"')
                db.commit()

                msgbox = QMessageBox()
                msgbox.setFixedSize(800, 800)
                msgbox.setIcon(QMessageBox.Information)

                msgbox.setText("Staff record successfully updated")
                msgbox.exec_()

           else:
                msgbox = QMessageBox()
                msgbox.setFixedSize(800, 800)
                msgbox.setIcon(QMessageBox.Warning)

                msgbox.setText("The price of a drug can not be less than 500")
                msgbox.exec_()

    # ----------function to go back to staff interface
    def go_back(self):
        self.hide()
        staffint = StaffInterface(self)
        staffint.show()


app = QtWidgets.QApplication(sys.argv)
window = Login()
app.setQuitOnLastWindowClosed(False)
app.exec_()
