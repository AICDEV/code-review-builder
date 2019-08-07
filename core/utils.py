import os
from os.path import abspath
import glob
import jinja2
 
class Templates():
    def __init__(self):
        self.templateLoader = jinja2.FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__),"templates"))
        self.templateEnv = jinja2.Environment(loader=self.templateLoader)

    def getTemplateForIndex(self, nav_object, name, ast):
        template = self.templateEnv.get_template("index.html.tpl")
        return template.render(name=name, nav_object=nav_object, ast=ast)

    def getTemplateForContentPage(self, nav_object, name, ast, code_content, syntax):
        template = self.templateEnv.get_template("content.html.tpl")
        return template.render(name=name, nav_object=nav_object, ast=ast, code_content=code_content, syntax=syntax)

class DirReader():

    def __init__(self, dir):
        self.dir = dir

    def readDir(self):
        return [f for f in glob.glob(self.dir+"/**/*.*", recursive=True)]


class HtmlBuilder():
    def __init__(self, files, name, ast, src, dest):
        self.__files = files
        self.__name = name
        self.__ast = ast
        self.__src = src
        self.__dest = dest

    def getPage(self):
        nav_obj = self.buildNavObject()
        return Templates().getTemplateForIndex(nav_obj, self.__name, self.__ast)

    def buildNavObject(self):
        nav = []
        for file in self.__files:
            file = file.replace(self.__src, self.__dest)
            nav_tupel = (file+".html",".."+file.rsplit(self.__dest)[1])
            nav.append(nav_tupel)
        return nav

class HtmlPageBuilder(HtmlBuilder):
    def __init__(self, files, name, raw_file, syntax, ast, src, dest):
        super().__init__(files, name, ast, src, dest)
        self.__raw_file = raw_file
        self.__syntax = syntax
        self.__name = name
        self.__ast = ast
    
    def getPage(self):
        nav_obj = super().buildNavObject()
        return Templates().getTemplateForContentPage(nav_obj, self.__name, self.__ast, self.__readSource(), self.__syntax)

    def __readSource(self):
        file = open(self.__raw_file, "r")
        content = file.read()
        file.close()
        return content

def FileWriter(file, content):
    path = os.path.dirname(file)

    if not os.path.isdir(path):
        os.makedirs(path)

    file = open(file, "w+")
    file.write(content)
    file.close()
