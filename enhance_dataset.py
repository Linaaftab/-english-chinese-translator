# enhanced_translator.py
import pandas as pd
import os
import re
from collections import defaultdict
import difflib

class EnhancedEnglishChineseTranslator:
    def __init__(self):
        self.translation_rules = defaultdict(list)
        self.loaded = False
        self._load_existing_rules()
    
    def _load_existing_rules(self):
        """Load existing translation rules from file"""
        print("Checking for existing translation rules...")
        rules_file = "translation_rules.csv"
        
        if os.path.exists(rules_file):
            try:
                df = pd.read_csv(rules_file)
                for _, row in df.iterrows():
                    english = str(row['english']).lower().strip()
                    chinese = str(row['chinese']).strip()
                    if english and chinese:
                        self.translation_rules[english].append(chinese)
                self.loaded = True
                print(f"✅ Loaded {len(df)} translation rules")
                return True
            except Exception as e:
                print(f"❌ Error loading rules: {e}")
        
        print("❌ No existing rules found. Please train on a dataset first.")
        return False
    
    def train(self, dataset_path):
        """Train the translator on OpenSubtitles dataset"""
        print(f"🚀 Training translator on: {dataset_path}")
        
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset not found: {dataset_path}")
            return False
        
        try:
            df = pd.read_csv(dataset_path)
            
            if 'english' not in df.columns or 'chinese' not in df.columns:
                print("❌ Dataset must have 'english' and 'chinese' columns")
                return False
            
            processed_pairs = []
            for _, row in df.iterrows():
                english = str(row['english']).strip()
                chinese = str(row['chinese']).strip()
                
                if english and chinese and len(english) > 2:
                    english_lower = english.lower()
                    self.translation_rules[english_lower].append(chinese)
                    processed_pairs.append((english, chinese))
            
            # Save the rules
            rules_df = pd.DataFrame(processed_pairs, columns=['english', 'chinese'])
            rules_df.to_csv("translation_rules.csv", index=False, encoding='utf-8')
            
            print(f"✅ Training completed! Processed {len(processed_pairs)} sentence pairs")
            self.loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return False
    
    def _find_best_match(self, text):
        """Find the best matching phrase in our translation rules"""
        text_lower = text.lower().strip()
        
        # 1. Exact match
        if text_lower in self.translation_rules:
            return self.translation_rules[text_lower][0]
        
        # 2. Check if text is part of any known phrase
        for known_phrase in self.translation_rules:
            if text_lower in known_phrase:
                return self.translation_rules[known_phrase][0]
        
        # 3. Check if any known phrase is part of the text
        for known_phrase in self.translation_rules:
            if known_phrase in text_lower:
                return self.translation_rules[known_phrase][0]
        
        # 4. Use fuzzy matching for similar phrases
        matches = difflib.get_close_matches(text_lower, self.translation_rules.keys(), n=1, cutoff=0.6)
        if matches:
            return self.translation_rules[matches[0]][0]
        
        return None
    
    def translate(self, english_text):
        """Enhanced translation with multiple matching strategies"""
        if not english_text.strip():
            return "请输入英文文本"
        
        if not self.loaded:
            return "请先训练翻译模型 (Please train the model first)"
        
        try:
            # Try to find the best match
            best_match = self._find_best_match(english_text)
            if best_match:
                return best_match
            
            # Fallback: word-by-word translation
            words = english_text.lower().split()
            translated_words = []
            
            for word in words:
                clean_word = re.sub(r'[^\w\s]', '', word)
                word_match = self._find_best_match(clean_word)
                if word_match:
                    translated_words.append(word_match)
                else:
                    translated_words.append(word)
            
            return ' '.join(translated_words)
            
        except Exception as e:
            return f"翻译错误: {str(e)}"
    
    def interactive_translation(self):
        """Interactive translation mode"""
        print("\n" + "="*50)
        print("🌟 Enhanced English to Chinese Translator 🌟")
        print("="*50)
        print("Commands:")
        print("  - Type 'quit', 'exit', or 'q' to exit")
        print("  - Type 'train <dataset_path>' to train on new data")
        print("  - Type 'stats' to show current statistics")
        print("  - Type 'match <phrase>' to test matching")
        print("-"*50)
        
        while True:
            try:
                user_input = input("\n🔤 Enter English text: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'stats':
                    if self.loaded:
                        print(f"📊 Loaded {len(self.translation_rules)} translation rules")
                        # Show some examples
                        print("📖 Sample phrases available:")
                        sample_phrases = list(self.translation_rules.keys())[:5]
                        for phrase in sample_phrases:
                            print(f"   - '{phrase}' -> '{self.translation_rules[phrase][0]}'")
                    else:
                        print("📊 No rules loaded")
                    continue
                elif user_input.lower().startswith('train '):
                    dataset_path = user_input[6:].strip()
                    self.train(dataset_path)
                    continue
                elif user_input.lower().startswith('match '):
                    test_phrase = user_input[6:].strip()
                    best_match = self._find_best_match(test_phrase)
                    print(f"🔍 Best match for '{test_phrase}': {best_match}")
                    continue
                
                if user_input:
                    translation = self.translate(user_input)
                    print(f"🔤 English: {user_input}")
                    print(f"🀄 Chinese: {translation}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

# Test the enhanced translator
def test_enhanced_translator():
    translator = EnhancedEnglishChineseTranslator()
    
    # Test with the OpenSubtitles dataset
    print("🧪 Testing Enhanced Translator with OpenSubtitles data:")
    
    test_phrases = [
        "Hello", "Thank you", "How are you?", "I love you",
        "What is this?", "Where is the bathroom?", "Good morning"
    ]
    
    for phrase in test_phrases:
        result = translator.translate(phrase)
        print(f"🔤 '{phrase}' → 🀄 '{result}'")
    
    # Test with phrases that might be in the dataset
    print("\n🧪 Testing with phrases that might match:")
    potential_matches = [
        "you want", "I want", "be careful", "the truth", "your husband"
    ]
    
    for phrase in potential_matches:
        result = translator.translate(phrase)
        print(f"🔤 '{phrase}' → 🀄 '{result}'")
    
    # Start interactive mode
    translator.interactive_translation()

if __name__ == "__main__":
    test_enhanced_translator()