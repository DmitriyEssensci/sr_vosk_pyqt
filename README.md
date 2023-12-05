# sr_vosk_pyqt
Project speech recognition with pyqt base
import os
import subprocess
import shutil


cd_on_desktop = 'cd C:/Users/DmitriyEssensci/Desktop &'
git_clone = 'git clone https://github.com/DmitriyEssensci/sr_vosk_pyqt.git'
cd_in_git_proj = 'C:/Users/DmitriyEssensci/Desktop/sr_vosk_pyqt/'
istall_venv = 'python -m venv .venv'
commant_requirements = 'pip install -r requirements.txt'
activate_venv = '.venv\Scripts\activate'
#create_txt = 'echo "pyinstaller -D --workpath --clean --add-data 'img:img' --hidden-import FileDialog --noupx run.py" > deploy_app.txt'


def create_sys_folder():
    ls_dirs = ['описание', 'models', 'modules', 'img', 'test_audio']
    for dir in ls_dirs:
        os.mkdir(dir)

def unzip_all_archives():
    ls_zips = ['ffmpeg-master-latest-win64-gpl', 'vosk-model-ru-0.42', 'vosk-model-small-ru-0.22']
    cd_download = 'cd C:/Users/DmitriyEssensci/Download/'
    subprocess.call(cd_download)
    com_unzip = 'tar -xf'
    for zip in ls_zips:
        subprocess.call(com_unzip+zip+'.zip')
        shutil.move(cd_download+zip, 'C:/Users/DmitriyEssensci/Desktop/sr_vosk_pyqt/models/' )

def deploy_app():
    com_deploy = 'pyinstaller -D --workpath --clean --add-data "img:img" -i "img/icon.ico" --hidden-import FileDialog --noupx run.py'
    'pyinstaller -D -y --clean --add-data "img:img" --hidden-import FileDialog --noupx run.py'
    subprocess.call(com_deploy)

# #subprocess.call(cd_on_desktop+git_clone)
# subprocess.call(git_clone)
# # subprocess.call(cd_in_git_proj)
# # subprocess.call(commant_requirements)
# # subprocess.call(istall_venv)
# # subprocess.call(activate_venv)
# # shutil.move('deploy_app.txt', 'описание/deploy_app.txt')
# # shutil.move('icon.ico', 'img/icon.ico')
# # shutil.move('my_wav.wav', 'test_audio/my_wav.wav')
# # create_sys_folder()
# # unzip_all_archives()
# deploy_app()
