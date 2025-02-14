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

def read_file(file_path:str):
    """
    Function to read text file 

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
            return data
    except FileNotFoundError:
        raise FileNotFoundError("The PDB file can not be found at {}".format(file_path))
    except Exception as e:
        raise Exception("Unexpected error: {}".format(e))
    
def get_atom_data_from_pdb(pdb_data:str):
    """
    Get the lines where the atom data is described

    Args:
        pdb_data (str): The read PDB data from the file

    Returns:
        atom_data(List): list of each atom data 
    """
    atom_data = re.findall(r'^ATOM\s+.*$', pdb_data, re.MULTILINE)
    return atom_data
    
def check_atom_files(atom_data: list):
    """
    Method to check Check that the PDB file contains all required atom types: C, CA, O, N

    Args:
        atom_data (list): list of each atom data  
    Raises:
        AtomMissingException(Exception)
    """
    # Required atom types
    REQ_ATOMS = ["C", "CA", "O", "N"]
    for atom in atom_data:
        # Get atom type of the line and check if is in the list of required atom types
        atom_type = re.findall(r'^ATOM\s+\d+\s+(\w+)\s+', atom)[0]
        if atom_type in REQ_ATOMS:
            # If the atom type is included, we will not look for it any longer.
            REQ_ATOMS.remove(atom_type)
            if not REQ_ATOMS:
                # Ones check all the atom types we are done in the fn
                return True
    raise AtomMissingException("The file does not has the following atom types: {}".format(" ".join(REQ_ATOMS)))

def read_mapping(mapping_file_path:str):
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

def extract_hl_protein_chain(atom_data:list):
    """
    Extract H and L protein chains from the validated PDB file.
    Retrieve the values from column 4 for the respective chains and remove duplicate values

    Args:
        atom_data (list): list of each atom data 
    """
    proteins = {"L":[], "H": []}
    chain_abrevation_mapper = read_mapping(os.path.join(INPUT_DATA_PATH, MAPPING_FILE_NAME))
    for atom in atom_data:
        # Get the protein data and type for each atom
        protein_chain, protein_type = re.findall(r'^ATOM\s+\d+\s+\w+\s+(\w+)\s+(\w+)\s+', atom)[0]
        # Store it in dict
        protein_chain_mapped = chain_abrevation_mapper[protein_chain]
        proteins[protein_type].append(protein_chain_mapped)
    # Now remove duplicates
    for protein_type in proteins.keys():
        proteins[protein_type] = set(proteins[protein_type])
    return proteins

def write_chain_to_json(file_name:str, proteins:dict, output_file_path:str):
    """
    Write the protein data into a file

    Args:
        file_name (str): File name path
        chain_H (list): List of H chain embeding
        chain_L (list): List of L chain embeding
        output_file_path (str): Output file path
    """
   
    metadata = {
        "Protein ID / Filename": file_name,
        "Processing Date and Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Extracted Chains": {
            "H": {
                "Acids": list(proteins["H"]),
                "Length": len(proteins["H"])
            },
            "L": {
                "Acids": list(proteins["L"]),
                "Length": len(proteins["L"])
            }
        }
    }
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)
    
    print(f"Metadata saved to {output_file_path}")


pbd_data = read_file(os.path.join(INPUT_DATA_PATH, FILE_NAME))
atom_data = get_atom_data_from_pdb(pbd_data)
check_atom_files(atom_data)
proteins = extract_hl_protein_chain(atom_data)
file_name = FILE_NAME.split(".")[0]
write_chain_to_json(file_name, proteins, os.path.join(RESULT_PATH, file_name + ".json"))

