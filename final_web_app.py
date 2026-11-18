# final_web_app.py
from flask import Flask, render_template, request, jsonify
from main import EnglishChineseTranslator
import json
import datetime
import os

app = Flask(__name__)

# Initialize and train translator
print("🚀 Initializing English-Chinese Translator...")
translator = EnglishChineseTranslator()

# Check if we need to train
if not translator.loaded:
    print("📚 Training translator on final enhanced dataset...")
    dataset_path = "datasets/opensubtitles_final_enhanced.csv"
    if os.path.exists(dataset_path):
        success = translator.train(dataset_path)
        if success:
            print(f"✅ Training completed! Loaded {len(translator.translation_rules)} rules")
        else:
            print("❌ Training failed! Using existing rules if any.")
    else:
        print("❌ Dataset not found, but continuing with existing rules...")
else:
    print(f"✅ Translator ready! Loaded {len(translator.translation_rules)} rules")

# Store translation history
translation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    english_text = data.get('text', '').strip()
    
    if not english_text:
        return jsonify({'error': 'No text provided'})
    
    try:
        # Translate
        chinese_translation = translator.translate(english_text)
        
        # Store in history
        translation_record = {
            'english': english_text,
            'chinese': chinese_translation,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        translation_history.append(translation_record)
        
        # Keep only last 50 translations
        if len(translation_history) > 50:
            translation_history.pop(0)
        
        return jsonify({
            'english': english_text,
            'chinese': chinese_translation,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/history')
def get_history():
    return jsonify({'history': translation_history[::-1]})

@app.route('/stats')
def get_stats():
    stats = {
        'total_translations': len(translation_history),
        'unique_phrases': len(set(t['english'].lower() for t in translation_history)),
        'translator_rules': len(translator.translation_rules) if translator.loaded else 0,
        'translator_ready': translator.loaded
    }
    return jsonify(stats)

@app.route('/test')
def test_translations():
    """Test endpoint to verify translations are working"""
    test_phrases = ["hello", "thank you", "how are you", "i love you"]
    results = []
    
    for phrase in test_phrases:
        translation = translator.translate(phrase)
        results.append({
            'english': phrase,
            'chinese': translation,
            'working': translation.lower() != phrase.lower()
        })
    
    return jsonify({'test_results': results})

if __name__ == '__main__':
    print("🌐 Starting English-Chinese Translator Web App...")
    print("📍 Open: http://localhost:5000 in your browser")
    print("🧪 Test page: http://localhost:5000/test")
    print("🛑 Press CTRL+C to stop the server")
    print("-" * 50)
    app.run(debug=True)