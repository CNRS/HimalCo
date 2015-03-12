#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config.mdf import mdf_lmf, lmf_mdf, mdf_semanticRelation
from common.range import partOfSpeech_range
from config.tex import lmf_to_tex, partOfSpeech_tex
from utils.io import EOL
import output.tex as tex
from common.defs import VERNACULAR, NATIONAL, ENGLISH, REGIONAL

## To define languages and fonts
import config
FRENCH = "French"

## Possible values allowed for LMF part of speech LexicalEntry attribute
partOfSpeech_range.update([
    "ideophone.1",
    "ideophone.2",
    "ideophone.3",
    "ideophone.4",
    "ideophone.5",
    "ideophone.6",
    "ideophone.7",
    "ideophone.8",
    "possessed noun",
    "stative intransitive verb",
    "expression"
])

## Functions to process some MDF fields (input)
def remove_char(value):
    """Function to remove '_', '^', '$', '&' character at the beginning of 'lx', 'se', 'a', 'xv', 'cf' MDF fields.
    """
    return value.lstrip('_^$&')

## Functions to process some MDF fields (output)
def process_audio(lexical_entry):
    sf = []
    for form_representation in lexical_entry.get_form_representations():
        if form_representation.get_audio() is not None and form_representation.get_audio().get_fileName() is not None:
            sf.append(form_representation.get_audio().get_fileName())
    return sf

mdf_lmf.update({
    "lx"    : lambda lx, lexical_entry: lexical_entry.set_lexeme(remove_char(lx)),
    "a"     : lambda a, lexical_entry: lexical_entry.set_variant_form(remove_char(a), type="phonetics"),
    "se"    : lambda se, lexical_entry: lexical_entry.create_and_add_related_form(remove_char(se), mdf_semanticRelation["se"]),
    "xv"    : lambda xv, lexical_entry: lexical_entry.create_example(remove_char(xv), language=config.xml.vernacular),
    "cf"    : lambda cf, lexical_entry: lexical_entry.create_and_add_related_form(remove_char(cf), mdf_semanticRelation["cf"]),
    "ps"    : lambda ps, lexical_entry: lexical_entry.set_partOfSpeech(ps, range=partOfSpeech_range)
})

lmf_mdf.update({
    "sf" : lambda lexical_entry: process_audio(lexical_entry)
})

## Mapping between LMF part of speech LexicalEntry attribute value and LaTeX layout (output)
partOfSpeech_tex.update({
    "ideophone.1"               : "idph.1",
    "ideophone.2"               : "idph.2",
    "ideophone.3"               : "idph.3",
    "ideophone.4"               : "idph.4",
    "ideophone.5"               : "idph.5",
    "ideophone.6"               : "idph.6",
    "ideophone.7"               : "idph.7",
    "ideophone.8"               : "idph.8",
    "possessed noun"            : "np",
    "stative intransitive verb" : "vi.s",
    "expression"                : "expr"
})

## Functions to process some LaTeX fields (output)

def format_lexeme(lexical_entry, font):
    import output.tex as tex
    lexeme = font[VERNACULAR](lexical_entry.get_lexeme())
    result = "\\hspace{-1cm} "
    if lexical_entry.get_homonymNumber() is not None:
        # Add homonym number to lexeme
        lexeme += " \\textsubscript{" + str(lexical_entry.get_homonymNumber()) + "}"
    if lexical_entry.get_contextual_variations() is not None and len(lexical_entry.get_contextual_variations()) != 0:
        # Format contextual variations
        for var in lexical_entry.get_contextual_variations():
            result += " " + font[VERNACULAR](var)
        result += " (from: " + lexeme + ")."
    else:
        # Format lexeme
        result += lexeme
    for form in lexical_entry.get_variant_forms(type = "phonetics"):
        result += " / " + font[VERNACULAR](form)
    result += " \\hspace{0.1cm} \\hypertarget{" + tex.format_uid(lexical_entry, font) + "}{}" + EOL
    if not lexical_entry.is_subentry():
        result += "\markboth{" + lexeme + "}{}" + EOL
    return result

def format_notes(lexical_entry, font):
    abbreviations = dict({
    })
    result = ""
    for note in lexical_entry.find_notes(type="grammar"):
        try:
            note = abbreviations[note]
        except KeyError:
            pass
        result += "\mytextsc{" + note + "} "
    return result

def format_definitions(lexical_entry, font, languages):
    result = ""
    for sense in lexical_entry.get_senses():
        for language in languages:
            if len(sense.find_definitions(language)) != 0:
                for definition in sense.find_definitions(language):
                    if language == config.xml.vernacular:
                        result += font[VERNACULAR](definition) + ". "
                    elif language == config.xml.national:
                        result += font[NATIONAL](tex.handle_font(definition)) + ". "
                    elif language == config.xml.regional:
                        # Do not display Tibetan for now (dr)
                        pass #result += "\\textit{[Regnl: " + font[REGIONAL](definition) + "]}. "
                    else:
                        result += definition + ". "
            elif len(sense.find_glosses(language)) != 0:
                for gloss in sense.find_glosses(language):
                    if language == config.xml.vernacular:
                        result += font[VERNACULAR](gloss) + ". "
                    elif language == config.xml.national:
                        result += font[NATIONAL](tex.handle_font(gloss)) + ". "
                    elif language == config.xml.regional:
                        # Do not display Tibetan for now (gr)
                        pass #result += "\\textit{[Regnl: " + font[REGIONAL](gloss) + "]}. "
                    else:
                        result += gloss + ". "
            if len(sense.get_translations(language)) != 0:
                for translation in sense.get_translations(language):
                    if language == config.xml.national:
                        result += font[NATIONAL](translation) + ". "
                    elif language == config.xml.regional:
                        result += "\\textbf{rr:}\\textit{[Regnl: " + translation + "]}. "
                    else:
                        result += translation + ". "
    return result

def format_examples(lexical_entry, font):
    result = ""
    for sense in lexical_entry.get_senses():
        for context in sense.get_contexts():
            result += u"\u00B6 "
            for example in context.find_written_forms(config.xml.vernacular):
                result += font[VERNACULAR](example) + EOL
            for example in context.find_written_forms(config.xml.English):
                result += example + EOL
            for example in context.find_written_forms(config.xml.national):
                result += "\\textit{" + font[NATIONAL](tex.handle_font(example)) + "}" + EOL
            for example in context.find_written_forms(config.xml.regional):
                # Do not display Tibetan for now (xr)
                pass #result += "\\textit{[" + font[REGIONAL](example) + "]}" + EOL
    return result

def format_usage_notes(lexical_entry, font):
    result = ""
    for sense in lexical_entry.get_senses():
        for usage in sense.find_usage_notes(language=config.xml.vernacular):
            result += "\\textit{VerUsage:} " + font[VERNACULAR](usage) + " "
        for usage in sense.find_usage_notes(language=config.xml.English):
            result += "\\textit{Usage:} " + usage + " "
        for usage in sense.find_usage_notes(language=config.xml.national):
            result += "\\textit{NatUsage:} " + font[NATIONAL](tex.handle_font(usage)) + " "
        for usage in sense.find_usage_notes(language=config.xml.regional):
            result += "\\textit{[" + font[REGIONAL](usage) + "]} "
    return result

def format_encyclopedic_informations(lexical_entry, font):
    result = ""
    for sense in lexical_entry.get_senses():
        for information in sense.find_encyclopedic_informations(language=config.xml.vernacular):
            result += font[VERNACULAR](information) + " "
        for information in sense.find_encyclopedic_informations(language=config.xml.English):
            result += information + " "
        for information in sense.find_encyclopedic_informations(language=config.xml.national):
            result += font[NATIONAL](tex.handle_font(information)) + " "
        for information in sense.find_encyclopedic_informations(language=config.xml.regional):
            # Do not display Tibetan for now (er)
            pass #result += "\\textit{[" + font[REGIONAL](information) + "]} "
    return result

def format_paradigms(lexical_entry, font):
    result = ""
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
    tex_entry = ""
    # lexeme, id and phonetic variants
    tex_entry += format_lexeme(lexical_entry, font)
    # sound
    tex_entry += tex.format_audio(lexical_entry, font)
    # part of speech
    tex_entry += tex.format_part_of_speech(lexical_entry, font)
    # grammatical notes
    tex_entry += format_notes(lexical_entry, font)
    # definition/gloss and translation
    tex_entry += format_definitions(lexical_entry, font, languages=[config.xml.vernacular, config.xml.French, config.xml.national])
    # example
    tex_entry += format_examples(lexical_entry, font)
    # usage note
    tex_entry += format_usage_notes(lexical_entry, font)
    # encyclopedic information
    tex_entry += format_encyclopedic_informations(lexical_entry, font)
    # restriction
    tex_entry += tex.format_restrictions(lexical_entry, font)
    # synonym, antonym, morphology, related form
    tex_entry += tex.format_related_forms(lexical_entry, font)
    # borrowed word
    tex_entry += tex.format_borrowed_word(lexical_entry, font)
    # etymology
    tex_entry += tex.format_etymology(lexical_entry, font)
    # paradigms
    tex_entry += tex.format_paradigms(lexical_entry, font)
    tex_entry += format_paradigms(lexical_entry, font)
    # semantic domain
    tex_entry += tex.format_semantic_domains(lexical_entry, font)
    # source
    tex_entry += tex.format_source(lexical_entry, font)
    # status
    tex_entry += tex.format_status(lexical_entry, font)
    # date
    tex_entry += tex.format_date(lexical_entry, font)
    # Handle reserved characters and fonts
    tex_entry = handle_reserved(tex_entry)
    tex_entry = tex.handle_fv(tex_entry, font)
    tex_entry = tex.handle_fn(tex_entry, font)
    # Special formatting
    tex_entry = tex.handle_pinyin(tex_entry)
    tex_entry = tex.handle_caps(tex_entry)
    return tex_entry + EOL