from os import remove
import re
import spacy
import pytesseract


def getTextFromOCR(image):
    return pytesseract.image_to_string(image)

def processCardText(extractedText):
    
    #when phone numbers have more than one space they are not recognized.
    #extractedText = 'FABRIKAM, INC.\n\nEric Rothenberg, Owner, License #M45678\n\n57 N. Walnut Drive, Suite 120, New Orleans,\nLA 12329\n\nPhone (304)  555-0112 + Fax (304) 555-0114\n\x0c'

    sanitisedText = sanitizeText(extractedText) # get string without any empty spaces

    phone = extractPhoneNumber(sanitisedText)
    # mob = getMobileNumber(sanitisedText)
    email = extractEmailIDFromText(sanitisedText)
    # remainingText = removeClassifiedFieldsFromText(sanitisedText, email, mob, "")
    # remainingText = sanitisedText
    # extractMobileAndRemoveItFromText(sanitisedText)
    name = extractContactName(sanitisedText, email) # passing email for the fallback of the

    org = extractOrgFromText(sanitisedText)

    return (sanitisedText, name, org, email, phone)

def extractEmailIDFromText(text):
    # emailIds = re.findall(r'[\w\.-]+@[\w\.-]+', text) #working expression
    emailIds = re.findall(r'[\w\.-]+@[_\w\.]+', text)
    if len(emailIds)==0:
        return ""
    emailId = emailIds[0]
    return emailId
    

def sanitizeText(text):
    lines = text.split("\n")
    string_without_empty_lines = ""
    nonEmptyLines = [line for line in lines if line.strip()]
    # It was noticed in some business cards the ocr creates a white space near the '@' symbol
    # in the email. This needs to be removed so that the email is identified by the regex.
    for line in nonEmptyLines:
      if '@' in line:
          indexOfAt = line.find('@')
          if line[indexOfAt+1] == " ":
              line = line[:indexOfAt+1] + '' + line[indexOfAt+2:]
          if line[indexOfAt-1] == " ":
              line = line[:indexOfAt-1] + '' + line[indexOfAt:]
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


# def removeClassifiedFieldsFromText(text, email, phone, organization):
#     cleanedText = text
#     if email!= "":
#        cleanedText = text.replace(email,"")
    
#     if phone!= "":
#       cleanedText = cleanedText.replace(phone,"")

#     remainingText = getNonEmptyLinesFromText(cleanedText)

#     return remainingText

def extractContactName(text, email):
    name = getNameUsingNlpLibrary(text)
    if name !='':
        return name

    else:    
        if email != '':
           text = removeEmailFromText(email,text)
           partialNameFromEmail = extractPartialNameFromEmailId(email)
           name = findNameFromEmailInCardText(partialNameFromEmail, text)
        if name != "":
           return name
        else:
            name = guessNameFromCardText(text)
            return name

def guessNameFromCardText(text):
    name=''
    linesIntheText = text.split('\n')
    for line in linesIntheText:
        numberOfWordInName = len(line.split(" "))
        if numberOfWordInName == 2 or numberOfWordInName ==3:
           if len(line.strip()) > 6:
              name = line.strip()
              return name
    return name
            




        

def removeEmailFromText(email,text):
    return text.replace(email,"")

       

def extractContactNameOldMethod(text, email):
    nameFromNLP = getNameUsingNlpLibrary(text)
    nameFromEmail = ''
    if email != '':
       nameFromEmail = extractNameFromEmailId(email)
    
    if nameFromNLP=='' and nameFromEmail=='':
       return ''

    elif nameFromNLP=='' and nameFromEmail != '' :
       name = findNameFromEmailInCardText(nameFromEmail,text.replace(email,""))
       if name=='':
           return nameFromEmail
       return name

    elif nameFromNLP !='' and nameFromEmail == '':
        return nameFromNLP
    
    elif nameFromNLP !='' and nameFromEmail != '':
        if nameFromEmail.casefold() in nameFromNLP.casefold():
           return nameFromNLP
        else:
           name = findNameFromEmailInCardText(nameFromEmail,text.replace(email,""))
           return name
        # return nameFromNLP

    return ''


# this method can be tested with card - Rafal Ulatee
def extractPartialNameFromEmailId(email):
    name = email.split('@')[0]
    if '.' in name:
        return name.split('.')[0]
    if '_' in name:
        return name.split('_')[0]
    return name

def findNameFromEmailInCardText(nameFromEmail, text):
    linesIntheText = text.split('\n')
    for line in linesIntheText:
        if len(nameFromEmail)>2 and nameFromEmail.casefold() in line.casefold():  # sometimes email contain only initials, in that case return empty string
            return line.strip()
        
    return ''


def extractOrgFromText(text):
    name = getOrgUsingNlpLibrary(text)
    return name

def getNameUsingNlpLibrary(text):
    # testing name extraction using spacy
    # text = 'Satthew University\nTITLE OR COMPANY\n»\nSOQnHE\n12 YOUR BUSINESS ROAD\nCITY, STATE\n55555\n555-555-5555,\nMAIL@EMAILADDRESS.COM\nYOUR INSTAGRAM\nYOUR FACEBOOK\n'
    # text = 'Hannah Dakota Fanning\nTITLE OR COMPANY\n»\nSOQnHE\n12 YOUR BUSINESS ROAD\nCITY, STATE\n55555\n555-555-5555,\nMAIL@EMAILADDRESS.COM\nYOUR INSTAGRAM\nYOUR FACEBOOK\n' # identified
    # text = 'HANNAH DAKOTA FANNING\nTITLE OR COMPANY\n»\nSOQnHE\n12 YOUR BUSINESS ROAD\nCITY, STATE\n55555\n555-555-5555,\nMAIL@EMAILADDRESS.COM\nYOUR INSTAGRAM\nYOUR FACEBOOK\n' # No - identifies Hannah as org.
    # text='Mansion Limited\n\James Paul McCartney\nTITLE OR COMPANY\n»\nSOQnHE\n12 YOUR BUSINESS ROAD\nCITY, STATE\n55555\n555-555-5555,\nMAIL@EMAILADDRESS.COM\nYOUR INSTAGRAM\nYOUR FACEBOOK\n' # Identifies only Paul McCartney
    # text='James Paul McCartney\nTITLE OR COMPANY\n»\nSOQnHE\n12 YOUR BUSINESS ROAD\nCITY, STATE\n55555\n555-555-5555,\nMAIL@EMAILADDRESS.COM\nYOUR INSTAGRAM\nYOUR FACEBOOK\n' # identifies full name when its in the beggning of the text
    # text ='James Paul McCartney\nKey Account Manager\nDeer Park Court, Donnington Wood, Telford, Shropshire TF2 7NB\nTel: 0845 075 5544\nMobile: 07766 472618\nEmail: alan.stewart@lyreco.com www.lyreco.com\n' # works
    # text ='Key Account Manager\nJames Paul McCartney\nDeer Park Court, Donnington Wood, Telford, Shropshire TF2 7NB\nTel: 0845 075 5544\nMobile: 07766 472618\nEmail: alan.stewart@lyreco.com www.lyreco.com\n'
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

# alok source - https://gist.github.com/AjjuSingh/cab9252f30bc321069e2c94fae83fe1b 
phoneRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))? # area code
    (\s|-|\.)? # separator
    (\d{3}) # first 3 digits
    (\s|-|\.) # separator
    (\d{4}) # last 4 digits
    (\s*(ext|x|ext.)\s*(\d{2,5}))? # extension
    )''', re.VERBOSE)
       