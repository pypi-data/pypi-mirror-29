
import os, re, sys, logging
from bl.string import String
from bl.text import Text

log = logging.getLogger(__name__)

def csv_to_data(fn, encoding='UTF-8', delimiter=',', quote='"', headers=True, omit_empty=True, unescape=True, return_keys=False):
    t = Text(fn=fn, encoding=encoding)
    text = normalize_text(t.text, quote=quote)
    lines = text.split('\n')
    if headers==True:
        keys = [String(v).hyphenify().strip('-').resub('-r$', '') for v in lines.pop(0).split(delimiter)]
    else:
        keys = [excel_key(i) for i in range(len(lines[0].split(delimiter)))]
    data = []
    log.debug("%d lines of data" % len(lines))
    for line in lines:
        if lines.index(line) % 1000 == 0: log.debug("%d lines processed" % lines.index(line))
        item = {}
        if unescape==True:
            values = [v.replace('\\t', '\t').replace('\\n', '\n').replace('\\r', '\n') for v in line.split(delimiter)]
        else:
            values = line.split(delimiter)
        for i in range(len(values)):
            if values[i].strip() != '' or omit_empty==False:        # omit empty elements
                item[keys[i]] = values[i].strip()
        if len(item.keys()) > 0:
            data.append(item)
    if return_keys==True:
        return data, keys
    else:
        return data

def normalize_text(text, quote='"', escape='\\'):
    """Ensures that the lines of the Excel UTF-16 are importable
    + Escape newline and tab characters in the input when between straight quotes.
    + Double quotes are escaped quotes
    + Remove the quotes from the text.
    """
    quoted = False
    i = 0
    n = len(text)
    log.debug('normalize: %d characters of text' % n)
    while i < n:
        if i > 0 and i % 100000 == 0: log.debug('  %d%% normalized' % int(100*i/n))
        c = text[i]
        if c in [escape, quote] and i < n-1 and text[i+1]==quote:
            text = text[:i] + text[i+1:]
            # i += 1
        elif c=='\r':
            text = text[:i] + '\\r' + text[i+1:]
            n = len(text)
            i -= 1
        elif c==quote:
            quoted = not(quoted)
            text = text[:i] + text[i+1:]
            n = len(text)
            i -=1 
        elif quoted==True:
            if c=='\n':
                text = text[:i] + '\\n' + text[i+1:]
                n = len(text)
                i += 1
            elif c=='\t':
                text = text[:i] + '\\t' + text[i+1:]
                n = len(text)
                i += 1
        i += 1
    return text

def excel_key(index):
    """create a key for index by converting index into a base-26 number, using A-Z as the characters."""
    X = lambda n: ~n and X((n // 26)-1) + chr(65 + (n % 26)) or ''
    return X(int(index))

