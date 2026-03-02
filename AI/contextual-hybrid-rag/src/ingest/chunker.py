def chunk_sections(text:str):
    chunks = []
    current_section = None
    buffer = []

    for line in text.splitlines():
        if line.startswith("##"):
            if buffer:
                chunks.append({
                    "section":current_section,
                    "text":"\n".join(buffer).strip()
                })
                buffer = [] 
            current_section = line.replace("##", "").strip()
        elif line and not line.startswith('#'):
            buffer.append(line)
    
    if buffer:
        chunks.append({
            "section": current_section,
            "text": "\n".join(buffer).strip()
        })
    return chunks