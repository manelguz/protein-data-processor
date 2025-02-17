import os


from pdb_processor import PDB
from esm_model import ESMModel

INPUT_DATA_PATH = "inputs"
FILE_NAME = "1bey.pdb"
MAPPING_FILE_NAME = "mapping.json"
RESULT_PATH = "results"

pdb = PDB()
pdb.read_file(os.path.join(INPUT_DATA_PATH, FILE_NAME))
pdb.get_atom_data_from_pdb()
pdb.check_atom_files()
pdb.extract_hl_protein_chain()
file_name = FILE_NAME.split(".")[0]
pdb.write_chain_to_json(file_name, os.path.join(RESULT_PATH, file_name + ".json"))
protein_data = pdb.read_json_data(os.path.join(RESULT_PATH, file_name + ".json"))
esm_model = ESMModel()
h_chain_embeddings = esm_model.extract_chain_embeddings(protein_data["chain"]["H"]["sequence"])
l_chain_embeddings = esm_model.extract_chain_embeddings(protein_data["chain"]["L"]["sequence"])








