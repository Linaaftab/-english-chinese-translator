import os

class Config:
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
    DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')
    
    # File paths
    DICTIONARY_PATH = os.path.join(PROCESSED_DIR, 'dictionary.json')
    RULES_PATH = os.path.join(PROCESSED_DIR, 'translation_rules.json')
    
    # Large dataset processing
    CHUNK_SIZE = 5000
    MAX_SENTENCE_LENGTH = 30
    MIN_FREQUENCY = 2
    
    # Translation parameters
    UNKNOWN_TOKEN = "[UNK]"
    
    # Supported dataset formats
    SUPPORTED_FORMATS = ['csv', 'json', 'jsonl', 'tsv', 'txt']
    
    def __init__(self):
        # Create directories if they don't exist
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.RAW_DATA_DIR, exist_ok=True)
        os.makedirs(self.PROCESSED_DIR, exist_ok=True)
        os.makedirs(self.DATASETS_DIR, exist_ok=True)
