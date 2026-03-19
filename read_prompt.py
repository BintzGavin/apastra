import json

with open('.sys/llmdocs/context-evaluation.md', 'rb') as f:
    text = f.read().decode('utf-8')
    text += '`'
    with open('.sys/llmdocs/context-evaluation.md', 'wb') as out_f:
        out_f.write(text.encode('utf-8'))
