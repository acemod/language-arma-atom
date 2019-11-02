__author__ = 'Simon'

import json
import re
import time
import urllib.request

params = {'format': 'json',
          'action': 'query',
          'list': 'categorymembers',
          'cmtitle': 'Category:Scripting_Commands',
          'cmtype':'page',
          'cmlimit':500,
          'cmcontinue':0}

f = urllib.request.urlopen("https://community.bistudio.com/wikidata/api.php?%s" % urllib.parse.urlencode(params))
content = json.loads(f.read().decode('utf-8'));
data = []
while 'continue' in content:
  data = data + content['query']['categorymembers']
  params['cmcontinue'] = content['continue']['cmcontinue']
  f = urllib.request.urlopen("https://community.bistudio.com/wikidata/api.php?%s" % urllib.parse.urlencode(params))
  content = json.loads(f.read().decode('utf-8'));

data = data + content['query']['categorymembers']

params = {'format': 'json',
          'action': 'parse',
          'pageid': '',
          'prop': 'text'}

blacklist = [
"a = b",
"for",
"switch",
"switch do"]

output = [];
index = 0;
for item in data:
  index = index + 1
  if index % 100 == 1:  # we need to pause in regular intervals to prevent DDos Protection from the Server
    time.sleep(1)
  if item['title'] not in blacklist:
    print (item['title'])
    params['pageid'] = item['pageid']
    f = urllib.request.urlopen("https://community.bistudio.com/wikidata/api.php?%s" % urllib.parse.urlencode(params))
    content = json.loads(str(f.read().decode()))['parse']
    text = str(content['text']['*'])
    rawText = text;

    description = ''
    description = re.search(r"<dt>Description:</dt>[\s]+<dd>(.+?)</dd>",text,re.DOTALL|re.MULTILINE).group(1);
    text = re.sub(r"(<dt>Description:</dt>\s+<dd>.+?</dd>)",'',text)
    syntaxRegex = re.search(r'<dt>Syntax:</dt>\s+<dd>(.+?)</dd>',text,re.DOTALL|re.MULTILINE)
    while syntaxRegex:
      command = {};
      text = text[syntaxRegex.end():];
      syntax=''
      syntax = re.sub(r'(<.*?>)','',syntaxRegex.group(1))

      returnValue = '';
      returnValueRegex = re.search(r"<dt>Return Value:</dt>\s*(?:<p>)?\s*<dd>(.+?)</dd>",text,re.DOTALL|re.MULTILINE)
      if returnValueRegex:
        returnValue = returnValueRegex.group(1)

      text = re.sub(r"(<dt>Return Value:</dt>\s+<dd>.+?</dd>)",'',text,1)

      parameter = '';
      parameterRegex = re.search(r'<dt>Parameters:</dt>\s*(.+?)</dl>',text,re.DOTALL|re.MULTILINE)
      if parameterRegex:
        parameter = parameterRegex.group(1)
      text = re.sub(r"(<dt>Parameters:</dt>\s*(.+?)</dl>)",'',text,1)

      command['title'] = str(item['title'])
      command['rawText'] = str(rawText);
      command['description'] = str(description);
      command['syntax'] = str(syntax);
      command['parameter'] = str(parameter);
      command['returnValue'] = str(returnValue);

      output.append(command)

      syntaxRegex = re.search(r"<dt>Syntax:</dt>\s+<dd>(.+?)</dd>",text,re.DOTALL|re.MULTILINE)

with open('bi-wiki-operator.json', 'w') as f:
  json.dump(output,f)

print("\nExecute 'parseOperators.py' to parse the retrieved information.")
