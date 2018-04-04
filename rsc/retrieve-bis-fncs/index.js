'use strict'
const http = require('http')
const write = require('fs').writeFile
const normalize = require('path').normalize
const request = require('request')
const cheerio = require('cheerio')
const chalk = require('chalk')
const progressBar = require('progress-bar')

const URL_BASE = 'http://community.bistudio.com'
const URL_FNC = `${URL_BASE}/wiki/Category:Arma_3:_Functions?${new Date().getTime()}` // Use timestamp as random get request to get uncached page (BI wiki has issues with caching)

const OUTPUT_FILE_PATH = normalize(`${__dirname}/../../settingsAvailable/language-sqf-functions-bis.json`)
const GRAMMAR_FILE_PATH = normalize(`${__dirname}/../../grammars/sqf.json`)
const GRAMMAR_FILE = require(GRAMMAR_FILE_PATH)

const MAX_DESC_LENGTH = 128
const MAX_REQUEST_RETRIES = 10
const ELLIPSIS = String.fromCharCode(8230)

const hardcodedDescriptions = require('./hardcoded_descriptions.json')

// Custom agent for max concurrent requests
let agent = new http.Agent({maxSockets: 6})

let scrapeURL = (url) => {
  return new Promise((resolve, reject) => {
    request.get({ url, agent }, (err, res, html) => {
      if (err) return reject(err)
      if (res.statusCode !== 200) {
        return reject(new Error(`Wrong HTTP code (${res.statusCode}) for URL ${url}, expected 200`))
      }

      resolve(html)
    })
  })
}

/*
  Extracts all functions from the main index page
*/
let parseFunctionsFromMainTable = (html) => {
  let $ = cheerio.load(html)
  let root = $('#mw-pages').first()
  let ret = []
  let added = new Set()

  root.find('h3').each(function () {
    $(this).next().find('li a[href]').each(function () {
      let $this = $(this)
      let text = $this.attr('title').trim().replace(/\s/g, '_') // replace space with _

      // Skip BIS_fnc_module**, BIS_fnc_VRCourse and duplicates
      let name = text.substr(8)
      if (name.startsWith('module') || name.startsWith('VRCourse') || added.has(text.toLowerCase())) return
      added.add(text.toLowerCase())

      let descriptionMoreURL = URL_BASE + $this.attr('href').trim()
      ret.push({
        text,
        rightLabel: 'BIS Function',
        type: 'function',
        description: '',
        descriptionMoreURL
      })
    })
  })

  return ret
}

/*
  HTTP GET for all functions after they are parsed from the main table
*/
let scrapeFunctions = (fncs) => {
  let completed = 0
  let expected = fncs.length
  let bar = progressBar.create(process.stdout, 20)
  console.info(chalk.green('Retrieving function descriptions\n'))

  return fncs.map(fnc => {
    return new Promise((resolve, reject) => {
      if (hardcodedDescriptions.hasOwnProperty(fnc.text)) {
        fnc.description = hardcodedDescriptions[fnc.text]
        completed++
        return resolve()
      }

      getFunctionHtml(fnc.descriptionMoreURL)
      .then(html => {
        fnc.description = parseFunctionDescription(html)
        bar.update(++completed / expected)
        resolve()
      })
      .catch(e => {
        reject(e)
      })
    })
  })
}

/*
  HTTP GET for a function, with retry if fail
*/
let getFunctionHtml = (url) => {
  return new Promise((resolve, reject) => {
    let tryRequest = (amountAttempts) => {
      scrapeURL(url)
      .then(html => resolve(html))
      .catch(e => {
        if (++amountAttempts >= MAX_REQUEST_RETRIES) {
          return reject(e)
        }
        // increase delay between retries each time, up to 10 sec
        setTimeout(() => {
          tryRequest(amountAttempts)
        }, 1000 * amountAttempts)
      })
    }
    tryRequest(0)
  })
}

/*
  Finds the function description inside html, clean it up a bit and try to figure out the format
*/
const REG_LF = /\r?\n/g
const REG_NA = /^n\/a/i
const REG_CONTAINS_WORD = /[A-Za-z]/
const REG_PURPOSE = /purpose?\s*:/i
const REG_DESCRIPTION = /description?\s*:/i
const REG_COMMENT = /\/\*\*.*|\/\/|\*.*\//g
let parseFunctionDescription = (html) => {
  let $ = cheerio.load(html)
  let element = $('._description').find('dl > dt:contains("Description:")').next('dd')
  element.find('[href="/wiki/BIS_fnc_exportFunctionsToWiki"]').parentsUntil('small').remove()

  let str = element.text().trim()
  if (!str || REG_NA.test(str) || str.includes('#define')) return ''

  let cleaned = str.split(REG_LF)
  .map(v => {
    v = v.replace(REG_COMMENT, '').trim()
    if (v.startsWith('*')) v = v.substr(v.lastIndexOf('*') + 1)
    if (!REG_CONTAINS_WORD.test(v)) return ''
    return v
  })
  .filter(Boolean)
  .join(' ')

  let idx = cleaned.search(REG_DESCRIPTION)
  if (idx !== -1) return findDescriptionEnd(cleaned.substr(idx + cleaned.match(REG_DESCRIPTION)[0].length))

  idx = cleaned.search(REG_PURPOSE)
  if (idx !== -1) return findDescriptionEnd(cleaned.substr(idx + cleaned.match(REG_PURPOSE)[0].length))

  // can't figure out the format, just return until first dot or max length
  return findDescriptionEnd(cleaned)
}

/*
  Figure out the end of a description
  Can be three things:
  1) The first dot encountered if it's before any words in REG_DO_NOT_INCLUDE
  2) The first occurence of a word from REG_DO_NOT_INCLUDE
  3) MAX_DESC_LENGTH characters (always checked)
  if > MAX_DESC_LENGTH, replace last word with ellipsis
*/
const REG_LAST_WORD = /\W*\s(\S)*$/
const REG_DO_NOT_INCLUDE = /www\.|http:|example?\s:|parameters?\s*:|parameter\(s\)?\s*:|arguments?\s*:|modes?\s*:|remarks?\s*:/i
let findDescriptionEnd = str => {
  let dotIdx = findFirstDot(str)
  let noInclude = str.search(REG_DO_NOT_INCLUDE)

  let end = str.length
  if (noInclude > -1) end = noInclude
  if (dotIdx !== -1 && (dotIdx < noInclude || noInclude === -1)) end = dotIdx

  let newStr = str.slice(0, end).trim()
  if (newStr.length > MAX_DESC_LENGTH) return newStr.slice(0, MAX_DESC_LENGTH).replace(REG_LAST_WORD, ` ${ELLIPSIS}`)
  return newStr
}

/*
    Finds the first dot in a string where the char after the dot is space or tab
*/
const REG_VALID_AFTER_DOT = /[ \s\t]/
let findFirstDot = str => {
  for (var i = 0; i < str.length; i++) {
    if (str[i] === '.' && REG_VALID_AFTER_DOT.test(str[i + 1])) return i
  }
  return -1
}

/*
  Creates syntax highlightning for sqf.json
*/
let createSyntaxHighlightString = fncs => {
  let str = '\\b(?i:BIS_fnc_('
  let l = fncs.length - 1

  fncs.forEach((fnc, i) => {
    str += fnc.text.substr(8)
    if (i < l) str += '|'
  })

  str += '))\\b'
  return str
}

/*
  Write sqf.json
*/
let writeSyntaxHighlightning = str => {
  GRAMMAR_FILE.patterns.some(pattern => {
    if (pattern.name === 'support.function.bis.sqf') {
      pattern.match = str
      write(GRAMMAR_FILE_PATH, JSON.stringify(GRAMMAR_FILE, null, 2).replace(/\n/gm, '\r\n'), err => {
        if (err) throw err
        console.log(chalk.green('\nWrote grammar file %s'), GRAMMAR_FILE_PATH)
      })
      return true
    }
  })
}

/* Main */
scrapeURL(URL_FNC)
.then(html => {
  let fncs = parseFunctionsFromMainTable(html)
  console.info(chalk.green(`Found ${fncs.length} functions`))

  Promise.all(scrapeFunctions(fncs))
  .then(() => {
    // Make sure descriptions ends with a dot
    let addDot = /[a-zA-Z\d\)]$/
    fncs.forEach(v => {
      let desc = v.description
      if (desc.length && addDot.test(desc)) {
        v.description = `${desc}.`
      }
    })

    let data = {
      '.source.sqf': {
        'autocomplete': {
          'symbols': {
            'BISfunctions': {
              'suggestions': fncs
            }
          }
        }
      }
    }

    // to only output descriptions
    // let d = fncs.map(v => `${v.text}: ${v.description}`).join('\n')
    // write('./out.txt', d)

    let syntax = createSyntaxHighlightString(fncs)
    writeSyntaxHighlightning(syntax)

    write(OUTPUT_FILE_PATH, JSON.stringify(data, null, 2).replace(/\n/gm, '\r\n'), err => {
      if (err) throw err
      console.info(chalk.green(`\nDone, created ${OUTPUT_FILE_PATH}`))
    })
  })
  .catch(err => {
    console.error(chalk.red(err))
  })
})
.catch((err) => {
  console.error(chalk.red(err))
})
