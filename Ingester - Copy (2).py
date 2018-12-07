import pandas as pd
import os 
from pypif import pif
from pypif.obj import *

class Ingester():
    """
    Data ingester class that serves as a middle man storage point for raw data
    files and the PIF class. Can add in file specific methods to ingest data
    files and convert the subsequent dataframes into PIF
    """
    
    def __init__(self, names=None, column_names=None, path=None):
        """
        Constructor
        
        :param names: a string or array of strings representing the names of
        dataframes used to store data (optional, is implemented for easier
        tracking)
        :param column_names: an array or nested array containing the column
        names for the dataframes used to store data
        :param path: string leading to directory where data is stored
        
        :rtype: Ingester Object
        """
        self.data = {}
        self.path = path
        
        if isinstance(names, str) & isinstance(column_names, list):
            self.data[names] = pd.DataFrame(columns=column_names)
        elif isinstance(names, list) & isinstance(column_names, list) & (len(names) == len(column_names)):
            for i in range(len(names)):
#                self.data[names[i]] = pd.DataFrame()
                self.data[names[i]] = pd.DataFrame(columns=column_names[i])
        else: 
            raise TypeError("Type or length of inputs does not match the specificed specs")
            
    def qm9_ingest(self):
        """
        Ingest method that will iterate through the files located in the path 
        and fill in the data attribute. This method has been made specific to
        the data files from the QM9 set.
        
        :rtype: None
        """
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in [os.path.join(self.path, f) for f in filenames if f.endswith(".xyz")]:
                with open(filename, 'r') as f:
                    content = f.read()
                    lines = content.rsplit('\n')
                    number_elements = int(lines[0])
                    element_id = lines[1].split()[1]
                    self.data["Scalar Properties"] = self.data["Scalar Properties"].append(pd.DataFrame([lines[1].split()], columns=list(self.data["Scalar Properties"])), ignore_index=True)
                    for x in range(number_elements):
                        self.data["Element Types"] = self.data["Element Types"].append(pd.DataFrame([[element_id] + lines[2 + x].split()], columns=list(self.data["Element Types"])), ignore_index=True)
                    print([[element_id] + lines[number_elements + 2].split()])
                    print(['id'] + list(range(1, len(lines[number_elements + 2]) + 1)))
                    self.data["Harmonic Frequencies"] = self.data["Harmonic Frequencies"].append(
                            pd.DataFrame([[element_id] + lines[number_elements + 2].split()], 
                                          columns=['id'] + list(range(1, len(lines[number_elements + 2].split()) + 1))), ignore_index=True, sort=True)
                    self.data["SMILES"] = self.data["SMILES"].append(pd.DataFrame([[element_id] + lines[number_elements+3].split()], columns=list(self.data["SMILES"])), ignore_index=True)
                    self.data["InChI"] = self.data["InChI"].append(pd.DataFrame([[element_id] + lines[number_elements + 4].split()], columns=list(self.data["InChI"])), ignore_index=True)
                    
    
    def qm9_df_to_PIF(self):
        """
        Method to transform a dataframe into a PIF. This is specific to the QM9
        data set. Will create a .json file for each molecule in a separate 
        'pif' folder.
        
        :rtype: None
        """
        for x in self.data["Scalar Properties"]["id"].unique():
            chemical_system = ChemicalSystem()
#            chemical_system.uid = self.data["Scalar Properties"].loc[x].values[]
#            chemical_system.chemicalFormula = 
            
            
            
        
        