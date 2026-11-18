import re

class TextPreprocessor:
    def __init__(self):
        self.contraction_map = {
            "don't": "do not", "can't": "cannot", "won't": "will not",
            "it's": "it is", "i'm": "i am", "he's": "he is", "she's": "she is",
            "that's": "that is", "what's": "what is", "where's": "where is"
        }
    
    def preprocess_english(self, text):
        """Clean and normalize English text"""
        text = text.lower().strip()
        
        # Handle contractions
        for contraction, expansion in self.contraction_map.items():
            text = text.replace(contraction, expansion)
        
        # Remove extra spaces and special characters
        text = re.sub(r'[^\w\s.,!?]', '', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def preprocess_chinese(self, text):
        """Clean Chinese text"""
        text = text.strip()
        text = re.sub(r'\s+', '', text)
        return text
    
    def is_valid_sentence_pair(self, en_text, zh_text):
        """Validate if sentence pair is suitable for training"""
        if not en_text or not zh_text:
            return False
        
        if len(en_text) < 2 or len(zh_text) < 1:
            return False
        
        # Check if Chinese text contains Chinese characters
        if not any('\u4e00' <= char <= '\u9fff' for char in zh_text):
            return False
        
        return True