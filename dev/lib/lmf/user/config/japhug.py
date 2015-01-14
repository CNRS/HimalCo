#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config.mdf import mdf_lmf, lmf_mdf, mdf_order, mdf_semanticRelation, VERNACULAR, NATIONAL, ENGLISH, REGIONAL, ps_partOfSpeech
from common.range import partOfSpeech_range
from config.tex import lmf_to_tex, partOfSpeech_tex
from utils.io import EOL

FRENCH = "fra"
AUDIO_PATH = "file:///Users/celine/Work/CNRS/workspace/HimalCo/dict/japhug/data/audio/"

ranks = dict({'':0,
    'a':1, 'æ':1.1, # 1.1 -> khaling/koyi/thulung
    'ɤ':2,
    'b':3, 'β':3.1,
    'c':4,
    'ɕ':5,
    'd':6,
    'e':7,
    'f':8,
    'g':9,
    'ɣ':10,
    'ɢ':11,
    'H':12, 'h':12,'ɦ':12.1,
    'i':13,
    'j':14,
    'ɟ':15,
    'K':16, 'k':16,
    'l':17,
    'ɬ':18,
    'm':19,
    'n':20,
    'ɳ':21,'ɲ':21.1,
    'ŋ':22,
    'ɴ':23,
    'o':24,
    'p':25,
    'q':26,
    'r':27,
    'ʀ':28,'ʁ':28.1,
    's':29,
    'ʂ':30,
    't':31,
    'u':32,
    'ɯ':33,
    'v':34,
    'w':35,
    'x':36,
    'χ':37,
    'y':38,
    'z':39,
    'ʐ':40,
    'ʑ':41,
    'ʕ':42, 'ʔ':42.1, # 42.1 -> khaling/koyi/thulung
    # Special characters
    '¹':43.1, '²':43.2, '³':43.3, '⁴':43.4, ' ':43.5, '_':43.6, '-':43.7})
unicode_ranks = ({})
for key in ranks.keys():
    unicode_ranks.update({key.decode(encoding='utf8'):ranks[key]})

## Mapping between 'ps' MDF marker value and LMF part of speech LexicalEntry attribute value (input)
ps2partOfSpeech = ps_partOfSpeech
ps2partOfSpeech.update({
    # HimalCo
    "adj"           : "adjective",                  # adjective
    "adv"           : "adverb",                     # adverb(ial)
    "class"         : "classifier",                 # classifier (MDF)
    "clf"           : "classifier",                 # classifier (Leipzig)
    "cnj"           : "conjunction",                # conjunction
    "disc.PTCL"     : "particle",                   # discourse particle
    "ideo"          : "ideophone",                  # ideophones
    "intj"          : "interjection",               # interjection
    "interj"        : "interjection",               # interjection -> khaling
    "lnk"           : "coordinating conjunction",   # linker
    "n"             : "noun",                       # noun
    "Np"            : "possessed noun",             # possessed nouns
    "_poss._pref"   : "possessed noun",             # possessed nouns -> koyi
    "neg"           : "negation",                   # negative
    "num"           : "numeral",                    # number
    "prep"          : "preposition",                # preposition
    "pro"           : "pronoun",                    # pronoun/pronominal
    "vi.s"          : "stative intransitive verb",  # stative intransitive verb
    # japhug
    "cl"            : "classifier",                 # classifier
    "conj"          : "conjunction",                # conjunction
    "expression"    : "expression",                 #
    "idph"          : "ideophone",                  # ideophones
    "idph.1"        : "ideophone.1",                # ideophones
    "idph.2"        : "ideophone.2",                # ideophones
    "idph.3"        : "ideophone.3",                # ideophones
    "idph.4"        : "ideophone.4",                # ideophones
    "idph.5"        : "ideophone.5",                # ideophones
    "idph.6"        : "ideophone.6",                # ideophones
    "idph.7"        : "ideophone.7",                # ideophones
    "idph.8"        : "ideophone.8",                # ideophones
    "n N"           : "noun",                       # noun
    "nq"            : "noun",                       # noun
    "np"            : "possessed noun",             # possessed nouns
    "nP"            : "possessed noun",             # possessed nouns
    "Posp"          : "possessed noun",             # possessed nouns
    "Post"          : "possessed noun",             # possessed nouns
    "postp"         : "possessed noun",             # possessed nouns
    "quant"         : "numeral",                    # number
    "part"          : "particle",                   # discourse particle
    "Part"          : "particle",                   # discourse particle
    "vi-"           : "intransitive verb",          # intransitive verb
    "vinh"          : "stative intransitive verb",  # stative intransitive verb
    "vStat"         : "stative intransitive verb",  # stative intransitive verb
    "vst"           : "stative intransitive verb",  # stative intransitive verb
    "vs"            : "stative intransitive verb",  # stative intransitive verb
    "vl"            : "bitransistive verb",         # labial verb
    "vlb"           : "bitransistive verb",         # labial verb
    "vlab"          : "bitransistive verb",         # labial verb
    "T"             : "time noun",                  # ?
    "indef"         : "indefinite determiner"       # ?
})

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

mdf2lmf = dict(mdf_lmf)
mdf2lmf.update({
    "hbf"   : lambda hbf, lexical_entry: lexical_entry.set_bibliography(hbf),
    "wav"   : lambda wav, lexical_entry: lexical_entry.set_audio(file_name=AUDIO_PATH + "wav/" + wav + ".wav", quality="very good", audio_file_format="wav"),
    "wav8"  : lambda wav8, lexical_entry: lexical_entry.set_audio(file_name=AUDIO_PATH + "mp3/8_" + wav8 + ".wav", quality="low", audio_file_format="wav"),
    "a"     : lambda a, lexical_entry: lexical_entry.set_variant_form(remove_char(a), type="phonetics"),
    "ge"    : lambda ge, lexical_entry: lexical_entry.set_gloss(ge, language=FRENCH),
    "lx"    : lambda lx, lexical_entry: lexical_entry.set_lexeme(remove_char(lx)),
    "se"    : lambda se, lexical_entry: lexical_entry.create_and_add_related_form(remove_char(se), mdf_semanticRelation["se"]),
    "xv"    : lambda xv, lexical_entry: lexical_entry.create_example(remove_char(xv), language=VERNACULAR),
    "cf"    : lambda cf, lexical_entry: lexical_entry.create_and_add_related_form(remove_char(cf), mdf_semanticRelation["cf"]),
    "ps"    : lambda ps, lexical_entry: lexical_entry.set_partOfSpeech(ps, range=partOfSpeech_range, mapping=ps2partOfSpeech)
})

lmf2mdf = dict(lmf_mdf)
lmf2mdf.update({
    "sf" : lambda lexical_entry: process_audio(lexical_entry),
    "gf" : lambda sense: sense.find_glosses(FRENCH)
})

order = list()
# Copy list of MDF markers without references
def copy_list(in_element, out_list):
    if type(in_element) is list:
        sub_list = list()
        out_list.append(sub_list)
        for element in in_element:
            copy_list(element, sub_list)
    else:
        out_list.append(in_element)
for marker in mdf_order:
    copy_list(marker, order)
order[7].insert(15, "gf")
order.insert(1, "sf")

## Mapping between LMF part of speech LexicalEntry attribute value and LaTeX layout (output)
partOfSpeech2tex = partOfSpeech_tex
partOfSpeech2tex.update({
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
    for form_representation in lexical_entry.get_form_representations():
        if form_representation.get_variantForm() is not None and form_representation.get_type() == "phonetics":
            result += " / " + font[VERNACULAR](form_representation.get_variantForm())
    result += " \\hspace{0.1cm} \\hypertarget{" + tex.format_uid(lexical_entry, font) + "}{}" + EOL
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

def format_font(text):
    """Replace '\{xxx}' and '{xxx}' by '\ipa{xxx}' in 'un', 'xn', 'gn', 'dn', 'en'.
    """
    return text.replace("\\{", "{").replace("{", "\\ipa{")

def format_definitions(lexical_entry, font, languages=[VERNACULAR, ENGLISH, NATIONAL, REGIONAL]):
    result = ""
    for sense in lexical_entry.get_senses():
        for language in languages:
            if len(sense.find_definitions(language)) != 0:
                for definition in sense.find_definitions(language):
                    if language == VERNACULAR:
                        result += font[VERNACULAR](definition) + ". "
                    elif language == NATIONAL:
                        result += font[NATIONAL](format_font(definition)) + ". "
                    elif language == REGIONAL:
                        result += "\\textit{[Regnl: " + font[REGIONAL](definition) + "]}. "
                    else:
                        result += definition + ". "
            elif len(sense.find_glosses(language)) != 0:
                for gloss in sense.find_glosses(language):
                    if language == VERNACULAR:
                        result += font[VERNACULAR](gloss) + ". "
                    elif language == NATIONAL:
                        result += font[NATIONAL](format_font(gloss)) + ". "
                    elif language == REGIONAL:
                        result += "\\textit{[Regnl: " + font[REGIONAL](gloss) + "]}. "
                    else:
                        result += gloss + ". "
            if len(sense.get_translations(language)) != 0:
                for translation in sense.get_translations(language):
                    if language == NATIONAL:
                        result += font[NATIONAL](translation) + ". "
                    elif language == REGIONAL:
                        result += "\\textbf{rr:}\\textit{[Regnl: " + translation + "]}. "
                    else:
                        result += translation + ". "
    return result

def format_examples(lexical_entry, font):
    result = ""
    for sense in lexical_entry.get_senses():
        for context in sense.get_contexts():
            result += u"\u00B6 "
            for example in context.find_written_forms(VERNACULAR):
                result += font[VERNACULAR](example) + EOL
            for example in context.find_written_forms(ENGLISH):
                result += example + EOL
            for example in context.find_written_forms(NATIONAL):
                result += "\\textit{" + font[NATIONAL](format_font(example)) + "}" + EOL
            for example in context.find_written_forms(REGIONAL):
                result += "\\textit{[" + font[REGIONAL](example) + "]}" + EOL
    return result

def format_usage_notes(lexical_entry, font):
    result = ""
    for sense in lexical_entry.get_senses():
        for usage in sense.find_usage_notes(language=VERNACULAR):
            result += "\\textit{VerUsage:} " + font[VERNACULAR](usage) + " "
        for usage in sense.find_usage_notes(language=ENGLISH):
            result += "\\textit{Usage:} " + usage + " "
        for usage in sense.find_usage_notes(language=NATIONAL):
            result += "\\textit{NatUsage:} " + font[NATIONAL](format_font(usage)) + " "
        for usage in sense.find_usage_notes(language=REGIONAL):
            result += "\\textit{[" + font[REGIONAL](usage) + "]} "
    return result

def format_encyclopedic_informations(lexical_entry, font):
    result = ""
    for sense in lexical_entry.get_senses():
        for information in sense.find_encyclopedic_informations(language=VERNACULAR):
            result += font[VERNACULAR](information) + " "
        for information in sense.find_encyclopedic_informations(language=ENGLISH):
            result += information + " "
        for information in sense.find_encyclopedic_informations(language=NATIONAL):
            result += font[NATIONAL](format_font(information)) + " "
        for information in sense.find_encyclopedic_informations(language=REGIONAL):
            result += "\\textit{[" + font[REGIONAL](information) + "]} "
    return result

def format_paradigms(lexical_entry, font):
    result = ""
    current_label = None
    for paradigm in lexical_entry.get_paradigms():
        if paradigm.get_paradigmLabel() is not None and paradigm.get_paradigm(language=VERNACULAR) is not None:
            if paradigm.get_paradigmLabel() != current_label:
                current_label = paradigm.get_paradigmLabel()
                # Display label
                result += "\\textit{" + current_label + ":} "
            else:
                # Just add semi-colomn
                result += "; "
            result += font[VERNACULAR](paradigm.get_paradigm(language=VERNACULAR)) + " "
    return result

## Function giving order in which information must be written in LaTeX and mapping between LMF representation and LaTeX (output)
def lmf2tex(lexical_entry, font):
    import output.tex as tex
    tex_entry = ""
    # lexeme, id and phonetic variants
    tex_entry += format_lexeme(lexical_entry, font)
    # sound
    tex_entry += tex.format_audio(lexical_entry, font)
    # part of speech
    tex_entry += tex.format_part_of_speech(lexical_entry, font, mapping=partOfSpeech2tex)
    # grammatical notes
    tex_entry += format_notes(lexical_entry, font)
    # definition/gloss and translation
    tex_entry += format_definitions(lexical_entry, font, languages=[VERNACULAR, FRENCH, NATIONAL])
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
    # Handle reserved characters: \ { } $ # & _ ^ ~ %
    if tex_entry.find("@") != -1:
        tex_entry = tex.format_pinyin(tex_entry)
    if tex_entry.find("#") != -1:
        tex_entry = tex_entry.replace('#', '\#')
    if tex_entry.find("_") != -1:
        tex_entry = tex_entry.replace('_', '\_').replace("\string\_", "\string_")
    if tex_entry.find("& ") != -1:
        tex_entry = tex_entry.replace('& ', '\& ')
    if tex_entry.find("$") != -1:
        tex_entry = tex_entry.replace('$', '')
    if tex_entry.find("^") != -1:
        tex_entry = tex_entry.replace('^', '\^')
    # Handle fonts
    if tex_entry.find("fn:") != -1:
        tex_entry = tex.format_fn(tex_entry)
    if tex_entry.find("fv:") != -1:
        tex_entry = tex.format_fv(tex_entry)
    # Special formatting
    if tex_entry.encode("utf8").find("°") != -1:
        tex_entry = tex.format_small_caps(tex_entry)
    return tex_entry + EOL
