from langchain.prompts import PromptTemplate

template = "Answer the follwing question in 2 sentences:\nQuestion:{question}"

prompt =PromptTemplate(
    input_variables = ['question'],
    template = template,
)

final_prompt =  prompt.format(question="Why is sky is blue?")
print(final_prompt)