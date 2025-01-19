import os
"""
This script converts an MkDocs site into a LaTeX document using the md2tex engine with custom pre- and post-processing to handle MkDocs-specific content.
Functions:
    preprocess_mkdocs_markdown(md_content: str) -> str:
        Preprocesses MkDocs-material content tabs by removing indentation and formatting headers.
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
        frontmatter_outpath: Path to the front matter output LaTeX file.
Example:
    python mkdocsparse.py /path/to/mkdocs /path/to/output/mainmatter.tex /path/to/output/frontmatter.tex
"""
import sys
import re
from os.path import join, isdir
import argparse

# Add the md2tex submodule folder to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'md2tex'))

from md2tex import convert as convert_md2tex

def preprocess_mkdocs_markdown(md_content: str):
    # preprocess mkdocs-material content tabs (remove indentation)
    # matches and processes sections that begin with '=== xyz' followed by indented content or empty lines
    content_tabs_blocks = re.finditer(r"^(===.*$)(?:\n(^\s*$|^ {4}.*$))+", md_content, re.M)
    for block in content_tabs_blocks:
        code = block.group(0)
        code = re.sub(r"^=== \"(.+)\"$", r"*\1*", code, flags=re.M)
        code = re.sub(r"^    ", "", code, flags=re.M)
        md_content = md_content.replace(block.group(0), code)
    
    return md_content

def postprocess_tex(tex: str):
    # replace tabs with spaces
    tex = tex.replace("\t", "    ")

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

def convert_section(md_file_path: str, section_label: str):
    # assume that each section is a markdown file
    print(f"Processing document: {md_file_path}")
    md_content = ""
    with open(md_file_path, mode="r") as file:
        md_content = file.read()
        md_content = preprocess_mkdocs_markdown(md_content)
    
    new_section = convert_md2tex(
        md_content,
        document_class="article",
        minted_language="'sc_lexer.py:SuperColliderLexer -x'",
        override_language=True
    )

    # add a label to each section for use in cross references
    new_section = re.sub(r"(\\section{.+?}\n)", r"\1\\label{" + section_label + r"}\n", new_section)

    return new_section

def make_chapter(chapter_title, chapter_dir):
    # loop over .md files, convert to tex, and return the string
    # remove "01. " etc. from the chapter title
    chapter_title = re.sub(r'^\d+\.\s+', '', chapter_title)
    chapter_tex = f"\\chapter{{{chapter_title}}}\n\\label{{chap:{chapter_title}}}\n"

    md_files = [f for f in os.listdir(chapter_dir) if f.endswith('.md')]
    md_files.sort()
    for filename in md_files:
        path = join(chapter_dir, filename)
        chapter_tex = chapter_tex + "\n" + convert_section(path, filename)
    
    # make symlinks to the figures in the tex/media folder (there must be a better way, but this works for now)
    media_dir = os.path.abspath(join(chapter_dir, 'media'))
    if os.path.exists(media_dir) and os.path.isdir(media_dir):
        media_files = [f for f in os.listdir(media_dir)]
        for f in media_files:
            src = join(media_dir, f)
            dst = join('tex', 'media', f)
            
            if os.path.exists(dst):
                if os.path.islink(dst):
                    if os.readlink(dst) == src:
                        continue
                    else:
                        os.unlink(dst)
                else:
                    os.remove(dst)
                os.symlink(src, dst)

    return chapter_tex

# Walk a 'docs' directory in an mkdocs site and convert markdown files to a Tex file containing everything
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert mkdocs site into a LaTeX document using the md2tex engine + some custom pre- and postprocessing to deal specifically with mkdocs content.")
    parser.add_argument("--mkdocs_folder", type=str, default="./", help="Path to the mkdocs root directory (where 'docs/' is a subdirectory)")
    parser.add_argument("--tex_outpath", type=str, default="./tex/content.tex", help="Path to the main output TeX file")
    parser.add_argument("--frontmatter_inpath", type=str, default="./tex/preface.md", help="Path to the front matter input markdown file")
    parser.add_argument("--convert-to-pdf", action="store_true", help="Convert the processed site into PDF form after converting to TeX")
    
    # Parse the arguments
    args = parser.parse_args()
    mkdocs_folder = os.path.join(args.mkdocs_folder, 'docs')
    tex_outpath = args.tex_outpath
    
    # First we process the preface
    if args.frontmatter_inpath:
        preface = "\\chapter{Forord}\n"
        preface += convert_section(args.frontmatter_inpath, "Forord")
        tex = preface + '\n\n' + "\\mainmatter\n\n"
    else:
        tex = "\\mainmatter\n\n"
    
    # walk the subdirectories of the docs directory and create chapters for each one
    chapters = [d for d in os.listdir(mkdocs_folder) if isdir(join(mkdocs_folder, d))]
    chapters.sort()
    for chap in chapters:
        tex = tex + '\n' + make_chapter(chap, join(mkdocs_folder, chap))

    tex = postprocess_tex(tex)

    with open(tex_outpath, 'w') as file:
        file.write(tex)
        print(f"File {tex_outpath} written successfully.")

    if args.convert_to_pdf:
        #os.chdir("tex")
        #os.system(f"latexmk -xelatex -latexoption='-shell-escape' -f template.tex")´
        os.system("./t2p.sh")


