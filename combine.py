import argparse
import glob
import os
import re
import shutil
import sys


def parse_args():
	p = argparse.ArgumentParser(description="A simple utility to combine files", epilog="Accepts UNIX style wildcards")

	p.add_argument(
		"-d",
		"--directory",
		type=str,
		default="",
		help="location of files to combine"
	)

	p.add_argument(
		"-e",
		"--extension",
		type=str,
		default=".*",
		help="extension of files to combine"
	)

	p.add_argument(
		"-n",
		"--name",
		type=str,
		default="*",
		help="file naming pattern"
	)

	p.add_argument(
		"-k",
		"--keep",
		action="store_true",
		help="keep original files after combining"
	)

	p.add_argument(
		"-s",
		"--sort",
		const="all",
		nargs="?",
		choices=["ASC", "DESC"],
		default="ASC",
		help="order in which to combine files"
	)

	p.add_argument(
		"-v",
		"--version",
		help="print the program version",
		action="store_true"
	)

	required = p.add_argument_group("required arguments")

	required.add_argument(
		"-o",
		"--output",
		type=argparse.FileType("wb"),
		help="output file",
		required=('-v' not in sys.argv and '--version' not in sys.argv)
	)

	return p.parse_args()


def handle_args(args):
	if args.version:
		print("combine v1.0\nWritten by Adeem Mawani")
		sys.exit(0)

	# Handle extension input
	if args.extension[0] != ".":
		args.extension = "." + args.extension

	# Handle sorting input
	if args.sort.upper() == "DESC":
		args.desc = True
	else:
		args.desc = False


if __name__ == "__main__":
	arg = parse_args()
	handle_args(arg)

	# Pattern to match files
	inclusion_pattern = arg.directory + arg.name + arg.extension

	# Get all files that match the pattern (ignoring the exclusions)
	exclude = ["combine.py", arg.output.name]
	file_list = [fn for fn in glob.glob(inclusion_pattern) if os.path.basename(fn) not in exclude]

	# Sort the list naturally
	file_list.sort(reverse=arg.desc, key=lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)])

	# Combine each file
	for f in file_list:
		with open(f, "rb") as infile:
			shutil.copyfileobj(infile, arg.output)

		print("[*] Combining: " + os.path.basename(f))

		if not arg.keep:
			os.remove(f)

	# Close output file descriptor
	arg.output.close()

	if file_list:
		print("[*] Done")
	else:
		print("[!] No files matched")
