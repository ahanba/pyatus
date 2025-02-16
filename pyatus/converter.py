import re

CHANGEFORM = {
    "TYPE1": (r"\b", r"(?:s|ed|ing)?\b"),  # Normal noun/verb
    "TYPE2": (r"\b", r"(?:y|ies|ied|ying)?\b"),  # Ends with 'y'
    "TYPE3": (r"\b", r"(?:e|es|ed|ing)?\b"),  # Ends with 'e'
}

IRREGULAR = {
    "axis": r"\b(?:axis|axes)\b",
    "analysis": r"\b(?:analysis|analyses)\b",
    "be": r"\b(?:be|is|are|am|being|was|were)\b",
    "become": r"\b(?:become|becomes|became|becoming)\b",
    "begin": r"\b(?:begin|begins|began|begun|beginning)\b",
    "break": r"\b(?:break|breaks|broke|broken|breaking)\b",
    "bring": r"\b(?:bring|brings|brought|bringing)\b",
    "build": r"\b(?:build|builds|built|building)\b",
    "buy": r"\b(?:buy|buys|bought|buying)\b",
    "catch": r"\b(?:catch|catches|caught|catching)\b",
    "choose": r"\b(?:choose|chooses|chose|chosen|choosing)\b",
    "come": r"\b(?:come|comes|came|coming)\b",
    "do": r"\b(?:do|did|does|doing|done)\b",
    "draw": r"\b(?:draw|draws|drew|drawn|drawing)\b",
    "drink": r"\b(?:drink|drinks|drank|drunk|drinking)\b",
    "drive": r"\b(?:drive|drives|drove|driven|driving)\b",
    "eat": r"\b(?:eat|eats|ate|eaten|eating)\b",
    "fall": r"\b(?:fall|falls|fell|fallen|falling)\b",
    "feel": r"\b(?:feel|feels|felt|feeling)\b",
    "find": r"\b(?:find|finds|found|found|finding)\b",
    "fly": r"\b(?:fly|flies|flew|flown|flying)\b",
    "forget": r"\b(?:forget|forgets|forgot|forgetting|forgotten)\b",
    "get": r"\b(?:get|got|gets|getting|gotten)\b",
    "give": r"\b(?:give|gives|gave|given|giving)\b",
    "go": r"\b(?:go|goes|went|gone|going)\b",
    "grow": r"\b(?:grow|grows|grew|grown|growing)\b",
    "have": r"\b(?:have|has|had|having)\b",
    "hear": r"\b(?:hear|hears|heard|heard|hearing)\b",
    "hide": r"\b(?:hide|hides|hid|hidden|hiding)\b",
    "hold": r"\b(?:hold|holds|held|holding)\b",
    "index": r"\b(?:index|indices)\b",
    "is": r"\b(?:be|is|are|am|being|was|were)\b",
    "keep": r"\b(?:keep|keeps|kept|keeping)\b",
    "know": r"\b(?:know|knows|knew|known|knowing)\b",
    "lay": r"\b(?:lay|lies|laid|laying)\b",
    "lead": r"\b(?:lead|leads|led|leading)\b",
    "learn": r"\b(?:learn|learns|learned|learnt|learning)\b",
    "leave": r"\b(?:leave|leaves|left|leaving)\b",
    "lend": r"\b(?:lend|lends|lent|lending)\b",
    "lie": r"\b(?:lie|lay|lies|lying|lain)\b",
    "lose": r"\b(?:lose|loses|lost|losing)\b",
    "make": r"\b(?:make|makes|made|making)\b",
    "mean": r"\b(?:mean|means|meant|meaning)\b",
    "meet": r"\b(?:meet|meets|met|meeting)\b",
    "pay": r"\b(?:pay|pays|paid|paid|paying)\b",
    "ride": r"\b(?:ride|rides|rode|ridden|riding)\b",
    "rise": r"\b(?:rise|rises|rose|risen|rising)\b",
    "run": r"\b(?:run|runs|ran|running)\b",
    "say": r"\b(?:say|says|said|said|saying)\b",
    "see": r"\b(?:see|sees|saw|seen|seeing)\b",
    "sell": r"\b(?:sell|sells|sold|selling)\b",
    "send": r"\b(?:send|sends|sent|sending)\b",
    "shake": r"\b(?:shake|shakes|shook|shaken|shaking)\b",
    "shine": r"\b(?:shine|shines|shone|shining)\b",
    "sit": r"\b(?:sit|sits|sat|sitting)\b",
    "sleep": r"\b(?:sleep|sleeps|slept|sleeping)\b",
    "write": r"\b(?:write|writes|wrote|written|writing)\b",
}

def convert_en(text):
    words = re.split(r"[ \-]", text)
    converted_terms = []

    for word in words:
        if re.match(r"^[\[\(\.\\^]", word) or re.match(r".*[\]\)]$", word):
            converted_terms.append(word)
        elif not re.match(r"^[ -~｡-ﾟ]*$", word):  # Contains double-byte characters
            converted_terms.append(word)
        elif word.lower() in IRREGULAR:
            converted_terms.append(IRREGULAR[word.lower()])
        elif re.search(r"y\b", word):
            converted_terms.append(CHANGEFORM["TYPE2"][0] + word[:-1] + CHANGEFORM["TYPE2"][1])
        elif re.search(r"e\b", word):
            converted_terms.append(CHANGEFORM["TYPE3"][0] + word[:-1] + CHANGEFORM["TYPE3"][1])
        elif re.search(r"[bcdfghjklmnpqrstvwxyz][aiueo]([bcdfghjklmnpqrstvwxyz])\b", word):
            converted_terms.append(convert_type4(word, re.search(r"([bcdfghjklmnpqrstvwxyz])\b", word).group(1)))
        else:
            converted_terms.append(CHANGEFORM["TYPE1"][0] + word + CHANGEFORM["TYPE1"][1])
    
    return " ".join(converted_terms)

def convert_type4(word, char): # case for "tap","let","swim", etc.
    return r"\b" + word + rf"(?:s|{char}ed|{char}ing|ed|ing)?\b"

