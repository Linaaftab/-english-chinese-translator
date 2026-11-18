import os
import sys

print(" DIAGNOSTIC CHECK")
print("=" * 50)
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"Files in directory: {[f for f in os.listdir('.') if f.endswith('.py')]}")

print(f"\n main.py exists: {os.path.exists('main.py')}")

print("\n TESTING IMPORT...")
try:
    from main import EnglishChineseTranslator
    print("✅ SUCCESS: EnglishChineseTranslator imported!")
    translator = EnglishChineseTranslator()
    print("✅ SUCCESS: Translator instance created!")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
