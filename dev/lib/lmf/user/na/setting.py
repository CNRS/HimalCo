#! /usr/bin/env python

from config.mdf import mdf_lmf, lmf_mdf, mdf_order, ps_partOfSpeech, mdf_semanticRelation
from config.tex import partOfSpeech_tex
from output.tex import format_definitions
from utils.io import EOL
from common.defs import VERNACULAR, ENGLISH, NATIONAL, REGIONAL

## To define languages and fonts
import config
FRENCH = "French"

def get_lx(lexical_entry):
    # Do not consider special character '-' or '=' preceeding 'lx'
    return lexical_entry.get_lexeme().lstrip('-=')

items = lambda lexical_entry: get_lx(lexical_entry)

## Functions to process some MDF fields (input)

def process_np(attributes, np, lexical_entry):
    # <type lang>
    try:
        if attributes["type"] == "tone":
            lexical_entry.set_tone(np)
    except KeyError:
        try:
            lexical_entry.set_note(np, type="phonology", language=attributes["lang"])
        except KeyError:
            pass

def process_ec(attributes, ec, lexical_entry):
    # <lang>
    lexical_entry.set_etymology_comment(ec, attributes["lang"])

def process_sd(attributes, sd, lexical_entry):
    # <lang>
    lexical_entry.set_semantic_domain(sd, attributes["lang"])

def process_nt(attributes, nt, lexical_entry):
    # <lang type print>
    type = None
    try:
        if attributes["type"] == "comp":
            type = "comparison"
        elif attributes["type"] == "hist":
            type = "history"
        elif attributes["type"] == "sem":
            type = "semantics"
    except KeyError:
        pass
    language = None
    try:
        language = attributes["lang"]
    except KeyError:
        pass
    lexical_entry.set_note(nt, type=type, language=language)

def process_cf(attributes, cf, lexical_entry):
    # <type>
    lexical_entry.create_and_add_related_form(cf, mdf_semanticRelation[attributes["type"]])

def force_caps(text):
    """Force first letter to be in upper case.
    """
    return text[0].upper() + text[1:]

mdf_lmf.update({
    "__nt"  : lambda attributes, nt, lexical_entry: process_nt(attributes, nt, lexical_entry),
    "__np"  : lambda attributes, np, lexical_entry: process_np(attributes, np, lexical_entry),
    "__ec"  : lambda attributes, ec, lexical_entry: process_ec(attributes, ec, lexical_entry),
    "__sd"  : lambda attributes, sd, lexical_entry: process_sd(attributes, sd, lexical_entry),
    "__cf"  : lambda attributes, cf, lexical_entry: process_cf(attributes, cf, lexical_entry),
    # Force first character of definitions to be in upper case
    "dv"    : lambda dv, lexical_entry: lexical_entry.set_definition(force_caps(dv), language=config.xml.vernacular),
    "de"    : lambda de, lexical_entry: lexical_entry.set_definition(force_caps(de), language=config.xml.English),
    "dn"    : lambda dn, lexical_entry: lexical_entry.set_definition(force_caps(dn), language=config.xml.national),
    "dr"    : lambda dr, lexical_entry: lexical_entry.set_definition(force_caps(dr), language=config.xml.regional),
    "df"    : lambda df, lexical_entry: lexical_entry.set_definition(force_caps(df), language=config.xml.French)
})

## Functions to process some MDF fields (output)

def get_ec(lexical_entry):
    ec = lexical_entry.get_etymology_comment()
    if lexical_entry.get_term_source_language() is not None:
        ec = "<lang=\"" + lexical_entry.get_term_source_language() + "\">" + " " + ec
    return ec

def get_sd(lexical_entry):
    sd = ''
    sd_fr = lexical_entry.get_semantic_domains(config.xml.French)
    if sd_fr != []:
        sd += "<lang=\"fra\"> " + sd_fr[0]
    sd_en = lexical_entry.get_semantic_domains(config.xml.English)
    if sd_en != []:
        sd += EOL + "\\sd <lang=\"eng\"> " + sd_en[0]
    if sd != '':
        return sd

lmf_mdf.update({
    "ec" : lambda lexical_entry: get_ec(lexical_entry),
    "sd" : lambda lexical_entry: get_sd(lexical_entry)
})

## Functions to process some LaTeX fields (output)

def format_tone(lexical_entry, font):
    result = ""
    if lexical_entry.get_tones() is not None and len(lexical_entry.get_tones()) != 0:
        result = lexical_entry.get_tones()[0]
    return result

def format_definition(lexical_entry, language_font, language):
    result = ""
    for sense in lexical_entry.get_senses():
        if sense.find_definitions(language) is not None:
            for definition in sense.find_definitions(language):
                result += language_font(definition)
    return result

def format_gloss(lexical_entry, font, language):
    result = ""
    for sense in lexical_entry.get_senses():
        if sense.find_glosses(config.xml.regional) is not None:
            for gloss in sense.find_glosses(config.xml.regional):
                if language == config.xml.French:
                    result += "Dialecte chinois local~"
                elif language == config.xml.English:
                    result += "Local Chinese dialect"
                result +=  ": " + font[REGIONAL](gloss + u"\u3002")
    # TODO : add 'gn' then 'ph' in italic
    return result

def format_etymology(lexical_entry, font, language):
    result = ""
    if lexical_entry.get_etymology() is not None:
        if language == config.xml.English:
            result += "\\textit{From:} \\textbf{" + lexical_entry.get_etymology().replace("; ", " and ") + "} "
        elif language == config.xml.French:
            result += "\\textit{De:} \\textbf{" + lexical_entry.get_etymology().replace("; ", " et ") + "} "
    # Do not display etymology comment
    #if lexical_entry.get_etymology_comment(term_source_language=language) is not None:
        #result += u"\u2018" + lexical_entry.get_etymology_comment(term_source_language=language) + u"\u2019" + ". "
    return result

def format_paradigm(lexical_entry, font, languages):
    result = ""
    cl = False
    for paradigm in lexical_entry.get_paradigms():
        if paradigm.get_paradigmLabel == "classifier" and paradigm.get_language() in languages:
            if not cl:
                result += " \\textit{CL~:}"
                cl = True
            result += " \\textsc{" + paradigm.get_paradigm() + "}"
    return result

def format_borrowed_word(lexical_entry, font, language):
    result = ""
    if lexical_entry.get_borrowed_word() is not None:
        if language == config.xml.French:
            result += " \\textit{De:} "
        elif language == config.xml.English:
            result += " \\textit{From:} "
        result += lexical_entry.get_borrowed_word()
        if lexical_entry.get_written_form() is not None:
            result += " " + lexical_entry.get_written_form()
        result += ". "
    return result

def tex_fra(lexical_entry, font):
    """<lx> (prononciation~: <lc>~; avec le verbe copule~: <lc <type="with copula">>) TAB <ps> TAB Ton~: <np <type="tone">>.
    <df>.
    <dn>u"\u3002" Dialecte chinois local~: <gr>u"\u3002"
    <xv>
    <xf>
    <xn>
    """
    import output.tex as tex
    tex_entry = ""
    # Do not display lexical entry if lexeme is '???'
    if lexical_entry.get_lexeme() == "???":
        return tex_entry
    tex_entry = (r"""%s %s \hspace{4pt} Ton~: %s.""" + EOL + "%s." + EOL + "%s" + config.xml.font[NATIONAL](u"\u3002") + "%s" + EOL + "%s%s%s%s%s" + EOL) % \
        ("{\Large " + tex.format_lexeme(lexical_entry, config.xml.font) + "}",\
        "\\textcolor{teal}{\\textsc{" + str(lexical_entry.get_partOfSpeech()) + "}}",\
        format_tone(lexical_entry, config.xml.font),\
        format_definition(lexical_entry, config.xml.font[FRENCH], language=config.xml.French),\
        format_definition(lexical_entry, config.xml.font[NATIONAL], language=config.xml.national),\
        format_gloss(lexical_entry, config.xml.font, language=config.xml.French),\
        format_etymology(lexical_entry, font=config.xml.font, language=config.xml.French),\
        format_borrowed_word(lexical_entry, font=config.xml.font, language=config.xml.French),\
        tex.format_examples(lexical_entry, config.xml.font, languages=[config.xml.vernacular, config.xml.French, config.xml.national]),\
        format_paradigm(lexical_entry, config.xml.font, [config.xml.vernacular, config.xml.national, config.xml.regional, config.xml.French]),\
        tex.format_related_forms(lexical_entry, font))
    # Special formatting
    tex_entry = tex.handle_caps(tex_entry).replace("textsc", "mytextsc")
    # Handle reserved characters and fonts
    tex_entry = tex.handle_reserved(tex_entry)
    tex_entry = tex.handle_fv(tex_entry, config.xml.font)
    tex_entry = tex.handle_fn(tex_entry, config.xml.font)
    return tex_entry

def tex_eng(lexical_entry, font):
    """<lx> (pronunciation: <lc>; with the copula verb: <lc <type="with copula">>) TAB <ps> TAB Tone: <np <type="tone">>.
    <df>.
    <dn>u"\u3002" Local Chinese dialect: <gr>u"\u3002"
    <xv>
    <xe>
    <xn>
    """
    import output.tex as tex
    tex_entry = ""
    # Do not display lexical entry if lexeme is '???'
    if lexical_entry.get_lexeme() == "???":
        return tex_entry
    tex_entry = (r"""%s %s \hspace{4pt} Tone: %s.""" + EOL + "%s." + EOL + "%s" + config.xml.font[NATIONAL](u"\u3002") + "%s" + EOL + "%s%s%s%s%s" + EOL) % \
        ("{\Large " + tex.format_lexeme(lexical_entry, config.xml.font) + "}",\
        "\\textcolor{teal}{\\textsc{" + str(lexical_entry.get_partOfSpeech()) + "}}",\
        format_tone(lexical_entry, config.xml.font),\
        format_definition(lexical_entry, config.xml.font[ENGLISH], language=config.xml.English),\
        format_definition(lexical_entry, config.xml.font[NATIONAL], language=config.xml.national),\
        format_gloss(lexical_entry, config.xml.font, language=config.xml.English),\
        format_etymology(lexical_entry, font=config.xml.font, language=config.xml.English),\
        format_borrowed_word(lexical_entry, font=config.xml.font, language=config.xml.English),\
        tex.format_examples(lexical_entry, config.xml.font, languages=[config.xml.vernacular, config.xml.English, config.xml.national]),\
        format_paradigm(lexical_entry, config.xml.font, [config.xml.vernacular, config.xml.national, config.xml.regional, config.xml.English]),\
        tex.format_related_forms(lexical_entry, font))
    # Special formatting
    tex_entry = tex.handle_caps(tex_entry).replace("textsc", "mytextsc")
    # Handle reserved characters and fonts
    tex_entry = tex.handle_reserved(tex_entry)
    tex_entry = tex.handle_fv(tex_entry, font)
    tex_entry = tex.handle_fn(tex_entry, font)
    return tex_entry