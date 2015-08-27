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

output = [];
blacklist = ["! a",
"- a",
"a != b",
"a % b",
"a && b",
"a * b",
"a - b",
"a / b",
"a = b",
"a == b",
"a greater b",
"a greater= b",
"a less b",
"a less= b",
"a or b",
"a plus b",
"a ^ b",
"a:b",
"config / name",
"config greater greater name",
"plus a",
"valuea plus valueb",
"for",
"if",
"in",
"switch"]


for item in data:
    if item['title'] not in blacklist:
        print item['title']
        params['pageid'] = item['pageid']
        f = urllib.urlopen("https://community.bistudio.com/wikidata/api.php?%s" % urllib.urlencode(params))
        content = json.loads(f.read())['parse']
        text = content['text']['*'].encode("ascii", "ignore")
        #fields = re.findall(r"^\|(?:\s*(\w+)\s*=|\s*)(.+?)\|=\s*([\w ]+)\s*\n",content['wikitext']['*'],re.DOTALL|re.MULTILINE);
        description = re.search(r"<dt>Description:</dt>\s+<dd>(.+?)</dd>",text,re.DOTALL|re.MULTILINE).group(1);
        syntaxRegex = re.search(r'<dt>Syntax:</dt>\s+<dd>(.+?)</dd>',text,re.DOTALL|re.MULTILINE)
        while syntaxRegex:
            temp = {}
            text = text[syntaxRegex.end():];
            syntax = re.sub(r'(<.*?>)','',syntaxRegex.group(1))
            syntax= re.sub(r'(\s*.*\s*[=])','',syntax)
            syntax= re.sub(r'(&#160;|   | \(.*?\)).*','',syntax)

            returnValueRegex = re.search(r"<dt>Return Value:</dt>\s+<dd>(.+?)</dd>",text,re.DOTALL|re.MULTILINE)

            #temp['replacementPrefix'] = str(item['title'])
            temp['rightLabel'] = 'SQF Command'
            temp['type'] = 'function'
            temp['leftLabel'] = ''
            if returnValueRegex:
                temp['leftLabel'] = re.search(r'\s*(\w+).*?',re.sub(r'(<.*?>)','',returnValueRegex.group(1))).group(1).strip()
                temp['leftLabel'] += ' ='
                if temp['leftLabel']=='Nothing =':
                    temp['leftLabel'] = '';

            syntaxRegex2 = re.search(r'(.*?)\s?'+str(item['title']),syntax);
            if syntaxRegex2:
                temp['leftLabel'] += ' '+syntaxRegex2.group(1).strip()
                syntax = re.sub(re.escape(syntaxRegex2.group(1)),'',syntax,0,re.IGNORECASE)

            temp['description'] = re.sub(r'(<.*?>)','',description).strip()
            temp['descriptionMoreURL'] = 'http://community.bistudio.com/wiki/' + urllib.quote(str(item['title']))

            cmdParamsRegex = re.search(r'<dt>Parameters:</dt>\s*(.+?)</dl>',text,re.DOTALL|re.MULTILINE)
            if cmdParamsRegex:
                cmdParams = re.findall(r'<(?:dd class\="param"|dt.*?)>(.*?)[:]',cmdParamsRegex.group(1),re.DOTALL|re.MULTILINE)
                k=1;
                for param in cmdParams:
                    if param != 'Return Value':
                        syntax = re.sub('(\W)('+re.escape(param.strip())+')(\W)',r'\g<1>${'+str(k)+':\g<2>}\g<3>',' '+syntax+' ',0,re.IGNORECASE)
                        k=k+1;
                syntax = re.sub(r'[.]{3}','${'+str(k)+':...}',' '+syntax+' ',0,re.IGNORECASE)
                temp['snippet'] = syntax.strip()+"$0";
                print temp['snippet']
            else:
                temp['text'] = str(item['title']).strip();


            output.append(temp)
            syntaxRegex = re.search(r"<dt>Syntax:</dt>\s+<dd>(.+?)</dd>",text,re.DOTALL|re.MULTILINE)
