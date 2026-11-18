# fix_capitalization.py
import pandas as pd

def fix_capitalization_issues():
    """Add capitalized versions of common phrases"""
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    df = pd.read_csv(dataset_file)
    
    print("🔍 Current dataset entries:")
    print(f"Total: {len(df)} sentences")
    
    # Phrases that need capitalized versions
    phrases_to_capitalize = [
        "hi", "hello", "thanks", "thank you", "how are you", 
        "what is this", "where is the bathroom", "i love you",
        "good morning", "good afternoon", "good evening", "good night"
    ]
    
    new_entries = []
    
    for phrase in phrases_to_capitalize:
        # Check if lowercase version exists
        lowercase_exists = len(df[df['english'].str.lower() == phrase.lower()]) > 0
        
        if lowercase_exists:
            # Get the Chinese translation from lowercase version
            lowercase_row = df[df['english'].str.lower() == phrase.lower()].iloc[0]
            chinese_translation = lowercase_row['chinese']
            
            # Add capitalized version
            capitalized_phrase = phrase.capitalize()
            
            # Check if capitalized version already exists
            capitalized_exists = len(df[df['english'] == capitalized_phrase]) > 0
            
            if not capitalized_exists:
                new_entries.append((capitalized_phrase, chinese_translation))
                print(f"➕ Adding: '{capitalized_phrase}' -> '{chinese_translation}'")
    
    # Add new entries to dataset
    if new_entries:
        df_new = pd.DataFrame(new_entries, columns=['english', 'chinese'])
        df_updated = pd.concat([df_new, df], ignore_index=True)
        
        # Remove duplicates (keep the new capitalized versions)
        df_updated = df_updated.drop_duplicates(subset=['english'], keep='first')
        
        df_updated.to_csv(dataset_file, index=False, encoding='utf-8')
        print(f"✅ Updated dataset: {len(df_updated)} sentences")
        print(f"💾 Added {len(new_entries)} capitalized phrases")
    else:
        print("✅ All capitalized versions already exist")
    
    return dataset_file

def test_fixed_translator():
    """Test the translator after fixing capitalization"""
    from main import EnglishChineseTranslator
    
    # Force reload by creating new instance
    translator = EnglishChineseTranslator()
    
    print("\n🧪 TESTING CAPITALIZED PHRASES:")
    test_phrases = [
        "Hi", "Hello", "Thank you", "Thanks", 
        "How are you?", "What is this?", "Where is the bathroom?",
        "I love you", "Good morning", "Good night"
    ]
    
    all_correct = True
    for phrase in test_phrases:
        result = translator.translate(phrase)
        expected_lower = phrase.lower()
        
        # Check if we got the original text back (translation failed)
        if result.lower() == phrase.lower():
            print(f"❌ '{phrase}' → '{result}' (FAILED - no translation found)")
            all_correct = False
        else:
            print(f"✅ '{phrase}' → '{result}'")
    
    if all_correct:
        print("\n🎉 ALL TRANSLATIONS WORKING PERFECTLY!")
    else:
        print("\n⚠️ Some translations still need work")

if __name__ == "__main__":
    fixed_dataset = fix_capitalization_issues()
    test_fixed_translator()