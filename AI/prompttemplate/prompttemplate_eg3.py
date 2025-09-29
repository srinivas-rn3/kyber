from langchain.prompts import PromptTemplate

template = "Translate the following sentences into {language}:\n\n{sentences}"

prompt = PromptTemplate(
    input_variable = ['language','sentences'],
    template = template
)
final_prompt = prompt.format(language='French',sentences="Good Morning,how are you")
print(final_prompt)

