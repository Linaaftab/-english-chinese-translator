# create_better_dataset.py
import pandas as pd
import os

def create_better_enhanced_dataset():
    """Create a better enhanced dataset with proper common phrases"""
    
    # More comprehensive common phrases
    common_phrases = [
        # Basic greetings
        ("hello", "你好"),
        ("hi", "你好"),
        ("hey", "嗨"),
        
        # Thank you variations
        ("thank you", "谢谢"),
        ("thanks", "谢谢"),
        ("thank you very much", "非常感谢"),
        ("thanks a lot", "多谢"),
        
        # How are you variations
        ("how are you", "你好吗"),
        ("how are you doing", "你怎么样"),
        ("how is it going", "最近怎么样"),
        
        # I love you variations
        ("i love you", "我爱你"),
        ("love you", "爱你"),
        
        # Good [time] variations
        ("good morning", "早上好"),
        ("good afternoon", "下午好"), 
        ("good evening", "晚上好"),
        ("good night", "晚安"),
        
        # Basic questions
        ("what is this", "这是什么"),
        ("what is that", "那是什么"),
        ("where is the bathroom", "洗手间在哪里"),
        ("where is the toilet", "厕所在哪里"),
        ("how much does this cost", "这个多少钱"),
        ("what is your name", "你叫什么名字"),
        ("my name is", "我的名字是"),
        
        # Basic responses
        ("yes", "是"),
        ("no", "不"),
        ("okay", "好的"),
        ("ok", "好的"),
        ("please", "请"),
        ("sorry", "对不起"),
        ("excuse me", "打扰一下"),
        
        # Common needs
        ("i don't understand", "我不明白"),
        ("can you help me", "你能帮我吗"),
        ("i need help", "我需要帮助"),
        ("where am i", "我在哪里"),
        
        # Food and drink
        ("water", "水"),
        ("food", "食物"),
        ("rice", "米饭"),
        ("tea", "茶"),
        ("coffee", "咖啡"),
        
        # Directions
        ("left", "左"),
        ("right", "右"),
        ("straight", "直走"),
        ("stop", "停"),
        
        # Emergency
        ("help", "救命"),
        ("emergency", "紧急情况"),
        ("police", "警察"),
        ("doctor", "医生"),
    ]
    
    # Load existing OpenSubtitles dataset
    input_file = "datasets/opensubtitles_minimal.csv"
    output_file = "datasets/opensubtitles_better_enhanced.csv"
    
    if not os.path.exists(input_file):
        print("❌ OpenSubtitles dataset not found. Run minimal_training.py first.")
        return
    
    df_existing = pd.read_csv(input_file)
    print(f"📊 Loaded existing dataset: {len(df_existing)} sentences")
    
    # Create common phrases dataframe
    df_common = pd.DataFrame(common_phrases, columns=['english', 'chinese'])
    
    # Enhanced dataset: common phrases FIRST, then OpenSubtitles
    df_enhanced = pd.concat([df_common, df_existing], ignore_index=True)
    
    # Remove any duplicates (keep the first occurrence - which will be our common phrases)
    df_enhanced = df_enhanced.drop_duplicates(subset=['english'], keep='first')
    
    # Save enhanced dataset
    df_enhanced.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✅ Better enhanced dataset created: {len(df_enhanced)} sentences")
    print(f"💾 Saved to: {output_file}")
    print(f"📝 Added {len(common_phrases)} common phrases")
    
    return output_file

def train_on_better_dataset():
    """Train on the better enhanced dataset"""
    from main import EnglishChineseTranslator
    
    better_dataset = create_better_enhanced_dataset()
    
    if better_dataset:
        translator = EnglishChineseTranslator()
        print("\n🚀 Training on better enhanced dataset...")
        success = translator.train(better_dataset)
        
        if success:
            print("🎉 Training completed!")
            
            # Test translations
            print("\n🧪 TESTING TRANSLATIONS:")
            test_phrases = [
                "Hello", "Thank you", "How are you?", 
                "What is this?", "Where is the bathroom?", "I love you",
                "Good morning", "Thanks", "Hi"
            ]
            
            for phrase in test_phrases:
                result = translator.translate(phrase)
                print(f"🔤 '{phrase}' → 🀄 '{result}'")

if __name__ == "__main__":
    train_on_better_dataset()