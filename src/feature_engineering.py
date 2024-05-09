import re


# The 'removeHTML' function is used to remove HTML tags from a given text or string 'x'
def removeHTML(x):
    html=re.compile(r'<.*?>')
    return html.sub(r'',x)
