# Taurus-Decode
A python script that replaces obfuscated strings within the Taurus AutoIT loader with their de-obfuscated equivalent. This is a proof-of-concept and it's not anticipated to be maintained over time. 

# Usage

```
-d, --delimiter,
	Define which delimiter should be used to split the strings on
-o, --output,
	Directory for output that exsists
-i, --input,
	Obfuscated AutoIT file
-f, --function,
	Name of function in obfuscated AutoIT which deocdes strings
```

## Example 
```
taurus_decode.py -d ">" -i Poi.xltx -o /path/to/output -f qLAEMpnctIeWhZ
```

# License
This is released unter the Apache-2.0 license included in the repo. 
