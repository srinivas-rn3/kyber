def create_section_context(doc_title, section_name, section_text, llm):
    prompt = f"""
You are generating context for document retrieval.

Document title: {doc_title}
Section name: {section_name}

Summarize the following section in ONE sentence
that explains what this section is about.

Text:
{section_text}
"""
    return llm.invoke(prompt)
