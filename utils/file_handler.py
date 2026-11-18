import json
import pandas as pd
import os
import gzip
from collections import defaultdict

# Import config using relative path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import Config

class LargeFileHandler:
    def __init__(self):
        self.config = Config()
    
    def load_dataset_chunks(self, file_path, en_col='english', zh_col='chinese', format='auto'):
        """Load large dataset in manageable chunks"""
        print(f"Loading dataset from: {file_path}")
        
        if format == 'auto':
            format = self._detect_format(file_path)
        
        if format == 'csv':
            return self._load_csv_chunks(file_path, en_col, zh_col)
        elif format == 'json':
            return self._load_json_chunks(file_path, en_col, zh_col)
        elif format == 'jsonl':
            return self._load_jsonl_chunks(file_path, en_col, zh_col)
        elif format == 'txt':
            return self._load_txt_parallel(file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _load_csv_chunks(self, file_path, en_col, zh_col):
        """Load CSV in chunks using pandas"""
        print(f"Loading CSV dataset: {file_path}")
        chunk_size = self.config.CHUNK_SIZE
        
        try:
            for chunk_num, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
                valid_pairs = []
                for _, row in chunk.iterrows():
                    en_text = str(row.get(en_col, '')).strip()
                    zh_text = str(row.get(zh_col, '')).strip()
                    
                    if (en_text and zh_text and 
                        en_text != 'nan' and zh_text != 'nan' and
                        len(en_text.split()) <= self.config.MAX_SENTENCE_LENGTH):
                        valid_pairs.append((en_text, zh_text))
                
                if valid_pairs:
                    print(f"Chunk {chunk_num}: {len(valid_pairs)} valid pairs")
                    yield valid_pairs, chunk_num
                    
        except Exception as e:
            print(f"Error loading CSV: {e}")
            raise
    
    def _load_json_chunks(self, file_path, en_col, zh_col):
        """Load JSON file in chunks"""
        print(f"Loading JSON dataset: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            all_pairs = []
            for item in data:
                en_text = str(item.get(en_col, '')).strip()
                zh_text = str(item.get(zh_col, '')).strip()
                
                if en_text and zh_text:
                    all_pairs.append((en_text, zh_text))
            
            print(f"Total pairs in JSON: {len(all_pairs)}")
            
            chunk_size = self.config.CHUNK_SIZE
            for i in range(0, len(all_pairs), chunk_size):
                chunk = all_pairs[i:i + chunk_size]
                yield chunk, i // chunk_size
                
        except Exception as e:
            print(f"Error loading JSON: {e}")
            raise
    
    def _load_jsonl_chunks(self, file_path, en_col, zh_col):
        """Load JSONL file line by line"""
        print(f"Loading JSONL dataset: {file_path}")
        
        current_chunk = []
        chunk_num = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        en_text = str(data.get(en_col, '')).strip()
                        zh_text = str(data.get(zh_col, '')).strip()
                        
                        if en_text and zh_text:
                            current_chunk.append((en_text, zh_text))
                        
                        if len(current_chunk) >= self.config.CHUNK_SIZE:
                            yield current_chunk, chunk_num
                            current_chunk = []
                            chunk_num += 1
                            
                    except json.JSONDecodeError:
                        continue
            
            if current_chunk:
                yield current_chunk, chunk_num
                
        except Exception as e:
            print(f"Error loading JSONL: {e}")
            raise
    
    def _load_txt_parallel(self, file_path):
        """Load parallel text files"""
        base_name = os.path.splitext(file_path)[0]
        en_file = base_name + '.en'
        zh_file = base_name + '.zh'
        
        if os.path.exists(en_file) and os.path.exists(zh_file):
            print(f"Loading parallel files: {en_file}, {zh_file}")
            
            try:
                with open(en_file, 'r', encoding='utf-8') as f_en, \
                     open(zh_file, 'r', encoding='utf-8') as f_zh:
                    en_lines = [line.strip() for line in f_en if line.strip()]
                    zh_lines = [line.strip() for line in f_zh if line.strip()]
                
                pairs = list(zip(en_lines, zh_lines))
                print(f"Total parallel pairs: {len(pairs)}")
                
                chunk_size = self.config.CHUNK_SIZE
                for i in range(0, len(pairs), chunk_size):
                    chunk = pairs[i:i + chunk_size]
                    yield chunk, i // chunk_size
                    
            except Exception as e:
                print(f"Error loading parallel files: {e}")
                raise
        else:
            raise FileNotFoundError(f"Parallel files not found: {en_file}, {zh_file}")
    
    def _detect_format(self, file_path):
        """Auto-detect file format"""
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        if ext in self.config.SUPPORTED_FORMATS:
            return ext
        else:
            return 'txt'
    
    def save_compressed_data(self, data, file_path):
        """Save data with compression"""
        try:
            with gzip.open(file_path, 'wt', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Data saved to: {file_path}")
        except Exception as e:
            print(f"Error saving data: {e}")
            raise
    
    def load_compressed_data(self, file_path):
        """Load compressed data"""
        try:
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except Exception as e:
            print(f"Error loading data: {e}")
            return None