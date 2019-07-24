import os
import glob

class DirReader():

    def __init__(self, dir):
        self.dir = os.path.join(os.getcwd(), dir)

    def readDir(self):
        return [f for f in glob.glob(self.dir, recursive=True)]

    def readDirStripped(self):
        stripped_files = []
        files = [f for f in glob.glob(self.dir, recursive=True)]
        for file in files:
            stripped_files.append(file.split("src/")[-1])
        return stripped_files


class HtmlBuilder():
    def __init__(self, files, name, uri, port):
        self.__files = files
        self.__name = name
        self.__uri = uri
        self.__port = port

    def getPage(self):
        doc = "<!doctype html>"
        doc += self.getHeader()
        doc += self.getBody()
        doc += "<html>"
        return doc


    def getBody(self):
        body = "<body><div class='content'>"
        body += self.getNav()
        body += "</div></body>"
        return body

    def getHeader(self):
        return ("""
                <head>
                    <title>"""+self.__name+"""</title>
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.8/styles/dracula.min.css">
                    <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.8/highlight.min.js"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlightjs-line-numbers.js/2.7.0/highlightjs-line-numbers.min.js"></script>
                    <script>hljs.initHighlightingOnLoad();</script>
                    <script>hljs.initLineNumbersOnLoad();</script>
                    <style>
                        html, body {
                          padding: 0px;
                          margin: 0px;
                          background-color: #333333;
                          color: #fff;
                          font-family: 'Open Sans', sans-serif;
                          overflow: hidden;
                        }


                        code {
                          font-size: 0.85em !important;
                        }

                        .content {
                          display: flex;
                          align-items: flex-start;
                        }

                        .navbar {
                          width: 25%;
                          height: 100vh;
                          overflow-x: hidden;
                          overflow-y: scroll;
                          background-color: lightgray;
                          font-size: 0.75em;
                        }

                        .code-box {
                          width: 75%;
                          height: 100vh;
                          overflow-y: scroll;
                          background-color: #e3e3e3e3;
                          margin: 5px;
                        }


                        .hljs-ln-code {
                          padding-left: 10px !important;
                        }

                        .hljs-ln-numbers {
                          text-align: right !important;
                        }

                        .helper-section {
                            height: 50px;
                            border-bottom: 1px solid lightgrey;
                            display: flex;
                            justify-content: space-around;
                            align-items: center;
                        }

                        .helper-el a {
                            color: #fff;
                        }
                    </style>
                </head>
                """)

    def getNav(self):
        navstart = "<section class='navbar'><nav><ul>"
        for f in self.__files:
            link = self.__uri+":"+str(self.__port)+"/"+f
            navstart += "<li><a href="+link+".html>"+f+"</a></li>"

        navstart += "</ul></nav></section>"
        return navstart

class HtmlPageBuilder(HtmlBuilder):
    def __init__(self, files, name, raw_file, uri, port, syntax):
        super().__init__(files, name, uri, port)
        self.raw_file = raw_file
        self.syntax = syntax

    # override getPage() method from HtmlBuilder
    def getPage(self):
        doc = "<!doctype html>"
        doc += super().getHeader()
        doc += self.getBody()
        doc += "<html>"
        return doc

    # override getBody() method from HtmlBuilder
    def getBody(self):
        body = "<body><div class='content'>"
        body += super().getNav()
        body += self.getSourceCodeFromFile()
        body += "</div></body>"
        return body

    def getSourceCodeFromFile(self):
        file = open(self.raw_file, "r")
        code_el = "<pre class='code-box'><code class="+self.syntax+">"
        for line in file:
            code_el += line
        code_el += "</code></pre>"
        file.close()
        return code_el



def FileWriter(file, content):
    path = os.path.dirname(file)
    if not os.path.isdir(path):
        os.makedirs(path)

    file = open(file, "w+")
    file.write(content)
    file.close()
