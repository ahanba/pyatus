import re
import logging
from pathlib import Path

from pyatus.converter import convert_en

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_glossary_regexp(term_info, source_lang: str, target_lang: str) -> dict:
    '''
    Generate RegExp pattern from term info.
    '''
    try:
        glossary_regexp = {
            'src': term_info.get("src", ""),
            'tgt': term_info.get("tgt", ""),
            'regSrc': None,
            'regTgt': None,
            'message': term_info.get("message", "")
        }

        option = term_info.get("option", "")
        if option.startswith("#"):
            flag = option.lstrip("#")
            flags = re.IGNORECASE if flag == 'i' else 0
            glossary_regexp['regSrc'] = re.compile(term_info['src'], flags)
            glossary_regexp['regTgt'] = re.compile(term_info['tgt'], flags)
        elif option.lower() == "z":
            glossary_regexp['regSrc'] = re.compile(re.escape(term_info['src']), re.IGNORECASE)
            glossary_regexp['regTgt'] = re.compile(re.escape(term_info['tgt']), re.IGNORECASE)
        else:
            converted_src = convert_en(term_info['src']) if "en" in source_lang.lower() else term_info['src']
            converted_tgt = convert_en(term_info['tgt']) if "en" in target_lang.lower() else term_info['tgt']
            flags = re.IGNORECASE if option == 'i' else 0
            glossary_regexp['regSrc'] = re.compile(converted_src, flags)
            glossary_regexp['regTgt'] = re.compile(converted_tgt, flags)

        return glossary_regexp
    except re.error as e:
        logging.error(f"Regex error for term '{term_info.get('src', 'UNKNOWN')}': {e}")
        return {}

def generate_glossary_terms(glossary_folder_path: str, source_lang: str, target_lang: str) -> list:
    '''
    Read glossary file and generate a list of glossary RegExps
    '''
    glossary_regexps = []
    try:
        for glossary_file in Path(glossary_folder_path).glob("**/*.txt"):
            try:
                with open(glossary_file, "r", encoding="utf-8") as file:
                    logging.info(f"Reading glossary file: {glossary_file}")
                    for i, line in enumerate(file, start=1):
                        if line.startswith("//"):  # Skip comment lines
                            continue
                        split_line = line.strip().split("\t")
                        if len(split_line) < 3:
                            logging.warning(f"Invalid entry on line {i} in {glossary_file}")
                            continue
                        term_info = {
                            "src": split_line[0].strip(),
                            "tgt": split_line[1].strip(),
                            "option": split_line[2].strip(),
                            "message": split_line[3].strip() if len(split_line) > 3 else ""
                        }
                        glossary_regexps.append(generate_glossary_regexp(term_info, source_lang, target_lang))
            except IOError as e:
                logging.error(f"Cannot open {glossary_file}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error processing glossary files: {e}")
    return glossary_regexps

def generate_monolingual_regexp(term_info, source_lang: str, target_lang: str) -> dict:
    '''
    Generate RegExp pattern from term info.
    '''
    try:
        monolingual_regexp = {
            's_or_t': term_info.get("s_or_t", ""),
            'term': term_info.get("term", ""),
            'regTerm': None,
            'message': term_info.get("message", "")
        }

        option = term_info.get("option", "")
        flags = re.IGNORECASE if option == 'i' else 0

        if option.startswith("#"):
            monolingual_regexp['regTerm'] = re.compile(term_info['term'], flags)
        elif option.lower() == "z":
            monolingual_regexp['regTerm'] = re.compile(re.escape(term_info['term']), re.IGNORECASE)
        else:
            converted_term = convert_en(term_info['term']) if ((term_info["s_or_t"] == "s" and "en" in source_lang.lower()) or (term_info["s_or_t"] == "t" and "en" in target_lang.lower())) else term_info['term']
            monolingual_regexp['regTerm'] = re.compile(converted_term, flags)
        
        return monolingual_regexp
    except re.error as e:
        logging.error(f"Regex error for term '{term_info.get('term', 'UNKNOWN')}': {e}")
        return {}

def generate_monolingual_terms(monolingual_folder_path: str, source_lang: str, target_lang: str) -> list:
    '''
    Read monolingual file and generate a list of monolingual RegExps.
    '''
    monolingual_regexps = []
    try:
        for monolingual_file in Path(monolingual_folder_path).glob("**/*.txt"):
            try:
                with open(monolingual_file, "r", encoding="utf-8") as file:
                    logging.info(f"Reading monolingual file: {monolingual_file}")
                    for i, line in enumerate(file, start=1):
                        if line.startswith("//"):  # Skip comment lines
                            continue
                        split_line = line.strip().split("\t")
                        if len(split_line) < 3:
                            logging.warning(f"Invalid entry on line {i} in {monolingual_file}")
                            continue
                        term_info = {
                            "s_or_t": split_line[0].strip(),
                            "term": split_line[1],
                            "option": split_line[2].strip(),
                            "message": split_line[3].strip() if len(split_line) > 3 else ""
                        }
                        if term_info["s_or_t"].lower() not in {"s", "t"}:
                            logging.warning(f"Invalid 's_or_t' value on line {i} in {monolingual_file}")
                            continue
                        monolingual_regexps.append(generate_monolingual_regexp(term_info, source_lang, target_lang))
            except IOError as e:
                logging.error(f"Cannot open {monolingual_file}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error processing monolingual files: {e}")
    return monolingual_regexps
