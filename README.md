# plotly-iframe-merger

Python script for embedding [plotly](https://plotly.com/python/ipython-notebook-tutorial/) iframes into HTML.

Unfortunately, Jupiter Notebook creates separate iframes for each plotly graph during notebook export to HTML. So to share your HTML with someone, you need to send a folder with plotly iframes also.
For HTML distribution simplicity, this script replaces `<iframe>` tags via iframe contents with small size optimization like moving JS script references from iframe bodies to HTML header.

## Usage

```
$ python embed_iframe.py -i <path to input HTML> -o <optional path to output HTML>
```

```
$ python embed_iframe.py -h
usage: embed_iframe.py [-h] -i INPUT [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input HTML file name
  -o OUTPUT, --output OUTPUT
                        [optional] output file name, if not set - 'embedded_' prefix will be added
```
