#! /usr/bin/env python

# Go under dev/lib/lmf/ and launch this script using the following command:
# ./user/na/alexis/run_na.py

import sys, os

# Define 'user_path' as path location of lib/lmf/user/ folder
user_path = sys.path[0] + '/../../'

# Add na configuration folder to path
sys.path.append(user_path + 'na')

# Add lib/ folder to path
sys.path.append(user_path + '../..')

# Import LMF library
import lmf

# Import user customized configuration
from setting import tex_eng, tex_fra, items

# Read user configuration
lexical_resource = lmf.read_config(user_path + "na/alexis/config.xml")

# Read MDF file and set lexicon identifier
os.system("python " + user_path + "../src/utils/eol/eol.py -i " + user_path + "../../../../dict/na/toolbox/Dictionary.txt -o " + user_path + "na/result/dictionary-eol.txt")
lexical_resource = lmf.read_mdf(id="na")

# Classify lexicon
xml_order = lmf.read_sort_order(user_path + "na/sort_order.xml")
lexical_resource.get_lexicon("na").sort_lexical_entries(items=items, sort_order=xml_order)

# Write LaTeX files
lmf.write_tex(lexical_resource, user_path + "na/result/dictionary_eng.tex", preamble=user_path + "na/alexis/na.tex", lmf2tex=tex_eng, items=items, sort_order=xml_order)
lmf.write_tex(lexical_resource, user_path + "na/result/dictionary_fra.tex", preamble=user_path + "na/alexis/na.tex", lmf2tex=tex_fra, items=items, sort_order=xml_order)

# Release created objects
del lexical_resource