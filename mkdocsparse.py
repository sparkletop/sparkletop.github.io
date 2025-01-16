import os
import sys
import re
from os.path import join, isdir
import argparse

# Add the md2tex submodule folder to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'md2tex'))

from md2tex import convert

# Walk a 'docs' directory in an mkdocs site and convert markdown files to a Tex file containing everything

def make_chapter(chapter_title, chapter_dir):
    # loop over .md files, convert to tex, and return the string
    # remove "01. " etc. from the chapter title
    chapter_title = re.sub(r'^\d+\.\s+', '', chapter_title)
    chapter_tex = f"\chapter{{{chapter_title}}}\n\label{{chap:{chapter_title}}}\n"

    md_files = [f for f in os.listdir(chapter_dir) if f.endswith('.md')]
    md_files.sort()
    
    for filename in md_files:
        path = join(chapter_dir, filename)
        print(f"Processing document: {path}")
        with open(path, mode="r") as file:
            new_section = convert(file.read(), document_class="article", minted_language="sc")
            
            # add a label to each section, corresponding to file name
            # for use in cross references
            new_section = re.sub(r"(\\section{.+?}\n)", r"\1\\label{" + filename + r"}\n", new_section)
            
            chapter_tex = chapter_tex + "\n" + new_section

            # remove tabs and replace with spaces
            chapter_tex = chapter_tex.replace("\t", "    ")
    
    # make symlinks to the figures in the tex/media folder (there must be a better way, but this works for now)
    media_dir = os.path.abspath(join(chapter_dir, 'media'))
    if os.path.exists(media_dir) and os.path.isdir(media_dir):
        media_files = [f for f in os.listdir(media_dir)]
        for f in media_files:
            src = join(media_dir, f)
            dst = join('tex', 'media', f)
            os.symlink(src, dst)

    return chapter_tex

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert mkdocs site into a LaTeX document using the md2tex engine.")
    parser.add_argument("inpath", type=str, help="Path to the mkdocs directory")
    parser.add_argument("outpath", type=str, help="Path to the output tex file")
    
    args = parser.parse_args()
    docs_folder = os.path.join(args.inpath, 'docs')
    tex_file = args.outpath if args.outpath else "output/output.tex"

    if not os.path.exists(docs_folder):
        raise FileNotFoundError(f"{docs_folder} does not exist.")
    if not os.path.isdir(docs_folder):
        raise IsADirectoryError(f"{docs_folder} is not a directory.")
    
    # Assume docs_folder contains the front matter (foreword and so on)
    tex = make_chapter("Front matter", docs_folder)

    # walk the subdirectories of the docs directory and create chapters for each one
    chapters = [d for d in os.listdir(docs_folder) if isdir(join(docs_folder, d))]
    chapters.sort()
    for chap in chapters:
        tex = tex + '\n\n' + make_chapter(chap, join(docs_folder, chap))

    # deal with internal links
    links = re.finditer(r"(?<!!)\[(.*?)\]\((.*?)\)", tex)
    for link in links:
        # Clean up link to only have filename
        filename = re.sub(r"\\#.+$", "", link[2]) # remove anchor, subsection labelling not implemented yet...
        filename = re.sub(r"^\.\./.+/", "", filename)

        if filename.endswith(".md"):
            # Internal link to other markdown document
            # assume that there is a \label in the section corresponding to file name
            tex = tex.replace(link[0], link[1] + r" (se afsnit \ref{" + filename + r"})")
        else:
            print(f"Unsupported link: {link}, leaving as is...")


    with open(tex_file, 'w') as file:
        file.write(tex)
        print(f"File {tex_file} written successfully.")

