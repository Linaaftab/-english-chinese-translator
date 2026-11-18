import re

class Tokenizer:
    def __init__(self):
        pass
    
    def tokenize_english(self, text):
        """Tokenize English text"""
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
    
    def tokenize_chinese(self, text):
        """Tokenize Chinese text - character level"""
        return list(text)
    
    def extract_phrases(self, tokens, max_phrase_length=3):
        """Extract phrases from token sequence"""
        phrases = []
        n_tokens = len(tokens)
        
        for length in range(2, max_phrase_length + 1):
            for i in range(n_tokens - length + 1):
                phrase = ' '.join(tokens[i:i + length])
                phrases.append(phrase)
        
        return phrases