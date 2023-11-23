#!/usr/bin/env python
#
# (c) 2023 Hans-Georg Esser <esser.hans-georg@fh-swf.de>
#
# - make this script executable, put somewhere in $PATH
# - run on any IEEEtran-based PDF to separate each column
#   into a single page; add original pages at the end;
#   this will generate a new PDF named origname-comments.pdf
#   with 3n pages when original file had n pages.

import sys
from os import mkdir, chdir, system, getcwd
from os.path import join as pathjoin
from tempfile import mkdtemp
from subprocess import check_output

# requires external programs:
# - pdfinfo
# - pdflatex

# constants
leftcolstring  = "trim=0 0 10.5cm 0, clip, offset=-5.2cm 0"
rightcolstring = "trim=10.5cm 0 0 0, clip, offset=-4cm 0"
ASK_BEFORE_DELETE = False  # set to True if not trusted

# LaTeX header and footer
header = """\\documentclass[a4paper]{article}
\\usepackage[final]{pdfpages}

\\begin{document}
"""

footer = """\\end{document}
"""

# function runs rm -r to delete temp directory - if allowed
def delete_temp_dir (dirname):
	if ASK_BEFORE_DELETE:
		try:
			check = input("Going to delete %s directory - ctrl+c to skip..." % dirname)
		except:
			print()
			sys.exit(0)
	system("rm -r %s" % dirname)


# program starts here
argc = len(sys.argv)
toolname = sys.argv[0]

# missing argument, too many arguments
if (argc == 1) or (argc > 2):
	print("%s: Expects a PDF file argument" % toolname)
	sys.exit(0)

# check if argv[1] is valid input filename
try:
	filename = sys.argv[1]
	with open(filename, "rb") as temp:
		fourbytes = temp.read(4)
except:
	print("%s: Cannot open input file: %s" % (toolname, filename))
	sys.exit(1)

#DEBUG: print ("fourbytes: %s" % fourbytes)

# check it is a PDF
if fourbytes != b'%PDF':
	print("%s: Input file is not a PDF file: %s" % (toolname, filename))
	sys.exit(1)

# check we can get a page count
pages = -1
try:
	res = check_output(["pdfinfo", filename])
	for line in res.splitlines():
		parts = line.split()
		#DEBUG: print("%s // %s" % (parts[0],parts[1]))
		if parts[0] == b'Pages:':
			pages = int(parts[1])
except:
	print("%s: Cannot determine page size of input file: %s" % (toolname, filename))
	sys.exit(1)

if pages == -1:
	print("%s: Cannot determine page size of input file: %s" % (toolname, filename))
	sys.exit(1)

#DEBUG: print ("DEBUG: pages = %d" % pages)

# create temp directory
tempdir = mkdtemp()

# copy source PDF to tempdir
workdir = getcwd()
ret = system("cp \"%s\" %s/input.pdf" % (filename, tempdir))
if ret != 0:
	print("%s: Cannot copy source PDF (%s) to temp directory (%s)" 
		% (toolname, filename, tempdir))
	sys.exit(1)
chdir(tempdir)
#DEBUG: print ("DEBUG: tempdir = %s" % tempdir)
#DEBUG: system ("ls -l")

texfile = "x.tex"
pdffile = "x.pdf"
# redirect stdout to texfile
with open(texfile, 'w') as sys.stdout:
	print(header)
	for i in range(pages):
		print("\includepdf[pages=%d, %s]{input.pdf}" % (i+1, leftcolstring) )
		print("\includepdf[pages=%d, %s]{input.pdf}" % (i+1, rightcolstring) )
	# all pages, original document
	print("\includepdf[pages=-]{input.pdf}")
	print(footer)

# restore stdout
sys.stdout = sys.__stdout__
#DEBUG: print("DEBUG: Running LaTeX...")
system("pdflatex %s > /dev/null" % texfile)

targetname = pathjoin(workdir,filename.replace(".pdf","-comments.pdf"))
system("mv %s \"%s\"" % (pdffile, targetname))

# delete temp directory
delete_temp_dir (tempdir)
