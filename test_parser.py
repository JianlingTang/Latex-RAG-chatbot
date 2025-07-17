import re
import json
from typing import List, Dict
import glob 

def extract_chunks(tex_text: str) -> List[Dict[str, str]]:
    import re
    chunks = []
    sections = re.split(r'\\section\*?\{(.+?)\}', tex_text)

    for i in range(1, len(sections), 2):
        section_title = sections[i].strip()
        content = sections[i + 1]

        pattern = r'\\begin\{(equation|align)\*?\}(.*?)\\end\{\1\*?\}'
        pos = 0
        for match in re.finditer(pattern, content, re.DOTALL):
            start, end = match.span()
            pre_text = content[pos:start].strip()
            equation = match.group(2).strip()

            if pre_text:
                chunks.append({
                    "section": section_title,
                    "text": re.sub(r'\\\w+', '', pre_text),
                    "equation": ""
                })

            chunks.append({
                "section": section_title,
                "text": "",
                "equation": equation
            })
            pos = end

        # any leftover trailing text
        if pos < len(content):
            tail_text = content[pos:].strip()
            if tail_text:
                chunks.append({
                    "section": section_title,
                    "text": re.sub(r'\\\w+', '', tail_text),
                    "equation": ""
                })

    return chunks

def save_chunks_to_json(chunks: List[Dict[str, str]], output_path: str = "chunks.json") -> None:
    with open(output_path, 'w') as f:
        json.dump(chunks, f, indent=2)

if __name__ == "__main__":
    tex_files = glob.glob("*.tex")
    for texfile in tex_files:
        with open(texfile, "r") as f:
            tex_content = f.read()
        parsed_chunks = extract_chunks(tex_content)
        save_chunks_to_json(parsed_chunks)
