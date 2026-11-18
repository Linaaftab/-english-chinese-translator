import os
import sys
import time
import pandas as pd
from collections import defaultdict
import re
import json

class EnglishChineseTranslator:
    def __init__(self):
        self.translation_rules = defaultdict(list)
        self.loaded = False
        self.character_voices = {}
        self.cultural_adaptations = {}
        self.emotional_tones = {}
        
        # Load all data
        self._load_existing_rules()
        self._load_character_voices()
        self._load_cultural_adaptations()
        self._load_emotional_tones()
    
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
    
    def _load_character_voices(self):
        """Load character voice patterns"""
        character_file = "character_voices.json"
        if os.path.exists(character_file):
            try:
                with open(character_file, 'r', encoding='utf-8') as f:
                    self.character_voices = json.load(f)
                print(f"✅ Loaded {len(self.character_voices)} character voices")
            except Exception as e:
                print(f"❌ Error loading character voices: {e}")
                # Default character voices
                self.character_voices = {
                    'protagonist': {'intense': '！', 'calm': '。', 'neutral': '。'},
                    'antagonist': {'intense': '！', 'calm': '。', 'neutral': '。'},
                    'narrator': {'intense': '', 'calm': '', 'neutral': ''},
                    'supporting': {'intense': '！', 'calm': '。', 'neutral': '。'},
                    'default': {'intense': '！', 'calm': '。', 'neutral': '。'}
                }
        else:
            print("💡 No character voices file found, using defaults")
            self.character_voices = {
                'protagonist': {'intense': '！', 'calm': '。', 'neutral': '。'},
                'antagonist': {'intense': '！', 'calm': '。', 'neutral': '。'},
                'narrator': {'intense': '', 'calm': '', 'neutral': ''},
                'supporting': {'intense': '！', 'calm': '。', 'neutral': '。'},
                'default': {'intense': '！', 'calm': '。', 'neutral': '。'}
            }
    
    def _load_cultural_adaptations(self):
        """Load cultural adaptations"""
        cultural_file = "cultural_adaptations.json"
        if os.path.exists(cultural_file):
            try:
                with open(cultural_file, 'r', encoding='utf-8') as f:
                    self.cultural_adaptations = json.load(f)
                print(f"✅ Loaded {len(self.cultural_adaptations)} cultural adaptations")
            except Exception as e:
                print(f"❌ Error loading cultural adaptations: {e}")
                # Default cultural adaptations
                self.cultural_adaptations = {
                    "Coney Island": "康尼岛",
                    "Times Square": "时代广场",
                    "Hollywood": "好莱坞",
                    "New York": "纽约",
                    "Los Angeles": "洛杉矶",
                    "San Francisco": "旧金山",
                    "Chicago": "芝加哥",
                    "Washington": "华盛顿",
                    "dollar": "美元",
                    "pound": "英镑",
                    "mile": "英里",
                    "foot": "英尺"
                }
        else:
            print("💡 No cultural adaptations file found, using defaults")
            self.cultural_adaptations = {
                "Coney Island": "康尼岛",
                "Times Square": "时代广场",
                "Hollywood": "好莱坞",
                "New York": "纽约",
                "Los Angeles": "洛杉矶",
                "San Francisco": "旧金山",
                "Chicago": "芝加哥",
                "Washington": "华盛顿",
                "dollar": "美元",
                "pound": "英镑",
                "mile": "英里",
                "foot": "英尺"
            }
    
    def _load_emotional_tones(self):
        """Load emotional tone patterns"""
        # Default emotional tone markers
        self.emotional_tones = {
            'intense': {'prefix': '', 'suffix': '！'},
            'emotional': {'prefix': '', 'suffix': '！'},
            'calm': {'prefix': '', 'suffix': '。'},
            'neutral': {'prefix': '', 'suffix': '。'},
            'sad': {'prefix': '唉，', 'suffix': '。'},
            'happy': {'prefix': '太好了，', 'suffix': '！'},
            'angry': {'prefix': '真是的，', 'suffix': '！'}
        }
        print("✅ Loaded emotional tone patterns")
    
    def _save_rules(self, df):
        """Save translation rules to file"""
        try:
            df.to_csv("translation_rules.csv", index=False, encoding='utf-8')
            print("💾 Translation rules saved")
            return True
        except Exception as e:
            print(f"❌ Error saving rules: {e}")
            return False
    
    def train(self, dataset_path, max_chunks=None):
        """Train the translator on a dataset"""
        print(f"🚀 Training translator on: {dataset_path}")
        
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset not found: {dataset_path}")
            return False
        
        try:
            # Read the dataset
            df = pd.read_csv(dataset_path)
            
            if 'english' not in df.columns or 'chinese' not in df.columns:
                print("❌ Dataset must have 'english' and 'chinese' columns")
                return False
            
            # Process the data
            processed_pairs = []
            for _, row in df.iterrows():
                english = str(row['english']).strip()
                chinese = str(row['chinese']).strip()
                
                if english and chinese and len(english) >= 1:
                    # Add to translation rules
                    english_lower = english.lower()
                    self.translation_rules[english_lower].append(chinese)
                    processed_pairs.append((english, chinese))
            
            # Save the rules
            rules_df = pd.DataFrame(processed_pairs, columns=['english', 'chinese'])
            self._save_rules(rules_df)
            
            print(f"✅ Training completed! Processed {len(processed_pairs)} sentence pairs")
            self.loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return False
    
    def translate(self, english_text, context=None, options=None):
        """Translate English text to Chinese with cinematic context support"""
        if not english_text.strip():
            return "请输入英文文本"
        
        if not self.loaded:
            return "请先训练翻译模型 (Please train the model first)"
        
        # Default values for backward compatibility
        if context is None:
            context = {}
        if options is None:
            options = {}
        
        try:
            # Step 1: Get base translation
            base_translation = self._get_base_translation(english_text)
            
            # Step 2: Apply processing options if provided
            if context or options:
                base_translation = self._apply_cinematic_adaptations(
                    base_translation, english_text, context, options
                )
            
            return base_translation
            
        except Exception as e:
            return f"翻译错误: {str(e)}"
    
    def _get_base_translation(self, english_text):
        """Get the base Chinese translation"""
        # Clean the input
        english_lower = english_text.lower().strip()
        
        # Try exact match first
        if english_lower in self.translation_rules:
            return self.translation_rules[english_lower][0]
        
        # Try partial matches (phrases)
        for key in sorted(self.translation_rules.keys(), key=len, reverse=True):
            if key in english_lower and len(key) > 3:
                # Replace the matched phrase
                start_idx = english_lower.find(key)
                end_idx = start_idx + len(key)
                original_phrase = english_text[start_idx:end_idx]
                translation = self.translation_rules[key][0]
                return english_text[:start_idx] + translation + english_text[end_idx:]
        
        # Word-by-word fallback
        words = english_lower.split()
        translated_words = []
        
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word)
            
            if clean_word in self.translation_rules:
                translated_words.append(self.translation_rules[clean_word][0])
            else:
                translated_words.append(word)
        
        return ' '.join(translated_words)
    
    def _apply_cinematic_adaptations(self, translation, original_text, context, options):
        """Apply cinematic adaptations to translation"""
        adapted_translation = translation
        
        # 1. Apply cultural adaptation if requested
        if options.get('cultural_adapt', True):
            adapted_translation = self._apply_cultural_adaptation(adapted_translation)
        
        # 2. Apply emotional tone if provided
        emotional_tone = context.get('emotional_tone', 'neutral')
        if options.get('emotional_adapt', True) and emotional_tone in self.emotional_tones:
            tone_config = self.emotional_tones[emotional_tone]
            if tone_config['prefix'] and not adapted_translation.startswith(tone_config['prefix']):
                adapted_translation = tone_config['prefix'] + adapted_translation
            if tone_config['suffix'] and not adapted_translation.endswith(tone_config['suffix']):
                # Remove any existing punctuation
                adapted_translation = adapted_translation.rstrip('。！？!?.')
                adapted_translation += tone_config['suffix']
        
        # 3. Apply character voice if requested
        character = context.get('character', 'default').lower()
        if options.get('preserve_voice', True) and character in self.character_voices:
            char_voice = self.character_voices[character].get(emotional_tone, '。')
            if char_voice and not adapted_translation.endswith(char_voice):
                adapted_translation = adapted_translation.rstrip('。！？!?.')
                adapted_translation += char_voice
        
        # 4. Handle code-switching if requested
        if options.get('detect_codeswitch', True):
            code_switch_detected = self._detect_code_switching(original_text)
            if code_switch_detected:
                adapted_translation += " [含其他语言]"
        
        # 5. Apply timing marks if requested and needed
        if options.get('maintain_timing', True):
            adapted_translation = self._apply_timing_marks(adapted_translation, original_text)
        
        return adapted_translation
    
    def _apply_cultural_adaptation(self, translation):
        """Apply cultural adaptations to translation"""
        for eng, chi in self.cultural_adaptations.items():
            if eng.lower() in translation.lower():
                # Case-insensitive replacement
                translation = re.sub(re.escape(eng), chi, translation, flags=re.IGNORECASE)
        return translation
    
    def _detect_code_switching(self, text):
        """Detect if text contains code-switching"""
        # Simple detection: check for non-Latin characters mixed with Latin
        has_latin = bool(re.search(r'[a-zA-Z]', text))
        has_non_latin = bool(re.search(r'[^\x00-\x7F]', text))
        return has_latin and has_non_latin
    
    def _apply_timing_marks(self, translation, original_text):
        """Apply timing marks for subtitles"""
        # Add timing markers if original has them
        if '[' in original_text and ']' in original_text:
            # Find all markers like [whispering], [shouts], etc.
            markers = re.findall(r'\[(.*?)\]', original_text)
            if markers:
                # Add markers to translation
                for marker in markers:
                    if marker not in translation:
                        translation += f' [{marker}]'
        
        return translation
    
    def add_translation_rule(self, english, chinese):
        """Manually add a translation rule"""
        english_lower = english.lower().strip()
        if english_lower not in self.translation_rules[english_lower]:
            self.translation_rules[english_lower].append(chinese.strip())
            print(f"✅ Added rule: '{english}' -> '{chinese}'")
            return True
        return False
    
    def interactive_translation(self):
        """Interactive translation mode"""
        print("\n" + "="*50)
        print("🌟 English to Chinese Translator 🌟")
        print("="*50)
        print("Commands:")
        print("  - Type 'quit', 'exit', or 'q' to exit")
        print("  - Type 'train <dataset_path>' to train on new data")
        print("  - Type 'stats' to show current statistics")
        print("  - Type 'add <english>=<chinese>' to add custom rule")
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
                        print(f"📊 Character voices: {len(self.character_voices)}")
                        print(f"📊 Cultural adaptations: {len(self.cultural_adaptations)}")
                    else:
                        print("📊 No rules loaded")
                    continue
                elif user_input.lower().startswith('train '):
                    dataset_path = user_input[6:].strip()
                    self.train(dataset_path)
                    continue
                elif user_input.lower().startswith('add '):
                    # Parse add command: add hello=你好
                    parts = user_input[4:].split('=', 1)
                    if len(parts) == 2:
                        english, chinese = parts
                        self.add_translation_rule(english.strip(), chinese.strip())
                    continue
                
                if user_input:
                    # Test with cinematic context
                    context = {
                        'movie_title': 'Test Movie',
                        'scene_number': '1',
                        'character': 'protagonist',
                        'emotional_tone': 'neutral'
                    }
                    options = {
                        'cultural_adapt': True,
                        'emotional_adapt': True,
                        'preserve_voice': True
                    }
                    
                    simple_translation = self.translate(user_input)
                    cinematic_translation = self.translate(user_input, context, options)
                    
                    print(f"🔤 English: {user_input}")
                    print(f"🀄 Simple: {simple_translation}")
                    print(f"🎬 Cinematic: {cinematic_translation}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def create_sample_dataset():
    """Create a sample dataset for testing"""
    sample_data = {
        'english': [
            'Hello',
            'Thank you',
            'Good morning',
            'I love you',
            'How are you?',
            'What is your name?',
            'Where are you from?',
            'Nice to meet you',
            'Goodbye',
            'See you later',
            'I am sorry',
            'Please help me',
            'How much is this?',
            'Where is the bathroom?',
            'I don\'t understand',
            'Can you speak English?',
            'What time is it?',
            'I need help',
            'This is delicious',
            'You are beautiful'
        ],
        'chinese': [
            '你好',
            '谢谢',
            '早上好',
            '我爱你',
            '你好吗？',
            '你叫什么名字？',
            '你从哪里来？',
            '很高兴认识你',
            '再见',
            '回头见',
            '对不起',
            '请帮帮我',
            '这个多少钱？',
            '洗手间在哪里？',
            '我不明白',
            '你会说英语吗？',
            '现在几点了？',
            '我需要帮助',
            '这个很好吃',
            '你很漂亮'
        ]
    }
    
    df = pd.DataFrame(sample_data)
    os.makedirs('datasets', exist_ok=True)
    df.to_csv('datasets/sample_dataset.csv', index=False, encoding='utf-8')
    print("✅ Created sample dataset at: datasets/sample_dataset.csv")
    return 'datasets/sample_dataset.csv'

def create_config_files():
    """Create configuration files for cinematic features"""
    
    # Character voices configuration
    character_voices = {
        "protagonist": {
            "intense": "！",
            "emotional": "！",
            "calm": "。",
            "neutral": "。",
            "description": "Heroic, determined voice"
        },
        "antagonist": {
            "intense": "！",
            "emotional": "！", 
            "calm": "。",
            "neutral": "。",
            "description": "Villainous, menacing voice"
        },
        "narrator": {
            "intense": "",
            "emotional": "",
            "calm": "",
            "neutral": "",
            "description": "Neutral, informative voice"
        },
        "supporting": {
            "intense": "！",
            "emotional": "！",
            "calm": "。", 
            "neutral": "。",
            "description": "Supporting character voice"
        },
        "default": {
            "intense": "！",
            "emotional": "！",
            "calm": "。",
            "neutral": "。",
            "description": "Default character voice"
        }
    }
    
    # Cultural adaptations
    cultural_adaptations = {
        "New York": "纽约",
        "Los Angeles": "洛杉矶", 
        "San Francisco": "旧金山",
        "Chicago": "芝加哥",
        "Washington": "华盛顿",
        "Times Square": "时代广场",
        "Hollywood": "好莱坞",
        "Coney Island": "康尼岛",
        "dollar": "美元",
        "pound": "英镑",
        "euro": "欧元",
        "mile": "英里",
        "foot": "英尺",
        "inch": "英寸",
        "pound (weight)": "磅",
        "Thanksgiving": "感恩节",
        "Christmas": "圣诞节",
        "Halloween": "万圣节"
    }
    
    # Save files
    try:
        with open('character_voices.json', 'w', encoding='utf-8') as f:
            json.dump(character_voices, f, ensure_ascii=False, indent=2)
        
        with open('cultural_adaptations.json', 'w', encoding='utf-8') as f:
            json.dump(cultural_adaptations, f, ensure_ascii=False, indent=2)
        
        print("✅ Created configuration files:")
        print("   - character_voices.json")
        print("   - cultural_adaptations.json")
        return True
    except Exception as e:
        print(f"❌ Error creating config files: {e}")
        return False

def main():
    print("=== English-Chinese Cinematic Translator ===")
    print("🎬 Now with cinematic localization features!")
    
    # Create necessary directories
    os.makedirs('datasets', exist_ok=True)
    
    # Create config files
    create_config_files()
    
    translator = EnglishChineseTranslator()
    
    # Check for sample dataset
    sample_dataset = "datasets/sample_dataset.csv"
    if not os.path.exists(sample_dataset):
        print("\n📚 Creating sample dataset...")
        sample_dataset = create_sample_dataset()
    
    # Train on sample dataset
    print(f"\n🚀 Training on sample dataset...")
    success = translator.train(sample_dataset)
    if not success:
        print("❌ Training failed. Using basic dictionary mode.")
    
    # Test cinematic translations
    test_sentences = [
        ("Hello world", "neutral", "protagonist"),
        ("I love you", "emotional", "protagonist"),
        ("Thank you very much", "calm", "supporting"),
        ("This costs 10 dollars", "neutral", "narrator"),
        ("I'm from New York", "neutral", "default")
    ]
    
    print("\n" + "🧪 Cinematic Translation Tests:")
    print("-" * 60)
    
    for english, tone, character in test_sentences:
        context = {
            'movie_title': 'Test Movie',
            'scene_number': '1',
            'character': character,
            'emotional_tone': tone
        }
        options = {
            'cultural_adapt': True,
            'emotional_adapt': True,
            'preserve_voice': True,
            'detect_codeswitch': True,
            'maintain_timing': True
        }
        
        cinematic_translation = translator.translate(english, context, options)
        print(f"🎬 Context: {character.title()} | {tone.title()}")
        print(f"🔤 English: {english}")
        print(f"🀄 Chinese: {cinematic_translation}")
        print("-" * 30)
    
    
    translator.interactive_translation()

if __name__ == "__main__":
    main()