# test_final_fix.py
import pandas as pd
import os
import sys

def test_fixed_translator():
    """Test the translator after fixing the training filter"""
    
    # Clear cache
    if os.path.exists("translation_rules.csv"):
        os.remove("translation_rules.csv")
    
    if 'main' in sys.modules:
        del sys.modules['main']
    
    from main import EnglishChineseTranslator
    
    print("🚀 TESTING FIXED TRANSLATOR")
    print("=" * 50)
    
    # Train on the fixed dataset
    translator = EnglishChineseTranslator()
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"  # Use original dataset
    
    print("🎯 Training with fixed filter...")
    success = translator.train(dataset_file)
    
    if success:
        print("🎉 Training completed with fixed filter!")
        
        # Test ALL previously problematic phrases
        print("\n🧪 COMPREHENSIVE TEST OF ALL PHRASES:")
        print("-" * 50)
        
        test_phrases = [
            # Previously failing short words
            "hi", "Hi", "HI", "no", "No", "OK", "ok",
            # Previously working phrases
            "hello", "Hello", "thank you", "Thank you", 
            "how are you", "How are you?", "what is this", "What is this?",
            "where is the bathroom", "Where is the bathroom?", 
            "I love you", "i love you", "I love you!", "i love you!",
            "good morning", "Good morning", "good night", "Good night",
            "thanks", "Thanks", "please", "Please", "sorry", "Sorry"
        ]
        
        all_working = True
        results = []
        
        for phrase in test_phrases:
            result = translator.translate(phrase)
            
            # Check if translation worked
            if result.lower() == phrase.lower():
                status = "❌ FAIL"
                all_working = False
            else:
                status = "✅ PASS"
            
            results.append((phrase, result, status))
            print(f"{status} '{phrase}' → '{result}'")
        
        # Summary
        print("\n" + "="*50)
        print("📊 FINAL RESULTS:")
        total = len(results)
        passed = sum(1 for _, _, status in results if status == "✅ PASS")
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        print(f"📈 Success rate: {(passed/total)*100:.1f}%")
        
        if all_working:
            print("\n🎉 🎉 🎉 100% SUCCESS RATE! 🎉 🎉 🎉")
            print("🌟 Your English-Chinese translator is now PERFECT!")
        else:
            print("\n⚠️ Some phrases still need attention")
            
        return translator, all_working
    
    else:
        print("❌ Training failed")
        return None, False

def interactive_demo(translator):
    """Interactive demo of the working translator"""
    print("\n" + "="*60)
    print("🚀 INTERACTIVE DEMO - TRY YOUR OWN PHRASES!")
    print("=" * 60)
    print("Type phrases to translate (or 'quit' to exit):")
    
    while True:
        try:
            user_input = input("\n🔤 Enter English: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thank you for testing the translator!")
                break
            
            if user_input:
                result = translator.translate(user_input)
                print(f"🀄 Chinese: {result}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # First, let's verify the main.py fix is applied
    print("🔧 VERIFYING MAIN.PY FIX")
    print("=" * 50)
    
    # Read main.py to check if fix is applied
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'len(english) > 2' in content:
            print("❌ main.py still has the old filter: 'len(english) > 2'")
            print("💡 Please update main.py line in train() method:")
            print("   FROM: if english and chinese and len(english) > 2:")
            print("   TO:   if english and chinese and len(english) >= 1:")
            exit()
        elif 'len(english) >= 1' in content:
            print("✅ main.py has the fixed filter: 'len(english) >= 1'")
        else:
            print("⚠️ Could not find filter in main.py")
    
    # Test the translator
    translator, success = test_fixed_translator()
    
    if success and translator:
        interactive_demo(translator)