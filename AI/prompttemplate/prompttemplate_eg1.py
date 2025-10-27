from langchain.prompts import PromptTemplate

# Step 1: Define a template with variables
template = "You are helpful AI.Summarize the book {book_name} in {num_points} bullet points."

# Step 2: Create a PromptTemplate object
prompt = PromptTemplate(
    input_variables = ['book_name','num_points'],
    template = template,
)

# Step 3: Fill the template with values
final_prompt = prompt.format(book_name = "The 7 habits Higly Effective People",num_points=7)

print(final_prompt)