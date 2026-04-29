from langchain_community.vectorstores import FAISS
from src.llm import llm, embeddings
from src.prompts import DOC_SUMMARY, SECTION_SUMMARY
from src.parser import split_sections, split_paragraphs
from src.contextual_chunk import build_contextual_chunk

def ingest(text: str):
    doc_summary = llm.invoke(
        DOC_SUMMARY.format(doc=text)
    ).content

    chunks = []

    for section_title, section_body in split_sections(text):
        paragraphs = split_paragraphs(section_body)
        if not paragraphs:
            continue

        section_summary = llm.invoke(
            SECTION_SUMMARY.format(section=section_body)
        ).content

        for para in paragraphs:
            chunk = build_contextual_chunk(
                doc_summary, section_summary, para
            )
            chunks.append(chunk)

    return FAISS.from_texts(chunks, embeddings)
