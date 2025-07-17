import re
import json
from typing import List, Dict
import glob 

def extract_chunks(tex_text: str) -> List[Dict[str, str]]:
    """
    Parses LaTeX content and extracts sections, text blocks, and equations.
    Returns a list of dictionaries with keys: section, text, equation
    """
    sections = re.split(r'\\section\*?\{(.+?)\}', tex_text)
    chunks = []

    for i in range(1, len(sections), 2):
        section_title = sections[i].strip()
        content = sections[i + 1]

        # Extract equations from equation and align environments
        eq_pattern = r'\\begin\{(?:equation|align)\*?\}(.*?)\\end\{(?:equation|align)\*?\}'
        equations = re.findall(eq_pattern, content, re.DOTALL)
        text_blocks = re.split(eq_pattern, content, flags=re.DOTALL)

        # Combine text blocks and equations into chunks
        eq_idx = 0
        for idx, text in enumerate(text_blocks):
            # Even index = text, odd = equation (because of how re.split works with capture group)
            if idx % 2 == 0:
                chunk = {
                    "section": section_title,
                    "text": re.sub(r'\\\w+', '', text.strip()),
                    "equation": equations[eq_idx].strip() if eq_idx < len(equations) else ""
                }
                chunks.append(chunk)
            else:
                eq_idx += 1

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
