from flask import Flask, request, jsonify


app = Flask(__name__)
from esm_model import ESMModel


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/get_embeddings', methods=['POST'])
def get_embeddings():
    try:
        data = request.get_json()
        esm_model = ESMModel()
        if not data or 'h_sequence' not in data or 'l_sequence' not in data:
            return jsonify({
                "error": "Missing required sequences. Please provide 'h_sequence' and 'l_sequence'"
            }), 400

        h_sequence = data['h_sequence']
        l_sequence = data['l_sequence']
        h_chain_embeddings, elapsed_time_h, _  = esm_model.extract_chain_embeddings(h_sequence)
        l_chain_embeddings, elapsed_time_l, _  = esm_model.extract_chain_embeddings(l_sequence)

        
        # Convert tensors to lists for JSON serialization
        embeddings = {
            "H_chain": {
                "sequence": h_sequence,
                "embeddings":h_chain_embeddings,
                "elapsed_time_h": elapsed_time_h
            },
            "L_chain": {
                "sequence": l_sequence,
                "embeddings": l_chain_embeddings,
                "elapsed_time_l": elapsed_time_l
            }
        }
        
        return jsonify(embeddings)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)