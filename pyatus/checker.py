from spellchecker import SpellChecker
import re
from pyatus.utilities import (
    generate_glossary_terms,
    generate_monolingual_terms
)

'''
An error is a dict in the following format:

{
    'segment': segment info passed from reader.py (dict)
    'category': 'error category' (str),
    'message': 'error details' (str),
    'match': 'matched term for glossary and monolingual' (str)
}
'''

class Checker:     
    def __init__(self, myconfig, segments):
        # read config
        self.source_lang       = myconfig.checker_source_lang 
        self.target_lang       = myconfig.checker_target_lang
        self.glossary          = myconfig.checker_glossary
        self.glossary_path     = myconfig.checker_glossary_path
        self.inconsistency_s2t = myconfig.checker_inconsistency_s2t
        self.inconsistency_t2s = myconfig.checker_inconsistency_t2s
        self.skip              = myconfig.checker_skip
        self.identical         = myconfig.checker_identical
        self.spell             = myconfig.checker_spell
        self.monolingual       = myconfig.checker_monolingual
        self.monolingual_path  = myconfig.checker_monolingual_path
        self.numbers           = myconfig.checker_numbers
        self.unsourced         = myconfig.checker_unsourced
        self.unsourced_rev     = myconfig.checker_unsourced_rev
        self.length            = myconfig.checker_length

        # regexp list for glossary and monolingual checks
        self.monolingual_regexps = []
        self.glossary_regexps = []
        # "segments" contain list of segments generated by reader.py
        self.segments = segments
        # "errors" contains a list of errors, passed from check_xxx methods.
        self.errors = []
        
    def check_glossary(self, segment: dict):
        '''
        Find regexp complied term in source and target segments.
        Return errors if the target not found when source is found.

        Each glossary_regexps is in the following format:

        glossary_regexp = {
            'src' : "original source",
            'tgt' : "original target",
            'regSrc' : "regexp compiles source",
            'regTgt' : "regexp compiles target",
            'message' : "message"
        }
        '''
        
        for glossary_regexp in self.glossary_regexps:
            matches = re.findall(glossary_regexp['regSrc'], segment["source"])
            for match in matches:
                if not re.search(glossary_regexp['regTgt'], segment["target"]):
                    error = {
                        'segment' : segment,
                        'category' : "Glossary",
                        "message" : glossary_regexp['message'],
                        'match' : f"'{glossary_regexp['src']}' found but '{glossary_regexp['tgt']}' not found"
                    }
                    self.errors.append(error)

    def _generate_glossary_regexps(self):
        return generate_glossary_terms(self.glossary_path, self.source_lang, self.target_lang)

    def _check_inconsistency_template(self, segments: list, srt_or_tgt: bool):
        '''
        This method runs inconsistency check to the given segment.
        This is used in check_inconsistencyy_src2tgt and check_inconsistencyy_tgt2src.
        if srt_or_tgt is True,  src2tgt inconsistency.
        if srt_or_tgt is False, tgt2src inconsistency.
        Add error info to the instance variable "errors".
        '''
        inconsistencies = {}

        if srt_or_tgt == True:
            lang1 = 'source'
            lang2 = 'target'
        else:
            lang1 = 'target'
            lang2 = 'source'
        
        for segment in segments:
            src = segment[lang1]
            tgt = segment[lang2]
            
            if src in inconsistencies:
                inconsistencies[src][0].append(tgt)
                inconsistencies[src][1].append(segment)
                inconsistencies[src][2] += 1
            else:
                inconsistencies[src] = [[tgt], [segment], 1]
        
        for str_key, value in inconsistencies.items():
            forms = list(set(value[0]))
            if value[2] == 1 or len(forms) == 1:
                continue
                
            for segment in value[1]:
                error = {
                    'segment': segment,
                    'category': f"Inconsistent ({lang1}->{lang2})",
                    'message': "",
                    "match" : ""
                }
                self.errors.append(error)

    def check_inconsistency_src2tgt(self):
        '''
        This method runs inconsistency check to the given segment.
        Errors are reported if the same source values have different target values.
        '''
        self._check_inconsistency_template(self.segments, True)

    def check_inconsistency_tgt2src(self):
        '''
        This method runs inconsistency check to the given segment.
        Errors are reported if the same source values have different target values.
        '''
        self._check_inconsistency_template(self.segments, False)
    
    def check_identical(self, segment):
        '''
        This method runs identical check to the given segment.
        Errors are reported if the source and target segment are identical.
        Add error info to the instance variable "errors".
        '''
        if segment['source'] == segment['target']:
            error = {}
            error['segment'] = segment
            error['category'] = 'Identical'
            error['message'] = 'Target is same as Source'
            error['match'] = ''
            self.errors.append(error)
        
    def check_length(self, segment: dict):
        '''
        This method runs length check to the given segment.
        Errors are reported if the "target length/source length" is either less than 50% or more than 200%.
        Add error info to the instance variable "errors".
        '''
        if len(segment['source']) == 0:
            pass
        elif len(segment['target'])/len(segment['source']) > 2:
            error = {}
            error['segment'] = segment
            error['category'] = 'Too long?'
            error['message'] = 'Target length is more than 200%'
            error['match'] = ''
            self.errors.append(error)
        elif len(segment['target'])/len(segment['source']) < 0.5:
            error = {}
            error['segment'] = segment
            error['category'] = 'Too short?'
            error['message'] = 'Target length is less than 50%'
            error['match'] = ''
            self.errors.append(error)

    def check_skip(self, segment: dict):
        '''
        This method runs skip check to the given segment.
        Errors are reported if the target segment is empty.
        Add error info to the instance variable "errors".
        '''
        if segment['target'] == '':
            error = {}
            error['segment'] = segment
            error['category'] = 'Empty'
            error['message'] = 'Target is empty'
            error['match'] = ''
            self.errors.append(error)

    def check_monolingual(self, segment: dict):
        '''
        Find regexp complied term in source or target segment.
        Each monolingual_regexp is in the following format:

        monolingual_regexp = {
            's_or_t' : 's (source) or t (target)',
            'term' : 'original term',
            'regTerm', : 'regexp complied term',
            'message' : 'error message'
        }
        '''
        
        for monolingual_regexp in self.monolingual_regexps:
            if monolingual_regexp['s_or_t'].lower() == 's':
                self._check_monolingual_template(segment, monolingual_regexp, 'source')
            elif monolingual_regexp['s_or_t'].lower() == 't':
                self._check_monolingual_template(segment, monolingual_regexp, 'target')
            
    def _check_monolingual_template(self, segment: dict, monolingual_regexp: dict, s_or_t: str='source'):
        matches = monolingual_regexp['regTerm'].findall(segment[s_or_t])

        if len(matches) > 0:
            for match in matches:
                error = {}
                error['segment'] = segment
                error['category'] = f'Found in {s_or_t.capitalize()}'
                error['message'] = monolingual_regexp['message']
                error['match'] = match
                self.errors.append(error)
    
    def _generate_monolingual_regexps(self):
        return generate_monolingual_terms(self.monolingual_path, self.source_lang, self.target_lang)

    def check_spell(self, segment: dict):
        if "en" in self.target_lang:
            self._check_spell_template(segment, "en")
        elif "es" in self.target_lang:
            self._check_spell_template(segment, "es")
        elif "fr" in self.target_lang:
            self._check_spell_template(segment, "fr")
        elif "pt" in self.target_lang:
            self._check_spell_template(segment, "pt")
        elif "de" in self.target_lang:
            self._check_spell_template(segment, "de")
        elif "it" in self.target_lang:
            self._check_spell_template(segment, "it")
        elif "ru" in self.target_lang:
            self._check_spell_template(segment, "ru")
        elif "ar" in self.target_lang:
            self._check_spell_template(segment, "ar")
        elif "eu" in self.target_lang:
            self._check_spell_template(segment, "eu")
        elif "lv" in self.target_lang:
            self._check_spell_template(segment, "lv")
        elif "nl" in self.target_lang:
            self._check_spell_template(segment, "nl")

    def _check_spell_template(self, segment: dict, lang: str = "en"):
        spell = SpellChecker(language=lang)
        misspelled = spell.unknown(re.compile(r'\w+').findall(segment['target']))

        if len(misspelled) > 0:
            for word in list(misspelled):
                error = {}
                error['segment'] = segment
                error['category'] = 'Spell'
                error['message'] = f'"{word}" => "{spell.correction(word)}"?'
                error['match'] = ''
                self.errors.append(error)

    def check_numbers(self, segment: dict):
        self._check_numbers_template(segment, True)
        self._check_numbers_template(segment, False)

    def _check_numbers_template(self, segment: dict, normal_or_rev: bool):
        # Dictionary mapping numbers to their patterns
        number_patterns = {
            "1": r"(1|一|one|single|January)",
            "2": r"(2|二|two|double|February)",
            "3": r"(3|三|three|March)",
            "4": r"(4|四|four|April)",
            "5": r"(5|五|five|May)",
            "6": r"(6|六|six|June)",
            "7": r"(7|七|seven|July)",
            "8": r"(8|八|eight|August)",
            "9": r"(9|九|nine|September)",
            "0": r"(0|ゼロ|零|zero)",
            "10": r"(10|十|ten|October)",
            "11": r"(11|十一|eleven|November)",
            "12": r"(12|十二|twelve|December)",
            "16": r"(16|sixteen|hex|hexadecimal|十六)",
            "100": r"(100|百|hundred)",
            "1000": r"(1,000|1 000|1000|千|thousand)",
            "10000": r"(10,000|10 000|10000|万)"
        }
        if normal_or_rev == True:
            lang1 = 'source'
            lang2 = 'target'
        else:
            lang1 = 'target'
            lang2 = 'source'
        
        # Find all numbers in the source text
        found_numbers = re.findall(r"(\d+[\d ,\.]*\d|\d)", segment[lang1])
        
        for found in found_numbers:
            if found in number_patterns:
                # Check special numbers (1-10000)
                if not re.search(number_patterns[found], segment[lang2], re.IGNORECASE):
                    error = {
                        "segment": segment,
                        "category": "Missing Number?",
                        "message": f"Number not found in {lang2}",
                        "match" : f"{found}"
                    }
                    self.errors.append(error)
            else:
                # Handle other numbers
                num_forms = [
                    found,
                    found.replace(",", ""),
                    found.replace(" ", ""),
                    # Reverse and add commas every 3 digits
                    re.sub(r"(\d{3})(?=\d)", r"\1,", found[::-1])[::-1],
                    # Reverse and add spaces every 3 digits
                    re.sub(r"(\d{3})(?=\d)", r"\1 ", found[::-1])[::-1]
                ]
                
                pattern = "|".join(set(num_forms))
                if not re.findall(f"({pattern})", segment[lang2]):
                    error = {
                        "segment": segment,
                        "category": "Missing Number?",
                        "message": f"Number not found in {lang2}",
                        "match" : f"{found}"
                    }
                    self.errors.append(error)
    
    def _check_unsourced_template(self, segment: dict, normal_or_rev: bool):
        '''
        This method runs unsourced check to the given segment.
        This is used in check_unsourced and check_unsourced_rev.
        if normal_or_rev is True,  normal way unsourced check.
        if normal_or_rev is False, reverse unsourced check.
        Add error info to the instance variable "errors".
        '''
        
        if normal_or_rev == True:
            lang1 = 'target'
            lang2 = 'source'
        else:
            lang1 = 'source'
            lang2 = 'target'
        
        enu_terms = re.findall(r'([@a-zA-Z][@\.a-zA-Z\d]*[@\.a-zA-Z\d]|[@a-zA-Z])', segment[lang1])
        
        for enu_term in enu_terms:
            conv_enu = re.compile(re.escape(enu_term))
            
            if conv_enu.search(segment[lang2]):
                continue
                
            error = {
                'segment': segment,
                'category': "Unsourced",
                'message': f'Matched word not found in {lang2}',
                'match' : enu_term         
            }
            self.errors.append(error)

    def check_unsourced(self, segment: dict):
        self._check_unsourced_template(segment, True)

    def check_unsourced_rev(self, segment: dict):
        self._check_unsourced_template(segment, False)

    def detect_errors(self) -> list[dict]:
        '''
        Process checks where marked True in the config.
        Return errors.
        '''

        # generate regexps for glossary and monolingual
        if self.monolingual is True:
            self.monolingual_regexps = self._generate_monolingual_regexps()
        if self.glossary is True:
            self.glossary_regexps = self._generate_glossary_regexps()
        
        for segment in self.segments:
            if self.glossary is True:
                self.check_glossary(segment)
            if self.skip is True:
                self.check_skip(segment)
            if self.identical is True:
                self.check_identical(segment)
            if self.spell is True:
                self.check_spell(segment)
            if self.monolingual is True:
                self.check_monolingual(segment)
            if self.numbers is True:
                self.check_numbers(segment)
            if self.unsourced is True:
                self.check_unsourced(segment)
            if self.unsourced_rev is True:
                self.check_unsourced_rev(segment)
            if self.length is True:
                self.check_length(segment)

        if self.inconsistency_s2t is True:
            self.check_inconsistency_src2tgt()
        if self.inconsistency_t2s is True:
            self.check_inconsistency_tgt2src()

        return self.errors
        