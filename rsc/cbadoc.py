__author__ = 'Simon'

import json
import re
import HTMLParser
import urllib
h = HTMLParser.HTMLParser()


fnc_base_url = 'https://dev.withsix.com/docs/cba/index/'
fncPrefix = 'CBA_fnc_'
macro_base_url = 'https://dev.withsix.com/docs/cba/files/main/script_macros_common-hpp.html'

f = urllib.urlopen(macro_base_url)
content = f.read()
f.close()

allMacros = re.findall(r'<div class=CTopic><h3 class=CTitle><a name="[^"]*"></a>([^<]*)</h3><div class=CBody>(.*?)</div>',content,re.DOTALL)

for macroContent in allMacros:
    c = re.search(r'(.*?)(<h4 class=CHeading>Parameters</h4>.*?)?(<h4 class=CHeading>Example</h4>.*?)?(?:<h4 class=CHeading>Author</h4>.*?)',macroContent[1],re.DOTALL)
    if c:
        description = c.group(1)
        
        descriptionTable = re.findall(r'<tr><td class=CDLEntry>(.*?)</td><td class=CDLDescription>(.*?)</td></tr>',macroContent[1],re.DOTALL)         
        for tableEntry in descriptionTable:
            re.search(r'(.*?)(<h4 class=CHeading>Parameters</h4>.*?)?(<h4 class=CHeading>Example</h4>.*?)?(?:<h4 class=CHeading>Author</h4>.*?)',macroContent[1],re.DOTALL)
    


f = urllib.urlopen(fnc_base_url + 'Functions.html')
content = f.read()
f.close()
    
allFunctions = re.findall(r'<a[^>]*href\s*=\s*"([^"]*)"[^>]*class=ISymbol[^>]*>([^<]*)',content)

output = [];

for function in allFunctions:
    outputTemplate = {}
    outputTemplate['rightLabel'] = "CBA Function"
    outputTemplate['text'] = ''
    outputTemplate['description'] = ''
    outputTemplate['type'] = 'function'
    outputTemplate['descriptionMoreURL'] = fnc_base_url + function[0]
    print function[1]
    f = urllib.urlopen(outputTemplate['descriptionMoreURL'])
    content = f.read()
    f.close()
    nameRegex = re.search(r'<a name="([^"]*)">',content)
    if nameRegex:
        outputTemplate['text'] = nameRegex.group(1)
        
    descriptionRegex = re.search(r'<h4 class=CHeading>Description</h4>(.*)<h4 class=CHeading>Parameters</h4>',content)
    if descriptionRegex:
        outputTemplate['description'] = h.unescape(re.sub(r'(<[^<]+?>)','',descriptionRegex.group(1)).strip()).encode('ascii', 'ignore')
        
    output.append(outputTemplate)
    
autocompleteDict = {
    '.source.sqf': {
        'autocomplete': {
            'symbols':{
                'CBAfunctions':{
                    'typePriority': 4,
                    'suggestions': output
                }
            }
        }
    }
};
    
with open('language-sqf-cba-functions.json', 'w') as f:
    json.dump(autocompleteDict,f)
    
f = urllib.urlopen(fnc_base_url + 'Functions.html')
content = f.read()
f.close()


        
