#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Go under dev/lib/lmf/ and launch this script using the following command:
# ./user/na/alexis/run_na.py

import sys, os

# Define 'user_path' as path location of lib/lmf/user/ folder
user_path = sys.path[0] + '/../../'

# Add na configuration folder to path
sys.path.append(user_path + 'na')

# Add lib/ folder to path
sys.path.append(user_path + '../..')

# Create result folder
if not os.path.exists(user_path + "na/result"):
    os.mkdir(user_path + "na/result")

# Import LMF library
import lmf

# Import user customized configuration
from setting import tex_eng, tex_fra, items, classify_lexicon

# Read user configuration
lexical_resource = lmf.read_config(user_path + "na/config.xml")

# Read MDF file, generate UID and set lexicon identifier
os.system("python " + user_path + "../src/utils/eol/eol.py -i " + user_path + "../../../../dict/na/toolbox/Dictionary.txt -o " + user_path + "na/result/dictionary-eol.txt")
os.system("python " + user_path + "../src/utils/uid/uid.py -i " + user_path + "na/result/dictionary-eol.txt -o " + user_path + "na/result/dictionary-uid.txt")
lexical_resource = lmf.read_mdf(id="na")

# Classify lexicon
(xml_order, xml_type) = lmf.read_sort_order(user_path + "na/sort_order.xml")
classify_lexicon(lexical_resource.get_lexicon("na"), xml_order, xml_type)

# Generate tables
os.system("python " + user_path + "../src/utils/tables/tables.py -i " + user_path + "../../../../dict/na/toolbox/Dictionary.txt -e " + user_path + "na/result/table_eng.tex -f " + user_path + "na/result/table_fra.tex")

# Write LaTeX files
lmf.write_tex(lexical_resource, user_path + "na/result/dictionary_eng.tex", preamble=user_path + "na/preamble.tex", introduction=user_path + "na/introduction_eng.tex", lmf2tex=tex_eng, items=items, sort_order=xml_order, tables=[user_path + "na/result/table_eng.tex"], title="Online Na-English-Chinese-French Dictionary (version 1.0)")
lmf.write_tex(lexical_resource, user_path + "na/result/dictionary_fra.tex", preamble=user_path + "na/preamble.tex", introduction=user_path + "na/introduction_fra.tex", lmf2tex=tex_fra, items=items, sort_order=xml_order, tables=[user_path + "na/result/table_fra.tex"], title=u"Dictionnaire na-chinois-français en ligne (version 1.0)", tex_language="french")

# Release created objects
del lexical_resource
