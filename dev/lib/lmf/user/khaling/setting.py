#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config.mdf import mdf_lmf, mdf_semanticRelation, ps_partOfSpeech, pd_grammaticalNumber, pd_person, pd_anymacy, pd_clusivity
from common.range import partOfSpeech_range
from config.tex import lmf_to_tex, partOfSpeech_tex
from utils.io import EOL
from utils.error_handling import Warning
from common.defs import VERNACULAR, NATIONAL, ENGLISH, REGIONAL

## To define languages and fonts
import config

def get_nep(lexical_entry):
    # Consider only the first form
    return lexical_entry.get_citation_forms(script_name="devanagari")[0]

items=lambda lexical_entry: get_nep(lexical_entry)

## Possible values allowed for LMF part of speech LexicalEntry attribute
partOfSpeech_range.update([
    "unknown"
])

def check_lx(lexical_entry, lx_tmp):
    import os
    if lexical_entry.get_lexeme() != lx_tmp and os.name == 'posix':
        # Following line generates an error on Windows
        print unicode(Warning("Lexeme '%s' generated for lexical entry '%s' is not consistant." % (lx_tmp, lexical_entry.get_lexeme())))

def check_nep(lexical_entry, nep):
    import os
    ok = False
    for form in lexical_entry.get_citation_forms(script_name="devanagari"):
        if form == nep:
            ok = True
    if not ok and os.name == 'posix':
        # Following line generates an error on Windows
        print unicode(Warning("Citation form '%s' of lexical entry '%s' is not consistant with generated one." % (nep, lexical_entry.get_lexeme())))

def check_se(lexical_entry, se_tmp):
    import os
    ok = False
    for form in lexical_entry.find_related_forms(mdf_semanticRelation["se"]):
        if form == se_tmp:
            ok = True
    if not ok and os.name == 'posix':
        # Following line generates an error on Windows
        print unicode(Warning("Subentry '%s' generated for lexical entry '%s' is not consistant." % (se_tmp, lexical_entry.get_lexeme())))

mdf_lmf.update({
    "nep"       : lambda nep, lexical_entry: check_nep(lexical_entry, nep), # infinitive in devanagari => check that it corresponds to 'lc_dev' value
    # Generated markers
    "lx_tmp"    : lambda lx_tmp, lexical_entry : check_lx(lexical_entry, lx_tmp), # root in IPA => check that it corresponds to 'lx' value
    "se_tmp"    : lambda se_tmp, lexical_entry : check_se(lexical_entry, se_tmp) # => check that it corresponds to 'se' value
})

## Mapping between LMF part of speech LexicalEntry attribute value and LaTeX layout (output)
partOfSpeech_tex.update({
    "unknown" : "\\textcolor{red}{?}"
})

## Functions to process some LaTeX fields (output)

def format_lexeme(lexical_entry, font):
    import output.tex as tex
    inf_dev = font[NATIONAL](lexical_entry.get_citation_forms(script_name="devanagari")[0]) # lc_dev
    inf_api = font[VERNACULAR](lexical_entry.get_citation_forms(script_name="ipa")[0]) # lc
    root_api = font[VERNACULAR](lexical_entry.get_lexeme()) # lx
    result = "\\hspace{-1cm} "
    if lexical_entry.get_homonymNumber() is not None:
        # Add homonym number to lexeme
        root_api += " \\textsubscript{" + str(lexical_entry.get_homonymNumber()) + "}"
    result += inf_dev + " " + inf_api + " (" + root_api + ")"
    result += " \\hspace{0.1cm} \\hypertarget{" + tex.format_uid(lexical_entry, font) + "}{}" + EOL
    if not lexical_entry.is_subentry():
        result += "\markboth{" + inf_dev + "}{}" + EOL
    return result

def format_notes(lexical_entry, font):
    result = ""
    for note in lexical_entry.find_notes(type="general"):
        result += "[Note: " + font[ENGLISH](note) + "] "
    for note in lexical_entry.find_notes(type="phonology"):
        result += "[Phon: " + font[ENGLISH](note) + "] "
    for note in lexical_entry.find_notes(type="grammar"):
        result += "[Gram: " + font[ENGLISH](note) + "] "
    for note in lexical_entry.find_notes(type="discourse"):
        result += "[Disc: " + font[ENGLISH](note) + "] "
    for note in lexical_entry.find_notes(type="anthropology"):
        result += "[Ant: " + font[ENGLISH](note) + "] "
    for note in lexical_entry.find_notes(type="sociolinguistics"):
        result += "[Socio: " + font[ENGLISH](note) + "] "
    for note in lexical_entry.find_notes(type="question"):
        result += "[Ques: " + font[ENGLISH](note) + "] "
    return result

def format_examples(lexical_entry, font):
    import output.tex as tex
    result = ""
    for sense in lexical_entry.get_senses():
        for context in sense.get_contexts():
            result += "\\begin{exe}" + EOL
            for example in context.find_written_forms(config.xml.vernacular, script_name="ipa"):
                result += "\\sn " + font[VERNACULAR](example) + EOL
            for example in context.find_written_forms(config.xml.vernacular, script_name="devanagari"): # xv_dev
                result += "\\trans " + font[NATIONAL](example) + EOL
            for example in context.find_written_forms(config.xml.English):
                result += "\\trans " + font[ENGLISH](example) + EOL
            for example in context.find_written_forms(config.xml.national):
                result += "\\trans " + font[NATIONAL](tex.handle_font(example)) + EOL
            for example in context.find_written_forms(config.xml.regional):
                result += "\\trans \\textit{[" + font[REGIONAL](example) + "]}" + EOL
            result += "\\end{exe}" + EOL
    return result

def format_examples_compact(lexical_entry, font):
    import output.tex as tex
    result = ""
    for sense in lexical_entry.get_senses():
        for context in sense.get_contexts():
            result += u"\u00B6 "
            for example in context.find_written_forms(config.xml.vernacular, script_name="ipa"):
                result += font[VERNACULAR](example) + EOL
            for example in context.find_written_forms(config.xml.vernacular, script_name="devanagari"): # xv_dev
                result += font[NATIONAL](example) + EOL
            for example in context.find_written_forms(config.xml.English):
                result += font[ENGLISH](example) + EOL
            for example in context.find_written_forms(config.xml.national):
                result += font[NATIONAL](tex.handle_font(example)) + EOL
            for example in context.find_written_forms(config.xml.regional):
                result += "\\textit{[" + font[REGIONAL](example) + "]}" + EOL
    return result

def format_paradigms(lexical_entry, font):
    result = ""
    persons_and_numbers = [(1, 's'), (2, 's'), (3, 's'), (1, 'd'), (3, 'd'), (1, 'p'), (2, 'p')]
    for (pers, nb) in persons_and_numbers:
        for form in lexical_entry.get_word_forms():
            if form.get_person() == pd_person[pers] and form.get_grammaticalNumber() == pd_grammaticalNumber[nb]:
                result += "\\textit{" + str(pers) + nb + ":} "
                for paradigm in form.get_written_forms("ipa"):
                    result += font[VERNACULAR](paradigm) + " "
                for paradigm in form.get_written_forms("devanagari"):
                    result += font[NATIONAL](paradigm) + " "
    for form in lexical_entry.get_word_forms():
        if form.get_anymacy() == pd_anymacy[4] and form.get_grammaticalNumber() == pd_grammaticalNumber['s']:
            result += "\\textit{4s:} "
            for paradigm in form.get_written_forms("ipa"):
                result += font[VERNACULAR](paradigm) + " "
            for paradigm in form.get_written_forms("devanagari"):
                result += font[NATIONAL](paradigm) + " "
    for form in lexical_entry.get_word_forms():
        if form.get_person() == pd_person[1] and form.get_grammaticalNumber() == pd_grammaticalNumber['p'] and form.get_clusivity() == pd_clusivity['e']:
            result += "\\textit{1e:} "
            for paradigm in form.get_written_forms("ipa"):
                result += font[VERNACULAR](paradigm) + " "
            for paradigm in form.get_written_forms("devanagari"):
                result += font[NATIONAL](paradigm) + " "
    # Customized paradigms
    current_label = None
    for paradigm in lexical_entry.get_paradigms():
        if paradigm.get_paradigmLabel() is not None and paradigm.get_paradigm(language=config.xml.vernacular) is not None:
            if paradigm.get_paradigmLabel() != current_label:
                current_label = paradigm.get_paradigmLabel()
                # Display label
                result += "\\textit{" + current_label + ":} "
            else:
                # Just add semi-colomn
                result += "; "
            result += font[VERNACULAR](paradigm.get_paradigm(language=config.xml.vernacular)) + " "
    return result

def handle_reserved(text):
    if text.find("$") != -1:
        text = text.replace('$', '')
    if text.find("#") != -1:
        text = text.replace('#', '\#')
    if text.find("& ") != -1:
        text = text.replace('& ', '\& ')
    if text.find("_") != -1:
        text = text.replace('_', '\_').replace("\string\_", "\string_")
    if text.find("^") != -1:
        text = text.replace('^', '\^')
    return text

## Function giving order in which information must be written in LaTeX and mapping between LMF representation and LaTeX (output)
def lmf2tex(lexical_entry, font):
    import output.tex as tex
    tex_entry = ""
    # lexeme and id
    tex_entry += format_lexeme(lexical_entry, config.xml.font)
    # TODO: phonetic variants ? or variant form ?
    # sound
    tex_entry += tex.format_audio(lexical_entry, config.xml.font)
    # part of speech
    tex_entry += tex.format_part_of_speech(lexical_entry, config.xml.font, mapping=partOfSpeech_tex)
    # grammatical notes
    tex_entry += format_notes(lexical_entry, config.xml.font)
    # definition/gloss and translation
    tex_entry += tex.format_definitions(lexical_entry, config.xml.font, languages=[config.xml.vernacular, config.xml.English, config.xml.national])
    # example
    tex_entry += format_examples_compact(lexical_entry, config.xml.font)
    # usage note
    tex_entry += tex.format_usage_notes(lexical_entry, config.xml.font)
    # encyclopedic information
    tex_entry += tex.format_encyclopedic_informations(lexical_entry, config.xml.font)
    # restriction
    tex_entry += tex.format_restrictions(lexical_entry, config.xml.font)
    # synonym, antonym, morphology, related form
    tex_entry += tex.format_related_forms(lexical_entry, config.xml.font)
    # TODO: variant form?
    tex_entry += tex.format_variant_forms(lexical_entry, config.xml.font)
    # borrowed word
    tex_entry += tex.format_borrowed_word(lexical_entry, config.xml.font)
    # etymology
    tex_entry += tex.format_etymology(lexical_entry, config.xml.font)
    # paradigms
    tex_entry += format_paradigms(lexical_entry, config.xml.font)
    # semantic domain
    tex_entry += tex.format_semantic_domains(lexical_entry, config.xml.font)
    # TODO? bibliography
    tex_entry += tex.format_bibliography(lexical_entry, config.xml.font)
    # source
    tex_entry += tex.format_source(lexical_entry, config.xml.font)
    # status
    tex_entry += tex.format_status(lexical_entry, config.xml.font)
    # date
    tex_entry += tex.format_date(lexical_entry, config.xml.font)
    # Handle reserved characters and fonts
    tex_entry = handle_reserved(tex_entry)
    tex_entry = tex.handle_fv(tex_entry, config.xml.font)
    tex_entry = tex.handle_fn(tex_entry, config.xml.font)
    # Special formatting
    tex_entry = tex.handle_pinyin(tex_entry)
    tex_entry = tex.handle_caps(tex_entry)
    return tex_entry + EOL
