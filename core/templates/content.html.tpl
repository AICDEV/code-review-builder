<!DOCTYPE html>
<html>

<head>
    <title>{{name}}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.8/styles/dracula.min.css">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.8/highlight.min.js"></script>
    <script
        src="https://cdnjs.cloudflare.com/ajax/libs/highlightjs-line-numbers.js/2.7.0/highlightjs-line-numbers.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mark.js/8.11.1/mark.min.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
    <script>hljs.initLineNumbersOnLoad();</script>
    <style>
        html,
        body {
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

<body>
    <div class="top-menu">
        <input type="text" placeholder="Search in code and files" id="search-input" />
    </div>
    <div class="content" id="code-content">
        <section class="navbar">
            <nav>
                <ul>
                    {%for nav in nav_object%}
                    <li><a class="code-link" href="{{nav[0]}}">{{nav[1]}}</a></li>
                    {% endfor %}
                </ul>
            </nav>
        </section>
        <pre class="code-box">
            <code class="{{syntax}}">
{{code_content.lstrip()}}
            </code>
        </pre>
    </div>
    <script>
        const code_map = {{ast}};
        const context = document.querySelector(".code-box");
        const instance = new Mark(context);
        const inputEl = document.getElementById("search-input");

        inputEl.onkeyup = function (event) {
            instance.unmark();
            if (inputEl.value.trim().length > 1) {
                searchInDom(inputEl.value.trim());
                code_map.map((entry) => {
                    const file_name = entry[0];
                    let foundEntry = false;

                    if (Array.isArray(entry[1])) {
                        entry[1].map((subEntry) => {
                            if (Array.isArray(subEntry)) {
                                for (let i = 0; i < subEntry.length; i++) {
                                    if (subEntry[i].trim() === inputEl.value.trim()) {
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
            for (let i = 0; i < links.length; i++) {
                let link = links[i].getAttribute("href");
                link = link.substring(link.lastIndexOf("/") + 1, link.length);
                name = name.substring(name.lastIndexOf("/") + 1, name.length);

                if (link === name) {
                    let span = document.createElement("span");
                    span.setAttribute("class", "span-sel");
                    links[i].appendChild(span);
                }
            }
        }

        function unhighlight() {
            const links = document.querySelectorAll(".code-link");
            for (let i = 0; i < links.length; i++) {
                let spanElementRemove = links[i].querySelectorAll(".span-sel");
                for (let a = 0; a < spanElementRemove.length; a++) {
                    spanElementRemove[a].remove();
                }
            }
        }

        function searchInDom(name) {
            instance.mark(name);
        }
    </script>
</body>

</html>