import os

import requests
from pdb_processor import PDB

INPUT_DATA_PATH = "inputs"
FILE_NAME = "1bey.pdb"
RESULT_PATH = "results"
URL = "http://localhost:5000/get_embeddings"

# Parse the PDB file and extract the protein chains
pdb = PDB()
pdb.read_file(os.path.join(INPUT_DATA_PATH, FILE_NAME))
pdb.get_atom_data_from_pdb()
pdb.check_atom_files()
proteins = pdb.extract_hl_protein_chain()

data = {
    "h_sequence": proteins["H"],
    "l_sequence": proteins["L"],
}

response = requests.post(URL, json=data)
print(response.json())

