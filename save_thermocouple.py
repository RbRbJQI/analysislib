from labscript_utils import import_or_reload
from lyse import *
import pandas as pd
from labscriptlib.RbRb.shared.read_thermocouple import receiving_teensy, open_channel, close_channel

'''

save thermocouples

'''
Is_save = False
temperture_list = []
with h5py.File(path,'r') as h5_file:
    try:
        temperture_list = h5_file['results']['save_thermocouple'].attrs['temperture_list']
    except Exception as e:
        Is_save = True
        ser = open_channel()
        temperture_list = receiving_teensy(ser)
        close_channel(ser)

if Is_save:
    run = Run(path)
    run.save_result('temperture_list', temperture_list)

print("Shot temperature: ",temperture_list)