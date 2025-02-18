import os
import argparse
from pathlib import Path
import json 


import requests
from pdb_processor import PDB


RESULT_PATH = "results"
URL = "http://localhost:5000/get_embeddings"


def main(input_file):
    # Parse the PDB file and extract the protein chains
    pdb = PDB()
    input_file = Path(input_file)
    file_name = os.path.split(input_file)[1].split(".")[0]
    pdb.read_file(input_file)
    pdb.get_atom_data_from_pdb()
    pdb.check_atom_files()
    proteins = pdb.extract_hl_protein_chain()

    data = {
        "h_sequence": proteins["H"],
        "l_sequence": proteins["L"],
    }

    response = requests.post(URL, json=data)
    print(response.json())

    os.makedirs(RESULT_PATH, exist_ok=True)
    output_file_path = os.path.join(RESULT_PATH, file_name + "_prediction.json")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a PDB file and send data to API.")
    parser.add_argument("input_file", type=str, help="Path to the input PDB file")
    args = parser.parse_args()
    main(args.input_file)