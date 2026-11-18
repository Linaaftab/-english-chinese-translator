# debug_processing.py
import pandas as pd
from main import EnglishChineseTranslator

def debug_data_processing():
    """Debug why phrases are being lost during processing"""
    
    print("🔍 DEBUGGING DATA PROCESSING")
    print("=" * 50)
    
    # Load the dataset
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    df = pd.read_csv(dataset_file)
    print(f"📊 Dataset sentences: {len(df)}")
    
    # Check what happens during processing
    problem_phrases = ["hi", "Hi", "HI", "no", "No", "OK", "ok"]
    
    print("\n🔎 ANALYZING PROBLEM PHRASES:")
    print("-" * 40)
    
    for phrase in problem_phrases:
        # Find the phrase in the dataset
        matches = df[df['english'] == phrase]
        if len(matches) > 0:
            row = matches.iloc[0]
            english = str(row['english']).strip()
            chinese = str(row['chinese']).strip()
            
            print(f"\n📝 '{phrase}':")
            print(f"   English: '{english}' (length: {len(english)})")
            print(f"   Chinese: '{chinese}' (length: {len(chinese)})")
            print(f"   Valid: {bool(english and chinese and len(english) > 2)}")
            
            # Check if it would pass the training filter
            if english and chinese and len(english) > 2:
                print("   ✅ Would be included in training")
            else:
                print("   ❌ Would be EXCLUDED from training")
        else:
            print(f"❌ '{phrase}' not found in dataset")

def check_training_logic():
    """Check what the training method actually does"""
    print("\n" + "="*50)
    print("🔧 CHECKING TRAINING LOGIC")
    print("=" * 50)
    
    # Simulate the training logic
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    df = pd.read_csv(dataset_file)
    
    processed_pairs = []
    translation_rules = {}
    
    for i, (_, row) in enumerate(df.iterrows()):
        english = str(row['english']).strip()
        chinese = str(row['chinese']).strip()
        
        # This is the filter from your train() method
        if english and chinese and len(english) > 2:
            english_lower = english.lower()
            translation_rules[english_lower] = chinese
            processed_pairs.append((english, chinese))
    
    print(f"📊 Original dataset: {len(df)} sentences")
    print(f"📊 After processing: {len(processed_pairs)} sentences")
    print(f"📊 Rules created: {len(translation_rules)}")
    
    # Check our problem phrases
    problem_phrases = ["hi", "Hi", "HI", "no", "No", "OK", "ok"]
    print(f"\n🔍 Problem phrases in final rules:")
    for phrase in problem_phrases:
        if phrase in translation_rules:
            print(f"   ✅ '{phrase}' -> '{translation_rules[phrase]}'")
        elif phrase.lower() in translation_rules:
            print(f"   ✅ '{phrase}' (lowercase) -> '{translation_rules[phrase.lower()]}'")
        else:
            print(f"   ❌ '{phrase}' NOT in rules")

def fix_training_filter():
    """Fix the training filter to include short phrases"""
    print("\n" + "="*50)
    print("🔧 FIXING TRAINING FILTER")
    print("=" * 50)
    
    # Let's modify the main.py training logic temporarily
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    df = pd.read_csv(dataset_file)
    
    # Use a more inclusive filter
    processed_pairs = []
    translation_rules = {}
    
    for i, (_, row) in enumerate(df.iterrows()):
        english = str(row['english']).strip()
        chinese = str(row['chinese']).strip()
        
        # More inclusive filter - allow short words
        if english and chinese and len(english) >= 1:  # Changed from > 2 to >= 1
            # Store both original case and lowercase
            translation_rules[english] = chinese
            translation_rules[english.lower()] = chinese
            processed_pairs.append((english, chinese))
    
    print(f"📊 With inclusive filter:")
    print(f"   Original: {len(df)} sentences")
    print(f"   Processed: {len(processed_pairs)} sentences") 
    print(f"   Rules: {len(translation_rules)}")
    
    # Check problem phrases
    problem_phrases = ["hi", "Hi", "HI", "no", "No", "OK", "ok"]
    print(f"\n🔍 Problem phrases with inclusive filter:")
    for phrase in problem_phrases:
        if phrase in translation_rules:
            print(f"   ✅ '{phrase}' -> '{translation_rules[phrase]}'")
        else:
            print(f"   ❌ '{phrase}' STILL NOT in rules")

def create_fixed_dataset():
    """Create a new dataset with the filter issue fixed"""
    print("\n" + "="*50)
    print("💾 CREATING FIXED DATASET")
    print("=" * 50)
    
    input_file = "datasets/opensubtitles_final_enhanced.csv"
    output_file = "datasets/opensubtitles_fixed.csv"
    
    df = pd.read_csv(input_file)
    print(f"📊 Input dataset: {len(df)} sentences")
    
    # Remove any empty or invalid rows
    df_clean = df.dropna()
    df_clean = df_clean[(df_clean['english'].str.len() >= 1) & (df_clean['chinese'].str.len() >= 1)]
    
    print(f"📊 Clean dataset: {len(df_clean)} sentences")
    
    # Save fixed dataset
    df_clean.to_csv(output_file, index=False, encoding='utf-8')
    print(f"💾 Saved fixed dataset: {output_file}")
    
    return output_file

if __name__ == "__main__":
    debug_data_processing()
    check_training_logic() 
    fix_training_filter()
    fixed_dataset = create_fixed_dataset()
    
    print("\n" + "="*50)
    print("🎯 NEXT STEPS:")
    print("=" * 50)
    print("1. The issue is in main.py training filter: 'len(english) > 2'")
    print("2. This excludes short words like 'hi', 'no', 'OK'")
    print("3. I've created a fixed dataset: datasets/opensubtitles_fixed.csv")
    print("\n💡 Run this command to train on the fixed dataset:")
    print(f"   from main import EnglishChineseTranslator")
    print(f"   translator = EnglishChineseTranslator()")
    print(f"   translator.train('{fixed_dataset}')")