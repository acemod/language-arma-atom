fs = require 'fs'
path = require 'path'
copyNewer = require 'copy-newer'

packageRoot = path.resolve(__dirname, '../')
fileList =
  cba:
    snippets: [
      'language-sqf-cba.json'
    ]
    settings: [
      'language-sqf-functions-cba.json'
      'language-sqf-macros-cba.json'
    ]
  ace:
    snippets: [
      'language-sqf-ace3.json'
    ]
    settings: [
      'language-sqf-functions-ace3.json'
      'language-sqf-macros-ace3.json'
    ]

module.exports =
  set: (addonName, required) ->
    addon = fileList[addonName]
    operations = []

    # If required always try to copy; If package was updated we'll get newest files
    if required
      for type of addon
        operations.push copyNewer(file, "#{packageRoot}/#{type}", {
          cwd: "#{packageRoot}/#{type}Available/"
        }) for file in addon[type]
    else
      for type of addon
        operations.push deleteFile "#{packageRoot}/#{type}/#{f}" for f in addon[type]

    # For debugging
    Promise.all(operations)
      .catch (err) -> console.error 'Error while updating autosuggest settings. =>', err


deleteFile = (file) ->
  return new Promise (resolve, reject) ->
    fs.unlink file, (err) ->
      # Ignore error for non-existing file
      if err and err.toString().indexOf('ENOENT') < 0
        reject("ERROR deleting file: #{file}")
      else resolve("#{file} removed")
