#!/usr/bin/env python3
"""
Script para corrigir formatação markdown do backlog
"""

import re
import sys

def fix_markdown_formatting(file_path):
    """Corrige problemas comuns de formatação markdown"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fix headings that don't have blank lines before them
        if line.strip().startswith('#'):
            # Check if previous line exists and is not blank
            if i > 0 and lines[i-1].strip() != '' and not lines[i-1].strip().startswith('#'):
                # Add blank line before heading (unless it's a subheading after another heading)
                fixed_lines.append('')
            fixed_lines.append(line)
            # Add blank line after heading if next line is not blank and not another heading
            if i < len(lines)-1 and lines[i+1].strip() != '' and not lines[i+1].strip().startswith('#'):
                fixed_lines.append('')
        # Fix list items
        elif line.strip().startswith(('- ', '* ', '+ ')):
            # Check if previous line exists and is not blank or part of the same list
            if fixed_lines and fixed_lines[-1].strip() != '' and not fixed_lines[-1].strip().startswith(('- ', '* ', '+ ')):
                fixed_lines.append('')
            fixed_lines.append(line)
            # Check if this is the last item in a list (next line is not a list item or is blank)
            if i < len(lines)-1:
                next_line = lines[i+1]
                if next_line.strip() == '' or not next_line.strip().startswith(('- ', '* ', '+ ')):
                    # This is the end of the list, add blank line after
                    fixed_lines.append('')
        else:
            fixed_lines.append(line)
        i += 1

    # Join back and ensure ends with newline
    fixed_content = '\n'.join(fixed_lines)
    if not fixed_content.endswith('\n'):
        fixed_content += '\n'

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"Fixed formatting in {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python fix_markdown.py <arquivo.md>")
        sys.exit(1)

    fix_markdown_formatting(sys.argv[1])