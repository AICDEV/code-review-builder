import os
import glob

class DirReader():

    def __init__(self, dir):
        self.dir = dir

    def readDir(self):
        return [f for f in glob.glob(self.dir+"/**/*.*", recursive=True)]

    def readDirStripped(self):
        stripped_files = []
        files = [f for f in glob.glob(self.dir, recursive=True)]
        for file in files:
            stripped_files.append(file.split("src/")[-1])
        return stripped_files


class HtmlBuilder():
    def __init__(self, files, name, ast, src, dest):
        self.__files = files
        self.__name = name
        self.__ast = ast
        self.__src = src
        self.__dest = dest

    def getSearchFunction(self):
        return ("""<script>
                        const code_map = """+str(self.__ast)+""";
                        const context = document.querySelector(".code-box");
                        const instance = new Mark(context);
                        const inputEl = document.getElementById("search-input");

                        inputEl.onkeyup = function(event) {
                                instance.unmark();
                                if(inputEl.value.trim().length > 1) {
                                    searchInDom(inputEl.value.trim());
                                    code_map.map((entry) => {
                                        	const file_name = entry[0];
                                        	let foundEntry = false;

                                        	if(Array.isArray(entry[1])) {
                                        		entry[1].map((subEntry) => {
                                        			if(Array.isArray(subEntry)) {
                                        				for(let i=0; i < subEntry.length;i++) {
                                        					if(subEntry[i].trim() === inputEl.value.trim()) {
                                                                highlightLink(file_name);
                                        					}
                                        				}
                                        			}
                                        		});
                                        	}
                                        })
                                } else {
                                    unhighlight();
                                }
                            }

                        function highlightLink(name) {
                            const links = document.querySelectorAll(".code-link");
                            for(let i = 0; i < links.length; i++) {
                                let link = links[i].getAttribute("href");
                                link = link.substring(link.lastIndexOf("/")+1, link.length);
                                name = name.substring(name.lastIndexOf("/")+1, name.length);

                                if(link === name) {
                                    let span = document.createElement("span");
                                    span.setAttribute("class", "span-sel");
                                    links[i].appendChild(span);
                                }
                            }
                        }

                        function unhighlight() {
                            const links = document.querySelectorAll(".code-link");
                            for(let i = 0; i < links.length; i++) {
                                let spanElementRemove = links[i].querySelectorAll(".span-sel");
                                for(let a = 0; a < spanElementRemove.length; a++) {
                                    spanElementRemove[a].remove();
                                }
                            }
                        }

                        function searchInDom(name) {
                            instance.mark(name);
                        }
                </script>""")

    def getPage(self):
        doc = "<!doctype html>"
        doc += self.getHeader()
        doc += self.getBody()
        doc += "<html>"
        return doc


    def getBody(self):
        body = "<body><div class='top-menu'><input type='text' placeholder='Search in code' id='search-input' /></div><div class='content' id='code-content'>"
        body += self.getNav()
        body += "</div>"+self.getSearchFunction()+"</body>"
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
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/mark.js/8.11.1/mark.min.js"></script>
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
                          height: 96vh;
                          overflow-x: hidden;
                          overflow-y: scroll;
                          background-color: #fff;
                          font-size: 0.75em;
                        }

                        .code-box {
                          width: 75%;
                          height: 96vh;
                          overflow-y: scroll;
                          background-color: #1E1F29;
                          margin: 5px;
                        }

                        .top-menu {
                            height: 50px;
                            border-bottom: 1px solid #fff;
                            display: flex;
                            justify-content: flew-start;
                            align-items: center;
                            padding: 7px;
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

                        #search-input {
                            width: 100%;
                        }

                        .span-sel {
                            color: #fff;
                            background-color: #e68217;
                            position: absolute;
                            width: 15px;
                            height: 15px;
                            text-align: center;
                            border-radius: 50px;
                            margin-left: 5px;
                            font-weight: bold;
                        }

                    </style>
                </head>
                """)

    def getNav(self):
        navstart = "<section class='navbar'><nav><ul>"
        for f in self.__files:
            f = f.replace(self.__src, self.__dest)
            name = f.rsplit(self.__dest)[1]
            navstart += "<li><a class='code-link' href="+f+".html>.."+name+"</a></li>"

        navstart += "</ul></nav></section>"
        return navstart

class HtmlPageBuilder(HtmlBuilder):
    def __init__(self, files, name, raw_file, syntax, ast, src, dest):
        super().__init__(files, name, ast, src, dest)
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
        body = "<body><div class='top-menu'><input type='text' placeholder='Search in code' id='search-input' /></div><div class='content' id='code-content'>"
        body += super().getNav()
        body += self.getSourceCodeFromFile()
        body += "</div>"+super().getSearchFunction()+"</body>"
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
