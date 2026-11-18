# debug_dataset.py
import pandas as pd

def debug_dataset():
    """Debug what's actually in the dataset"""
    dataset_file = "datasets/opensubtitles_final_enhanced.csv"
    df = pd.read_csv(dataset_file)
    
    print("🔍 DEBUGGING DATASET:")
    print(f"Total entries: {len(df)}")
    
    # Look for 'hi' and related entries
    print("\n🔎 Searching for 'hi' and variations:")
    hi_entries = df[df['english'].str.contains('hi', case=False, na=False)]
    
    if len(hi_entries) > 0:
        print(f"Found {len(hi_entries)} entries with 'hi':")
        for _, row in hi_entries.iterrows():
            print(f"  '{row['english']}' -> '{row['chinese']}'")
    else:
        print("❌ No 'hi' entries found!")
    
    # Check exact matches
    print("\n🔎 Exact matches:")
    exact_matches = ['hi', 'Hi', 'HI', 'hello', 'Hello']
    for phrase in exact_matches:
        matches = df[df['english'] == phrase]
        if len(matches) > 0:
            print(f"✅ '{phrase}': '{matches.iloc[0]['chinese']}'")
        else:
            print(f"❌ '{phrase}': NOT FOUND")

if __name__ == "__main__":
    debug_dataset()