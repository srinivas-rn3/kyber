def split_sections(text: str):
    sections = []
    current = "Main"
    buffer = []

    for line in text.splitlines():
        if line.startswith("## "):
            sections.append((current, "\n".join(buffer)))
            current = line.replace("## ", "").strip()
            buffer = []
        else:
            buffer.append(line)

    sections.append((current, "\n".join(buffer)))
    return sections


def split_paragraphs(text: str):
    return [p.strip() for p in text.split("\n\n") if len(p.strip()) > 80]
