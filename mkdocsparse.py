"""
This script converts an MkDocs site into a LaTeX document using the md2tex engine with custom pre- and post-processing to handle MkDocs-specific content.
Functions:
    preprocess_mkdocs_markdown(md_content: str) -> str:
        Preprocesses MkDocs-material content tabs by removing indentation from admonitions-style mkdocs-material blocks and formatting headers.
    postprocess_tex(tex: str) -> str:
        Post-processes the LaTeX content by replacing tabs with spaces and handling internal links.
    convert_section(md_file_path: str, filename: str) -> str:
        Converts a markdown file to a LaTeX section, adding labels for cross-references.
    make_chapter(chapter_title: str, chapter_dir: str) -> str:
        Converts all markdown files in a directory to a LaTeX chapter, handling media files.
Usage:
    Run the script with the following command:
    python mkdocsparse.py <mkdocs_folder> <tex_outpath> <frontmatter_outpath>
    Arguments:
        mkdocs_folder: Path to the MkDocs directory.
        tex_outpath: Path to the main output LaTeX file.
        frontmatter_inpath: Path to the preface markdown file.
    Flags:
        --convert-to-pdf: Convert the processed site into PDF form after converting to TeX.
Example:
    python mkdocsparse.py /path/to/mkdocs /path/to/output/mainmatter.tex /path/to/output/frontmatter.tex
"""
import os
import sys
import re
from os.path import join, isdir
import argparse
import yaml

# Add the md2tex submodule folder to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'md2tex'))

from md2tex import convert as convert_md2tex

BASE_URL = 'https://sparkletop.github.io/'
IGNORED_MD_FILES_LIST = 'ignored_MD_files.txt'
SOLOED_MD_FILES_LIST = 'soloed_MD_files.txt'
PREFACE_MD_FILE = './tex/preface.md'

def get_matching_brackets(code: str):
    r"""
    Finds and returns the substring of the input code contained by an 
    outer pair of matching opening and closing curly brackets `{...}`, assuming that any inner pairs of brackets which are opened are closed again.
    
    Escaped brackets `\{` and `\}` are ignored.
    
    :param code: The input string containing code with curly brackets.
    :return: The substring from the start of the input code up to and including
             the matching closing bracket.
    """
    pos = 0
    numOpened = 0
    hasOpened = False
    for c in code:
        if c == '{' and code[pos-1] != "\\":
            numOpened += 1
            hasOpened = True
        elif c == '}' and code[pos-1] != "\\":
            numOpened -= 1
            if numOpened == 0 and hasOpened:
                # we found the closing bracket
                pos += 1
                break
        pos += 1
    return code[:pos]

def preprocess_mkdocs_markdown(md_content: str):
    # Processes one markdown page at a time

    # preprocess mkdocs-material content tabs (remove indentation)
    # matches and processes sections that begin with '=== xyz' followed by indented content or empty lines
    content_tabs_blocks = re.finditer(r"^(===.*$)(?:\n(^\s*$|^ {4}.*$))+", md_content, re.M)
    for block in content_tabs_blocks:
        code = block.group(0)
        code = re.sub(r"^=== \"(.+)\"$", r"*\1*", code, flags=re.M)
        code = re.sub(r"^    ", "", code, flags=re.M)
        md_content = md_content.replace(block.group(0), code)
    
    # process markdown frontmatter
    frontmatter = re.match(r"^--- *\n(.+?)(?:^(?:\.{3}|-{3}))", md_content, re.MULTILINE | re.DOTALL)
    if frontmatter:
        yml = yaml.load(frontmatter.group(1), yaml.FullLoader)
        doctype = yml['tags'][0]   # assuming the first tag is the document type
        prefix = '' if doctype not in ['Øvelser', 'Cheat sheets'] else '!!!!!NEWPAGE!!!!!' + '\n' + '!!!!!' + doctype + '!!!!!'
        md_content = md_content.replace(frontmatter.group(0), prefix)
    
    # turn 'abstract' admonition into plain text intro
    abstract = re.search(r"^(?:!{3}|\?{3}) abstract.+?\n((?:\s.*\n+)+?)^#", md_content, re.MULTILINE)
    if abstract:
        intro = abstract.group(1)
        intro = '\n'.join([line.strip() for line in intro.split('\n')])

        md_content = md_content.replace(abstract.group(0), intro + '#')
    
    return md_content

def postprocess_tex(tex: str):
    # Processes the full tex document contents as one string
    # replace tabs with spaces
    tex = tex.replace("\t", "    ")
    
    tex = re.sub("!!!!!NEWPAGE!!!!!", r'\\newpage', tex)
    tex = re.sub("!!!!!RESETPAGECOLOR!!!!!", r'\\pagecolor{normal}', tex)
    tex = re.sub("!!!!!Øvelser!!!!!", r'\\pagecolor{exercise}', tex)
    tex = re.sub("!!!!!Cheat sheets!!!!!", r'\\pagecolor{cheatsheet}', tex)
    tex = re.sub(r"!!!!!faHeadphones\*!!!!!", r'\\faHeadphones*', tex)
    tex = re.sub("!!!!!faLink!!!!!", r'\\faLink', tex)
    
    # Show section coloring in preface
    tex = tex.replace('\\item[Cheat sheets]', '\\item[\\colorbox{cheatsheet}{Cheat sheets}]')
    tex = tex.replace('\\item[Øvelser]', '\\item[\\colorbox{exercise}{Øvelser}]')

    # update figure paths
    tex = tex.replace("../media/", "../docs/media/")

    # change link to web edition in preface
    tex = tex.replace('href{https://sparkletop.github.io/./tex/preface/', 'href{https://sparkletop.github.io/')

    # add sound icon to relevant code block captions
    audio_examples = re.finditer(r"\\caption{(.+?)}(?:.*\n){,5}(%AUDIO_FILE:(.+?.ogg))", tex, re.M)
    for example in audio_examples:
        match = example.group(0)
        old_icon_code = re.search(r"(\\faLink)(?!\\faHeadphones)", match, re.M).group(1)
        new_icon_code = old_icon_code + "\\enskip\\faHeadphones*"
        tex = tex.replace(match, match.replace(old_icon_code, new_icon_code))
    
    # Replace \mintinline with \texttt in footnotes
    fnotes = re.finditer(r"\\footnote{.+}", tex, re.MULTILINE)
    for f in fnotes:
        match = f.group(0)
        old_fnote = get_matching_brackets(match)
        new_fnote = re.sub(r"\\mintinline{.+?}{(.+?)}", r"\\texttt{\1}", old_fnote)
        tex = tex.replace(old_fnote, new_fnote)
    
    # deal with internal links
    links = re.finditer(r"(?<!!)\[([^@\n\{\}]+?)\]\((.*?)\)", tex)
    for link in links:
        # Clean up link to only have filename
        filename = re.sub(r"\\#.+$", "", link[2]) # remove anchor, subsection labelling not implemented yet...
        filename = re.sub(r"^\.\./.+/", "", filename)

        if filename.endswith(".md"):
            # This is a link to other markdown document, so we assume there
            # is a \label in the corresponding LaTeX section corresponding to file name
            tex = tex.replace(link[0], link[1] + r" (se afsnit \ref{" + filename + r"})")
        else:
            print(f"Unsupported link: {link}, leaving as is...")
    return tex

def convert_section(md_file_path: str):
    # assume that each section is a markdown file
    print(f"Processing document: {md_file_path}")
    md_content = ""
    with open(md_file_path, mode="r") as file:
        md_content = file.read()
        md_content = preprocess_mkdocs_markdown(md_content)
    
    tex = convert_md2tex(
        md_content,
        document_class="article",
        minted_language="./sc_lexer.py:SuperColliderLexer",
        override_language=True
    )

    # add a label to each section for use in cross references
    md_filename = os.path.basename(md_file_path)
    tex = re.sub(
        r"(\\section{.+?}\n)",
        r"\1\\label{" + md_filename + r"}\n",
        tex
    )

    # for each code block, add a link to the web version
    code_block_captions = re.finditer(r"\\caption\{(.+?)\}\n\\end\{listing\}", tex)
    for num, block in enumerate(code_block_captions):
        segment = block.group(0)
        section_page_url = md_file_path.replace('./docs/', '').replace('.md', '/')
        url = BASE_URL + section_page_url + "\#__code_" + str(num)
        tex_link = '\\href{' + url + '}{\\faLink}'
        caption_text = block.group(1)
        new_caption_text = caption_text + '\\hfill' + tex_link
        new_segment = segment.replace(caption_text, new_caption_text)
        tex = tex.replace(segment, new_segment)

    return tex

def make_chapter(chapter_title, md_files, ignore_files, solo_files):
    # loop over the given .md files, convert to tex, and return the string

    # remove "1. " etc. from the chapter title, since LaTeX handles the numbering for us
    chapter_title = re.sub(r'^\d+\.\s+', '', chapter_title)
    chapter_tex = f"\\chapter{{{chapter_title}}}\n\\label{{chap:{chapter_title}}}\n!!!!!RESETPAGECOLOR!!!!!"

    for file_path in md_files:
        filename = os.path.basename(file_path)
        if len(solo_files) > 0:
            # Solo files have been specified
            if filename in solo_files:
                chapter_tex = chapter_tex + "\n" + convert_section(file_path)
        elif filename not in ignore_files:
            # This is a normal build, process files not in ignore list
            chapter_tex = chapter_tex + "\n" + convert_section(file_path)            

    return chapter_tex

if __name__ == "__main__":
    """
    Convert the sources for an mkdocs site to a LaTeX file
    """
    parser = argparse.ArgumentParser(description="Convert mkdocs site into a LaTeX document using the md2tex engine + some custom pre- and postprocessing to deal specifically with mkdocs content.")
    parser.add_argument("--mkdocs_folder", type=str, default="./", help="Path to the mkdocs root directory (where 'docs/' is a subdirectory)")
    parser.add_argument("--tex_outpath", type=str, default="./tex/content.tex", help="Path to the main output TeX file")
    
    # Parse the arguments
    args = parser.parse_args()
    docs_folder = join(args.mkdocs_folder, 'docs')
    tex_outpath = args.tex_outpath

    # Read the list of ignored markdown files
    with open(IGNORED_MD_FILES_LIST, 'r') as ignore_file:
        ignore_files = ignore_file.read().split('\n')
    with open(SOLOED_MD_FILES_LIST, 'r') as solo_file:
        solo_files = solo_file.read().split('\n')
        if solo_files == ['']:
            solo_files = []
    tex = ''

    # Process preface first
    tex = tex + make_chapter('Forord', [PREFACE_MD_FILE], ignore_files, solo_files)

    tex = tex + "\n\n\\mainmatter\n"

    # Get the navigation from mkdocs.yml
    mkdocs_config_file = join(args.mkdocs_folder, 'mkdocs.yml')
    with open(mkdocs_config_file, 'r') as m:
        mkdocs_config = yaml.load(m.read(), yaml.FullLoader)
        if 'nav' in mkdocs_config.keys():
            # Follow the structure of mkdocs.yml nav list
            nav = mkdocs_config['nav']
            nav.pop(0) # ignore index page

            # Turn web page top hierarchy categories into chapters
            for top_level_dict in nav:
                chapter_title = list(top_level_dict.keys())[0]                
                md_files = []
                for page in list(top_level_dict.values())[0]:
                    if isinstance(page, dict):  # Page has been given 
                        md_file = list(page.values())[0]
                    else:
                        md_file = page
                    md_files.append(join(docs_folder, md_file))
                tex = tex + '\n' + make_chapter(chapter_title, md_files, ignore_files, solo_files)
        else:
            # There is no nav specified, so we walk the subdirectories of
            # the docs directory and create chapters for each one
            chapter_dirs = [d for d in os.listdir(docs_folder) if isdir(join(docs_folder, d))]
            chapter_dirs.sort()
            for chapter_dir in chapter_dirs:
                md_files = [f for f in os.listdir(join(docs_folder, chapter_dir)) if f.endswith('.md')]
                if not md_files:
                    continue
                else:
                    md_files.sort()
                    tex = tex + '\n' + make_chapter(chapter_dir, md_files, ignore_files, solo_files)

    tex = postprocess_tex(tex)

    with open(tex_outpath, 'w') as file:
        file.write(tex)
        print(f"{tex_outpath} generated successfully.")
    
    exit(0)