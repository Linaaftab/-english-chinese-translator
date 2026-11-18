import re

class RuleBasedEncoder:
    def __init__(self):
        self.syntax_patterns = {
            'SVO': r'(\w+)\s+(\w+)\s+(\w+)',
            'SV': r'(\w+)\s+(\w+)',
            'Question': r'(what|who|where|when|why|how)\s+(\w+)\s+(\w+)',
            'Modal': r'(can|will|should|would|could)\s+(\w+)\s+(\w+)'
        }
    
    def encode(self, sentence):
        """Convert English sentence to structured representation"""
        sentence = sentence.lower().strip()
        
        encoded = {
            'original': sentence,
            'tokens': self._tokenize(sentence),
            'sentence_type': self._detect_sentence_type(sentence),
            'structure': self._analyze_structure(sentence),
            'tense': self._detect_tense(sentence)
        }
        
        return encoded
    
    def _tokenize(self, sentence):
        """Tokenize sentence into words"""
        return re.findall(r'\b\w+\b', sentence)
    
    def _detect_sentence_type(self, sentence):
        """Detect if sentence is question, statement, or imperative"""
        if any(word in sentence.lower().split() for word in ['what', 'who', 'where', 'when', 'why', 'how']):
            return 'question'
        elif any(sentence.lower().startswith(word) for word in ['please', 'let', 'go']):
            return 'imperative'
        else:
            return 'statement'
    
    def _analyze_structure(self, sentence):
        """Analyze sentence structure"""
        for pattern_name, pattern in self.syntax_patterns.items():
            if re.search(pattern, sentence):
                return pattern_name
        return 'unknown'
    
    def _detect_tense(self, sentence):
        """Simple tense detection without spaCy"""
        words = sentence.split()
        if any(word in ['will', 'shall', 'going'] for word in words):
            return 'future'
        elif any(word.endswith('ed') for word in words) or any(word in ['was', 'were'] for word in words):
            return 'past'
        else:
            return 'present'