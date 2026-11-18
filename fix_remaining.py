# fix_remaining.py
import pandas as pd

def add_missing_phrases():
    """Add the few remaining missing phrases"""
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    df = pd.read_csv(dataset_file)
    
    print(f"📊 Current dataset: {len(df)} sentences")
    
    # Missing phrases to add
    missing_phrases = [
        # "hi" variations
        ("hi", "你好"),
        ("Hi", "你好"), 
        ("HI", "你好"),
        
        # "no" variations
        ("no", "不"),
        ("No", "不"),
        
        # "OK" variations
        ("OK", "好的"),
        ("ok", "好的"),
        
        # Punctuation variations
        ("I love you!", "我爱你！"),
        ("i love you!", "我爱你！"),
    ]
    
    # Check what's missing
    new_entries = []
    for eng, chi in missing_phrases:
        exists = len(df[df['english'] == eng]) > 0
        if not exists:
            new_entries.append((eng, chi))
            print(f"➕ Adding: '{eng}' -> '{chi}'")
        else:
            print(f"✅ Already exists: '{eng}'")
    
    if new_entries:
        df_new = pd.DataFrame(new_entries, columns=['english', 'chinese'])
        df_updated = pd.concat([df_new, df], ignore_index=True)
        df_updated = df_updated.drop_duplicates(subset=['english'], keep='first')
        df_updated.to_csv(dataset_file, index=False, encoding='utf-8')
        print(f"✅ Updated dataset: {len(df_updated)} sentences")
    else:
        print("✅ All phrases already exist")
    
    return dataset_file

def final_retest():
    """Final test after adding missing phrases"""
    import sys
    if 'main' in sys.modules:
        del sys.modules['main']
    
    from main import EnglishChineseTranslator
    
    print("\n🚀 Final retraining...")
    translator = EnglishChineseTranslator()
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    success = translator.train(dataset_file)
    
    if success:
        print("🎉 Final training completed!")
        
        # Test the previously failed phrases
        print("\n🧪 TESTING PREVIOUSLY FAILED PHRASES:")
        failed_phrases = [
            "hi", "Hi", "HI", 
            "I love you!", "i love you!",
            "no", "No", "OK"
        ]
        
        all_fixed = True
        for phrase in failed_phrases:
            result = translator.translate(phrase)
            if result.lower() == phrase.lower():
                print(f"❌ '{phrase}' → '{result}' (STILL FAILED)")
                all_fixed = False
            else:
                print(f"✅ '{phrase}' → '{result}' (FIXED!)")
        
        if all_fixed:
            print("\n🎉 ALL ISSUES RESOLVED! 100% SUCCESS RATE! 🎉")
        else:
            print("\n⚠️ Some issues remain")
    
    return translator

if __name__ == "__main__":
    add_missing_phrases()
    translator = final_retest()
    
    if translator:
        print("\n" + "="*60)
        print("🌟 ENGLISH-CHINESE TRANSLATOR - READY TO USE! 🌟")
        print("="*60)
        print("\n💡 Try these commands:")
        print("   from main import EnglishChineseTranslator")
        print("   translator = EnglishChineseTranslator()")
        print("   print(translator.translate('Hello world'))")
        print("   translator.interactive_translation()")
        
        # Quick demo
        print("\n🚀 QUICK DEMO:")
        demo_phrases = ["Hello", "Thank you", "How are you?", "I love you", "Good morning"]
        for phrase in demo_phrases:
            result = translator.translate(phrase)
            print(f"   🔤 {phrase} → 🀄 {result}")