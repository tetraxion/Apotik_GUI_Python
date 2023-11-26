import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
from login import *
import mysql.connector


class Create (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('creat.ui', self)
        self.setWindowTitle('CREATE ACCOUNT')
        self.btn_Creat.clicked.connect(self.createAccount)
        self.btnKembali.clicked.connect(self.kembali)

    #mendefinisikan fungsi untuk tampil pesan
    def tampilPesan (self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle('Create| Form login')
        msgbox.setText(pesan)
        msgbox.exec()

    #mendefinisikan fungsi untuk menghapus teks
    def hapusTeks(self):
        self.edit_User.setText('')
        self.edit_Pasword.setText('')

    def createAccount (self):
        try:
            #mengambil data account pada form
            user = self.edit_User.displayText()
            pasword = self.edit_Pasword.displayText()

            if  user!='' and pasword!='':
                #membuat koneksi ke server Mysql
                con=mysql.connector.connect(host='localhost', user='root', password='p&l4ever', database='dbapotik')

                #memasukkan data ke dalam tabel obat_table
                query='INSERT INTO login_table(user, pw)VALUES(%s, %s)'
                data=(user,pasword)
                cursor=con.cursor()
                cursor.execute(query, data)
                con.commit()

                #menampilkan pesan menggunakan fungsi tampilPesan
                self.tampilPesan('Data account berhasil dimasukkan')

                #menghapus text pada kotak text
                self.hapusText()
            else:
                #menampilkan pesan menggunakan fungsi tampilPesan
                self.tampilPesan('Silahkan isi dan lengkapi data terlebih dahulu !')
        except :
            #menampilkan pesan eror menggunakan fungsi tampilPesan
            self.tampilPesan('Terjadi kesalahan pada entri data account')

    def kembali(self):
        self.form=login()
        self.form.show()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=Create()
    form.show()
    sys.exit(app.exec_())

