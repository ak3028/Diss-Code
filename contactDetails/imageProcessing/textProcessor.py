import re

def processCardText(cardInfo):
    sanitisedText = getNonEmptyLinesFromText(cardInfo) # get string without any empty spaces
    mob, remText = extractMobileAndRemoveItFromText(sanitisedText)
    # extractMobileAndRemoveItFromText(sanitisedText)
    return (sanitisedText,mob,"")



def getNonEmptyLinesFromText(text):
    lines = text.split("\n")
    string_without_empty_lines = ""
    nonEmptyLines = [line for line in lines if line.strip()]
    for line in nonEmptyLines:
      string_without_empty_lines += line + "\n"
    return string_without_empty_lines


def extractMobileAndRemoveItFromText(text):
    lines = text.split("\n")
    mob = ""
    mob = re.findall(r'\+[-()\s\d]+?(?=\s*[+<])', text)
    return mob, text