## Code review builder

### What can this program do for you
Sometimes it is, for some strange reason, quite helpful to convert your whole source code,
into a html page where others can view your code. In short terms: this tool converts your
source code into a html structure with syntax highlighting. Nothing more, nothing less.

### Requirements

Please make sure that you have [click](https://pypi.org/project/click/) installed and python as well. Program is tested with python3.

```text
  pip install click
```

### Run code template get

You have a few command line arguments to play with:

- --uri url to host on a web server and to build the right working links
- --src source folder to serve from
- --port optional port for web server
- --syntax syntax highlighting. leave for autodetect.

Output is in folder "out"

Call examples:


C
```text
python3 main.py --uri http://localhost --src /src/**/*.c --port 8888 --syntax c
```

Typescript
```text
python3 main.py --uri http://localhost --src /src/**/*.ts --port 8888 --syntax typescript
```

Java
```text
python3 main.py --uri http://localhost --src /src/**/*.java --port 8888 --syntax java
```
