import os
os.environ['HF_HOME'] = r'D:\AI\hugging_face' # Or any other drive with space

# 2. NOW import Hugging Face libraries
from transformers import pipeline,AutoModel,AutoTokenizer
from datasets import load_dataset

# 3. Your code here...
classifier = pipeline("sentiment-analysis")
print(classifier("I love Starwars!"))