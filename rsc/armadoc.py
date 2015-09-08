__author__ = 'Simon'

import urllib
import json
import re

params = {'format': 'json',
          'action': 'query',
          'list': 'categorymembers',
          'cmtitle': 'Category:Scripting_Commands_Arma_3',
          'cmtype':'page',
          'cmlimit':500,
          'cmcontinue':0}
f = urllib.urlopen("https://community.bistudio.com/wikidata/api.php?%s" % urllib.urlencode(params))
content = json.loads(f.read());
data = []
while content.has_key('query-continue'):
    data = data + content['query']['categorymembers']
    params['cmcontinue'] = content['query-continue']['categorymembers']['cmcontinue']
    f = urllib.urlopen("https://community.bistudio.com/wikidata/api.php?%s" % urllib.urlencode(params))
    content = json.loads(f.read());

data = data + content['query']['categorymembers']

params = {'format': 'json',
          'action': 'parse',
          'pageid': '',
          'prop': 'text'}

blacklist = [
"a = b",
"for",
"in",
"switch"]

output = [];

for item in data:
    if item['title'] not in blacklist:
        print item['title']
        params['pageid'] = item['pageid']
        f = urllib.urlopen("https://community.bistudio.com/wikidata/api.php?%s" % urllib.urlencode(params))
        content = json.loads(f.read())['parse']
        text = content['text']['*'].encode("ascii", "ignore")
        rawText = text;

        description = ''
        description = re.search(r"<dt>Description:</dt>\s+<dd>(.+?)</dd>",text,re.DOTALL|re.MULTILINE).group(1);
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

