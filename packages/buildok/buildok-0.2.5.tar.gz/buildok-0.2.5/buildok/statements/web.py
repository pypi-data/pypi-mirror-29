# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import webbrowser as wb

def exec_web(url=None, *args, **kwargs):
    r"""Open a link in default browser.

    Args:
        url (str): URL to open.

    Retuns:
        str: Output as string.

    Raises:
        TypeError: If an invalid `url` is provided.

    Accepted statements:
        ^open in browser `(?P<url>.+)`[\.\?\!]$
        ^open link `(?P<url>.+)`[\.\?\!]$
        ^open url `(?P<url>.+)`[\.\?\!]$

    Sample (input):
        1) Open link `https://github.com/lexndru/buildok`.

    Expected:
        Opened URL in browser => https://github.com/lexndru/buildok
    """
    try:
        wb.get().open(url, new=2)
        return "Opened URL in browser => %s" % url
    except TypeError as e:
        raise e
    return "Nothing to do"
