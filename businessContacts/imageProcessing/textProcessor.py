import re
import spacy
import pytesseract


# This method extracts text from business card image 
def getTextFromOCR(image):
    return pytesseract.image_to_string(image)

# This is the main method which performs all the 
# text classification to 
def processCardText(extractedText):
    
    sanitisedText = sanitizeText(extractedText) 

    phone = extractPhoneNumber(sanitisedText)
    # mob = getMobileNumber(sanitisedText)
    email = extractEmailIDFromText(sanitisedText)
    # remainingText = removeClassifiedFieldsFromText(sanitisedText, email, mob, "")
    # remainingText = sanitisedText
    # extractMobileAndRemoveItFromText(sanitisedText)
    name = extractContactName(sanitisedText, email) # passing email for the fallback of the

    org = extractOrgFromText(sanitisedText, email)

    return (sanitisedText, name, org, email, phone)

# This method returns the first string which matches
# the email id pattern defined by the regular expression
def extractEmailIDFromText(text):
    emailIds = re.findall(r'[\w\.-]+@[_\w\.]+', text)
    if len(emailIds)==0:
        return ""
    emailId = emailIds[0]
    return emailId
    

# This method removes the vertical white spaces
# from the recognized string returned by the OCR
# It also removes any whitespace that is mistakenly
# introduced in the Email Id during OCR
def sanitizeText(text):
    lines = text.split("\n")
    string_without_empty_lines = ""
    nonEmptyLines = [line for line in lines if line.strip()]
    for line in nonEmptyLines:
       if '@' in line:
           indexOfAt = line.find('@')
           indexOfDot = line.find('.')
           if len(line) > indexOfAt+1 and line[indexOfAt+1] == " ":
               line = line[:indexOfAt+1] + '' + line[indexOfAt+2:]
           if len(line) > indexOfDot+1 and line[indexOfDot+1] == " ":
               line = line[:indexOfDot+1] + '' + line[indexOfDot+2:]
           if indexOfAt-1>0 and line[indexOfAt-1] == " ":
               line = line[:indexOfAt-1] + '' + line[indexOfAt:]
           if indexOfDot-1>0 and line[indexOfDot-1] == " ":
               line = line[:indexOfDot-1] + '' + line[indexOfDot:]
       string_without_empty_lines += line + "\n"
    return string_without_empty_lines



# This function returns the identified phone number that matches 
# the regular expression defined in the function
# Source - 
def extractPhoneNumber(text):

    phoneRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))? # captures the area code
    (\s|-|\.)? # separator can be -  a white space, a "-" or a "."
    (\d{3}) # captures last 4 digits
    (\s|-|\.)? # separator can be -  a white space, a "-" or a "."
    (\d{4}) # captures last 4 digits
    (\s*(ext|x|ext.|ext:|Ext.|Ext:)\s*(\d{2,5}))? # extension
    )''', re.VERBOSE)

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



# This method identifies the name field from the text
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

def extractOrgNameFromEmailId(email):
    if email != '':
     domain = email.split('@')[1]
     return domain.split('.')[0]
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


def extractOrgFromText(text, email):
    orgName = getOrgUsingNlpLibrary(text)
    if orgName=='':
       orgName = extractOrgNameFromEmailId(email)
    return orgName

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


# alok source - https://gist.github.com/AjjuSingh/cab9252f30bc321069e2c94fae83fe1b 



    # ((\d{3}|\(\d{3}\))?(\s|-|\.)?(\d{3})(\s|-|\.)(\d{4})(\s*(ext|x|ext.|ext:|Ext.|Ext:)\s*(\d{2,5}))?)