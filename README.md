# plotly-iframe-merger

Python script for embedding [plotly](https://plotly.com/python/ipython-notebook-tutorial/) iframes into HTML.

Unfortunately, Jupiter Notebook creates separate iframes for each plotly graph during notebook export to HTML. So to share your HTML with someone, you need to send a folder with plotly iframes also.
For HTML distribution simplicity, this script replaces `<iframe>` tags via iframe contents with small size optimization like moving JS script references from iframe bodies to HTML header.

## Usage

```sh
python embed_iframe.py -i <path to input HTML> -o <optional path to output HTML>
```
