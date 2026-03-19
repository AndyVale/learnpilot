from js import Object, console
from pyodide.ffi import to_js as _to_js

# to_js converts between Python dictionaries and JavaScript Objects
def to_js(obj):
    """
    Function to convert python objects to JavaScript objects.
    This is required for the Python Workers to work with JavaScript.
    From https://developers.cloudflare.com/workers/languages/python/ffi/
    """
    return _to_js(obj, dict_converter=Object.fromEntries)
