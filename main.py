import click
import os
from os.path import abspath
from core import utils

@click.command()
@click.option("--src", help="src folder to server.")
@click.option("--out", help="out folder to server. ")
@click.option("--syntax", default="", help="syntax for code highlighting. example: typescript, python and much more")

def run(src, out, syntax):

    if not out:
        print("missing option --out")
        exit(1)

    if not src:
        print("missing option --src")
        exit(1)

    if not os.path.exists(abspath(src)):
        print("you src diretory doesn't exists " + abspath(src))
        exit(1)

    if not os.path.exists(os.path.join(abspath(out),"out")):
        print("creating output directory: " + abspath(out))
        os.makedirs(os.path.join(abspath(out),"out"))


    source_folder = abspath(src)
    destination_folder = os.path.join(abspath(out),"out")

    print("read sources from: " + source_folder)

    reader = utils.DirReader(source_folder)
    raw_files = reader.readDir()
    print("found following source files")
    print(raw_files)

    code_ast = []
    for raw_file in raw_files:
        raw_file_link = raw_file+".html"
        file_content_map = []
        file_content = open(raw_file, "r")

        for content in file_content:
            file_content_map.append(content.strip().split(" "))
        file_content.close

        inner_ast = [raw_file_link, file_content_map]
        code_ast.append(inner_ast)

    utils.FileWriter(os.path.join(destination_folder,"index.html"), utils.HtmlBuilder(raw_files, "Code Review Builder", code_ast, source_folder, destination_folder).getPage())

    for file in raw_files:
        target_file_name = file.replace(source_folder, destination_folder)+".html"
        c_page = utils.HtmlPageBuilder(raw_files, file, file, syntax, code_ast, source_folder, destination_folder)
        utils.FileWriter(target_file_name, c_page.getPage())


if __name__ == '__main__':
    run()
