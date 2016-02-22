__author__ = 'Simon'

import json
import re
import html
import string
import urllib.parse

sqfTypes = ['Array','Boolean','Bool','Group','Number','Object','Side','String','Code','Config','Control','Display','Script','Structured Text','Task','Team Member','Namespace','Trans','Orient','Target','Vector','Editor Object','Any Value','Anything','Any','Nothing','Void','If Type','While Type','Switch Type','For Type','Waypoint','Location','PositionAGL','PositionATL','PositionASLW','Color','Position','Eden Entity']
sqfTypeSub = {'Waypoint': 'Array','PositionAGL': 'Array', 'PositionASLW': 'Array', 'PositionATL': 'Array','Color': 'Array','Any': 'Any Value','Bool':'Boolean'}

typeExpr = r'(' + '|'.join(sqfTypes)+')'
arrayExpr = r'(\[[^=\n]*\])'
strExpr = r'(".*?")'
paramExpr = arrayExpr+'|'+strExpr+'|[\w_\-0-9()]+|for /\.\.\./'
opExpr = r'([|&+\-><!%*/\^:]{1,2}|==|<=|>=|!=|[a-zA-Z0-9_]+)'

data = {};
with open('bi-wiki-operator.json', 'r') as f:
    data = json.load(f)


outputParser = {'null':{},'unary':{},'binary':{}};
outputAutocomplete = [];
outputSyntaxStr = [];

for cmd in data:
    cmdTemplateParser = {};
    cmdTemplateAutocomplete = {};
    cmdTemplateAutocomplete['rightLabel'] = 'SQF Command'
    cmdTemplateAutocomplete['type'] = 'function'
    cmdTemplateAutocomplete['leftLabel'] = ''
    cmdTemplateAutocomplete['descriptionMoreURL'] = 'http://community.bistudio.com/wiki/' + urllib.parse.quote(str(cmd['title']))

    cmdTemplateAutocomplete['description'] = re.sub(r'(<[^<]+?>)','',cmd['description']).strip()
    cmdTemplateAutocomplete['description'] = str(html.unescape(cmdTemplateAutocomplete['description']))

    syntax = re.sub(r'(<[^<]+?>)','',cmd['syntax']).strip()
    syntax = re.sub(r'(&#160;|   ).*','',syntax)
    syntax = str(html.unescape(syntax))

    returnValueStr = re.sub(r'(<[^<]+?>)','',cmd['returnValue']).strip()
    returnValueStr = str(html.unescape(returnValueStr))
    returnValue = []
    typeListRegex = re.search(typeExpr,returnValueStr)


    while typeListRegex:
        t = typeListRegex.group(0)
        t = sqfTypeSub.get(t,t)
        returnValue.append(t)
        returnValueStr = re.sub(re.escape(typeListRegex.group(0)),'',returnValueStr)
        typeListRegex = re.search(typeExpr,returnValueStr)

    if ((not 'Nothing' in returnValue) and len(returnValue)==1) or len(returnValue)>1:
        cmdTemplateAutocomplete['leftLabel'] = '('+', '.join(returnValue)+') = '

    cmdTemplateParser['type'] = returnValue;

    params = re.sub(r'</dd>','\n',cmd['parameter']).strip()
    params = re.sub(r'(<[^<]+?>)','',params).strip()
    params = str(html.unescape(params))

    params = params + '\n'
    paramListExpr = r'(?P<name>'+paramExpr+')\s*(\(Optional\))?\s*[:]\s*(\([^)]+\))?\s*(?P<type>('+typeExpr+'(,\s*| or )?)+)';
    paramRegex = re.search(paramListExpr,params)
    parameters = {}
    parametersR = []
    while paramRegex:
        parameter = {}
        parametersR.append(re.escape(paramRegex.group('name')))

        typeList = []
        typeListStr = paramRegex.group('type')
        typeListRegex = re.search(typeExpr,typeListStr)
        while typeListRegex:
            t = typeListRegex.group(0)
            t = sqfTypeSub.get(t,t)
            typeList.append(t)
            typeListStr = re.sub(re.escape(typeListRegex.group(0)),'',typeListStr)
            typeListRegex = re.search(typeExpr,typeListStr)

        parameter['type'] = typeList;
        parameters[paramRegex.group('name')] = parameter
        params = re.sub(re.escape(paramRegex.group(0)),'',params)
        paramRegex = re.search(paramListExpr,params)


    sParaExpr = r'((?i)'+'|'.join(parametersR)+')'
    syntaxFieldsRegex = re.search(r'('+typeExpr+'\s+=\s+)?(?P<left>'+sParaExpr+'|'+arrayExpr+'|'+strExpr+')\s+(?P<op>'+opExpr+')\s+(\()?(?P<right>'+sParaExpr+'|'+arrayExpr+'|'+strExpr+')(\))?',syntax)
    snippet = ''

    if syntaxFieldsRegex and len(parametersR)>0:
        cmdTemplateParser['optype'] = 'binary'
        cmdTemplateParser['op'] = syntaxFieldsRegex.group('op')

        snippet = syntaxFieldsRegex.group('right')
        k=1;
        for para in parametersR:
            snippet = re.sub('(\W)('+para+')(\W)',r'\g<1>${'+str(k)+':\g<2>}\g<3>',' '+snippet+' ',0,re.IGNORECASE)
            k=k+1;
            snippet = snippet.strip()

        snippet = snippet.strip()+"$0";


        if syntaxFieldsRegex.group('left') in parameters:
            cmdTemplateParser['left'] = parameters[syntaxFieldsRegex.group('left')]['type']
        if re.match(strExpr,syntaxFieldsRegex.group('left')):
            cmdTemplateParser['left'] = ['String']
        if re.match(arrayExpr,syntaxFieldsRegex.group('left')):
            cmdTemplateParser['left'] = ['Array']

        if syntaxFieldsRegex.group('right') in parameters:
            cmdTemplateParser['right'] = parameters[syntaxFieldsRegex.group('right')]['type']
        if re.match(strExpr,syntaxFieldsRegex.group('right')):
            cmdTemplateParser['right'] = ['String']
        if re.match(arrayExpr,syntaxFieldsRegex.group('right')):
            cmdTemplateParser['right'] = ['Array']


    if not ('optype' in cmdTemplateParser) and len(parametersR)>0:
        syntaxFieldsRegex = re.search(r'('+typeExpr+'\s+=\s+)?(?P<op>'+opExpr+')\s+(\()?(?P<right>'+sParaExpr+'|'+arrayExpr+'|'+strExpr+')(\))?',syntax)
        if syntaxFieldsRegex:
            cmdTemplateParser['optype'] = 'unary'
            cmdTemplateParser['op'] = syntaxFieldsRegex.group('op')

            snippet = syntaxFieldsRegex.group('right')
            k=1;
            for para in parametersR:
                snippet = re.sub('(\W)('+para+')(\W)',r'\g<1>${'+str(k)+':\g<2>}\g<3>',' '+snippet+' ',0,re.IGNORECASE)
                k=k+1;
                snippet = snippet.strip()

            snippet = snippet.strip()+"$0";

            if syntaxFieldsRegex.group('right') in parameters:
                cmdTemplateParser['right'] = parameters[syntaxFieldsRegex.group('right')]['type']
            if re.match(strExpr,syntaxFieldsRegex.group('right')):
                cmdTemplateParser['right'] = ['String']
            if re.match(arrayExpr,syntaxFieldsRegex.group('right')):
                cmdTemplateParser['right'] = ['Array']




    if not ('optype' in cmdTemplateParser):
        syntaxFieldsRegex = re.search(r'('+typeExpr+'\s+=\s+)?(?P<op>'+opExpr+')',syntax)
        if syntaxFieldsRegex:
            cmdTemplateParser['optype'] = 'null'
            cmdTemplateParser['op'] = syntaxFieldsRegex.group('op')

    if not (cmdTemplateParser['op'] in outputParser[cmdTemplateParser['optype']]):
        outputParser[cmdTemplateParser['optype']][cmdTemplateParser['op'].lower()] = []

    if cmdTemplateParser['optype']!='null':
        if cmdTemplateParser['optype']=='binary':
            cmdTemplateAutocomplete['leftLabel'] = cmdTemplateAutocomplete['leftLabel'] + syntaxFieldsRegex.group('left') + ' '
        cmdTemplateAutocomplete['snippet'] = cmdTemplateParser['op'] + ' ' + snippet
    else:
        cmdTemplateAutocomplete['text'] = cmdTemplateParser['op']

    if re.match(r"[a-zA-Z0-9_]+",cmdTemplateParser['op']):
        outputSyntaxStr.append(cmdTemplateParser['op'])


    outputParser[cmdTemplateParser['optype']][cmdTemplateParser['op'].lower()].append(cmdTemplateParser)
    outputAutocomplete.append(cmdTemplateAutocomplete)

with open('operatorParser.json', 'w') as f:
    json.dump(outputParser,f)

autocompleteDict = {
    '.source.sqf': {
        'autocomplete': {
            'symbols':{
                'builtin':{
                    'typePriority': 4,
                    'suggestions': outputAutocomplete
                }
            }
        }
    }
};

with open('language-sqf-native-commands.json', 'w') as f:
    json.dump(autocompleteDict,f,indent=2)

with open('syntax_cmd_string.json', 'w') as f:
    f.write('|'.join(outputSyntaxStr))
