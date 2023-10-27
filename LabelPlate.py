import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import shutil
from PercetProgressBar import PercentProgressBar

image_path="D:/data/test_labelplate0"

def init_listview(image_path,listview:QListWidget):
    # image_list = []
    for filename in os.listdir(image_path):
        # image_list.append(os.path.join(image_path,filename))
        path_tmp = os.path.join(image_path,filename)
        listview.addItem(QListWidgetItem(path_tmp))



    


class LabelPlateView(QWidget):
    def __init__(self,*args, **kwargs):
        super(LabelPlateView, self).__init__(*args, **kwargs)
        self.resize(800,600)
        self.plateNumberLabel = QLabel(self)
        self.plateNumberLabel.setText("车牌号：")
        self.line = QLineEdit(self)
        
        self.line.move(75,540)
        self.line.resize(200,32)
        self.plateNumberLabel.move(20,550)
        self.listWidget=QListWidget(self)
        self.listWidget.resize(380,150)
        self.listWidget.move(400,410)
        
        self.openfolder_line=QLineEdit(self)
        self.savefolder_line=QLineEdit(self)
        self.openfolder_line.resize(int(self.openfolder_line.width()*2),self.openfolder_line.height())
        self.savefolder_line.resize(int(self.savefolder_line.width()*2),self.savefolder_line.height())

        self.openfolder_line.move(20,410)
        self.savefolder_line.move(20,460)

        self.auto_save_checkbox=QCheckBox(self)
        self.auto_save_checkbox.setText("Auto_Save")
        self.auto_save_checkbox.move(280,503)
        self.auto_save_checkbox.setChecked(True)


        self.progressbar=PercentProgressBar(self)
        self.progressbar.move(300,400)
        self.progressbar.value=0
        # self.listWidget.clicked.connect(self.get_selected_image)
        self.openfolder=""
        self.savefolder=""
        # self.openfolder=QFileDialog.getExistingDirectory(self,"选择数据路径")
        # self.savefolder=QFileDialog.getExistingDirectory(self,"选择保存路径")
        self.image_format="jpg"
        if self.savefolder!="":
            init_listview(self.openfolder,self.listWidget)
            self.image_number=self.listWidget.count()
            self.cur_image_index=0
            self.listWidget.setCurrentRow(self.cur_image_index)
            self.progressbar.value=int((self.cur_image_index+1.0)/self.image_number*100)
            self.progressbar.update()
            self.cur_path=self.listWidget.currentItem().text()
            self.plate_num=self.cur_path.split('\\')[-1].split('.')[0]
            self.image_format="."+self.cur_path.split('\\')[-1].split('.')[1]
            self.line.setText(self.plate_num)
            self.image=QLabel(self,pixmap=QPixmap(self.cur_path))
            self.image.move(200,100)

        
        
        
        
        self.next_bn=QPushButton("下一张",self)
        self.pre_bn=QPushButton("上一张",self)
        self.next_bn.move(110,500)
        self.pre_bn.move(20,500)

        self.open_bn=QPushButton("打开目录",self)
        self.save_bn=QPushButton("保存目录",self)

        self.open_bn.move(225,415)
        self.save_bn.move(225,465)

        self.saveimage_bn=QPushButton("保存",self)
        self.saveimage_bn.move(200,500)

        self.next_bn.clicked.connect(self.onClicked_next)
        self.pre_bn.clicked.connect(self.onClicked_pre)
        self.open_bn.clicked.connect(self.open_folderDialog)
        self.save_bn.clicked.connect(self.save_folderDialog)
        self.saveimage_bn.clicked.connect(self.onClicked_saveimage)    


        self.listWidget.clicked.connect(self.set_cur_platenumber_onlistchange)




    def onClicked_next(self):
        if self.openfolder!="":
            if self.auto_save_checkbox.isChecked():
                self.onClicked_saveimage()
            if self.cur_image_index>=self.image_number-1:
                self.cur_image_index=self.image_number-1
            else:
                self.cur_image_index+=1

            self.progressbar.value=int((self.cur_image_index+1.0)/self.image_number*100)
            self.progressbar.update()
            self.listWidget.setCurrentRow(self.cur_image_index)
            self.cur_path=self.listWidget.currentItem().text()
            self.plate_num=self.cur_path.split('\\')[-1].split('.')[0]
            self.line.setText(self.plate_num)
            self.image_format="."+self.cur_path.split('\\')[-1].split('.')[1]
            self.image.clear()
            self.image=QLabel(self,pixmap=QPixmap(self.cur_path))
            self.image.move(200,100)
            self.image.show()
            

    def onClicked_pre(self):
        if self.openfolder!="":
            if self.cur_image_index==0:
                self.cur_image_index=0
            else:
                self.cur_image_index-=1
            self.progressbar.value=int((self.cur_image_index+1.0)/self.image_number*100)
            self.progressbar.update()
            
            self.listWidget.setCurrentRow(self.cur_image_index)
            self.cur_path=self.listWidget.currentItem().text()
            self.plate_num=self.cur_path.split('\\')[-1].split('.')[0]
            self.line.setText(self.plate_num)

            self.image_format="."+self.cur_path.split('\\')[-1].split('.')[1]
            self.image.clear()
            self.image=QLabel(self,pixmap=QPixmap(self.cur_path))
            self.image.move(200,100)
            self.image.show()
  
            


    def onClicked_saveimage(self):
        if self.savefolder!="":
            cur_save_path=os.path.join(self.savefolder,self.line.text())+"."+self.image_format
            print(cur_save_path)
            shutil.copy(self.cur_path,cur_save_path) 
            
        
    def set_cur_platenumber_onlistchange(self):
        self.cur_image_index=self.listWidget.currentRow()
        # print(self.cur_image_index)
        self.progressbar.value=int((self.cur_image_index+1.0)/self.image_number*100)
        self.progressbar.update()

        self.cur_path=self.listWidget.currentItem().text()
        self.plate_num=self.cur_path.split('\\')[-1].split('.')[0]
        self.line.setText(self.plate_num)
        self.image.clear()
        self.image=QLabel(self,pixmap=QPixmap(self.cur_path))
        self.image.move(200,100)
        self.image.show()


    def open_folderDialog(self):
        self.openfolder=QFileDialog.getExistingDirectory(self,"选择数据路径")
        self.openfolder_line.setText(self.openfolder)
        init_listview(self.openfolder,self.listWidget)
        self.image_number=self.listWidget.count()
        self.cur_image_index=0
        self.listWidget.setCurrentRow(self.cur_image_index)
        self.cur_path=self.listWidget.currentItem().text()
        self.plate_num=self.cur_path.split('\\')[-1].split('.')[0]
        self.line.setText(self.plate_num)
        self.image=QLabel(self,pixmap=QPixmap(self.cur_path))
        self.image.move(200,100)
        self.image.show()
    
    def save_folderDialog(self):
        self.savefolder=QFileDialog.getExistingDirectory(self,"选择保存路径")
        self.savefolder_line.setText(self.savefolder)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w=LabelPlateView()
    w.setWindowTitle("LabelPlate")
    w.show()
    sys.exit(app.exec_())