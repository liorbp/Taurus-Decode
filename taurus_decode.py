import argparse
from datetime import datetime
import os
import re


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
# Use Regex to identify and extract the obfuscated strings in the line (can be multilpe in the same line)
# For example: DECRYPT("87>120>118>109>114>107>77>119>74>112>115>101>120>44>43>79>85>75>101>107>106>125>82>94>106>71>93>88>43>45", 1)
# The regex also extracts the "offset" key that appears next to the encoded string. The key can appear as a single number, or a division of two numbers (e.g. 12/4)
# Finally it will replace the obfuscated string with the deobfuscated one and return the line after all deobfuscation is done
    try:
        clean_func = re.escape(func)
        clean_delim = re.escape(delim)
        encoded_strings = re.findall(clean_func + r'\("((?:\d{1,3}' + clean_delim + r'\d{1,3})*)",([\d]{1,3})(?:\/([\d]{1,3}))?', line)
        for encoded_string in encoded_strings:
            if not all(encoded_string):
                key = int(encoded_string[1])
                replacement_text = '{}("{}",{})'.format(func, encoded_string[0], encoded_string[1])
            else:
                key = int(int(encoded_string[1]) / int(encoded_string[3]))
                replacement_text = '{}("{}",{}/{})'.format(func, encoded_string[0], encoded_string[1], encoded_string[3])
            
            plaintext = decode_taurus(encoded_string[0], key, delim)
            plaintext = '"{}"'.format(plaintext)
            line = line.replace(replacement_text, plaintext)
            
        return line
    except:
        print("Error on line:" + line)


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
    filename = args.input + '.deobfuscated_' + datetime.now().isoformat().replace(':', '.')
    print('Saving deobfuscated output to: {}\\{}'.format(args.output_dir, filename))
    return os.path.join(args.output_dir, filename)


def get_args():
# Collect arguments. 
# "Function" paramter should be name of malicious function used to decode strings
# I.e. qLAEMpnctIeWhZ
# Example command line: $ python taurus_decode.py -d ">" -i Poi.xltx -o /path/to/output/directory -f qLAEMpnctIeWhZ
    parser = argparse.ArgumentParser(
        description='Decode strings from AutoIT Taurus Loader'
    )
    parser.add_argument('-d', '--delimiter', help='Define which delimiter should be used to split the strings on', required=True)
    parser.add_argument('-o', '--output_dir', help='Directory for output that exsists', required=True)
    parser.add_argument('-i', '--input',  help='Obfuscated AutoIT file', required=True)
    parser.add_argument('-f', '--function', help='Name of function in obfuscated AutoIT which deocdes strings', required=True)
    return parser.parse_args()


def main():
# Start and ensure the output path exsists
    args = get_args()
    os.makedirs(args.output_dir, exist_ok=True)
    decode_obfuscated_file(args)


if __name__ == '__main__':
    main()
