import time
import pyaudio
import os
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import wave
import sys
import json

def recog_vosk5(audio,model, frame_rate, save_result_dir, save_result_name):
    SetLogLevel(0)
    # Проверяем наличие модели
    if not os.path.exists(model):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)
    
    CHANNELS=1
    print('Load lodel:')
    try:
        model = Model(model)
    except:
        print('Модель не может быть подргужена')
    
    rec = KaldiRecognizer(model, frame_rate)
    rec.SetWords(True)
    print('Inference processing')
    try:
        wav = AudioSegment.from_file(file = audio, format = "wav") 
        wav = wav.set_channels(CHANNELS)
        wav = wav.set_frame_rate(frame_rate)
    except:
        print('аудио не может быть подгружено')

    rec.AcceptWaveform(wav.raw_data)
    result = rec.Result()
    text = json.loads(result)["text"]
    save_full_name = save_result_dir+save_result_name+'.txt'
    with open(save_full_name, 'w+', encoding='utf-8') as f: #в 100% идёт запись, w лучше не менять
        json.dump(text,f, ensure_ascii=False, indent=1)
        return save_full_name
        
def run_inference(audio, model_vosk, save_result_dir, save_result_name):
    if model_vosk == 'small':
        start = time.time()
        frame_rate = 44100 #def 44000
        try:
            save_full_name = recog_vosk5(audio, "C:/Users/"+str(os.getlogin())+"/Desktop/recognition_proj/models/vosk-model-small-ru-0.22", frame_rate, save_result_dir, save_result_name)
        except:
            msg = 'Модель не может быть подгружена run_inference' 
            end = time.time() - start 
            return msg, save_full_name

        end = time.time() - start 
        msg = 'Время обработки данных:', end
        return msg, save_full_name

    elif model_vosk == 'big':
        start = time.time()
        frame_rate = 18200 #def 16600
        try: 
            save_full_name = recog_vosk5(audio, 'C:/Users/'+str(os.getlogin())+"/Desktop/recognition_proj/models/vosk-model-ru-0.42", frame_rate, save_result_dir, save_result_name)
        except:
            msg = 'Модель не может быть подгружена run_inference' 
            end = time.time() - start 
            return msg, save_full_name
        end = time.time() - start 
        msg = 'Время обработки данных:', end
        return msg, save_full_name

    elif model_vosk == 'big_0.52':
        block = 1
        if block == 0:
            start = time.time()
            frame_rate = 16600
            save_full_name = recog_vosk5(audio, 'models/vosk-model-ru-0.52', frame_rate, save_result_dir, save_result_name)
            end = time.time() - start 
            msg = 'Время обработки данных:', end
            return msg, save_full_name
        else:
            print('Model in work, its blocked')