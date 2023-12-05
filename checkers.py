import os
import subprocess
import sys

def ckeck_subprocces():
    out = subprocess.call(['pip','--version'])
    status_subprocces = 'permission subprocces: ', len(str(out))
    return status_subprocces

def check_model_dir(model_dir):
    if os.path.isdir(model_dir):
        file_size = os.path.getsize(model_dir)
        msg = "Директория " +model_dir + " существует"
        return msg
    else:
        msg = "Директория " +model_dir+ " не существует, загрузите модель в рабочую директорию - " +model_dir
        return msg
    
def check_dirs(dir,lng):
    for i in dir:
        if os.path.isdir(i):
            if lng=='en':
                msg = 'Main directories already exist'
            elif lng=='ru': 
                msg = 'Базовые директории существуют'
            print("Ae - " + i)
        else:
            os.mkdir(i)
            if lng=='en':
                msg = 'Main directories was created'
            elif lng=='ru':
                msg = 'Базовые директории были созданы'
                
            print("Cr - " + i)
    return msg