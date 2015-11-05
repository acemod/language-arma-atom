'use strict'
const write = require('fs').writeFileSync
const normalize = require('path').normalize
const request = require('request')
const cheerio = require('cheerio')
const chalk = require('chalk')

const URL_BASE = 'http://community.bistudio.com'
const URL_FNC = `${URL_BASE}/wiki/Category:Arma_3:_Functions`
const OUTPUT_FILE = normalize(`${__dirname}/../../settings/language-sqf-functions-bis.json`)

let scrapeURL = (siteUrl, callback) => {
  request(siteUrl, (err, res, html) => {
    if (err) return callback(err)
    if (res.statusCode === 200) parseMainTable(html, callback)
    else callback(new Error(`Did not get expected status code (200) for URL ${siteUrl}, was ${res.statusCode}`))
  })
}

let parseMainTable = (html, callback) => {
  let $ = cheerio.load(html)
  let root = $('#mw-pages table').first()
  let ret = []

  root.find('h3').each(function () {
    $(this).next().find('li a[href]').each(function () {
      let text = $(this).attr('title').trim().replace(/\s/g, '_')
      let descriptionMoreURL = URL_BASE + $(this).attr('href').trim()
      ret.push({
        text,
        descriptionMoreURL,
        rightLabel: 'BIS Function',
        type: 'function',
        description: ''
      })
    })
  })

  callback(null, ret)
}

scrapeURL(URL_FNC, (err, fncs) => {
  if (err) throw err
  console.log(chalk.green(`Found ${fncs.length} functions`))

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

  write(OUTPUT_FILE, JSON.stringify(data, null, 2), 'utf-8')
  console.log(chalk.green(`Done, created ${OUTPUT_FILE}`))
})
