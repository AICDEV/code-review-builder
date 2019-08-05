## Code review builder

### What can this program do for you
Sometimes it is, for some strange reason, quite helpful to convert your whole source code,
into a html page where others can view your code. Also, there is a cool search function included. Enjoy. In short terms: this tool converts your
source code into a html structure with syntax highlighting. Nothing more, nothing less.

### Requirements

Please make sure that you have [click](https://pypi.org/project/click/) installed and python as well. Program is tested with python3.

```text
  pip install click
```


### Example
Preview:
![alt text](https://github.com/AICDEV/code-review-builder/blob/master/example.png)

### Run code template builder

You have a few command line arguments to play with:

- --src source folder to serve from
- --out destination folder to write output html
- --syntax syntax highlighting. leave for autodetect.


Call examples:


Autodetect syntax
```text
python3 main.py  --src ../mimecraft/src  --out . 
```

Typescript
```text
python3 main.py  --src ../mimecraft/src  --out . --syntax typescript
```
