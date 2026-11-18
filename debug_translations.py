# debug_translations.py
import pandas as pd
from main import EnglishChineseTranslator

def debug_translations():
    print("🔍 DEBUGGING TRANSLATIONS")
    print("=" * 50)
    
    # Check the saved translation rules
    rules_file = "translation_rules.csv"
    if not os.path.exists(rules_file):
        print("❌ translation_rules.csv not found!")
        return
    
    # Load and inspect the rules
    df = pd.read_csv(rules_file)
    print(f"📊 Rules file has {len(df)} entries")
    print("\n📖 First 10 entries:")
    print(df.head(10))
    
    # Check what's actually in the translator's rules
    translator = EnglishChineseTranslator()
    print(f"\n🔍 Translator has {len(translator.translation_rules)} rules loaded")
    
    # Test specific words
    test_words = ["hello", "thank", "you", "how", "are", "what", "where", "love"]
    print("\n🧪 Testing word matches:")
    for word in test_words:
        if word in translator.translation_rules:
            print(f"✅ '{word}' -> {translator.translation_rules[word]}")
        else:
            print(f"❌ '{word}' not found in rules")
    
    # Test exact phrase matches
    test_phrases = ["hello", "thank you", "how are you", "i love you"]
    print("\n🧪 Testing phrase matches:")
    for phrase in test_phrases:
        if phrase in translator.translation_rules:
            print(f"✅ '{phrase}' -> {translator.translation_rules[phrase]}")
        else:
            print(f"❌ '{phrase}' not found in rules")

if __name__ == "__main__":
    import os
    debug_translations()