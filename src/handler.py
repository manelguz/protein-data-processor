import json
import torch
torch.hub.set_dir('/opt/ml/torch')
from esm_model import ESMModel


def lambda_handler(event, context):
    body = json.loads(event['body'])
    esm_model = ESMModel()
    if not body or 'h_sequence' not in body or 'l_sequence' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps({
                    'error':"Bad Request"
            })
        }
    try:
        h_sequence = body['h_sequence']
        l_sequence = body['l_sequence']
        h_chain_embeddings, elapsed_time_h, _, _  = esm_model.extract_chain_embeddings(h_sequence)
        l_chain_embeddings, elapsed_time_l, _, metadata  = esm_model.extract_chain_embeddings(l_sequence)

        
        # Convert tensors to lists for JSON serialization
        embeddings = {
            "metadata": metadata,
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
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                    'error': str(e)
            })
        }        
    
    return {
        'statusCode': 200,
        'body': json.dumps(embeddings)
    }