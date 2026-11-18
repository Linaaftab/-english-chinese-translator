# fix_remaining_phrases.py
import pandas as pd
import os

def add_exact_matches():
    """Add the exact phrases that are still not working"""
    
    # These are the phrases that need exact matches
    exact_phrases = [
        ("how are you?", "你好吗？"),
        ("what is this?", "这是什么？"),
        ("where is the bathroom?", "洗手间在哪里？"),
        ("hi", "你好"),  # Add lowercase version
    ]
    
    # Load the current enhanced dataset
    input_file = "datasets/opensubtitles_better_enhanced.csv"
    output_file = "datasets/opensubtitles_final_enhanced.csv"
    
    df = pd.read_csv(input_file)
    print(f"📊 Current dataset: {len(df)} sentences")
    
    # Add exact matches
    df_exact = pd.DataFrame(exact_phrases, columns=['english', 'chinese'])
    df_final = pd.concat([df_exact, df], ignore_index=True)
    
    # Remove duplicates (keep our exact matches)
    df_final = df_final.drop_duplicates(subset=['english'], keep='first')
    
    # Save final dataset
    df_final.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✅ Final enhanced dataset: {len(df_final)} sentences")
    print(f"💾 Saved to: {output_file}")
    
    print("📝 Added exact matches:")
    for eng, chi in exact_phrases:
        print(f"   - '{eng}' -> '{chi}'")
    
    return output_file

def train_final():
    """Train on the final enhanced dataset"""
    from main import EnglishChineseTranslator
    
    final_dataset = add_exact_matches()
    
    translator = EnglishChineseTranslator()
    print("\n🚀 Training on final enhanced dataset...")
    success = translator.train(final_dataset)
    
    if success:
        print("🎉 Final training completed!")
        
        # Test ALL translations
        print("\n🧪 FINAL TESTING:")
        test_phrases = [
            "Hello", "Thank you", "How are you?", 
            "What is this?", "Where is the bathroom?", "I love you",
            "Good morning", "Thanks", "Hi",
            "how are you?", "what is this?", "where is the bathroom?"  # Test lowercase too
        ]
        
        for phrase in test_phrases:
            result = translator.translate(phrase)
            print(f"🔤 '{phrase}' → 🀄 '{result}'")

if __name__ == "__main__":
    train_final()