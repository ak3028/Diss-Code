import re
import spacy

def processCardText(cardInfo):
    sanitisedText = getNonEmptyLinesFromText(cardInfo) # get string without any empty spaces

    phone = extractPhoneNumber(sanitisedText)
    # mob = getMobileNumber(sanitisedText)
    email = extractEmailIDFromText(sanitisedText)
    # remainingText = removeClassifiedFieldsFromText(sanitisedText, email, mob, "")
    # remainingText = sanitisedText
    # extractMobileAndRemoveItFromText(sanitisedText)
    name = extractNameFromText(sanitisedText)

    org = extractOrgFromText(sanitisedText)

    return (sanitisedText, name, org, email, phone, "")

def extractEmailIDFromText(text):
    # emailIds = re.findall(r'[\w\.-]+@[\w\.-]+', text) #working expression
    emailIds = re.findall(r'[\w\.-]+@[_\w\.]+', text)
    if len(emailIds)==0:
        return ""
    emailId = emailIds[0]
    return emailId
    

def getNonEmptyLinesFromText(text):
    lines = text.split("\n")
    string_without_empty_lines = ""
    nonEmptyLines = [line for line in lines if line.strip()]
    for line in nonEmptyLines:
      string_without_empty_lines += line + "\n"
    return string_without_empty_lines


def extractPhoneNumber(text):
    # lines = text.split("\n")
    # mob = re.findall(r'\+[-()\s\d]+?(?=\s*[+<])', text)
    # if len(mob) == 1:
    #    return mob[0], text
    # return "", text

    matches = []
    result = phoneRegex.findall(text)
    if len(result) > 0:
        for groups in phoneRegex.findall(text):
            phoneNum = '-'.join([groups[1], groups[3], groups[5]])
            if groups[8] != '':
                phoneNum += ' x' + groups[8]
            matches.append(phoneNum)
        if len(matches) >= 1:
           return matches[0] # return the first number that is found
    return ""


def removeClassifiedFieldsFromText(text, email, phone, organization):
    cleanedText = text
    if email!= "":
       cleanedText = text.replace(email,"")
    
    if phone!="":
      cleanedText = cleanedText.replace(phone,"")

    remainingText = getNonEmptyLinesFromText(cleanedText)

    return remainingText

def extractNameFromText(text):
    name = getNameUsingNlpLibrary(text)
    return name


def extractOrgFromText(text):
    name = getOrgUsingNlpLibrary(text)
    return name

def getNameUsingNlpLibrary(text):
    nlp = spacy.load("en_core_web_sm") #spacy.load('en')
    classifiedText = nlp(text)
    for entity in classifiedText.ents:
        if(entity.label_ == "PERSON"):
           return entity.text
    return ""

def getOrgUsingNlpLibrary(text):
    nlp = spacy.load("en_core_web_sm") #spacy.load('en')
    classifiedText = nlp(text)
    for entity in classifiedText.ents:
        if(entity.label_ == "ORG"):
           return entity.text
    return ""

def getMobileNumber(text):
    expression = r'((^\(?(?:(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?\(?(?:0\)?[\s-]?\(?)?|0)(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}|\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4}|\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3})|\d{5}\)?[\s-]?\d{4,5}|8(?:00[\s-]?11[\s-]?11|45[\s-]?46[\s-]?4\d))(?:(?:[\s-]?(?:x|ext\.?\s?|\#)\d+)?)$)|(\(?[2-9][0-8][0-9]\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}))'
    phoneNumbers = re.findall(r'''((^\(?(?:(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?\(?(?:0\)?[\s-]?\(?)?|0)(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}|\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4}|\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3})|\d{5}\)?[\s-]?\d{4,5}|8(?:00[\s-]?11[\s-]?11|45[\s-]?46[\s-]?4\d))(?:(?:[\s-]?(?:x|ext\.?\s?|\#)\d+)?)$)|(\(?[2-9][0-8][0-9]\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}))''', text)
    if len(phoneNumbers) > 0:
      return phoneNumbers[0]
    return ""

    # mob = re.findall(r'M:[0-9]', text)
    # mob = re.findall(r'M: [0-9]', text)
    # mob = re.findall(r'm: [0-9]', text)
    # mob = re.findall(r'm:[0-9]', text)
    
    # mob = re.findall(r'mob: [0-9]', text)
    # mob = re.findall(r'mob:[0-9]', text)

    # mob = re.findall(r'Mob: [0-9]', text)
    # mob = re.findall(r'Mob:[0-9]', text)

    # mob = re.findall(r'Mob: [0-9]', text)
    # mob = re.findall(r'Mob:[0-9]', text)



    # M/m: 7552329158            - [M|m|]: [0-9]+
    # M/m:7552329158             - [M|m|]: [0-9]+ - without space
    # [M|m][O|o][B|b]:[0-9]+     - Mob/MOB:[0-9]+
    # [M|m][O|o][B|b]: [0-9]+    - Mob/MOB: [0-9]+

    # MOB:\d\d\d.\d\d\d.\d\d\d\d - MOB:755 232 9158
    # MOB:\d\d\d[-.\s]\d\d\d[-.\s]\d\d\d\d - - MOB:755 232 9158 (with any kind of separator)


phoneRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))? # area code
    (\s|-|\.)? # separator
    (\d{3}) # first 3 digits
    (\s|-|\.) # separator
    (\d{4}) # last 4 digits
    (\s*(ext|x|ext.)\s*(\d{2,5}))? # extension
    )''', re.VERBOSE)
       