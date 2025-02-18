import os


from pdb_processor import PDB
from esm_model import ESMModel

INPUT_DATA_PATH = "inputs"
FILE_NAME = "1bey.pdb"
RESULT_PATH = "results"

# Create the objects 
pdb = PDB()
esm_model = ESMModel()
pdb.read_file(os.path.join(INPUT_DATA_PATH, FILE_NAME))
pdb.get_atom_data_from_pdb()
pdb.check_atom_files()
pdb.extract_hl_protein_chain()
file_name = FILE_NAME.split(".")[0]
pdb.write_chain_to_json(file_name, os.path.join(RESULT_PATH, file_name + ".json"))

# Load the data
protein_data = pdb.read_json_data(os.path.join(RESULT_PATH, file_name + ".json"))

# Predict the chain embeddings
h_chain_embeddings, elapsed_time_h, model_output_h  = esm_model.extract_chain_embeddings(protein_data["chain"]["H"]["sequence"])
l_chain_embeddings, elapsed_time_l, model_output_l  = esm_model.extract_chain_embeddings(protein_data["chain"]["L"]["sequence"])

# Print the results
print(f"The protein data for {file_name} is:")

print(f"The L chain is: {protein_data['chain']['L']['sequence']}")
print(f"Elapsed time for L chain: {elapsed_time_l}")
print(f"Embeddings for L chain: {l_chain_embeddings}")

print(f"The H chain is: {protein_data['chain']['H']['sequence']}")
print(f"Elapsed time for H chain: {elapsed_time_h}")
print(f"Embeddings for H chain: {h_chain_embeddings}")





