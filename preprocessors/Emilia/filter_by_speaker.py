import argparse
import numpy as np
import os, glob, sys
import pandas as pd

from utils.tool import (
    export_to_wav,
    load_cfg,
    get_audio_files,
    detect_gpu,
    check_env,
    calculate_audio_stats,
)
from utils.logger import Logger, time_logger
# from models import separate_fast, dnsmos, whisper_asr, silero_vad
from natsort import natsorted


results_dir = '/workspace/Amphion/preprocessors/Emilia/raws_processed/'
os.chdir(results_dir)
folders = glob.glob('*')

for folder in folders:
    try:
        os.chdir(results_dir)
        os.chdir(folder)
        print(folder)
        json_file = glob.glob('*.json')[0]
        df = pd.read_json(json_file)
        # make output directories
        # get filenames in order
        wav_files = glob.glob('*.wav')
        mp3_files = glob.glob('*.mp3')
        
        if len(mp3_files) == 0:
            files = wav_files
        else:
            files = mp3_files
        
        files = natsorted(files)
        # add filename column to df
        df['filename'] = files
        speakers = df.speaker.unique()
        for speaker in speakers:
            os.makedirs(speaker, exist_ok=True)
        # now go line by line and copy the data into the right folder
        speakers = df.speaker.values
        
        fns = []
        for idx in range(len(speakers)):
            fn = speakers[idx] +'/'+files[idx]
            os.rename(files[idx], fn)
            fns.append(fn)
    
        df['filename'] = fns
        df.to_csv('metadata.csv', sep='|')
    except:
        print(f'something went wrong with {folder}')