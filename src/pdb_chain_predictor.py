import os
import argparse
from pathlib import Path
import json

from pdb_processor import PDB
from esm_model import ESMModel


RESULT_PATH = "results"

def main(input_file):
    # Create the objects 
    pdb = PDB()
    esm_model = ESMModel()
    input_file = Path(input_file)
    pdb.read_file(input_file)
    pdb.get_atom_data_from_pdb()
    pdb.check_atom_files()
    pdb.extract_hl_protein_chain()
    file_name = os.path.split(input_file)[1].split(".")[0]
    pdb.write_chain_to_json(file_name, os.path.join(RESULT_PATH, file_name + ".json"))

    # Load the data
    protein_data = pdb.read_json_data(os.path.join(RESULT_PATH, file_name + ".json"))

    # Predict the chain embeddings
    h_chain_embeddings, elapsed_time_h, model_output_h, _ = esm_model.extract_chain_embeddings(protein_data["chain"]["H"]["sequence"])
    l_chain_embeddings, elapsed_time_l, model_output_l, metadata  = esm_model.extract_chain_embeddings(protein_data["chain"]["L"]["sequence"])

    # Print the results
    print(f"The protein data for {file_name} is:")

    print(f"The L chain is: {protein_data['chain']['L']['sequence']}")
    print(f"Elapsed time for L chain: {elapsed_time_l}")
    print(f"Embeddings for L chain: {l_chain_embeddings}")

    print(f"The H chain is: {protein_data['chain']['H']['sequence']}")
    print(f"Elapsed time for H chain: {elapsed_time_h}")
    print(f"Embeddings for H chain: {h_chain_embeddings}")

    embeddings = {
            "metadata": metadata,
            "H_chain": {
                "sequence": protein_data["chain"]["H"]["sequence"],
                "embeddings":h_chain_embeddings,
                "elapsed_time_h": elapsed_time_h
            },
            "L_chain": {
                "sequence": protein_data["chain"]["L"]["sequence"],
                "embeddings": l_chain_embeddings,
                "elapsed_time_l": elapsed_time_l
            }
        }
    os.makedirs(RESULT_PATH, exist_ok=True)
    output_file_path = os.path.join(RESULT_PATH, file_name + "_prediction.json")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(embeddings, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a PDB file and send data to API.")
    parser.add_argument("input_file", type=str, help="Path to the input PDB file")
    args = parser.parse_args()
    main(args.input_file)



