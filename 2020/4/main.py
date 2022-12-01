import sys
import re

from kitchen_sink import u

def valid_passports(data):
    required_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    for record in data:
        if not required_keys.issubset(set(record.keys())):
            continue
        if not validate_record(record):
            continue
        yield record


def validate_record(record):
    try:
        return (
            1920 <= int(record['byr']) <= 2002 and
            2010 <= int(record['iyr']) <= 2020 and
            2020 <= int(record['eyr']) <= 2030 and
            validate_height(record['hgt']) and
            re.match(r'^#[a-f0-9]{6}$', record['hcl']) and
            record['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth',) and
            re.match(r'^\d{9}$', record['pid'])
        )
    except Exception:
        return False

def validate_height(hgt):
    value, unit, _ = re.split(r'(in|cm)', hgt)
    if unit == 'cm':
        return 150 <= int(value) <= 193
    elif unit == 'in':
        return 59 <= int(value) <= 76
    else:
        raise ValueError()


def load(filename):
    return [parse_record(record.rstrip(b'\n')) for record in open(filename,
        'rb').read().split(b'\n\n')]


def parse_record(record):
    return dict([k_v.split(':') for k_v in re.split(r'\s+', u(record).rstrip('\n'))])

if __name__ == '__main__':
    data = load(sys.argv[1])
    print(len(list(valid_passports(data))))
