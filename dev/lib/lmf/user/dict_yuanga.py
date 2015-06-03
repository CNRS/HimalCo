#! /usr/bin/env python

## Needed to import LMF library properly
# Also automatically define 'user_path' as location of lib/lmf/user/ folder
from startup import *
import os

# Add user yuanga folder to path
sys.path.append(user_path + 'yuanga')

# Create result folder
if not os.path.exists(user_path + "yuanga/result"):
    os.mkdir(user_path + "yuanga/result")

# Import user customized configuration
from setting import lmf2tex, items, reverse_items, sd_order, sd_errors, compare_sd, sd_list

# Read user configuration
lexical_resource = lmf.read_config(user_path + "yuanga/config.xml")

# Read MDF file and set lexicon identifier
lexical_resource = lmf.read_mdf(id="yuanga", encoding='latin-1')

# Display global information
print lexical_resource.get_bibliographic_citation()

# Classify lexicon twice: first by lexeme, then by semantic domain
xml_order = lmf.read_sort_order(user_path + "yuanga/sort_order.xml")
lexical_resource.get_lexicon("yuanga").sort_lexical_entries(sort_order=xml_order)
lexical_resource.get_lexicon("yuanga").sort_lexical_entries(items=items, sort_order=sd_order, comparison=compare_sd)

# Display all undefined semantic domains
for sd in sd_errors:
    print sd

# Write XML LMF file
lmf.write_xml_lmf(lexical_resource, user_path + "yuanga/result/yuanga.xml")

# Write document file
lmf.write_doc(lexical_resource, user_path + "yuanga/result/yuanga.docx", items=items, sort_order=sd_list)

# Write MDF file
lmf.write_mdf(lexical_resource, user_path + "yuanga/result/yuanga.txt")

# Write HTML file
os.system("xsltproc -o " + user_path + "yuanga/result/yuanga.html " + user_path + "../src/output/htm.xsl " + user_path + "yuanga/result/yuanga.xml")

# Classify lexicon twice: first by French gloss, then by semantic domain
lexical_resource.get_lexicon("yuanga").sort_lexical_entries(items=reverse_items, sort_order=xml_order)
lexical_resource.get_lexicon("yuanga").sort_lexical_entries(items=items, sort_order=sd_order, comparison=compare_sd)

# Write document file
lmf.write_doc(lexical_resource, user_path + "yuanga/result/reverse_yuanga.docx", items=items, sort_order=sd_list, reverse=True)

# Release created objects
del lexical_resource
