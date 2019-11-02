__author__ = 'Simon'

import json
import re
import urllib.request
import html

fnc_base_url = 'http://cbateam.github.io/CBA_A3/docs/index/'
fnc_page_names = ['Functions', 'Functions2', 'Functions3']
fncPrefix = 'CBA_fnc_'
macro_base_url = 'http://cbateam.github.io/CBA_A3/docs/files/main/script_macros_common-hpp.html'

f = urllib.request.urlopen(macro_base_url)
content = f.read().decode("utf-8")
f.close()

allMacros = re.findall(r'<div class=CTopic><h3 class=CTitle><a name="[^"]*"></a>([^<]*)</h3><div class=CBody>(.*?)</div>',content,re.DOTALL)

for macroContent in allMacros:
  c = re.search(r'(.*?)(<h4 class=CHeading>Parameters</h4>.*?)?(<h4 class=CHeading>Example</h4>.*?)?(?:<h4 class=CHeading>Author</h4>.*?)',macroContent[1],re.DOTALL)
  if c:
    description = c.group(1)

    descriptionTable = re.findall(r'<tr><td class=CDLEntry>(.*?)</td><td class=CDLDescription>(.*?)</td></tr>',macroContent[1],re.DOTALL)
    for tableEntry in descriptionTable:
      re.search(r'(.*?)(<h4 class=CHeading>Parameters</h4>.*?)?(<h4 class=CHeading>Example</h4>.*?)?(?:<h4 class=CHeading>Author</h4>.*?)',macroContent[1],re.DOTALL)


output = []
functionList = []

for fnc_page in fnc_page_names:
  f = urllib.request.urlopen(fnc_base_url + fnc_page + '.html')
  content = f.read().decode("utf-8")
  f.close()

  allFunctions = re.findall(r'<a[^>]*href\s*=\s*"([^"]*)"[^>]*class=ISymbol[^>]*>([^<]*)',content)

  for function in allFunctions:
    outputTemplate = {}
    outputTemplate['rightLabel'] = "CBA Function"
    outputTemplate['text'] = ''
    outputTemplate['description'] = ''
    outputTemplate['type'] = 'function'
    outputTemplate['descriptionMoreURL'] = fnc_base_url + function[0]
    print(function[1])
    functionList.append(function[1])
    f = urllib.request.urlopen(outputTemplate['descriptionMoreURL'])
    content = f.read().decode("utf-8")
    f.close()
    nameRegex = re.search(r'<a name="([^"]*)">',content)
    if nameRegex:
      outputTemplate['text'] = nameRegex.group(1)

    descriptionRegex = re.search(r'<h4 class=CHeading>Description</h4>(.*)<h4 class=CHeading>Parameters</h4>',content)
    if descriptionRegex:
      outputTemplate['description'] = str(html.unescape(re.sub(r'(<[^<]+?>)','',descriptionRegex.group(1)).strip()))

    output.append(outputTemplate)

autocompleteDict = {
  '.source.sqf': {
    'autocomplete': {
      'symbols':{
        'CBAfunctions':{
          'suggestions': output
        }
      }
    }
  }
};

with open('../settingsAvailable/language-sqf-functions-cba.json', 'w') as f:
  json.dump(autocompleteDict,f,indent=2)

with open('grammars-sqf-functions-cba.json', 'w') as f:
  f.write('|'.join(functionList))

print("\nCopy contents of 'grammars-sqf-functions-cba.json' into the 'support.function.cba.sqf' section of 'grammars/sqf.json'")
