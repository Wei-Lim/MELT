# -*- coding: utf-8 -*-
# !/usr/bin/python3

# Test control on measurement instrument via 
import PySimpleGUI as sg
import pyvisa
import pandas as pd
import pytz
import datetime as dt
import time
import string
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

# PyVISA Resource Manager
rm = pyvisa.ResourceManager()
# Chroma 66202
chroma = rm.open_resource('USB0::0x0A69::0x0835::A66200110997::INSTR')
print(chroma.query("*IDN?"))
chroma.write("SYSTEM:HEADER ON")

# PeakTech 4095
peak = rm.open_resource('USB0::0x5345::0x1234::2101323::INSTR')
print(peak.query("*IDN?"))
peak.query("CONFigure:VOLTage:DC")
time.sleep(1.3)

# GUI
input_column = [
  [sg.Text("Company:")],
  [sg.In("Tridonic", size = (30, 1), enable_events = True, key = "-COMPANY-")],
  [sg.Text("Model:")],
  [sg.In("LC 50W", size = (30, 1), enable_events = True, key = "-MODEL-")],
  [sg.Text("Article number:")],
  [sg.In("-", size = (30, 1), enable_events = True, key = "-ARTNO-")],
  [sg.Text("Output current:")],
  [sg.In("0.30", size = (30, 1), enable_events = True, key = "-CURRENT_OUT-")],
  [
    sg.Button("Measure"), 
    sg.InputText(visible = False, enable_events = True, key = "-FILE_PATH-"),
    sg.FileSaveAs( 
      key = '-FILE_SAVE-', 
      file_types=(('CSV', '.csv'), ('all', '.*')), 
      ), 
    sg.Button("Remove"), 
    sg.Button("Cancel")
  ]
]

## For Table column
data = []
header_list = [
  'Company', 'Model', 'Article number', 'datetime', 
  'I_out', 'U_out', 'P_out', 'P', 'efficiency','PF', 'THD_v'
  ]

## window layout
layout = [
  [
    sg.Column(input_column),
    sg.Table(
      values = data,
      headings = header_list,
      display_row_numbers = False,
      auto_size_columns = False,
      num_rows = min(25, len(data)),
      enable_events = True,
      key = "-table-"
      )
  ]
]

window = sg.Window("Measurement Software", layout)

while True:
  event, values = window.read()
  if event == "Measure":
    ## local PC
    tz = pytz.timezone('Europe/Berlin')
    datetime = dt.datetime.now(tz)
    # User inputs
    company = values['-COMPANY-']
    model = values['-MODEL-']
    article_number = values['-ARTNO-']
    # try converting to float else error message
    I_out = float(values['-CURRENT_OUT-']) # in A

    ## Chroma 66202
    chroma.query("MEASure?")
    P = float(chroma.query("FETCh:POWer:REAL?").split()[1])
    PF = float(chroma.query("FETCh:POWer:PFACtor?").split()[1])
    THD_v = float(chroma.query("FETCh:VOLTage:THD?").split()[1])
    
    ## PeakTech 4095
    U_out = float(peak.query("MEAS1?"))
    P_out = I_out * U_out
    if P > 0:
      efficiency = P_out / P
    else:
      efficiency = 0
    data.append([
      company, model, article_number, datetime, 
      I_out, U_out, P_out, P, efficiency, PF, THD_v
    ])
    window["-table-"].update(
      values = data, 
      num_rows = min(10, len(data))
    )
  if (event == '-FILE_PATH-') and (values['-FILE_PATH-'] != ''):
    print('Saving to:', values['-FILE_PATH-'])
    df = pd.DataFrame(data, columns = header_list)

    s = ''.join(c for c in model if c in valid_chars)
    filename = values['-FILE_PATH-'] + s + "_" + time.strftime(
      "%Y%m%j",
      time.localtime()
      )
    df.to_csv(filename, index = False)
  if (event == "Remove") and (len(an_array) > 0):
    data.pop()
  if (event == "Cancel") or (event == sg.WIN_CLOSED):
    break

window.close()
