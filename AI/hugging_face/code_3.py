from transformers import pipeline
"""
# 1. Sentiment Analysis
classifier = pipeline("sentiment-analysis",framework="pt")
result = classifier("I love the movie 1917 for cinematography and sound desing")
print(result)
"""
"""
# 2. Text Generation
generator = pipeline("text-generation",model='gpt2')
result = generator("The Star Wars next movie",max_length=30,num_return_sequences=1)
print(result[0]['generated_text'])
"""
# 3. Named Entity Recognition (NER)
ner = pipeline("ner",aggregation_strategy="simple")
result =  ner("My name is Kenobi and I live in Tatooine")
print(result)