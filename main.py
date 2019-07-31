import click
import os
from os.path import abspath
from core import utils

@click.command()
@click.option("--uri", help="uri from webserver. we need to generate clean links")
@click.option("--src", help="src folder to server. example: src/**/*.ts")
@click.option("--port", default=80, help="port from your webserver. default is 80")
@click.option("--syntax", default="", help="syntax for code highlighting. example: typescript, python and much more")

def run(uri, port, src, syntax):

    if not uri:
        print("missing option --uri")
        exit(1)

    if not src:
        print("missing option --src")
        exit(1)

    if not os.path.exists(os.path.join(os.getcwd(),"out")):
        os.makedirs(os.path.join(os.getcwd(),"out"))


    filename = abspath(src)
    print(filename)
    code_ast = []

    reader = utils.DirReader(abspath(src))
    raw_files = reader.readDir()

    for raw_file in raw_files:
        raw_file_link = raw_file.split(src.split("/")[1])[1][1:]+".html"

        file_content_map = []
        file_content = open(raw_file, "r")

        for content in file_content:
            file_content_map.append(content.strip().split(" "))
        file_content.close

        inner_ast = [raw_file_link, file_content_map]
        code_ast.append(inner_ast)

    stripped_files = reader.readDirStripped()

    # write index html
    utils.FileWriter(os.path.join(os.getcwd(),"out/index.html"), utils.HtmlBuilder(stripped_files, "Code Review Builder",uri, port, code_ast).getPage())

    # generate others generic
    for file in raw_files:
        c_page = utils.HtmlPageBuilder(stripped_files, file, file,uri, port, syntax, code_ast)
        utils.FileWriter(os.path.join(os.getcwd(),"out/"+file.split(src.split("/")[1])[-1]+".html"), c_page.getPage())


if __name__ == '__main__':
    run()
