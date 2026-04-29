from langchain_core.prompts import PromptTemplate

DOC_SUMMARY = PromptTemplate.from_template(
    "Summarize this document in 1–2 sentences for retrieval:\n{doc}"
)

SECTION_SUMMARY = PromptTemplate.from_template(
    "Explain what this section covers in one sentence:\n{section}"
)

PARA_INTENT = PromptTemplate.from_template(
    "Write ONE sentence starting with 'This paragraph explains ...':\n{paragraph}"
)
