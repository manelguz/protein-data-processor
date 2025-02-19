import torch
import time
import platform
# Load ESM model

class ESMModel:
    def __init__(self):
        self.model_name = "esm2_t33_650M_UR50D"
        self.model, self.alphabet = torch.hub.load("facebookresearch/esm:main", self.model_name)
        self.model.eval() 

    def extract_chain_embeddings(self, sequence):
        """
        Extract embeddings for a sequence using ESM model.
        
        Args:
            sequence (str): Amino acid sequence
            model: ESM model
            alphabet: ESM alphabet
            
        Returns:
            torch.Tensor: Embeddings for the sequence
        """
        # Prepare batch
        batch_converter = self.alphabet.get_batch_converter()
        data = [("protein", sequence)]
        _, _, batch_tokens = batch_converter(data)
        batch_lens = (batch_tokens != self.alphabet.padding_idx).sum(1)

        # Move to GPU if available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(device)
        batch_tokens = batch_tokens.to(device)
        
        # Extract per-residue representations
        start_time = time.time()
        with torch.no_grad():
            # THe model returns a tuple with the output, and the output is a dictionary with the keys "logits" and "representations"
            results = self.model(batch_tokens, repr_layers=[33])
        end_time = time.time()
        elapsed_time = end_time - start_time
        if torch.cuda.is_available():
            results = results.cpu()
        embeddings = results["representations"][33].numpy()
        
        # Generate per-sequence representations via averaging
        # NOTE: token 0 is always a beginning-of-sequence token, so the first residue is token 1.
        sequence_representations = []
        for i, tokens_len in enumerate(batch_lens):
            sequence_representations.append(embeddings[i, 1 : tokens_len - 1].mean(0).tolist())

        metadata =  {
            "system_info": {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "cuda_available": torch.cuda.is_available(),
                "gpu_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"
            },
            "model_info": {
                "model_name": self.model_name,
                "model_parameters": sum(p.numel() for p in self.model.parameters()),
                "device": "cuda" if torch.cuda.is_available() else "cpu"
            }
        }

        return sequence_representations, elapsed_time, results, metadata

if "__main__" == __name__:
    sequence = "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"
    esm_model = ESMModel()
    sequence_representations, elapsed_time, results, metadata = esm_model.extract_chain_embeddings(sequence)
    print(sequence_representations)