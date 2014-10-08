#! /usr/bin/env python

## Needed to import LMF library properly
# Also automatically define 'user_path' as location of lib/lmf/user/ folder
from startup import *

# Import user customized configuration if any
from na import mdf2lmf

# Read MDF file
input = lmf.read_mdf(user_path + "input.txt", mdf2lmf)

# Set some information
input.set_creationDate("2014-10-01")
input.set_lastUpdate("2014-10-10")
input.set_author("Celine Buret")
input.set_description("This is a testing lexicon.")
print input.get_bibliographicCitation()

# Write XML LMF file
lmf.write_xml_lmf(input, user_path + "output.xml")

# Read XML LMF file
output = lmf.read_xml_lmf(user_path + "output.xml")

# Write LaTeX file
lmf.write_tex(output, user_path + "output.tex", preamble=user_path + "config/japhug.tex")

# Write MDF file
lmf.write_mdf(output, user_path + "output.txt")

# Release created objects
del input, output
