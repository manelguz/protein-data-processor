import re
import json
import datetime
import os

class AtomMissingException(Exception):
    pass

INPUT_DATA_PATH = "inputs"
FILE_NAME = "1bey.pdb"
MAPPING_FILE_NAME = "mapping.json"
RESULT_PATH = "results"


class PDB(object):
    """
    The PDB object that reads, validates and extractss (H,L) chain protein from pdb files. 
    """
    def __init__(self):
        self.pdb_data = None
        self.attom_data = None
        self.proteins = {"L":[], "H": []}

    def read_file(self, file_path:str):
        """
        Metho to read text file 

        Args:
            file_path (str): The path of the PDB file
        return:
            data(str): The read PDB data from the file
        Raises:
            FileNotFoundError(Exception)
        """

        try:
            with open(file_path, 'r') as file:
                data = file.read()
                self.pdb_data = data
                return data
        except FileNotFoundError:
            raise FileNotFoundError("The PDB file can not be found at {}".format(file_path))
        except Exception as e:
            raise Exception("Unexpected error: {}".format(e))
        
    def get_atom_data_from_pdb(self):
        """
        Methot that gets the lines where the atom data is described

        Class Variables:
            self.pdb_data (str): The read PDB data from the file
            self.atom_data (List): List of each atom data

        """
        self.atom_data = re.findall(r'^ATOM\s+.*$', self.pdb_data, re.MULTILINE)
        
    def check_atom_files(self):
        """
        Method to check that the PDB file contains all required atom types: C, CA, O, N

        Class Variables:
            self.atom_data (List): List of each atom data

        Raises:
            AtomMissingException(Exception)
        """
        # Required atom types
        REQ_ATOMS = ["C", "CA", "O", "N"]
        for atom in self.atom_data:
            # Get atom type of the line and check if is in the list of required atom types
            atom_type = re.findall(r'^ATOM\s+\d+\s+(\w+)\s+', atom)[0]
            if atom_type in REQ_ATOMS:
                # If the atom type is included, we will not look for it any longer.
                REQ_ATOMS.remove(atom_type)
                if not REQ_ATOMS:
                    # Ones check all the atom types we are done in the fn
                    return True
        raise AtomMissingException("The file does not has the following atom types: {}".format(" ".join(REQ_ATOMS)))

    def read_mapping(self, mapping_file_path:str):
        """
        Read the json mapping file

        Args:
            mapping_file_path (str): The path of the mapping file
        """
        try:
            with open(mapping_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError("The mapping file can not be found at {}".format(mapping_file_path))
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Error: The file {} contains invalid JSON.".format(mapping_file_path))

    def extract_hl_protein_chain(self):
        """
        Extract H and L protein chains from the validated PDB file.
        Retrieve the values from column 4 for the respective chains and remove duplicate values

        Class Variables:
            self.atom_data (List): List of each atom data
            self.proteins (Dict): Dictionary to store the chain protein data
        """

        chain_abrevation_mapper = self.read_mapping(os.path.join(INPUT_DATA_PATH, MAPPING_FILE_NAME))
        for atom in self.atom_data:
            # Get the protein data and type for each atom
            protein_chain, protein_type = re.findall(r'^ATOM\s+\d+\s+\w+\s+(\w+)\s+(\w+)\s+', atom)[0]
            # Store it in dict
            protein_chain_mapped = chain_abrevation_mapper[protein_chain]
            self.proteins[protein_type].append(protein_chain_mapped)
        # Now remove duplicates
        for protein_type in self.proteins.keys():
            ## Use this inseted of set to keep the order
            self.proteins[protein_type] = list(dict.fromkeys(self.proteins[protein_type]))
        return self.proteins

    def write_chain_to_json(self, file_name:str, output_file_path:str):
        """
        Write the protein data into a file

        Args:
            file_name (str): File name path
            output_file_path (str): Output file path

        Class Variables:
            self.proteins (Dict): Dictionary to store the chain protein data
        """
        
    
        metadata = {
            "Protein ID / Filename": file_name,
            "Processing Date and Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Extracted Chains": {
                "H": {
                    "Acids": "".join(self.proteins["H"]),
                    "Length": len(self.proteins["H"])
                },
                "L": {
                    "Acids": "".join(self.proteins["L"]),
                    "Length": len(self.proteins["L"])
                }
            }
        }
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)
        
        print(f"Metadata saved to {output_file_path}")


if "__main__" == __name__:
    pdb = PDB()
    pdb.read_file(os.path.join(INPUT_DATA_PATH, FILE_NAME))
    pdb.get_atom_data_from_pdb()
    pdb.check_atom_files()
    pdb.extract_hl_protein_chain()
    file_name = FILE_NAME.split(".")[0]
    pdb.write_chain_to_json(file_name, os.path.join(RESULT_PATH, file_name + ".json"))
