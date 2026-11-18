# debug_app.py
from flask import Flask, request, jsonify
from main import EnglishChineseTranslator
import os

app = Flask(__name__)

print("🚀 Starting Debug English-Chinese Translator...")

# Initialize translator
translator = EnglishChineseTranslator()
print(f"✅ Translator ready with {len(translator.translation_rules)} rules")

@app.after_request
def after_request(response):
    """Add CORS headers manually"""
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
        <title>English-Chinese Translator - DEBUG</title>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background: #f5f5f5;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
                margin-bottom: 20px;
            }
            textarea {
                width: 100%;
                height: 80px;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                margin-bottom: 10px;
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
                margin-bottom: 10px;
            }
            button:hover {
                background: #2980b9;
            }
            button:active {
                background: #21618c;
                transform: scale(0.98);
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 4px solid #3498db;
                min-height: 80px;
            }
            .loading {
                display: none;
                text-align: center;
                color: #3498db;
                margin: 10px 0;
            }
            .debug {
                background: #2c3e50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                font-size: 12px;
                margin-top: 10px;
                max-height: 200px;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔤 English → 🀄 Chinese Translator</h1>
            <p style="text-align: center; color: #666; margin-bottom: 20px;">DEBUG MODE - Click test buttons first</p>
            
            <!-- Test Buttons -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                <button style="background: #27ae60;" onclick="testTranslation('hello')">Test: Hello</button>
                <button style="background: #e74c3c;" onclick="testTranslation('thank you')">Test: Thank You</button>
            </div>
            
            <textarea id="textInput" placeholder="Or type your own English text here..."></textarea>
            <button onclick="translateText()" id="translateBtn">Translate Now →</button>
            
            <div class="loading" id="loading">⏳ Translating...</div>
            
            <div class="result" id="result">
                <strong>Translation will appear here...</strong>
            </div>
            
            <div class="debug" id="debug">
                Debug info will appear here...
            </div>
        </div>

        <script>
            let debugLog = [];
            
            function log(message) {
                const timestamp = new Date().toLocaleTimeString();
                const logMessage = `[${timestamp}] ${message}`;
                debugLog.push(logMessage);
                
                // Keep only last 10 messages
                if (debugLog.length > 10) {
                    debugLog.shift();
                }
                
                // Update debug display
                document.getElementById('debug').innerHTML = debugLog.join('<br>');
                console.log(logMessage);
            }
            
            function testTranslation(text) {
                document.getElementById('textInput').value = text;
                translateText();
            }
            
            function translateText() {
                const text = document.getElementById('textInput').value.trim();
                const resultDiv = document.getElementById('result');
                const loading = document.getElementById('loading');
                const button = document.getElementById('translateBtn');
                
                log('Translate button clicked');
                
                if (!text) {
                    resultDiv.innerHTML = '<span style="color: red;">Please enter some text to translate</span>';
                    log('No text entered');
                    return;
                }

                log('Starting translation for: "' + text + '"');
                
                // Show loading, disable button
                loading.style.display = 'block';
                button.disabled = true;
                button.textContent = 'Translating...';
                resultDiv.innerHTML = '<strong>Processing...</strong>';

                // Simple fetch with detailed logging
                log('Sending POST request to /translate');
                
                fetch('/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({text: text})
                })
                .then(response => {
                    log('Response received. Status: ' + response.status);
                    if (!response.ok) {
                        throw new Error('HTTP error! status: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    log('JSON parsed successfully');
                    loading.style.display = 'none';
                    button.disabled = false;
                    button.textContent = 'Translate Now →';
                    
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
                        log('Translation successful: ' + data.english + ' → ' + data.chinese);
                    } else {
                        resultDiv.innerHTML = '<span style="color: red;">Error: ' + (data.error || 'Unknown error') + '</span>';
                        log('Translation failed: ' + (data.error || 'Unknown error'));
                    }
                })
                .catch(error => {
                    log('Fetch error: ' + error.message);
                    loading.style.display = 'none';
                    button.disabled = false;
                    button.textContent = 'Translate Now →';
                    resultDiv.innerHTML = '<span style="color: red;">Error: ' + error.message + '</span>';
                });
            }

            // Allow Enter key to translate
            document.getElementById('textInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && e.ctrlKey) {
                    translateText();
                }
            });

            // Initialize
            log('Page loaded successfully');
            log('Try clicking the test buttons first');
        </script>
    </body>
    </html>
    """

@app.route('/translate', methods=['POST', 'OPTIONS'])
def translate_text():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        print("📨 Translation request received")
        data = request.get_json()
        
        if not data:
            print("❌ No data received")
            return jsonify({'error': 'No data received', 'success': False})
        
        english_text = data.get('text', '').strip()
        print(f"📝 Translating: '{english_text}'")
        
        if not english_text:
            print("❌ No text provided")
            return jsonify({'error': 'No text provided', 'success': False})
        
        # Translate
        chinese_translation = translator.translate(english_text)
        print(f"✅ Translation: '{english_text}' → '{chinese_translation}'")
        
        return jsonify({
            'english': english_text,
            'chinese': chinese_translation,
            'success': True
        })
        
    except Exception as e:
        print(f"❌ Translation error: {str(e)}")
        return jsonify({'error': str(e), 'success': False})

if __name__ == '__main__':
    print("🌐 Open: http://localhost:5000")
    print("🔧 Debug mode enabled - check browser console and Python terminal")
    print("🛑 Press CTRL+C to stop")
    app.run(debug=True, port=5000)