#Author MU
#Wavefrom aqcuisition from tektro oscilloscope
#from documentation : https://www.pyvisa.org/docs/tektronix-instruments

import os
import test_connexion as tc
import tek_aqui as ta
from utils import graph_utils as gu
from utils import files_utils as fu

# === VAR ===
On_channels=[1]
Acq_time_range=1e-3
Acq_Y_range=1
Acq_sample_rate= None
Trig_channel=1
Trig_level=0
Acq_channel=1
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
scope=tc.scope_init()
print("Connected to " + str(scope))

ta.encod(scope)

ta.acqui_conf(scope,On_channels,Acq_time_range,Acq_Y_range,Acq_sample_rate)

ta.trig_conf(scope,Trig_channel,Trig_level)

Lx,Ly = ta.wavefrom_acqui(scope,Acq_channel,Acq_timeout)
M=[[Lx,Ly]]
tc.close(scope)

gu.multigraph(M,Path,Graph_Repo,Fig_name,Y_axe,X_axe,Y_min,Y_max,X_min,X_max)
print(f"graphs saved to {Path}/{Graph_Repo}")

fu.save_tuple_csv(Lx,Ly,Path,Data_Repo,Data_name)
print(f"data saved to {Path}/{Data_Repo}")
