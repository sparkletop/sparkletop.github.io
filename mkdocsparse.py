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

chapter_titles = []

AUDIO_EXAMPLE_BASE_URL = 'https://sparkletop.github.io/Ressourcer/lydeksempler'
AUDIO_EXAMPLE_FILE_PATH = './docs/Ressourcer/lydeksempler.md'
IGNORED_MD_FILES_LIST = 'ignored_MD_files.txt'
SOLOED_MD_FILES_LIST = 'soloed_MD_files.txt'

def preprocess_mkdocs_markdown(md_content: str):
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
        print(doctype)
    
    return md_content

def postprocess_tex(tex: str):
    # replace tabs with spaces
    tex = tex.replace("\t", "    ")

    tex = re.sub("!!!!!NEWPAGE!!!!!", r'\\newpage', tex)
    tex = re.sub("!!!!!RESETPAGECOLOR!!!!!", r'\\nopagecolor', tex)
    tex = re.sub("!!!!!Øvelser!!!!!", r'\\pagecolor{exercise}', tex)
    tex = re.sub("!!!!!Cheat sheets!!!!!", r'\\pagecolor{cheatsheet}', tex)
    

    # update figure paths
    tex = tex.replace("../media/", "../docs/media/")

    # deal with internal links
    links = re.finditer(r"(?<!!)\[(.*?)\]\((.*?)\)", tex)
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
    
    new_section = convert_md2tex(
        md_content,
        document_class="article",
        minted_language="./sc_lexer.py:SuperColliderLexer",
        override_language=True
    )

    # add a label to each section for use in cross references
    label = os.path.basename(md_file_path)
    new_section = re.sub(
        r"(\\section{.+?}\n)",
        r"\1\\label{" + label + r"}\n",
        new_section
    )

    return new_section

def generate_audio_examples_page(tex: str):
    # generate aux file to get code block numbers
    print("Generating .aux files to find code block numbering")
    os.chdir('./tex/')
    os.system('lualatex -draftmode template.tex')
    os.chdir('..')

    # find audio files + caption text
    audio_examples_info = []
    audio_examples = re.finditer(r"\\caption{(.+?)}(?:.*\n){,5}(%AUDIO_FILE:(.+?.ogg))", tex, re.M)
    for example in audio_examples:
        path = example.group(3)
        comment_substring = example.group(2)
        caption = example.group(1)
        slugified_caption = re.sub(r"[^a-zA-Z0-9_]+", '-', caption).lower()
        
        # insert LaTeX link to sound example
        url = AUDIO_EXAMPLE_BASE_URL + r'\#' + slugified_caption
        # here we need to find the minted code block's number from the .aux file
        example_link = r" - \href{" + url + r"}{Lydeksempel}"
        tex = tex.replace(caption, caption + example_link) # add a link to the caption
        tex = tex.replace(comment_substring, "") # delete the comment now that it's been processed

        audio_examples_info.append(dict(path=path, caption=caption))

    # Build examples page
    md = "# Lydeksempler\n\nHerunder finder du alle lydeksempler til bogen *Musik- og lydprogrammering med SuperCollider*. Lydeksemplerne er organiseret efter kapitel.\n\n"

    with open('tex/content.aux', 'r') as aux_file:
        aux_data = aux_file.read()
    
    current_chapter = -42
    for example in audio_examples_info:
        data = re.search(r'{\\numberline {(.*?)}.*' + example['caption'], aux_data, re.M)
        if data:
            caption_number = data.group(1)
            
            chapter_number = int(re.sub(r"\.\d+", '', caption_number))
            if chapter_number is not current_chapter:
                md += f"## Kapitel {chapter_number}: {chapter_titles[chapter_number]}\n\n"
                current_chapter = chapter_number

            md = md + f"### Lydeksempel {caption_number}: {example['caption']}\n\n"
            md = md + f"![type:audio]({example['path']})\n\n"
    
    # If audio examples page has changed, overwrite the old one with the newly generated data
    with open(AUDIO_EXAMPLE_FILE_PATH, 'r+') as file_contents:
        old_examples_md = file_contents.read()
        if md != old_examples_md:
            file_contents.seek(0)
            file_contents.write(md)
            file_contents.truncate()
            print(f"New version of {AUDIO_EXAMPLE_FILE_PATH} generated.")

def make_chapter(chapter_title, md_files, ignore_files, solo_files):
    # loop over the given .md files, convert to tex, and return the string

    # remove "1. " etc. from the chapter title, since LaTeX handles the numbering for us
    chapter_title = re.sub(r'^\d+\.\s+', '', chapter_title)
    chapter_tex = f"\\chapter{{{chapter_title}}}\n\\label{{chap:{chapter_title}}}\n!!!!!RESETPAGECOLOR!!!!!"

    chapter_titles.append(chapter_title)

    for file_path in md_files:
        filename = os.path.basename(file_path)
        if (solo_files and filename in solo_files) or (filename not in ignore_files):
            chapter_tex = chapter_tex + "\n" + convert_section(file_path)

    return chapter_tex

if __name__ == "__main__":
    """
    Convert the sources for an mkdocs site to a LaTeX file
    """
    parser = argparse.ArgumentParser(description="Convert mkdocs site into a LaTeX document using the md2tex engine + some custom pre- and postprocessing to deal specifically with mkdocs content.")
    parser.add_argument("--mkdocs_folder", type=str, default="./", help="Path to the mkdocs root directory (where 'docs/' is a subdirectory)")
    parser.add_argument("--tex_outpath", type=str, default="./tex/content.tex", help="Path to the main output TeX file")
    parser.add_argument("--frontmatter_inpath", type=str, default="./tex/preface.md", help="Path to the front matter input markdown file")
    parser.add_argument("--generate_examples_page", action="store_true", default=False, help="Generate new sound examples page for mkdocs")
    
    # Parse the arguments
    args = parser.parse_args()
    docs_folder = join(args.mkdocs_folder, 'docs')
    tex_outpath = args.tex_outpath

    # Read the list of ignored markdown files
    with open(IGNORED_MD_FILES_LIST, 'r') as ignore_file:
        ignore_files = ignore_file.read().split('\n')
    with open(SOLOED_MD_FILES_LIST, 'r') as solo_file:
        solo_files = solo_file.read().split('\n')
    
    tex = ''

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
        print(f"File {tex_outpath} written successfully.")

    if args.generate_examples_page:
        generate_audio_examples_page(tex)

    exit(0)