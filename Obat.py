import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic import loadUi
import mysql.connector


class Obat(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('form_obat.ui', self)
        self.setWindowTitle('PYTHON GUI & MySQL')
        self.tampilDataObat()
        self.btnTambah.clicked.connect(self.entriDataObat)
        self.tabelObat.itemSelectionChanged.connect(self.tampilDataTerpilih)
        self.btnPerbarui.clicked.connect(self.perbaruiDataObat)
        self.btnHapus.clicked.connect(self.hapusDataObat)
        self.btnCari.clicked.connect(self.cariDataObat)

    def tampilPesan (self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle('PYTHON GUI & | Form Obat')
        msgbox.setText(pesan)
        msgbox.exec()

    def tampilDataObat (self):
        #membuat koneksi ke server mysql
        con=mysql.connector.connect(host='localhost', user='root', password='p&l4ever', database='dbapotik')

        #menampilkan data tabel
        query='SELECT * FROM obat_table'
        cursor=con.cursor()
        cursor.execute(query)
        data_obat=cursor.fetchall()

        #menampilkan data obat pada tabel yang terdapat pada form
        n_obat=len(data_obat)
        self.tabelObat.setRowCount(n_obat)
        baris=0

        for x in data_obat:
            self.tabelObat.setItem(baris, 0, QTableWidgetItem(str(x[0])))
            self.tabelObat.setItem(baris, 1, QTableWidgetItem(x[1]))
            self.tabelObat.setItem(baris, 2, QTableWidgetItem(x[2]))
            self.tabelObat.setItem(baris, 3, QTableWidgetItem(x[3]))
            self.tabelObat.setItem(baris, 4, QTableWidgetItem(str(x[4])))
            self.tabelObat.setItem(baris, 5, QTableWidgetItem(str(x[5])))
            baris=baris+1

    def entriDataObat(self):
        try:
            #mengambil data obat pada form
            nomerBatch=self.editNomer.displayText()
            namaObat=self.editNama.displayText()
            kategori=self.editKategori.displayText()
            jenis=self.editJenis.displayText()
            dosis=self.editDosis.displayText()
            stok=self.editStok.displayText()

            if nomerBatch!='' and namaObat!='' and kategori!='' and jenis!='' and dosis!='' and stok!='':
                #membuat koneksi ke server Mysql
                con=mysql.connector.connect(host='localhost', user='root', password='p&l4ever', database='dbapotik')

                #memasukkan data ke dalam tabel obat_table
                query='INSERT INTO obat_table(Nomor_Batch, Nama_Obat, Kategori_obat, Jenis_Obat, Dosis, Stok_Obat)VALUES(%s, %s, %s, %s, %s, %s)'
                data=(int(nomerBatch), namaObat, kategori, jenis, int(dosis), int(stok))
                cursor=con.cursor()
                cursor.execute(query, data)
                con.commit()

                #menutup koneksi
                con.close()

                #menampilkan pesan menggunakan fungsi tampilPesan
                self.tampilPesan('Data obat berhasil dimasukkan')

                #menampilkan data obat pada tabel menggunakan fungsi tampilDatabase
                self.tampilDataObat()

                #menghapus text pada kotak text
                self.hapusText()
            else:
                #menampilkan pesan menggunakan fungsi tampil obat
                self.tampilPesan('Silahkan isi dan lengkapi data terlebih dahulu !')
        except :
            #menampilkan pesan eror menggunakan fungsi tampilPesan
            self.tampilPesan('Terjadi kesalahan pada entri data obat')

    def tampilDataTerpilih(self):
        # menyimpan detail data obat yang akan dipilih
        data=self.tabelObat.selectedItems()
        if data !=[]:
            nomerBatch=data[0].text ()
            namaObat=data[1].text ()
            kategori=data[2].text ()
            jenis=data[3].text ()
            dosis=data[4].text ()
            stok=data[5].text ()

            #menampilkan detail obat pada kotak text line edit
            self.editNomer.setText(nomerBatch)
            self.editNama.setText(namaObat)
            self.editKategori.setText(kategori)
            self.editJenis.setText(jenis)
            self.editDosis.setText(dosis)
            self.editStok.setText(stok)

    def perbaruiDataObat (self):
        try:
            #menyimpan data yang dimasukkan pada kotak text
            nomerBatch=self.editNomer.displayText()
            namaObat=self.editNama.displayText()
            kategori=self.editKategori.displayText()
            jenis=self.editJenis.displayText()
            dosis=self.editDosis.displayText()
            stok=self.editStok.displayText()

            if nomerBatch!='' and namaObat!='' and kategori!='' and jenis!='' and dosis!='' and stok!='':
                #membuat koneksi ke server MySQL
                con=mysql.connector.connect(host='localhost', user='root', password='p&l4ever', database='dbapotik')

                #memperbarui data Obat
                query= 'UPDATE obat_table SET Nama_Obat=%s, Kategori_obat=%s, Jenis_Obat=%s, Dosis=%s, Stok_Obat=%s WHERE Nomor_Batch=%s'
                data=(namaObat, kategori, jenis, int(dosis), int(stok), int(nomerBatch))
                cursor=con.cursor()
                cursor.execute(query, data)
                con.commit()

                #menutup koneksi
                self.tampilPesan('Data berhasil diperbarui')

                #menampilkan data obat menggunakan fungsi tampilData
                self.tampilDataObat()
            
                #menghapus text pada kotak text
                self.hapusText()
            else:
                #menampilkan pesan menggunakan fungsi tampilPesan
                self.tampilPesan('Silahkan pilih data terlebih dahulu !')
        except:
            #menampilkan pesan eror menggunakan fungsi tampilPesan
            self.tampilPesan('Terjadi kesalahan pada saat pembaruan data')

    def tampilJendelaKonfirmasi(self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setWindowTitle('Konfirmasi')
        msgbox.setText(pesan)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return msgbox.exec()

    def hapusText (self):
        self.editNomer.setText('')
        self.editNama.setText('')
        self.editKategori.setText('')
        self.editJenis.setText('')
        self.editDosis.setText('')
        self.editStok.setText('')

    def hapusDataObat (self):
        try :
            #menyimpan data item
            nomerBatch=self.editNomer.displayText()

            if nomerBatch!='':
                jendela_konfirmasi=self.tampilJendelaKonfirmasi('Apakah anda yakin akan dihapus?')
                if jendela_konfirmasi==QMessageBox.Ok:
                    #menciptakan koneksi ke server MySQL
                    con=mysql.connector.connect(host='localhost', user='root', password='p&l4ever', database='dbapotik')

                    #menghapus data Obat
                    query='DELETE FROM obat_table WHERE Nomor_Batch=%s'
                    data=(nomerBatch,)
                    cursor=con.cursor()
                    cursor.execute(query, data)
                    con.commit()

                    #menutup koneksi
                    con.close()

                    #menampilkan pesan menggunakan fungsi tampilPesan
                    self.tampilPesan('Data berhasil dihapus')

                    #menampilkan data buku menggunakan fungsi tampilDataObat
                    self.tampilDataObat()

                     #menghapus text pada kotak text
                    self.hapusText()

            else:
                #menampilkan pesan menggunakan fungsi tampilPesan
                self.tampilPesan('Silahkan pilih data terlebih dahulu !')
        except:
            #menampilkan pesan menggunakan fungsi tampilPesan
            self.tampilPesan('Terjadi kesalahan saat menghapus data')

    
    def cariDataObat(self):
        try :
            #menyimpan kata kunci
            kata_kunci=self.editKataKunci.displayText()

            #membuat koneksi ke server MySQL
            con=mysql.connector.connect(host='localhost', user='root', password='p&l4ever', database='dbapotik')

            #mencari data Obat berdasarkan kata kunci yang dimasukkan
            query="SELECT * FROM obat_table WHERE Nama_Obat LIKE '%"+kata_kunci+"%'"
            cursor=con.cursor()
            cursor.execute(query)
            data_obat=cursor.fetchall()

            #menutup koneksi
            con.close()

            #menampilkan data pada tabel
            n_dataobat=len(data_obat)
            self.tabelObat.setRowCount(n_dataobat)
            baris=0
        
            for x in data_obat:
                self.tabelObat.setItem(baris, 0, QTableWidgetItem(str(x[0])))
                self.tabelObat.setItem(baris, 1, QTableWidgetItem(x[1]))
                self.tabelObat.setItem(baris, 2, QTableWidgetItem(x[2]))
                self.tabelObat.setItem(baris, 3, QTableWidgetItem(x[3]))
                self.tabelObat.setItem(baris, 4, QTableWidgetItem(str(x[4])))
                self.tabelObat.setItem(baris, 5, QTableWidgetItem(str(x[5])))
                baris=baris+1  
        except:
            #menampilkan pesan menggunakan fungsi tampilPesan
            self.tampilPesan('Terjadi kesalahan saat pencarian data')

if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=Obat()
    form.show()
    sys.exit(app.exec_())

