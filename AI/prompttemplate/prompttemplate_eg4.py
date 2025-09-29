from langchain.prompts import PromptTemplate

template = "Summarize  the following text in {num_points} bullet points:\n\n{text}"

prompt = PromptTemplate(
    input_variables =['num_points','text'],
    template = template
)

final_prompt = prompt.format(num_points = 3,
text = "Artificial Intelligence is transforming industries by enabling automation, improving decision-making, and creating new possibilities in healthcare, finance, and education."
)
print(final_prompt)