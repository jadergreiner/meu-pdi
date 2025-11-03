#!/usr/bin/env python3
import re

def fix_markdown_formatting(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add blank line before LA-004 heading
    pattern = r'(---)\n(### \*\*LA-004: Commits Diretos na Branch Main\*\*)'
    replacement = r'\1\n\n\2'

    fixed_content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print("Fixed markdown formatting for LA-004 heading")

if __name__ == "__main__":
    fix_markdown_formatting('planning/backlog-por-portais.md')