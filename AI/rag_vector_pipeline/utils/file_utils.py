import os
import hashlib
import json

MANIFEST = r"C:\Users\srini\OneDrive\kiro\kyber\AI\rag_vector_pipeline\manifest.json"

# Generate hash of a file (used to detect changes)
def get_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# Load record of processed files
def load_manifest():
    if not os.path.exists(MANIFEST):
        return {}
    return json.load(open(MANIFEST, "r"))

# Save record of processed files
def save_manifest(manifest):
    json.dump(manifest, open(MANIFEST, "w"), indent=4)

# Return only new or changed files
def filter_new_files(files):
    manifest = load_manifest()
    new_files = []

    for file in files:
        h = get_file_hash(file)

        if file not in manifest or manifest[file] != h:
            new_files.append(file)
            manifest[file] = h

    save_manifest(manifest)
    return new_files
