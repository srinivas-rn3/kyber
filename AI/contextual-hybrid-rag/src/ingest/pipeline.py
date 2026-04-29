from ingest.context_llm import create_section_context

def contextualize(doc_title, chunks, llm):
    results = []

    for i, c in enumerate(chunks):
        summary = create_section_context(
            doc_title, c['section'], c['text'], llm
        )
        
        results.append({
            "chunk_id": f"{doc_title}_{i}",
            "section": c["section"],
            "raw_text": c["text"],
            "contextual_text": f"""
Document: {doc_title}
Section: {c["section"]}
Section summary: {summary}

Content:
{c["text"]}
""".strip()
        })
    return results
