# combine
> A simple utility to combine files

Combines several files into a single output file. Accepts UNIX style wildcards for pattern matching.

## Requirements
Python >= 2.5


## Usage Examples
Combine every file in the current working directory into out.txt (excluding the script itself):
```sh
python combine.py -o out.txt
```

Combine every .bin file in ./foo/bar/ into out.bin (keeping each original file):
```sh
python combine.py -k -d ./foo/bar/ -e .bin -o out.bin
```

Combine files named 1, 2, or 3 (with any extension) in a descending order in the current working directory:
```sh
python combine.py -n [1-3] -s DESC -o out.txt
```

***Note: if -k flag isn't included, original files are removed after combining***