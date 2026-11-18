# minimal_training.py
import pandas as pd
import os
import sys

print("🚀 Starting minimal training...")

try:
    from main import EnglishChineseTranslator
    print("✅ Import successful!")
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit(1)

def minimal_training():
    """Train on just 2,000 sentences for quick testing"""
    print("🎯 Minimal training with OpenSubtitles...")
    
    en_file = "datasets/OpenSubtitles.en-zh_CN.en"
    zh_file = "datasets/OpenSubtitles.en-zh_CN.zh_CN"
    
    # Check if files exist
    print(f"🔍 English file: {os.path.exists(en_file)}")
    print(f"🔍 Chinese file: {os.path.exists(zh_file)}")
    
    if not os.path.exists(en_file) or not os.path.exists(zh_file):
        print("❌ Dataset files not found!")
        return False
    
    pairs = []
    
    with open(en_file, 'r', encoding='utf-8') as f_en, \
         open(zh_file, 'r', encoding='utf-8') as f_zh:
        
        for i, (en_line, zh_line) in enumerate(zip(f_en, f_zh)):
            if i >= 2000:
                break
            
            if i % 500 == 0:
                print(f"Reading line {i}/2000...")
            
            en_clean = en_line.strip()
            zh_clean = zh_line.strip()
            
            if en_clean and zh_clean and len(en_clean) > 5 and len(zh_clean) > 2:
                pairs.append((en_clean, zh_clean))
    
    # Save minimal dataset
    df = pd.DataFrame(pairs, columns=['english', 'chinese'])
    output_file = "datasets/opensubtitles_minimal.csv"
    
    # Create datasets directory if needed
    os.makedirs('datasets', exist_ok=True)
    
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"✅ Minimal dataset created: {len(df)} sentences")
    print(f"💾 Saved to: {output_file}")
    
    # Show samples
    print("\n📖 Sample sentences:")
    for i in range(min(3, len(df))):
        print(f"  EN: {df.iloc[i]['english']}")
        print(f"  CN: {df.iloc[i]['chinese']}")
        print()
    
    # Train
    translator = EnglishChineseTranslator()
    print("🚀 Training on minimal dataset...")
    success = translator.train(output_file)
    
    if success:
        print("🎉 Training completed!")
        
        # Test
        print("\n🧪 Testing translations:")
        tests = [
            "Hello", 
            "Thank you", 
            "How are you?",
            "What is this?",
            "Where is the bathroom?",
            "I love you"
        ]
        for test in tests:
            result = translator.translate(test)
            print(f"🔤 {test} → 🀄 {result}")
    else:
        print("❌ Training failed")
    
    return success

if __name__ == "__main__":
    minimal_training()