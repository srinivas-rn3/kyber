from transformers import pipeline

classifier = pipeline("sentiment-analysis",framework="pt")
result = classifier("I love Learning AI with Hugging Face!!!")
print(result)