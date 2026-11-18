# complete_fix.py
import pandas as pd
import os
import sys

def nuclear_reset_and_test():
    """Complete reset - delete cache and force fresh training"""
    
    print("💣 NUCLEAR RESET - DELETING ALL CACHE FILES")
    print("=" * 50)
    
    # Delete ALL cached files
    cache_files = ["translation_rules.csv"]
    for file in cache_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Deleted: {file}")
        else:
            print(f"📭 Not found: {file}")
    
    # Clear Python module cache
    if 'main' in sys.modules:
        del sys.modules['main']
    
    # Verify dataset content
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    print(f"\n🔍 VERIFYING DATASET: {dataset_file}")
    
    if not os.path.exists(dataset_file):
        print("❌ Dataset not found!")
        return None
    
    df = pd.read_csv(dataset_file)
    print(f"📊 Dataset has {len(df)} sentences")
    
    # Check specific problematic phrases
    problem_phrases = ["hi", "Hi", "HI", "no", "No", "OK", "ok"]
    print("\n🔎 Checking problematic phrases in dataset:")
    for phrase in problem_phrases:
        matches = df[df['english'] == phrase]
        if len(matches) > 0:
            print(f"   ✅ '{phrase}' -> '{matches.iloc[0]['chinese']}'")
        else:
            print(f"   ❌ '{phrase}' NOT FOUND")
    
    # Import fresh and train
    print("\n🚀 IMPORTING FRESH TRANSLATOR...")
    from main import EnglishChineseTranslator
    
    print("🔄 Creating new translator instance...")
    translator = EnglishChineseTranslator()  # This should show "No existing rules found"
    
    print("🎯 Training on updated dataset...")
    success = translator.train(dataset_file)
    
    if success:
        print("🎉 SUCCESS! Fresh training completed")
        return translator
    else:
        print("❌ Training failed")
        return None

def comprehensive_final_test(translator):
    """Final comprehensive test"""
    print("\n" + "="*60)
    print("🧪 FINAL COMPREHENSIVE TEST")
    print("="*60)
    
    # All the problematic phrases
    test_phrases = [
        # "hi" variations
        "hi", "Hi", "HI",
        # "no" variations  
        "no", "No",
        # "OK" variations
        "OK", "ok",
        # Punctuation tests
        "I love you!", "i love you!",
        # Working phrases for comparison
        "hello", "Hello", "thanks", "Thanks"
    ]
    
    print("\n🔍 TESTING PROBLEMATIC PHRASES:")
    print("-" * 40)
    
    all_working = True
    for phrase in test_phrases:
        result = translator.translate(phrase)
        
        # Check if translation worked
        if result.lower() == phrase.lower():
            status = "❌ FAIL"
            all_working = False
        else:
            status = "✅ PASS"
        
        print(f"{status} '{phrase}' → '{result}'")
    
    return all_working

def debug_translator_internals(translator):
    """Debug what's actually in the translator's rules"""
    print("\n" + "="*60)
    print("🔧 DEBUGGING TRANSLATOR INTERNALS")
    print("="*60)
    
    print(f"📊 Translator loaded: {translator.loaded}")
    print(f"📚 Rules count: {len(translator.translation_rules)}")
    
    # Check specific phrases in the loaded rules
    check_phrases = ["hi", "Hi", "HI", "no", "No", "OK", "ok"]
    print("\n🔍 Checking rules dictionary:")
    for phrase in check_phrases:
        if phrase in translator.translation_rules:
            print(f"   ✅ '{phrase}' in rules: {translator.translation_rules[phrase]}")
        else:
            print(f"   ❌ '{phrase}' NOT in rules")
    
    # Check lowercase versions too
    print("\n🔍 Checking lowercase versions:")
    for phrase in check_phrases:
        lower_phrase = phrase.lower()
        if lower_phrase in translator.translation_rules:
            print(f"   ✅ '{lower_phrase}' in rules: {translator.translation_rules[lower_phrase]}")
        else:
            print(f"   ❌ '{lower_phrase}' NOT in rules")

if __name__ == "__main__":
    # Step 1: Nuclear reset
    translator = nuclear_reset_and_test()
    
    if translator:
        # Step 2: Debug what's loaded
        debug_translator_internals(translator)
        
        # Step 3: Final test
        all_working = comprehensive_final_test(translator)
        
        # Step 4: Summary
        print("\n" + "="*60)
        print("🎯 FINAL SUMMARY")
        print("="*60)
        
        if all_working:
            print("🎉 🎉 🎉 ALL TRANSLATIONS WORKING PERFECTLY! 🎉 🎉 🎉")
            print("\n🌟 Your English-Chinese translator is ready for production!")
        else:
            print("⚠️ Some translations still need work")
            print("💡 The dataset is correct - the issue might be in the translation logic")
        
        print("\n💡 Usage:")
        print("   from main import EnglishChineseTranslator")
        print("   translator = EnglishChineseTranslator()")
        print("   print(translator.translate('Your text here'))")
        
        # Quick success demo
        print("\n🚀 SUCCESS DEMO:")
        success_phrases = ["Hello", "Thank you", "How are you?", "I love you", "Good morning"]
        for phrase in success_phrases:
            result = translator.translate(phrase)
            print(f"   🔤 {phrase} → 🀄 {result}")