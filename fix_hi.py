# fix_hi.py
import pandas as pd

def fix_hi_translation():
    """Fix the 'hi' translation"""
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    
    df = pd.read_csv(dataset_file)
    
    # Find and update the 'hi' entry
    hi_index = df[df['english'].str.lower() == 'hi'].index
    if len(hi_index) > 0:
        df.loc[hi_index, 'chinese'] = '你好'
        print("✅ Fixed 'hi' translation")
    else:
        # Add it if not found
        new_row = pd.DataFrame({'english': ['hi'], 'chinese': ['你好']})
        df = pd.concat([new_row, df], ignore_index=True)
        print("✅ Added 'hi' translation")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['english'], keep='first')
    df.to_csv(dataset_file, index=False, encoding='utf-8')
    print(f"💾 Updated dataset: {len(df)} sentences")
    
    # Retrain
    from main import EnglishChineseTranslator
    translator = EnglishChineseTranslator()
    translator.train(dataset_file)
    print("🔄 Retrained translator")
    
    # Test
    print("🧪 Final test:")
    print(f"🔤 'Hi' → 🀄 '{translator.translate('Hi')}'")
    print(f"🔤 'hi' → 🀄 '{translator.translate('hi')}'")

if __name__ == "__main__":
    fix_hi_translation()