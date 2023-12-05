import sys, os, shutil, datetime, pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import * 
from PyQt5.QtGui import QIcon, QFont,  QWindow,  QKeySequence
from PyQt5.QtWidgets import * 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QAction, QMainWindow, QStatusBar, QMenu, QMessageBox, qApp, QListWidget, QListWidgetItem
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 

from convert import convert_audio
from inference import run_inference
from compressor import compressed_audio, voulume_changer
from get_filename import get_filename
from checkers import check_dirs
from checkers import ckeck_subprocces
from checkers import check_model_dir

now = datetime.datetime.now()
time_name = now.strftime("%H.%M")

directry_app_img = 'img/'
model_vosk = 'small'

if model_vosk == "big":
    full_name_model = 'vosk-model-ru-0.42'
if model_vosk == 'small':
    full_name_model = 'vosk-model-small-ru-0.22'
save_result_name = model_vosk+'_model_'

proj_dir = "C:/Users/"+str(os.getlogin())+"/Desktop/recognition_proj/"
dir_audio = proj_dir + "audio_wav/"
recog_txt = proj_dir + "result/"
audio_procces = proj_dir + "audio_procces/"
models_dir = proj_dir + "models/"
ext_mp3, ext_mp4, ext_aac, ext_wma, ext_aac = (audio_procces + "mp3/",
                                                audio_procces + "mp4/",
                                                audio_procces + "aac/",
                                                audio_procces + "wma/",
                                                audio_procces + "aac/")

system_dirs = [proj_dir, dir_audio, audio_procces, 
              models_dir, ext_mp3, ext_mp4,
              ext_aac, ext_wma, recog_txt]
version_app = 0.1
lng = language_msg = 'ru'

#create main directories
def output_words(file):
        file = open(file, "rb")
        data = file.read()
        words = data.split()
        n_of_words = len(words)
        return n_of_words

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(550, 200) # длинна, ширина
        self.move(20,50) # х, у

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                # https://doc.qt.io/qt-5/qurl.html
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def message_windows(self,message,three_button, icon):
        msg = QMessageBox()
        msg.setWindowTitle("Info window")
        if three_button == False:
            msg.setIcon(icon)
        elif three_button == True:
            msg.setStandardButtons(QMessageBox.Yes |  QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            msg.buttonClicked.connect(self.rewrite_file_3btn)
        msg.setText(message)
        x = msg.exec_()
        return x
    
    def rewrite_file_3btn(self, i): #Штука для перезаписи файлов 
        pass
    
    def initUI(self):

        #create main window
        self.setGeometry(500, 500, 900, 500)
        self.setWindowTitle("App speeach_recognition")
        self.setFixedSize(590, 600) # длинна, ширина

        #create drag&drops filed
        self.listbox_view = ListBoxWidget(self) 

        #create background window
        self.setAcceptDrops(True)
        self.setGeometry(500, 500, 440, 280)
        #self.label = QLabel("White", self) 
        # oImage = QtGui.QImage() #os.path.join("C:/Users/"+str(os.getlogin())+"/Desktop/Projects/speech_recognition/img/background1.jpg")
        # sImage = oImage.scaled(QtCore.QSize(440, 280))
        # palette = QtGui.QPalette()
        # palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(sImage))
        # self.setPalette(palette)

        #create debug box
        self.groupBox_2 = QtWidgets.QGroupBox("Поле вывода операций", self)
        self.groupBox_2.setFixedSize(550, 270) 
        self.groupBox_2.move(20,300) #x, y
        
        #create debug- text field 
        self.output_rd = QtWidgets.QTextBrowser(self.groupBox_2)
        self.output_rd.setFixedSize(530, 235) 
        self.output_rd.move(10,20) #x, y
        self.output_rd.setObjectName("output_rd")
        
        ##############################################Buttons
        #######create first buttom
        b_s = [220, 30] #button size
        self.btnOne = QPushButton("Перевести без обработки (TWoP)", self)
        self.btnOne.setFixedSize(b_s[0], b_s[1]) # длинна, ширина
        self.btnOne.move(245,257) #x, y
        self.btnOne.clicked.connect(lambda: print(self.getSelectedForTWoP()))

        ########create two buttom
        self.btnTwo = QPushButton("Перевести с обработкой (TWP)", self)
        self.btnTwo.setFixedSize(b_s[0], b_s[1]) # длинна, ширина
        self.btnTwo.move(20,257) #x, y
        self.btnTwo.clicked.connect(lambda: print(self.getSelectedForTWP()))

        #######create three buttom
        self.btnThree = QPushButton('Конвертировать', self)
        self.btnThree.setFixedSize(b_s[0]-120, b_s[1]) # длинна, ширина
        self.btnThree.move(470,257)  #x, y
        self.btnThree.clicked.connect(lambda: print(self.getSelectedItemConvert()))

        self.onExportButtonClicked.connect(lambda: print(self.getSelectedItemConvert(filename)))
        ##############################################Buttons

        #create navigation bars
        self._createActions()                                            
        self._createMenuBar()                                               
        self._createStatusBar()
        
        ############################################## Checkers 
        #use writing status in statusbar
        status_dirs = check_dirs(system_dirs, lng)
        self.output_rd.append(f"<p style='color:green'>{status_dirs}</p>")
        self.statusbar.showMessage(status_dirs, 3000)
        #chech subprocces acces status
        try:
            status_dirs = ckeck_subprocces()
            self.output_rd.append(f"<p style='color:green'>{status_dirs}</p>")
        except:
            self.output_rd.append(f"<p style='color:red'>{status_dirs +' permission denied subprocces'}</p>")
            return    
        #check model dirs 
        msg = check_model_dir(models_dir+full_name_model)
        self.output_rd.append(f"<p style='color:green'>{msg}</p>")
        self.statusbar.showMessage(msg, 3000)
        ############################################## Checkers

    ######################### Format converter for adding files
    def get_convert(self, dir,ext, ls_fl ,filename):

    
        self.output_rd.append('Начинается конвертация ' +filename+ ' в wav')
        shutil.copyfile(dir, ext+filename)
        self.output_rd.append( f"<p style='color:green'>{'Переместили ' +filename+ ' в рабочую директорию'}</p>")
        self.statusbar.showMessage("Ожидайте", 6000) 
        file_WEN, parent_audio_dir, message, status = convert_audio(wav_dir = dir_audio, dir = audio_procces,file_name = filename, 
                                                    ext_parent = filename[-4:], ext_for_conv = '.wav')
        if status == 1:
            self.statusbar.showMessage("Готово", 6000)
            self.output_rd.append(f"<p style='color:green'>{'Статус ' +str(status)+' - '+str(message)}</p>")
            self.statusbar.showMessage('Статус ' +str(status)+' - '+str(message), 6000)

            self.output_rd.append( f"<p style='color:green'>{'Конвертация прошла успешно'}</p>")
            self.message_windows("Конвертация прошла успешно", False, QMessageBox.Information )
            self.statusbar.showMessage("Конвертация прошла успешно", 6000)  
        else:
            self.output_rd.append(f"<p style='color:red'>{'Статус ' +str(status)+' - '+str(message)}</p>")
            self.message_windows('Статус ' +str(status)+' - '+str(message), False, QMessageBox.Information )

        # if ls_fl.count(filename) == 2:
        #     status_button = self.message_windows("Файл с именем " +filename+ " уже есть в рабочей директории, заменить его?"
        #                                         , True, QMessageBox.Retry | QMessageBox.Cancel)
        #     self.output_rd.append("Файл с именем " +filename+ " уже есть в рабочей поддиректории - " +ext+ " , заменить его?")
        #     yes = 16384
        #     cancel = 4194304 
        #     if status_button == yes:
        #         self.output_rd.append('Нажатие кнопки - Yes')
        #         shutil.copyfile(dir, dir_audio+filename[:-4]+'.wav')
        #         self.output_rd.append( f"<p style='color:green'>{'Переместили ' +filename+ ' в рабочую директорию (с заменой)'}</p>") 
        #         self.statusbar.showMessage("Ожидайте", 6000) 
        #         conv_file_name, conv_dir, message, status = convert_parent_to_need_ext(wav_dir = dir_audio, dir = audio_procces,file_name = filename, 
        #                                                        ext_parent = filename[-4:], ext_for_conv = '.wav')    
        #         self.statusbar.showMessage("Готово", 6000)
        #         self.output_rd.append(f"<p style='color:green'>{'Статус ' +str(status)+' - '+str(message)}</p>")
        #         self.statusbar.showMessage(str(message), 6000)
        #         return conv_file_name, conv_dir
        #     elif status_button == cancel:
        #         self.output_rd.append('Нажатие кнопки - Cancel')
        #         self.output_rd.append("Отмена процедуры")
        #         self.statusbar.showMessage("Отмена процедуры", 6000)
        #         return
        #     else:
        #         self.output_rd.append("Произошла ошибка непредвиденная ошибка, код = 404, Ошибка селектора конвертации")
        #         self.message_windows("Произошла ошибка непредвиденная ошибка, код = 404", False, QMessageBox.Critical)  
        #         self.statusbar.showMessage("Ошибка селектора конвертации", 6000)  
        #         return
        # else:
    ######################### Format converter for adding files

    ######################### Selecter for Add files and convert his
    def getSelectedItemConvert(self):
        
        item = QListWidgetItem(self.listbox_view.currentItem())
        dir = item.text()
 
        if len(dir) == 0 or len(dir) <= 0:
            self.output_rd.append(f"<p style='color:red'>{'Не выбран файл для конвертации, см. вкладку Help content'}</p>")
            self.message_windows("Не выбран файл для конвертации", False, QMessageBox.Information )  
            return
                
        if '.WMA' in dir: # WORKER
            filename = get_filename(dir)
            ls_fl = os.listdir(ext_wma)  
            self.output_rd.append( f"<p style='color:blue'>{dir,ext_wma, ls_fl ,filename}</p>")
            self.get_convert(dir,ext_wma, ls_fl ,filename)

        elif '.mp3' in dir: # WORKER
            filename = get_filename(dir)
            ls_fl = os.listdir(ext_mp3)
            self.output_rd.append( f"<p style='color:blue'>{dir,ext_mp3, ls_fl ,filename}</p>")
            self.get_convert(dir,ext_mp3, ls_fl ,filename)

        elif '.aac' in dir: # WORKER
            filename = get_filename(dir)
            ls_fl = os.listdir(ext_aac)
            self.output_rd.append( f"<p style='color:blue'>{dir,ext_aac, ls_fl ,filename}</p>")
            self.get_convert(dir,ext_aac, ls_fl ,filename)

        elif '.mp4' in dir: # WORKER
            filename = get_filename(dir)
            ls_fl = os.listdir(ext_mp4)
            self.output_rd.append( f"<p style='color:blue'>{dir,ext_mp4, ls_fl ,filename}</p>")
            self.get_convert(dir, ext_mp4, ls_fl ,filename)     

        elif '.wav' in dir:

            file_name = get_filename(dir)
            file = file_name[:-4]+'.wav'
            #self.output_rd.append( f"<p style='color:red'>{'Проверьте рабочие директории, с ними что-то не так'}</p>")
            status_button = self.message_windows("Файл " +file+ " раширения <b>.wav</b> не может быть конвертирован, но его можно переместить в рабочую область, выполнить это? "
                                                ,True, QMessageBox.Yes | QMessageBox.Cancel)
            self.output_rd.append('Перенос в рабочую область файла wav - ' +file)
            yes = 16384
            cancel = 4194304 
            if status_button == yes:
                self.output_rd.append(f"<p style='color:green'>{'Нажатие кнопки - Yes'}</p>") 
                ls_fl = os.listdir(dir_audio)
                if ls_fl.count(file) == 1:
                    status_button = self.message_windows("Файл с этим именем уже есть в рабочей "
                                            "директории, заменить его?", True, QMessageBox.Yes | QMessageBox.Cancel)
                    self.output_rd.append('Встретился файл с таким же именем, заменить его?')
                    yes = 16384
                    cancel = 4194304 
                    if status_button == yes:
                        self.output_rd.append(f"<p style='color:green'>{'Нажатие кнопки - Yes'}</p>") 
                        try:
                            shutil.copyfile(dir, dir_audio+file )
                        except:
                            self.output_rd.append(f"<p style='color:red'>{'Конвертировать файлы одного и того же названия, расширения и расположения нельзя в одинаковую им рабочую директорию. '}</p>")
                            return
                        self.output_rd.append(f"<p style='color:green'>{'Произошла замена ' +file+ ' в рабочей директории'}</p>")
                        self.statusbar.showMessage('Произошла замена ' +file+ ' в рабочей директории', 6000)
                    elif status_button == cancel:
                        self.output_rd.append('Нажатие кнопки - Cancel')
                        self.output_rd.append("Отмена процедуры")
                        self.statusbar.showMessage("Отмена процедуры", 6000)
                        return
                    else:
                        self.output_rd.append("Произошла ошибка непредвиденная ошибка, код = 404, Ошибка селектора конвертации")
                        self.message_windows("Произошла ошибка непредвиденная ошибка, код = 404", False, QMessageBox.Critical)  
                        self.statusbar.showMessage("Ошибка селектора конвертации", 6000) 
                        return
                else:
                    shutil.copyfile(dir, dir_audio+file)
                    self.output_rd.append( f"<p style='color:green'>{'Переместили ' +dir_audio+file+ ' в рабочую директорию(с заменой)'}</p>")
                    self.statusbar.showMessage('Переместили '+file+ ' в рабочую директорию', 6000)
            elif status_button == cancel:
                self.output_rd.append('Нажатие кнопки - Cancel')
                self.output_rd.append("Отмена процедуры")
                self.statusbar.showMessage("Отмена процедуры переноса " +file+ ' в рабочую директорию', 6000)
            else:
                self.output_rd.append("Произошла ошибка непредвиденная ошибка, код = 404, Ошибка селектора конвертации")
                self.message_windows("Произошла ошибка непредвиденная ошибка, код = 404", False, QMessageBox.Critical)  
                self.statusbar.showMessage("Ошибка селектора конвертации", 6000)
        else:
            self.output_rd.append(f"<p style='color:red'>{'Данное расширение файла ' +dir+ ' не может быть конвертировано, см. вкладку Help content'}</p>")
            self.message_windows("Данное расширение не может быть конвертировано, см. вкладку 'Help content'", False, QMessageBox.Critical)  
            self.statusbar.showMessage("Ошибка расширения конвертации", 6000)  
            return
        return dir
    
    ######################### Selecter for Add files and convert his

    ######################### Selecter for trans without processing
    def getSelectedForTWoP(self): # TWP - Transcribe with processing
        item = QListWidgetItem(self.listbox_view.currentItem())
        dir = item.text()
        if len(dir) == 0:
            self.output_rd.append(f"<p style='color:red'>{'Не выбран файл для перевода без обработки (TWoP), см. вкладку Help content'}</p>")
            self.message_windows("Не выбран файл для перевода без обработки (TWoP)", False, QMessageBox.Information )  
            return
        else:
            file_name = get_filename(dir)
            name_for_name = file_name[:-4]+'.wav'
            file = dir_audio+file_name[:-4]+'.wav'
            self.output_rd.append("Начинается процесс перевода файла " +dir+' '+file+ " без обработки.")
            self.statusbar.showMessage("Ожидайте", 6000)
            try:
                now = datetime.datetime.now()
                time_name = now.strftime("%H.%M")
                msg, save_full_name = run_inference(audio =file , model_vosk = model_vosk , save_result_dir = recog_txt, save_result_name = name_for_name+'_'+save_result_name+time_name ) #save_result_name / time_name+'test'+'.txt' 
            except: 
                self.output_rd.append( f"<p style='color:red'>{'Случились проблемы с моделью перевода - ' +full_name_model+ ' перезапустите приложение , либо замените текущую модель в директории: ' +models_dir}</p>")
                return
            
            self.output_rd.append( f"<p style='color:green'>{'Перевод прошла успешно'}</p>")
            self.message_windows("Перевод прошла успешно", False, QMessageBox.Information )
            self.statusbar.showMessage("Перевод прошла успешно", 6000) 
            words = output_words(save_full_name)
            self.output_rd.append('Использована модель: '+full_name_model+ ' ' +str(msg) +' место расположение файла результата: ' +recog_txt+name_for_name+save_result_name+'.txt.')
            self.output_rd.append(f"<p style='color:green'>{'Распознано - ' +str(words)+ ' слов'}</p>")
            self.output_rd.append(f"<p style='color:green'>{'Время перевода: ' +time_name}</p>")
    ######################### Selecter for trans without processing

    ######################### Selecter for trans with processing
    def getSelectedForTWP(self): # TWP - Transcribe with processing
        item = QListWidgetItem(self.listbox_view.currentItem())
        dir = item.text()
        if len(dir) == 0:
            self.output_rd.append(f"<p style='color:red'>{'Не выбран файл для перевода без обработки (TWP), см. вкладку Help content'}</p>")
            self.message_windows("Не выбран файл для перевода с обработкой (TWP)", False, QMessageBox.Information )  
            return
        else:
            compressed = 0
            volumer = 1
            self.message_windows("Обработка аудиозаписи может привести к ухудшению качества распознавания", False, QMessageBox.Information )
            #compressor #########################
            lowpass= 400 
            highpass= 16400
            #volume_changer #########################
            mode = 'p'
            scale = 20
            file_name = get_filename(dir)
            name_for_name = file_name[:-4]
            if compressed == 1:
                self.output_rd.append(f"<p style='color:blue'>{'Происходит обработка компессором'}</p>")
                fo = compressed_audio(dir = dir_audio, fn = name_for_name+'.wav', lowpass= lowpass, highpass= highpass)
                self.output_rd.append(f"<p style='color:blue'>{name_for_name+ ' обработан компрессором на lp - ' +str(lowpass)+ ' hp ' +str(highpass)}</p>")
            else:
                lowpass = 0
                highpass = 0
            if volumer == 1:
                f_v = dir_audio+name_for_name+'.wav'
                self.output_rd.append(f"<p style='color:blue'>{'Происходит смена порога громкости в режиме -' +mode+ ' на ' +str(scale)}</p>")
                try:
                    voulume_changer(file_name = f_v, mode = mode, scale = scale )
                    self.output_rd.append(f"<p style='color:blue'>{name_for_name+ ' изменён порог громкости в режиме - ' +mode+ ' на ' +str(scale)}</p>")
                    file = f_v
                except:
                    self.output_rd.append(f"<p style='color:red'>{'Обрабатываемый файл - ' +file_name+ ' не находится в рабочей директории: ' +dir_audio+ ' , конвертируйте его для переноса в рабочую директорию'}</p>")   
                    return  
            else:
                mode = '0'
                scale = 0
            self.output_rd.append("Начинается процесс перевода " +dir+' '+file+ " c обработкой.")
            self.statusbar.showMessage("Ожидайте", 6000)
            try:
                now = datetime.datetime.now()
                time_name = now.strftime("%H.%M")
                msg, save_full_name = run_inference(audio =file, 
                                    model_vosk = model_vosk, save_result_dir = recog_txt, 
                                    save_result_name = name_for_name+'_compress ls'+str(lowpass)+'_hp'+str(highpass)+'_'+mode+'_'+str(scale)+'_'+save_result_name) #save_result_name / time_name+'test'+'.txt' 
            except:
                self.output_rd.append( f"<p style='color:red'>{'Случились проблемы с моделью перевода - ' +full_name_model+ ' перезапустите приложение , либо замените текущую модель в директории: ' +models_dir}</p>")
                return
            
            self.output_rd.append( f"<p style='color:green'>{'Операциия перевода прошла успешно'}</p>")
            self.message_windows("Операциия перевода прошла успешно", False, QMessageBox.Information )
            self.statusbar.showMessage("Операциия перевода прошла успешно", 6000) 
            words = output_words(save_full_name)
            self.output_rd.append('Использована модель: '+full_name_model+ ' ' +str(msg) +' место расположение файла результата: ' +recog_txt+name_for_name+'_compress ls'+str(lowpass)+'_hp'+str(highpass)+'_'+mode+'_'+str(scale)+'_'+save_result_name+'.txt.')
            self.output_rd.append(f"<p style='color:green'>{'Распознано - ' +str(words)+ ' слов'}</p>")
            self.output_rd.append(f"<p style='color:green'>{'Время перевода: ' +time_name}</p>")
    ######################### Selecter for trans with processing

    ######################### navigation bars
    def _createActions(self):
        #########fileMenu
        self.exitAction = QAction("&Выйти", self)
        self.exitAction.triggered.connect(self.close)
        #
        self.saveLogsWindow = QAction("&ВыгрузкаЛогов", self)
        self.saveLogsWindow.setStatusTip("Сохраняет нижнее окно со статусами выполненных операций")
        self.saveLogsWindow.triggered.connect(self.saveLogs)
        #
        #self.openFile = QAction(QIcon('open.png'), '&Open', self)   
        # self.openFiles = QAction("&Открыть файл", self)
        # self.openFiles.setStatusTip("Открывает файл")
        # self.openFiles.triggered.connect(self.onExportButtonClicked)
        #########fileMenu

        #########helpMenu
        self.helpContentAction = QAction("&Инструкция", self)
        self.helpContentAction.setStatusTip("Последовательные шаги выполнения операция перевода аудиофайлов")
        self.helpContentAction.triggered.connect(self.Helpfull)
        #
        self.aboutContentAction = QAction("&Описание", self)
        self.aboutContentAction.setStatusTip("Показывает информацию - описание приложения")
        self.aboutContentAction.triggered.connect(self.about)
        #########helpMenu

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&Меню", self)
        fileMenu.addAction(self.exitAction)
        fileMenu.addAction(self.saveLogsWindow)
        # fileMenu.addAction(self.openFiles)
        menuBar.addMenu(fileMenu)

        helpMenu = menuBar.addMenu("&Помощь")
        helpMenu.addAction(self.aboutContentAction)   
        helpMenu.addAction(self.helpContentAction)

    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        #self.statusbar.showMessage("Hello StatusBar", 3000)
        self.text_1 = "<h5 style='color: black;'>v "+str(version_app)+"</h5>"
        self.wcLabel = QLabel(f"{self.text_1}")
        self.statusbar.addPermanentWidget(self.wcLabel)         

    def about(self):
        QMessageBox.about(self, "Описание приложения ",
                                "Поддерживаемые форматы: <b>WMA, MP3, ACC, WAV</b>. "
                                "Для перевода аудиофайла в текст необходимо выбрать 2 варианта: "
                                "<b>1. С обработкой</b>, вариант перевода с обработкой имеет алгоритмы изменения загруженного аудиофайла "
                                "для улучшения распознавания текста, механизм обработки аудиофайла на данный момент тестируется и находится в разработке для улучшения стабильности работы приложения. "
                                "<b>2. Без обработки</b>, вариант перевода без обработки не имеет алгоритмов для изменения, то есть аудиофайл с такими параметрами поступает в систему с какими и был загружен. ")
    def Helpfull(self):
         QMessageBox.about(self, "Инструкции ",
                                 "Переместите аудиофайл в <b>Рабочую область</b>, выберите объект в <b>Рабочей области</b>, нажмите кнопку <b>Конвертировать</b> "
                                 "После конвертации и сопутствующего перемещения файла в <b>Рабочую область</b> выберите предпочтительный тип перевода аудио в текст. "
                                 "После каждого действия в окошко описания записывается статус выполненных операция для отслеживания процесса перевода.")
    
    def saveLogs(self):
         QMessageBox.about(self, "Логи ", "Окно сохранения логов")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())

