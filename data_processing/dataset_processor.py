import json
import pandas as pd
from collections import Counter, defaultdict
import os
import re

# Import using relative paths
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import Config
from utils.file_handler import LargeFileHandler
from utils.preprocessor import TextPreprocessor
from utils.tokenizer import Tokenizer

class LargeDatasetProcessor:
    def __init__(self):
        self.config = Config()
        self.file_handler = LargeFileHandler()
        self.preprocessor = TextPreprocessor()
        self.tokenizer = Tokenizer()
        
        self.word_translations = defaultdict(Counter)
        self.phrase_translations = defaultdict(Counter)
    
    def process_dataset(self, dataset_path, max_chunks=None):
        """Process entire dataset and extract translation rules"""
        print("Starting dataset processing...")
        
        chunk_count = 0
        total_pairs = 0
        
        try:
            for chunk, chunk_num in self.file_handler.load_dataset_chunks(dataset_path):
                print(f"Processing chunk {chunk_num}...")
                
                chunk_stats = self._process_chunk(chunk)
                total_pairs += chunk_stats['processed_pairs']
                
                chunk_count += 1
                if max_chunks and chunk_count >= max_chunks:
                    break
            
            self._post_process_rules()
            self._save_extracted_rules()
            
            print(f"Dataset processing completed!")
            print(f"Total chunks processed: {chunk_count}")
            print(f"Total sentence pairs: {total_pairs}")
            return True
            
        except Exception as e:
            print(f"Error processing dataset: {e}")
            return False
    
    def _process_chunk(self, chunk):
        """Process a single chunk of data"""
        stats = {'processed_pairs': 0, 'skipped_pairs': 0}
        
        for en_text, zh_text in chunk:
            clean_en = self.preprocessor.preprocess_english(en_text)
            clean_zh = self.preprocessor.preprocess_chinese(zh_text)
            
            if not self.preprocessor.is_valid_sentence_pair(clean_en, clean_zh):
                stats['skipped_pairs'] += 1
                continue
            
            # Extract direct word mappings using a simpler approach
            self._extract_direct_mappings(clean_en, clean_zh)
            
            stats['processed_pairs'] += 1
        
        return stats
    
    def _extract_direct_mappings(self, en_text, zh_text):
        """Extract direct word mappings using position-based alignment"""
        en_words = self.tokenizer.tokenize_english(en_text)
        zh_chars = list(zh_text)  # Chinese characters
        
        # Simple position-based alignment
        for i, en_word in enumerate(en_words):
            if i < len(zh_chars) and len(en_word) > 1:  # Skip very short words
                # Map English word to Chinese character at similar position
                zh_char = zh_chars[min(i, len(zh_chars)-1)]
                if zh_char.strip():  # Only if Chinese character is not empty
                    self.word_translations[en_word][zh_char] += 1
        
        # Also try to map common patterns
        common_mappings = {
            'hello': '你好', 'hi': '你好', 'how': '怎么', 'what': '什么',
            'where': '哪里', 'when': '什么时候', 'why': '为什么', 'who': '谁',
            'thank': '谢谢', 'thanks': '谢谢', 'good': '好', 'morning': '早上',
            'afternoon': '下午', 'evening': '晚上', 'night': '晚上',
            'you': '你', 'your': '你的', 'my': '我的', 'me': '我',
            'i': '我', 'he': '他', 'she': '她', 'it': '它',
            'we': '我们', 'they': '他们', 'this': '这个', 'that': '那个',
            'is': '是', 'are': '是', 'am': '是', 'be': '是',
            'have': '有', 'has': '有', 'had': '有', 'do': '做',
            'love': '爱', 'like': '喜欢', 'want': '想要', 'need': '需要',
            'can': '可以', 'could': '可以', 'will': '会', 'would': '会',
            'book': '书', 'pen': '笔', 'water': '水', 'food': '食物',
            'house': '房子', 'car': '汽车', 'computer': '电脑', 'phone': '电话'
        }
        
        for en_word in en_words:
            if en_word in common_mappings:
                zh_translation = common_mappings[en_word]
                self.word_translations[en_word][zh_translation] += 10  # Higher weight for known mappings
    
    def _post_process_rules(self):
        """Clean and filter extracted rules"""
        min_freq = 1  # Lower frequency threshold to capture more words
        
        filtered_word_translations = {}
        for word, translations in self.word_translations.items():
            if translations:
                # Get all translations that meet frequency threshold
                valid_translations = {trans: count for trans, count in translations.items() 
                                   if count >= min_freq}
                if valid_translations:
                    # Keep top 2 translations
                    top_translations = dict(sorted(valid_translations.items(), 
                                                 key=lambda x: x[1], reverse=True)[:2])
                    filtered_word_translations[word] = top_translations
        
        self.word_translations = filtered_word_translations
        
        print(f"Extracted {len(self.word_translations)} word translations")
        
        # Print some examples for debugging
        if self.word_translations:
            print("Sample learned translations:")
            sample_words = list(self.word_translations.keys())[:10]
            for word in sample_words:
                translations = self.word_translations[word]
                print(f"  '{word}': {translations}")
    
    def _save_extracted_rules(self):
        """Save all extracted rules to file"""
        # Ensure processed directory exists
        os.makedirs(os.path.dirname(self.config.RULES_PATH), exist_ok=True)
        
        rules_data = {
            'word_translations': dict(self.word_translations),
            'phrase_translations': dict(self.phrase_translations)
        }
        
        self.file_handler.save_compressed_data(rules_data, self.config.RULES_PATH)
        print(f"Rules saved to: {self.config.RULES_PATH}")
    
    def load_rules(self):
        """Load previously extracted rules"""
        rules = self.file_handler.load_compressed_data(self.config.RULES_PATH)
        if rules:
            self.word_translations = defaultdict(Counter, rules.get('word_translations', {}))
            self.phrase_translations = defaultdict(Counter, rules.get('phrase_translations', {}))
            return True
        return False
    
    def get_statistics(self):
        """Get statistics about loaded rules"""
        return {
            'total_words': len(self.word_translations),
            'total_phrases': len(self.phrase_translations)
        }