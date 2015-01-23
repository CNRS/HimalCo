#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config.mdf import mdf_lmf, lmf_mdf, mdf_order, mdf_semanticRelation, VERNACULAR, NATIONAL, ENGLISH, REGIONAL, ps_partOfSpeech
from common.range import partOfSpeech_range
from config.tex import lmf_to_tex, partOfSpeech_tex
from utils.io import EOL

AUDIO_PATH = "file:///Users/celine/Work/CNRS/workspace/HimalCo/dict/khaling/data/audio/"

def get_ge(lexical_entry):
    for sense in lexical_entry.get_senses():
        if len(sense.find_glosses(ENGLISH)) != 0:
            return sense.find_glosses(ENGLISH)[0]
    return "aaa"
items=lambda lexical_entry: get_ge(lexical_entry)

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
    # khaling
    "vi-t"          : "bitransistive verb",         # labial verb
    "vt-i"          : "bitransistive verb",         # labial verb
    "Vi"            : "intransitive verb",          # intransitive verb
    "vt4"           : "transitive verb",            # transitive verb
    "???"           : "unknown"
})

## Possible values allowed for LMF part of speech LexicalEntry attribute
partOfSpeech_range.update([
    "unknown"
])

mdf2lmf = dict(mdf_lmf)
mdf2lmf.update({
    "a"         : lambda a, lexical_entry: lexical_entry.set_spelling_variant(a),
    "nep"       : lambda nep, lexical_entry: lexical_entry.set_variant_form(nep, type="orthography"),
    "wav"       : lambda wav, lexical_entry: None,
    "se2"       : lambda se2, lexical_entry : None,
    # Generated markers
    "lx_dev"    : lambda lx_dev, lexical_entry : None,
    "lx_gen"    : lambda lx_gen, lexical_entry : None,
    "lc"        : lambda lc, lexical_entry : None,
    "lc_dev"    : lambda lc_dev, lexical_entry : None,
    "se_gen"    : lambda se_gen, lexical_entry : None,
    "se2_gen"   : lambda se2_gen, lexical_entry : None,
    "se2_dev"   : lambda se2_dev, lexical_entry : None,
    "xv_dev"    : lambda xv_dev, lexical_entry : None,
    "1s_dev"    : lambda a1s_dev, lexical_entry : None,
    "1d_dev"    : lambda a1d_dev, lexical_entry : None,
    "1e_dev"    : lambda a1e_dev, lexical_entry : None,
    "2s_dev"    : lambda a2s_dev, lexical_entry : None,
    "3s_dev"    : lambda a3s_dev, lexical_entry : None,
    "4s_dev"    : lambda a4s_dev, lexical_entry : None
})

lmf2mdf = dict(lmf_mdf)
lmf2mdf.update({
    "a"     : lambda lexical_entry: lexical_entry.get_spelling_variants(),
    "nep"   : lambda lexical_entry: lexical_entry.get_variant_forms(type="orthography")
})

order = list(mdf_order)
order.insert(1, "a")
order.insert(2, "nep")

## Mapping between LMF part of speech LexicalEntry attribute value and LaTeX layout (output)
partOfSpeech2tex = partOfSpeech_tex
partOfSpeech2tex.update({
    "unknown" : "\\textcolor{red}{?}"
})

## Functions to process some LaTeX fields (output)

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
    # lexeme and id
    tex_entry += tex.format_lexeme(lexical_entry, font)
    # TODO: phonetic variants ? or variant form ?
    # sound
    #tex_entry += tex.format_audio(lexical_entry, font)
    # part of speech
    tex_entry += tex.format_part_of_speech(lexical_entry, font, mapping=partOfSpeech2tex)
    # grammatical notes
    tex_entry += tex.format_notes(lexical_entry, font)
    # definition/gloss and translation
    tex_entry += tex.format_definitions(lexical_entry, font, languages=[VERNACULAR, ENGLISH, NATIONAL])
    # example
    tex_entry += tex.format_examples(lexical_entry, font)
    # usage note
    tex_entry += tex.format_usage_notes(lexical_entry, font)
    # encyclopedic information
    tex_entry += tex.format_encyclopedic_informations(lexical_entry, font)
    # restriction
    tex_entry += tex.format_restrictions(lexical_entry, font)
    # synonym, antonym, morphology, related form
    tex_entry += tex.format_related_forms(lexical_entry, font)
    # TODO: variant form?
    tex_entry += tex.format_variant_forms(lexical_entry, font)
    # borrowed word
    tex_entry += tex.format_borrowed_word(lexical_entry, font)
    # etymology
    tex_entry += tex.format_etymology(lexical_entry, font)
    # paradigms
    tex_entry += tex.format_paradigms(lexical_entry, font)
    tex_entry += format_paradigms(lexical_entry, font)
    # semantic domain
    tex_entry += tex.format_semantic_domains(lexical_entry, font)
    # TODO? bibliography
    tex_entry += tex.format_bibliography(lexical_entry, font)
    # source
    tex_entry += tex.format_source(lexical_entry, font)
    # status
    tex_entry += tex.format_status(lexical_entry, font)
    # date
    tex_entry += tex.format_date(lexical_entry, font)
    # Handle reserved characters: \ { } $ # & _ ^ ~ %
    if tex_entry.find("{") != -1:
        tex_entry = tex.format_font(tex_entry)
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
    tex_entry = tex.format_fn(tex_entry, font)
    tex_entry = tex.format_fv(tex_entry, font)
    # Special formatting
    if tex_entry.encode("utf8").find("°") != -1:
        tex_entry = tex.format_small_caps(tex_entry)
    return tex_entry + EOL
