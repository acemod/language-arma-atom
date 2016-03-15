'use strict'
const write = require('fs').writeFile
const normalize = require('path').normalize

const chalk = require('chalk')
const ace3Reader = require('ace3-functions-reader')

const MAX_DESC_LENGTH = 128
const ELLIPSIS = String.fromCharCode(8230)

const URL_BASE = 'https://github.com/acemod/ACE3/tree/release/addons/'
const OUTPUT_FILE_PATH = normalize(`${__dirname}/../../settings/language-sqf-functions-ace3.json`)
const GRAMMAR_FILE_PATH = normalize(`${__dirname}/../../grammars/sqf.json`)
const GRAMMAR_FILE = require(GRAMMAR_FILE_PATH)

const ace3Dir = process.argv.slice(2)[0]
if (!ace3Dir) {
  throw new Error('Expected ace3 root directory as argument')
}

/*
  Parses description
  Assumes that the first 'token' is Author:
  description is assumed to be any text until next token
*/
function getDescription (text) {
  let tokens = 0
  let strs = []

  text.split(/\r?\n/).some(v => {
    if (/^[a-z]+\s*?:/i.test(v)) {
      tokens++
      return
    }
    if (tokens > 1) return true
    if (tokens === 1) {
      strs.push(v)
    }
    return false
  })

  if (!strs.length) return ''

  let str = strs.join('\r\n')
  if (str.length > MAX_DESC_LENGTH) return str.slice(0, MAX_DESC_LENGTH).replace(/\W*\s(\S)*$/, ` ${ELLIPSIS}`)
  else if (!str.endsWith('.')) str += '.'
  return str
}

/*
  Create syntax highlightning for sqf.json
*/
function createSyntaxHighlightString (fncs) {
  let str = '\\b(?i:ace_('
  let l = fncs.length - 1

  fncs.forEach((fnc, i) => {
    str += fnc.text.split('_').slice(1).join('_')
    if (i < l) str += '|'
  })

  str += '))\\b'
  return str
}

/*
  Write sqf.json
*/
function writeSyntaxHighlightning (str) {
  GRAMMAR_FILE.patterns.some(pattern => {
    if (pattern.name === 'support.function.ace3.sqf') {
      pattern.match = str
      write(GRAMMAR_FILE_PATH, JSON.stringify(GRAMMAR_FILE, null, 2).replace(/\n/gm, '\r\n'), err => {
        if (err) throw err
        console.info(chalk.green(`Wrote grammar file ${GRAMMAR_FILE_PATH}`))
      })
      return true
    }
  })
}

/*
  Write grammar and autocomplete files
*/
function writeOutput (fncs) {
  let data = {
    '.source.sqf': {
      'autocomplete': {
        'symbols': {
          'ACE3functions': {
            'suggestions': fncs
          }
        }
      }
    }
  }

  let syntax = createSyntaxHighlightString(fncs)
  writeSyntaxHighlightning(syntax)

  write(OUTPUT_FILE_PATH, JSON.stringify(data, null, 2).replace(/\n/gm, '\r\n'), err => {
    if (err) throw err
    console.info(chalk.green(`Wrote autocomplete file ${OUTPUT_FILE_PATH}`))
  })
}

/*
  Main
*/
ace3Reader.getFunctions(ace3Dir, { onlyComments: true }, (err, functions) => {
  if (err) throw err

  // flatmap the result and filter the public functions
  // match public: y (yes|ye|yeah|yup) and public: t (true)
  let publicFunctions = Array.prototype.concat
  .apply([], Object.keys(functions).map(v => functions[v]))
  .filter(v => /public\s*?:\s*?[yt]/gmi.test(v.text))

  console.info(chalk.green(`\nFound ${publicFunctions.length} public functions`))

  let data = publicFunctions.map(v => {
    let description = getDescription(v.text)
    if (!description) console.warn(chalk.yellow(`Found no description for ${v.file}`))

    return {
      text: v.name,
      rightLabel: 'ACE3 Function',
      type: 'function',
      description,
      descriptionMoreURL: URL_BASE + v.file
    }
  })

  writeOutput(data)
})
