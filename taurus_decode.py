import argparse
from datetime import datetime
import os
import re
import sys


def get_letter(tab, offset):
# Apply the offset key to the integer and return the corresponding character
    for letter in tab:
        yield chr(int(letter)-int(offset))


def decode_taurus(payload, offset, delim):
# Take the payload line, offset key, and delimeter. Split on the delemiter and call "get_letter" to apply the offset key to the integer 
    tab = payload.split(delim)
    res = ''.join(get_letter(tab, offset))
    return res


def extract_encoded_line(line, delim, func):
# Use Regex to identify and extract the obfuscated string in the line
# For example: 87>120>118>109>114>107>77>119>74>112>115>101>120>44>43>79>85>75>101>107>106>125>82>94>106>71>93>88>43>45
# Use further regex to extract the "offset" key by looking for the delimeter, followed by a 1-3 character digit, comma, and finally the offset key
# Replace the obfuscated line with the deobfuscated one
    clean_fucn = re.escape(func)
    clean_delim = re.escape(delim)
    encoded_strings = re.findall(clean_fucn + '\("(?:[\d]{1,3}[' + clean_delim + ']{0,1}){1,}\",([\d]{1,3})', line)
    key_ints = re.findall(delim + '[0-9]{1,3}",(\d)', line)
    if len(key_ints) == len(encoded_strings):
        i = 0
        for i in range(len(encoded_strings)):
            plaintext = decode_taurus(encoded_strings[i], key_ints[i], delim)
            replacement_text = '%s("%s",%s)' % (func, encoded_strings[i], key_ints[i])
            plaintext = '"%s"' % (plaintext)
            line = line.replace(replacement_text, plaintext)
            i = i + 1
    else:
        print("MISSING KEY:" + line)
    return line


def decode_obfuscated_file(args):
# Open files fo input and output
    with open(args.input) as inputFile, open(make_output(args), 'w', newline='', encoding='utf8') as output_file:
        lines = inputFile.readlines()
        for line in lines:
            if args.function in line and args.delimiter in line:
                deobfuscated_line = extract_encoded_line(line, args.delimiter, args.function)
                output_file.write(deobfuscated_line)
            else:
                output_file.write(line)


def make_output(args):
# Create name of output file based on date and time
    filename = args.input + '.deobfuscated_' + datetime.utcnow().isoformat().replace(':', '.')
    return os.path.join(args.output, filename)


def get_args():
# Collect arguments. 
# "Function" paramter should be name of malicious function used to decode strings
# I.e. qLAEMpnctIeWhZ
# Example command line: $ python taurus_decode.py -d ">" -i Poi.xltx -o /path/to/output -f qLAEMpnctIeWhZ
    parser = argparse.ArgumentParser(
        description='Decode strings from AutoIT Taurus Loader'
    )
    parser.add_argument('-d', '--delimiter', help='Define which delimiter should be used to split the strings on', required=True)
    parser.add_argument('-o', '--output', help='Directory for output that exsists', required=True)
    parser.add_argument('-i', '--input',  help='Obfuscated AutoIT file', required=True)
    parser.add_argument('-f', '--function', help='name of function in obfuscated AutoIT which deocdes strings', required=True)
    return parser.parse_args()


def main():
# Start and ensure the output path exsists
    args = get_args()
    print(args.output)
    os.makedirs(args.output, exist_ok=True)
    decode_obfuscated_file(args)


if __name__ == '__main__':
    main()
