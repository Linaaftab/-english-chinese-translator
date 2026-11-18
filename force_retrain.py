# force_retrain.py
import pandas as pd
import os
import sys

def force_retrain_translator():
    """Completely retrain the translator with the updated dataset"""
    
    # Clear any cached modules
    if 'main' in sys.modules:
        del sys.modules['main']
    
    # Import fresh
    from main import EnglishChineseTranslator
    
    # Create new translator instance (this will load old rules first)
    print("🔄 Creating new translator instance...")
    translator = EnglishChineseTranslator()
    
    # Force retrain on the updated dataset
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    print(f"🚀 Force retraining on: {dataset_file}")
    
    # Check if dataset exists and show what's in it
    if os.path.exists(dataset_file):
        df = pd.read_csv(dataset_file)
        print(f"📊 Dataset has {len(df)} sentences")
        
        # Check if our capitalized phrases are there
        capitalized_phrases = ["Hi", "Hello", "Thank you", "Thanks", "How are you"]
        print("🔍 Checking for capitalized phrases in dataset:")
        for phrase in capitalized_phrases:
            matches = df[df['english'] == phrase]
            if len(matches) > 0:
                print(f"✅ '{phrase}' found: '{matches.iloc[0]['chinese']}'")
            else:
                print(f"❌ '{phrase}' NOT FOUND in dataset")
    else:
        print("❌ Dataset file not found!")
        return None
    
    # Now retrain
    success = translator.train(dataset_file)
    
    if success:
        print("🎉 Retraining completed successfully!")
        return translator
    else:
        print("❌ Retraining failed")
        return None

def comprehensive_test(translator):
    """Run a comprehensive test of all phrases"""
    print("\n" + "="*50)
    print("🧪 COMPREHENSIVE TRANSLATION TEST")
    print("="*50)
    
    test_phrases = [
        # Basic greetings
        "hi", "Hi", "HI", "hello", "Hello", "HELLO",
        "hey", "Hey",
        
        # Thank you variations
        "thanks", "Thanks", "thank you", "Thank you", "Thank You",
        
        # Questions
        "how are you", "How are you", "How are you?", "how are you?",
        "what is this", "What is this", "What is this?", "what is this?",
        "where is the bathroom", "Where is the bathroom", "Where is the bathroom?", "where is the bathroom?",
        
        # Love
        "i love you", "I love you", "I love you!", "i love you!",
        
        # Time greetings
        "good morning", "Good morning", "Good Morning",
        "good afternoon", "Good afternoon", "Good Afternoon", 
        "good evening", "Good evening", "Good Evening",
        "good night", "Good night", "Good Night",
        
        # Basic responses
        "yes", "Yes", "no", "No", "okay", "Okay", "OK",
        "please", "Please", "sorry", "Sorry",
    ]
    
    results = []
    for phrase in test_phrases:
        result = translator.translate(phrase)
        
        # Check if translation failed (returned original text)
        if result.lower() == phrase.lower():
            status = "❌ FAIL"
        else:
            status = "✅ PASS"
        
        results.append((phrase, result, status))
        print(f"{status} '{phrase}' → '{result}'")
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY:")
    total = len(results)
    passed = sum(1 for _, _, status in results if status == "✅ PASS")
    failed = total - passed
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    print(f"📈 Success rate: {(passed/total)*100:.1f}%")
    
    # Show failed ones
    if failed > 0:
        print("\n🔍 FAILED TRANSLATIONS:")
        for phrase, result, status in results:
            if status == "❌ FAIL":
                print(f"   '{phrase}' → '{result}'")

if __name__ == "__main__":
    translator = force_retrain_translator()
    
    if translator:
        comprehensive_test(translator)
        
        print("\n🎉 TRANSLATOR IS READY FOR USE!")
        print("\n💡 Usage examples:")
        print("   from main import EnglishChineseTranslator")
        print("   translator = EnglishChineseTranslator()")
        print("   print(translator.translate('Hello'))")
        print("   translator.interactive_translation()")