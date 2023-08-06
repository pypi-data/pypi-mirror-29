
import os, re, sys, logging, json

log = logging.getLogger(__name__)

def csv_to_records(fn, encoding='UTF-8', delimiter=',', quote='"', headers=True, omit_empty=True):
    """parse a CSV file and return it as a list of records, each record as a dict"""
    data = parse_file(fn, encoding=encoding, delimiter=delimiter, quote=quote)
    if headers==True and len(data) > 0:
        keys = data.pop(0)
    else:
        keys = [excel_key(i) for i in range(len(data[0]))]
    log.debug("%d lines of data" % len(lines))
    records = []
    for values in data:
        record = {}
        for i in range(len(values)):
            value = values[i]
            if omit_empty = False or value not in ['', None]:
                if i < len(keys):
                    key = keys[i]
                else:
                    key = excel_key(i)
                record[key] = values[i]
        if len(record.keys()) > 0:
            records.append(record)
    return records

def excel_key(index):
    """create a key for index by converting index into a base-26 number, using A-Z as the characters."""
    X = lambda n: ~n and X((n // 26)-1) + chr(65 + (n % 26)) or ''
    return X(int(index))

def write_file(fn, data, encoding='UTF-8', delimiter='\t', quote=''):
    """write the data to the file: data is a list of records, each record as a list of values"""
    with open(fn, 'wb') as f:
        text = '\n'.join([delimiter.join([(quote+val+quote) for val in line]) for line in data])
        f.write(bytes(text, encoding=encoding))

def parse_file(fn, encoding='UTF-8', delimiter='\t', quote='"'):
    with open(fn, 'rb') as f:
        text = f.read().decode(encoding)
        return parse_text(text, delimiter=delimiter, quote=quote)

def parse_text(text, delimiter='\t', quote='"'):
    """parse the text into data: return a list of records, each record as a list"""
    def value_string(val):
        value = ''.join(val).strip()
        while value[:2] in ['\\n', '\\r', '\\t']:
            value = value[2:]
        while value[-2:] in ['\\n', '\\r', '\\t']:
            value = value[:-2]
        return value
    records = []
    n = len(text)
    quoted = False
    record = []
    val = []
    for i in range(n):
        c = text[i]
        if (c==delimiter and quoted==False):              # end of value
            record.append(value_string(val))
            val = []
        elif c==quote:                                  # quoting
            if val==[]:
                quoted = True
            elif quoted==True and text[i+1] == delimiter:  
                quoted = False
            else:
                val.append(c)
        elif c=='\n':
            if quoted==True:
                val.append('\\n')
            else:                                       # end of record
                record.append(value_string(val))
                records.append(record)
                record = []
                val = []
        elif c in ['\r', '\t']:                         # escaped values
            if c=='\r': val.append('\\r')
            if c=='\t': val.append('\\t')
        else:                                           # any other character
            val.append(c)
    if val != []:
        record.append(value_string(val))
    if record != []:
        records.append(record)
    return records

