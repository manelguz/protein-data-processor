import torch

# Load ESM model

class ESMModel:
    def __init__(self):
        self.model, self.alphabet = torch.hub.load("facebookresearch/esm:main", "esm2_t33_650M_UR50D")
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
        with torch.no_grad():
            results = self.model(batch_tokens, repr_layers=[33])
            embeddings = results["representations"][33]
        
        # Generate per-sequence representations via averaging
        # NOTE: token 0 is always a beginning-of-sequence token, so the first residue is token 1.
        sequence_representations = []
        for i, tokens_len in enumerate(batch_lens):
            sequence_representations.append(embeddings[i, 1 : tokens_len - 1].mean(0))
        
        return sequence_representations

if "__main__" == __name__:
    sequence = "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"
    esm_model = ESMModel()
    sequence_representations = esm_model.extract_chain_embeddings(sequence)
    print(sequence_representations)