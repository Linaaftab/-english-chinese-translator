from collections import defaultdict

# Import using relative paths
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import Config
from utils.file_handler import LargeFileHandler

class RuleBasedDecoder:
    def __init__(self):
        self.config = Config()
        self.file_handler = LargeFileHandler()
        self.translation_rules = self._load_translation_rules()
        
        # Enhanced fallback dictionary for common words
        self.fallback_dictionary = {
            'world': '世界', 'happy': '开心', 'sad': '伤心', 'beautiful': '美丽',
            'smart': '聪明', 'friend': '朋友', 'family': '家人', 'home': '家',
            'school': '学校', 'work': '工作', 'play': '玩', 'eat': '吃',
            'drink': '喝', 'sleep': '睡觉', 'walk': '走', 'run': '跑',
            'big': '大', 'small': '小', 'hot': '热', 'cold': '冷',
            'new': '新', 'old': '旧', 'young': '年轻', 'fast': '快',
            'slow': '慢', 'day': '天', 'night': '夜', 'year': '年',
            'man': '男人', 'woman': '女人', 'child': '孩子', 'student': '学生',
            'teacher': '老师', 'doctor': '医生', 'city': '城市', 'country': '国家',
            'water': '水', 'food': '食物', 'book': '书', 'pen': '笔',
            'computer': '电脑', 'phone': '电话', 'car': '汽车', 'house': '房子',
            'dog': '狗', 'cat': '猫', 'red': '红', 'blue': '蓝',
            'green': '绿', 'white': '白', 'black': '黑', 'one': '一',
            'two': '二', 'three': '三', 'four': '四', 'five': '五',
            'six': '六', 'seven': '七', 'eight': '八', 'nine': '九',
            'ten': '十', 'yes': '是', 'no': '不', 'please': '请',
            'sorry': '对不起', 'excuse': ' excuse', 'me': '我', 'help': '帮助',
            'need': '需要', 'want': '想要', 'like': '喜欢', 'love': '爱',
            'hate': '恨', 'think': '想', 'know': '知道', 'understand': '明白',
            'learn': '学习', 'study': '学习', 'read': '读', 'write': '写',
            'speak': '说', 'listen': '听', 'see': '看', 'find': '找',
            'buy': '买', 'sell': '卖', 'give': '给', 'take': '拿',
            'come': '来', 'go': '去', 'start': '开始', 'stop': '停止',
            'open': '开', 'close': '关', 'make': '做', 'create': '创造'
        }
    
    def _load_translation_rules(self):
        """Load translation rules from processed data"""
        rules = self.file_handler.load_compressed_data(self.config.RULES_PATH)
        if not rules:
            return self._create_basic_dictionary()
        return rules
    
    def _create_basic_dictionary(self):
        """Create basic fallback dictionary"""
        return {
            'word_translations': {
                'hello': {'你好': 10}, 'hi': {'你好': 10},
                'how': {'怎么': 10}, 'are': {'是': 10}, 'you': {'你': 10},
                'what': {'什么': 10}, 'is': {'是': 10}, 'your': {'你的': 10},
                'name': {'名字': 10}, 'thank': {'谢谢': 10}, 'good': {'好': 10},
                'morning': {'早上': 10}, 'i': {'我': 10}, 'love': {'爱': 10},
                'old': {'老': 5, '年纪': 5}, 'where': {'哪里': 10}, 'time': {'时间': 10},
                'the': {'': 10}, 'a': {'': 10}, 'an': {'': 10},
                'this': {'这个': 10}, 'that': {'那个': 10}, 'my': {'我的': 10},
                'me': {'我': 10}, 'he': {'他': 10}, 'she': {'她': 10}, 'it': {'它': 10},
                'we': {'我们': 10}, 'they': {'他们': 10}
            },
            'phrase_translations': {}
        }
    
    def decode(self, encoded_structure):
        """Convert encoded structure to Chinese sentence"""
        # First check for known patterns
        pattern_translation = self._check_known_patterns(encoded_structure['tokens'])
        if pattern_translation:
            return pattern_translation
        
        # Then translate individual words
        word_translations = self._translate_words(encoded_structure['tokens'])
        ordered_translations = self._apply_grammar_rules(word_translations, encoded_structure)
        chinese_sentence = self._construct_sentence(ordered_translations, encoded_structure)
        
        return chinese_sentence
    
    def _check_known_patterns(self, tokens):
        """Check if the sentence matches any known patterns"""
        sentence_text = ' '.join(tokens).lower()
        
        # Check exact matches first
        exact_matches = {
            'how are you': '你好吗？',
            'what is your name': '你叫什么名字？', 
            'thank you': '谢谢',
            'good morning': '早上好',
            'good afternoon': '下午好', 
            'good evening': '晚上好',
            'good night': '晚安',
            'i love you': '我爱你',
            'how old are you': '你多大了？',
            'what time is it': '现在几点？',
            'where is the bathroom': '洗手间在哪里？',
            'can you help me': '你能帮我吗？',
            'do you speak english': '你会说英语吗？',
            'nice to meet you': '很高兴认识你',
            'see you tomorrow': '明天见',
            'i am hungry': '我饿了',
            'how much does this cost': '这个多少钱？',
            'i don\'t understand': '我不明白',
            'please speak slowly': '请说慢一点',
            'where do you live': '你住在哪里？',
            'what do you do': '你是做什么工作的？'
        }
        
        for pattern, translation in exact_matches.items():
            if pattern in sentence_text:
                return translation
        
        return None
    
    def _translate_words(self, english_tokens):
        """Translate individual words using extracted rules"""
        translations = []
        
        for token in english_tokens:
            # First try learned translations
            if token in self.translation_rules['word_translations']:
                chinese_options = self.translation_rules['word_translations'][token]
                # Get the most frequent translation
                best_translation = max(chinese_options.items(), key=lambda x: x[1])[0]
                translations.append((token, best_translation))
            # Then try fallback dictionary
            elif token in self.fallback_dictionary:
                translations.append((token, self.fallback_dictionary[token]))
            else:
                # Unknown word - keep in English but mark as unknown
                translations.append((token, f"[{token}]"))
        
        return translations
    
    def _apply_grammar_rules(self, word_translations, encoded_structure):
        """Apply Chinese grammar rules to word order"""
        sentence_type = encoded_structure['sentence_type']
        chinese_words = [trans[1] for trans in word_translations if trans[1] and trans[1] != '[UNK]']
        
        # Remove articles and unnecessary words for Chinese
        chinese_words = [word for word in chinese_words if not word.startswith('[') or len(word) > 3]
        
        # Basic Chinese grammar rules
        if sentence_type == 'question':
            # For questions, often end with 吗
            if not any('吗' in word for word in chinese_words) and not any('什么' in word for word in chinese_words):
                if chinese_words and not chinese_words[-1].endswith('？'):
                    chinese_words.append('吗？')
                else:
                    chinese_words.append('吗？')
            elif chinese_words and not chinese_words[-1].endswith('？'):
                chinese_words[-1] += '？'
        
        return chinese_words
    
    def _construct_sentence(self, chinese_words, encoded_structure):
        """Construct proper Chinese sentence"""
        if not chinese_words:
            return "无法翻译"
            
        # Chinese doesn't use spaces between words
        sentence = ''.join(chinese_words)
        
        # Clean up any remaining English words in brackets
        import re
        sentence = re.sub(r'\[(\w+)\]', r'\1', sentence)
        
        return sentence