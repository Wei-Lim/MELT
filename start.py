# -*- coding: utf-8 -*-
# !/usr/bin/python3

# Test control on measurement instrument via 
import PySimpleGUI as sg
import pyvisa
import pandas as pd
import pytz
import datetime as dt

# GUI
input_column = [
  [sg.Text("Model:")],
  [sg.In("LC 50W", size = (30, 1), enable_events = True, key = "-MODEL-")],
  [sg.Text("Article number:")],
  [sg.In("1111", size = (30, 1), enable_events = True, key = "-ARTNO-")],
  [sg.Text("Output current:")],
  [sg.In("0.30", size = (30, 1), enable_events = True, key = "-CURRENT_OUT-")],
  [sg.Button("Measure"), sg.Button("Export"), sg.Button("Cancel")]
]

# For Table column
data = []
header_list = [
  'Model', 'Article number', 'I_out',
  'datetime', 'P', 'PF', 'THD_v'
  ]

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
  if event == "Cancel" or event == sg.WIN_CLOSED:
    break
  if event == "Measure":
    ## local PC
    tz = pytz.timezone('Europe/Berlin')
    datetime = dt.datetime.now(tz)
    # User inputs
    model = values['-MODEL-']
    article_number = values['-ARTNO-']
    # try converting to float else error message
    I_out = float(values['-CURRENT_OUT-']) # in A
    P = 50
    PF = 0.95
    THD_v = 0.07
    
    ## Multimeter
    U_out = 130
    P_out = I_out * U_out

    efficiency = P_out / P
    data.append([model, article_number, I_out, datetime, P, PF, THD_v])
    window["-table-"].update(
      values = data, 
      num_rows = min(10, len(data))
      )
  if event == "Export":
    break

window.close()


rm = pyvisa.ResourceManager()
print(rm.list_resources())

inst = rm.open_resource('USB0::0x0A69::0x0835::A66200110997::INSTR')
print(inst.query("*IDN?"))

inst.write("SYSTEM:HEADER ON")

print(inst.query("MEASure?"))

# User inputs
model = "LC 50"
article_number = "28000680"
I_out = "0.300" # in A

# measurement data
## local PC
tz = pytz.timezone('Europe/Berlin')
datetime = dt.datetime.now(tz)

## Chroma 66202
P = inst.query("FETCh:POWer:REAL?").split()[1]
PF = inst.query("FETCh:POWer:PFACtor?").split()[1]
THD_v = inst.query("FETCh:VOLTage:THD?").split()[1]

P = 50
PF = 0.95
THD_v = 0.07

## Multimeter
U_out = 130
P_out = I_out * U_out

efficiency = P_out / P


data = []
data.append([model, article_number, I_out, datetime, P, PF, THD_v])

df = pd.DataFrame(data, columns = [
    'model', 'article_number', 'I_out',
    'datetime', 'P', 'PF', 'THD_v'
    ])

str(df)
