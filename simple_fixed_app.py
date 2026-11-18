# simple_fixed_app.py
from flask import Flask, request, jsonify
from main import EnglishChineseTranslator
import os

app = Flask(__name__)

print("🚀 Starting Simple Fixed English-Chinese Translator...")

# Initialize translator
translator = EnglishChineseTranslator()
print(f"✅ Translator ready with {len(translator.translation_rules)} rules")

@app.after_request
def after_request(response):
    """Add CORS headers manually without flask-cors"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>English-Chinese Translator</title>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 50px; 
                background: #f5f5f5;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
            }
            textarea {
                width: 100%;
                height: 100px;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                margin-bottom: 15px;
            }
            button {
                background: #3498db;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
            }
            button:hover {
                background: #2980b9;
            }
            .result {
                margin-top: 20px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 4px solid #3498db;
                min-height: 100px;
            }
            .loading {
                display: none;
                text-align: center;
                color: #3498db;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔤 English → 🀄 Chinese Translator</h1>
            <p style="text-align: center; color: #666;">Final Project - AI Translation System</p>
            
            <textarea id="textInput" placeholder="Enter English text here... (e.g., Hello, Thank you, How are you?)"></textarea>
            <button onclick="translateText()">Translate Now →</button>
            
            <div class="loading" id="loading">⏳ Translating...</div>
            
            <div class="result" id="result">
                <strong>Translation will appear here...</strong>
            </div>
        </div>

        <script>
            function translateText() {
                const text = document.getElementById('textInput').value.trim();
                const resultDiv = document.getElementById('result');
                const loading = document.getElementById('loading');
                
                if (!text) {
                    resultDiv.innerHTML = '<span style="color: red;">Please enter some text to translate</span>';
                    return;
                }

                // Show loading
                loading.style.display = 'block';
                resultDiv.innerHTML = '';

                // Simple fetch with error handling
                fetch('/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({text: text})
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    loading.style.display = 'none';
                    
                    if (data.success) {
                        resultDiv.innerHTML = 
                            '<div style="margin-bottom: 15px;">' +
                            '<strong>🔤 English:</strong><br>' +
                            '<div style="background: white; padding: 10px; border-radius: 3px; margin-top: 5px; border: 1px solid #ddd;">' + data.english + '</div>' +
                            '</div>' +
                            '<div>' +
                            '<strong>🀄 Chinese:</strong><br>' +
                            '<div style="background: white; padding: 10px; border-radius: 3px; margin-top: 5px; font-size: 1.2em; border: 1px solid #ddd;">' + data.chinese + '</div>' +
                            '</div>';
                    } else {
                        resultDiv.innerHTML = '<span style="color: red;">Error: ' + (data.error || 'Unknown error') + '</span>';
                    }
                })
                .catch(error => {
                    loading.style.display = 'none';
                    resultDiv.innerHTML = '<span style="color: red;">Error: Could not connect to server. Make sure the Python app is running.</span>';
                    console.error('Error:', error);
                });
            }

            // Allow Enter key to translate
            document.getElementById('textInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && e.ctrlKey) {
                    translateText();
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/translate', methods=['POST', 'OPTIONS'])
def translate_text():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received', 'success': False})
        
        english_text = data.get('text', '').strip()
        
        if not english_text:
            return jsonify({'error': 'No text provided', 'success': False})
        
        # Translate
        chinese_translation = translator.translate(english_text)
        
        return jsonify({
            'english': english_text,
            'chinese': chinese_translation,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False})

@app.route('/test')
def test():
    # Quick test
    test_text = "hello"
    translation = translator.translate(test_text)
    return f"Test: '{test_text}' → '{translation}'"

if __name__ == '__main__':
    print("🌐 Open: http://localhost:5000")
    print("🧪 Test: http://localhost:5000/test")
    print("🛑 Press CTRL+C to stop")
    app.run(debug=True, port=5000)