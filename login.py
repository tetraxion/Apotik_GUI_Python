import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from Obat import *
from Create import *
import mysql.connector


class login (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('login.ui', self)
        self.setWindowTitle('LOGIN')
        self.btnLogin.clicked.connect(self.userLogin)
        self.btnCreat.clicked.connect(self.creat)
        
        
    #mendefinisikan fungsi untuk tampil pesan
    def tampilPesan (self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle('Login| Form login')
        msgbox.setText(pesan)
        msgbox.exec()

    #mendefinisikan fungsi untuk menghapus teks
    def hapusTeks(self):
        self.editUser.setText('')
        self.editPasword.setText('')

    #mendefinisikan fungsi untuk melakukan login
    def userLogin (self):
        try:
            username = self.editUser.displayText()
            password = self.editPasword.displayText()

            if username!=''and password!='':
                #menciptakan koneksi ke server mysql
                con=mysql.connector.connect(host='localhost', user='root', password='p&l4ever', database='dbapotik')

                #login ke dalam sistem berdasarkan username dan password yang tersimpan didalam tabel login_tabel
                query='SELECT * FROM login_table WHERE user=%s AND pw=%s'
                data=(username,password)
                cursor=con.cursor()
                cursor.execute(query, data)
                data_user=cursor.fetchall()

                if len(data_user) == 1:
                    self.tampilPesan('Login Sukses')
                    self.hapusTeks()
                    self.berhasil()
                else :
                    self.tampilPesan('Login gagal, silahkan masukkan ulang')
                    self.hapusTeks()
                
            else:
                self.tampilPesan('Username dan Password tidak boleh kosong')
        except:
            self.tampilPesan('Terjadi kesalahan pada login')

    def berhasil(self):
        self.form=Obat()
        self.form.show()

    def creat(self):
        self.form=Create()
        self.form.show()

        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=login()
    form.show()
    sys.exit(app.exec_())

