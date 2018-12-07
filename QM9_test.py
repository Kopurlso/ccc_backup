"""
Example script to run that will process process the subset of data files 
assumed to be in the data subdirectory and output a resulting .json file in the
results folder. 
"""

import Ingester as ig
from tkinter import filedialog

"""
The 'names' array is designed to split the data files into subcategories for
easier storage and identification.
The 'column_names' nested array contains data names for each data entry of the 
'names' array.
The 'path' is set assuming all data is in the data subdirectory.
"""
names = ["Scalar Properties", 
         "Element Types", 
         "Harmonic Frequencies",
         "SMILES", 
         "InChI"]
column_names = [["tag", "id", "A", "B", "C", "mu", "alpha", "e_homo", "e_lumo", "e_gap", "<R^2>", "zpve", "U_o", "U", "H", "G", "C_v"],
                ["id", "Element", "x", "y", "z", "Mulliken partial charge"],
                ["id"],
                ["id", "GDP-17", "B3LYP"],
                ["id", "Corina", "B3LYP"]]

filenames = filedialog.askopenfilenames()

test = None

for file_path in filenames:
    QM9_Ingester = ig.Ingester(file_path)
    QM9_Ingester.qm9_ingest()
    QM9_Ingester.df_to_PIF()
#    print(QM9_Ingester.data)
        
#print(QM9_Ingester.data)
#QM9_Ingester.qm9_ingest()
#print(QM9_Ingester.data)
#QM9_Ingester.qm9_df_to_PIF()

