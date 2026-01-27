#Author MU
#Wavefrom aqcuisition from tektro oscilloscope
#from documentation : https://www.pyvisa.org/docs/tektronix-instruments

import os
import test_connexion as tc
import tek_aqui as ta
from utils import graph_utils as gu
from utils import files_utils as fu

# === VAR ===
On_channels=[1,2,3,4]
Acq_time_range=25e-6
Acq_Y_range=1
Acq_sample_rate= None
Trig_channel=1
Trig_level=0
Acq_channel=[2,3,4]
Acq_timeout=10

# = GRAPH =
Path = os.getcwd()
Graph_Repo = "graph_oscillo"
Fig_name = ["Acqui_oscillo"]
Y_axe = ["Tension"]
X_axe = ["temps"]
Y_min = None
Y_max = None
X_min = None
X_max = None

# = DATA =
Data_Repo = "data"
Data_name = "rec.csv"

# === VAR ===

# === RUN ===
rm = tc.open_rm()
try :
    scope = tc.scope_init(rm)

    ta.encod(scope)

    ta.acqui_conf(scope,On_channels,Acq_time_range,Acq_Y_range,Acq_sample_rate)

    ta.trig_conf(scope,Trig_channel,Trig_level)

    Lx,My = ta.wavefrom_acqui_multich(scope,Acq_channel,Acq_timeout)
    
finally :
    tc.close(scope,rm)

print(len(Lx))
for i in range(len(Acq_channel)):
    print(len(My[i]))

fu.save_mult_csv(Lx,My,Path,Data_Repo,Data_name)