import pandas as pd
from pypif import pif
from pypif.obj import *

class Ingester():
    """
    Data ingester class that serves as a middle man storage point for raw data
    files and the PIF class. Can add in file specific methods to ingest data
    files and convert the subsequent dataframes into PIF
    """
    
    def __init__(self, path=None):
        """
        Constructor
        
        :param path: string leading to directory where data is stored
        
        :rtype: Ingester Object
        """
        self.properties = None
        self.frequencies = None
        self.elements = None
        self.path = path
        self.pif = ChemicalSystem()
        
            
    def qm9_ingest(self):
        """
        Ingest method that will iterate through the file and fill in the 
        properties and elements attribute.
        
        :rtype: None
        """
        properties = [["tag", 
                       "id", 
                       "Rotational Constant (A)", 
                       "Rotational Constant(B)", 
                       "Rotational Constant(C)", 
                       "Dipole Movement", 
                       "Isotropic polarizability",
                       "Energy of HOMO", 
                       "Energy of LUMO", 
                       "Gap (e_lumo-e_homo)", 
                       "Electronic Spatial Constant", 
                       "Zero Point Vibrational Energy", 
                       "Internal Energy at 0K", 
                       "Interal Energy at 298.15K", 
                       "Enthalpy at 298.15K", 
                       "Free Energy at 298.15K", 
                       "Heat Capacity at 298.15K"],
                      ["Element", 
                       "x", 
                       "y", 
                       "z", 
                       "Mulliken partial charge"],
                      ["GDP-17", 
                       "B3LYP"],
                      ["Corina", 
                       "B3LYP"]]
        units = [["", 
                  "", 
                  "GHz", 
                  "GHz", 
                  "GHz", 
                  "D", 
                  "a^3", 
                  "Ha", 
                  "Ha", 
                  "Ha", 
                  "a^2", 
                  "Ha", 
                  "Ha", 
                  "Ha", 
                  "Ha", 
                  "Ha", 
                  "cal/mol*K"],
                 ["", 
                  "Angstroms", 
                  "Angstroms", 
                  "Angstroms", 
                  "e"],
                 ["", ""],
                 ["", ""]]
                
        with open(self.path, 'r') as f:
            content = f.read()
            lines = content.rsplit('\n')
            number_elements = int(lines[0])
            system_property = properties[0] + properties[2] + properties[3]
            unit = units[0] + units[2] + units[3]
            values = lines[1].split() + lines[number_elements+3].split() + lines[number_elements+4].split()
            self.properties = pd.DataFrame(data=[system_property, values, unit], 
                                           index=["property", "value", "unit"]).transpose()
            
            elements = [lines[x+2].split() for x in range(number_elements)]
            self.elements = pd.DataFrame(data=elements, 
                                         columns=["Element", "x", "y", "z", "Mulliken Partial Charge"])
            self.elements.loc[number_elements] = ["", "Angstrom", "Angstrom", "Angstrom", "e"]

            frequencies = [lines[number_elements+2].split(), len(lines[number_elements+2].rsplit("\t"))*["cm^-1"]]
            self.frequencies = pd.DataFrame(data=frequencies, 
                                            index=["value", "unit"]).transpose()

    def df_to_PIF(self):
        """
        Method to transform a dataframe into a PIF. This is specific to the QM9
        data set. Will create a .json file for each molecule in a separate 
        'pif' folder.
        
        :rtype: None
        """
        self.pif.chemical_formula = self.properties.iloc[20]["value"].rsplit("/")[1]
        
        all_properties = self.to_array_of_Objects(self.properties)
        all_properties.append(Property(name="Harmonic Vibrational Frequency", values=self.frequencies["value"].values, unit ="cm^-1"))
        self.pif.properties = all_properties
        
        self.pif.subsystems = self.to_array_of_Systems(self.elements)
            
        
    def to_array_of_Objects(self, data):
        """
        Given a dataframe containing columns: "property", "value", and "unit", 
        Will return Property[]. Dataframe simply needs columns in that order,
        not necessarily with the exact column names.
        
        :rtype: Property[]
        """
        properties = []
        for index, row in data.iterrows():
            properties.append(Property(name=row.iloc[0], scalars=row.iloc[1], units=row.iloc[2]))
        return properties
    
    def to_array_of_Systems(self, data):
        units = data.tail().values
        print(units)
        
        return 
        

        
            
            
            
        
        