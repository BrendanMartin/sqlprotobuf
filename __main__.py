import re
from dataclasses import dataclass, field
from pathlib import Path

from fire import Fire
import sqlparse

pg_to_proto_type_mapping = {
    'smallint': 'int32',
    'bigint': 'int64',
    'integer': 'int32',
    'text': 'string',
    'real': 'float',
    'date': 'string',
    'boolean': 'bool',
    'timestamp': 'google.protobuf.Timestamp'
}


@dataclass
class Message:
    name: str
    enums: list = field(default_factory=list)
    messages: list = field(default_factory=list)
    fields: list = field(default_factory=list)


@dataclass
class Field:
    name: str
    type: str


def normalize(s):
    return re.sub('''['`"]''', '', s, flags=re.I)


def stringify(result):
    final = ['syntax = "' + result["syntax"] + '";\n']
    for message in result['messages']:
        final.append('message ' + message.name + ' {')
        field_idx = 1
        for field in message.fields:
            final.append(f'\t{field.type} {field.name} = {str(field_idx)};')
            field_idx += 1
        final.append('}\n')
    return '\n'.join(final)


def remove_ddl_comments(data):
    return re.sub('--\s+.*', '', data)


def main(in_file, out_file=None, in_string=None):
    if in_string:
        data = in_string
    else:
        in_file_path = Path(in_file)
        if not in_file_path.exists():
            print(f"{in_file_path} doesn't exist")
            exit()

        with open(in_file_path.absolute(), 'r') as f:
            data = f.read()

    data = remove_ddl_comments(data)

    out_file_path = None
    if out_file:
        out_file_path = Path(out_file)

    result = {
        'syntax': 'proto3',
        'package': None,
        'enums': [],
        'messages': []
    }
    statements = sqlparse.parse(data)

    for s in statements:
        match = re.search('.*CREATE\s+TABLE\s+(IF\s+NOT\s+EXISTS)?[\s+]?([\S|\`]+).*', str(s))
        if match:
            table_name = normalize(match.group(2))
            table_name = table_name.split('.')[-1]
            table_name = ''.join([t.title() for t in table_name.split('_')])
            fields_match = re.search('\((.+)\);', str(s), flags=re.M | re.S | re.I)
            field_filters = ['constraint']
            if fields_match:
                fields = fields_match.group(1).split(',')
                fields = [f.strip() for f in fields if not any(filt in f.lower() for filt in field_filters)]
                fields = [tuple(f.split()[:2]) for f in fields]
                fields = [Field(name=name, type=pg_to_proto_type_mapping[type_]) for (name, type_) in fields]
                result['messages'].append(Message(name=table_name, fields=fields))

    stringed = stringify(result)

    if out_file_path:
        with open(out_file_path.absolute(), 'w') as f:
            f.write(stringed)
    else:
        print(stringed)


if __name__ == '__main__':
    fire = Fire(main)
