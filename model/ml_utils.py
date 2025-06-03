from transformers import BertTokenizer, BertModel
import torch
import torch.nn.functional as F
import numpy as np

class LogAnomalyDetector:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.model.eval()

    def get_bert_embedding(self, text):
        # Tokenize and prepare input
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        
        # Get BERT embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]
        
        return embeddings

    def calculate_anomaly_score(self, log_message, threshold=0.7):
        # Get embedding for current log
        current_embedding = self.get_bert_embedding(log_message)
        
        # For demonstration, we'll use a simple approach:
        # 1. Check for error-related keywords
        # 2. Use BERT embeddings to detect unusual patterns
        error_keywords = ['error', 'exception', 'failed', 'crash', 'critical']
        
        # Basic keyword check
        keyword_score = any(keyword in log_message.lower() for keyword in error_keywords)
        
        # Embedding-based analysis (simplified)
        # In a real implementation, you would compare with historical embeddings
        embedding_norm = torch.norm(current_embedding)
        embedding_score = torch.sigmoid(embedding_norm - threshold).item()
        
        # Combine scores (70% embedding-based, 30% keyword-based)
        final_score = 0.7 * embedding_score + 0.3 * float(keyword_score)
        
        return final_score

    def analyze_log(self, log_message):
        score = self.calculate_anomaly_score(log_message)
        is_anomaly = score > 0.5
        
        return {
            'anomaly_score': score,
            'is_anomaly': is_anomaly,
            'model_version': 'bert-base-uncased-v1'
        }