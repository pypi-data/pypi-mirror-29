"""Evaluate {{expr}} in Markdown source and fenced code.

If expr starts with '#', expr is not evaluated: {{#abc}} -> {{abc}}

If expr starts with '^', expr is converted into HTML after execution.

Above settings is default values and configurable.
"""

import re

import nbformat

from .config import config
from .exporter import inline_export, run_and_export


def replace(match) -> str:
    convert = 'pheasant.jupyter.convert_inline'
    source = match.group(1)

    if source.startswith(config['inline_ignore_character']):
        return match.group().replace(source, source[1:])
    elif '=' in source:
        return source

    if source.startswith(config['inline_html_character']):
        source = source[1:]
        output = 'html'
    else:
        output = 'markdown'

    if ';' in source:
        sources = source.split(';')
        source = '_pheasant_dummy'
        sources[-1] = f'{source} = {sources[-1]}'
        sources = '\n'.join(sources)
        cell = nbformat.v4.new_code_cell(sources)
        run_and_export(cell, inline_export)

    return f'{convert}({source}, output="{output}")'


def preprocess_code(source: str) -> str:
    return re.sub(config['inline_pattern'], replace, source)


def preprocess_markdown(source: str) -> str:
    if source[:3] in ['```', '~~~', '<di']:  # escaped or already converted.
        return source

    def replace_and_run(match):
        source = match.group(1)
        if source.startswith(config['inline_ignore_character']):
            return match.group().replace(source, source[1:])

        source = replace(match)
        cell = nbformat.v4.new_code_cell(source)
        return run_and_export(cell, inline_export)

    return re.sub(config['inline_pattern'], replace_and_run, source)
