import os
import subprocess
from pydub import AudioSegment
import sys
import subprocess
from PyQt5.QtCore import QProcess

#class convert_audio(QObject):
def convert_module(mode_format, wav_dir,dir, file_WEP, file_WEN, parent_ext, need_ext ):
    if mode_format == 'AS':
        parent_audio_dir = dir+parent_ext+'/'
        wav_audio = AudioSegment.from_file(parent_audio_dir+file_WEP) # ОТВАЛ
        wav_audio.export(wav_dir+file_WEN, format="wav")
        os.remove(parent_audio_dir+file_WEP) 
        message = file_WEP, "конвертирован в", file_WEN
        status = 1
        return  file_WEN, parent_audio_dir, message, status
    if mode_format == 'SP':
        parent_audio_dir = dir+parent_ext+'/'
        ####### ex why subprocces shell = True dogshit
        #   subprocess.call('echo $HOME')
        #   [Errno 2] No such file or directory
        #
        #   subprocess.call('echo $HOME', shell=True)
        #   /user/khong
        ####### ex why subprocces shell = True dogshit
        subprocess.call(['ffmpeg', '-i', parent_audio_dir+file_WEP, wav_dir+file_WEN], shell=False)
        os.remove(parent_audio_dir+file_WEP) 
        message = file_WEP, "конвертирован в", file_WEN
        status = 1
        return  file_WEN, parent_audio_dir, message, status 

def convert_audio(wav_dir, dir, file_name, ext_parent, ext_for_conv): # Дерево ниже можно так же переписать под унифицированную фукнцию, которая будет подхватывать расширения с листа, где лежат все расширения
    parent_ext =  file_name[-3:].lower()
    need_ext = ext_for_conv.lower()
    ls_dir = os.listdir(dir+parent_ext+'/')
    wav_dir = "C:/Users/"+str(os.getlogin())+"/Desktop/recognition_proj/audio_wav/"
    file_WOE = file_name[:-4] #file without extension
    file_WEP = file_WOE+'.'+parent_ext #file with extation paret
    file_WEN = file_WOE+need_ext ##file with extation need
    if len(ls_dir) >= 1:
        if ls_dir.count(file_name) == 1:
            if ext_parent == '.WMA':
                try:
                    file_WEN, parent_audio_dir, message, status = convert_module('AS', wav_dir, dir, file_WEP, file_WEN, parent_ext, need_ext )
                    return file_WEN, parent_audio_dir, message, status
                except:
                    message = 'Проблема в конвертации '+ parent_ext +' в ' + need_ext
                    status = 0
                    file_WEN, parent_audio_dir = '0', '0'
                    return  file_WEN, parent_audio_dir, message, status
            elif ext_parent == '.mp3':      #CONV MP3 IN WAV
                try:
                    file_WEN, parent_audio_dir, message, status = convert_module('AS',wav_dir,dir, file_WEP, file_WEN, parent_ext, need_ext )
                    return file_WEN, parent_audio_dir, message, status
                except:
                    message = 'Проблема в конвертации '+ parent_ext +' в ' + need_ext
                    status = 0
                    file_WEN, parent_audio_dir = '0', '0'
                    return  file_WEN, parent_audio_dir, message, status
            elif ext_parent == '.aac':      #CONV AAC IN WAV
                try:
                    file_WEN, parent_audio_dir, message, status = convert_module('AS',wav_dir,dir, file_WEP, file_WEN, parent_ext, need_ext )
                    return file_WEN, parent_audio_dir, message, status
                except:
                    message = 'Проблема в конвертации '+ parent_ext +' в ' + need_ext
                    status = 0
                    file_WEN, parent_audio_dir = '0', '0'
                    return  file_WEN, parent_audio_dir, message, status
            elif ext_parent == '.mp4':
                try:
                    file_WEN, parent_audio_dir, message, status = convert_module('AS',wav_dir,dir, file_WEP, file_WEN, parent_ext, need_ext )
                    return file_WEN, parent_audio_dir, message, status
                except:
                    message = 'Проблема в конвертации '+ parent_ext +' в ' + need_ext
                    status = 0
                    file_WEN, parent_audio_dir = '0', '0'
                    return  file_WEN, parent_audio_dir, message, status
    else: 
        file_WEN, parent_audio_dir = '0', '0'
        message = 'Родительская директория для',file_name, "пуста" 
        status = 0
        return message, status, file_WEN, parent_audio_dir




    
    
    