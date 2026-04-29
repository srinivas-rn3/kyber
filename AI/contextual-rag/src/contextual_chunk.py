from src.llm import llm
from src.prompts import PARA_INTENT

def build_contextual_chunk(doc_summary, section_summary, paragraph):
    intent = llm.invoke(
        PARA_INTENT.format(paragraph=paragraph)
    ).content

    return f"""
Document context: {doc_summary}
Section context: {section_summary}
Paragraph intent: {intent}
Content: {paragraph}
""".strip()
