# pdfcolsplit
Split LaTeX/IEEEtran generated PDF files

Documents generated with the IEEEtran document class in LaTeX have a two-column layout. If you feel a 
need to convert each of those two-column pages into two separate pages with one of the columns on the
left and a lot of white space on the right, you can use this tool.

Why would you want to do this? This provides huge margins for handwritten notes, such as in an
educational environment.

![Image of three PDF pages, the first two pages show only one column of text, the third page shows the
the original page with both columns](doc/editing-examples.jpg)

I manage two "conference seminars" where students write papers, submit them anonymously, peer-review
papers of other students (double-blind), re-submit, and give a talk on a conference day. There's
also a tutor role, and a tutor will need to add many comments to early versions of the papers.

Since some documents contain floats that span both columns (pictures, tables), the script adds the
original document at the end so that the full view of such objects is available; in the one-column
pages those objects are simply cut in half.

## Requirements

You need to have LaTeX (the `pdflatex` command) installed, and you also need `pdfinfo` from the
`poppler-utils` package. The script has only been tested on a Mac but should work just fine on a 
Linux system.

## Installation

Download `pdfcolsplit.py`, make it executable, move it to a folder that is in your `$PATH`, perhaps
lose the `.py` ending.

## Usage

Run
```
pdfcolsplit.py filename.pdf
```
to have the script generate `filename-comments.pdf`.


## Trusting an `rm -r`

The Python script runs `rm -r` in order to delete the temp directory. Set
```
ASK_BEFORE_DELETE = True
```
to make it ask if you really want to delete; then hit Ctrl+C to keep the directory (the script
shows the location).
