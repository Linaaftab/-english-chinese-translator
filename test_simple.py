import os

print("=== Simple System Test ===")

# Check critical files
files = [
    "config/settings.py",
    "utils/file_handler.py",
    "utils/preprocessor.py", 
    "utils/tokenizer.py",
    "data_processing/dataset_processor.py",
    "models/encoder.py",
    "models/decoder.py",
    "main.py",
    "datasets/sample_dataset.csv"
]

for file in files:
    exists = os.path.exists(file)
    status = "✅ EXISTS" if exists else "❌ MISSING"
    print(f"{status}: {file}")

# Test dataset content
if os.path.exists("datasets/sample_dataset.csv"):
    with open("datasets/sample_dataset.csv", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"✅ Dataset has {len(lines)} lines")
        print("First 3 lines:")
        for i, line in enumerate(lines[:3]):
            print(f"  {i+1}: {line.strip()}")
else:
    print("❌ Dataset file missing")

print("=== Test Complete ===")