{CompositeDisposable} = require 'atom'
copyNewer = require 'copy-newer'

buildProject = require './lib/build-project'
openLatestRptFile = require './lib/open-latest-rpt-file'
optionalAutosuggests = require './lib/optional-autosuggests'

module.exports =
  subscriptions: null

  config:
    appDataFolder:
      title: "Arma 3 AppData Folder",
      description: "Location of the Arma 3 Application Data Folder (location of RPT files)",
      type: "string",
      default: "%LOCALAPPDATA%\\Arma 3\\"
      order: 1
    buildDevScript:
      title: "Development Build Script",
      description: "Location of the Development Build Script (requires a compatible script, such as CBA's or ACE3's build.py)",
      type: "string",
      default: "<current-project>/tools/build.py"
      order: 2
    buildReleaseScript:
      title: "Release Build Script"
      description: "Location of the Release Build Script (requires a compatible script, such as CBA's or ACE3's make.py)"
      type: "string"
      default: "<current-project>/tools/make.py"
      order: 3
    autosuggest:
      title: "Autosuggestions"
      type: "object"
      order: 4
      properties:
        includeCba:
          title: "Include CBA"
          description: "Autosuggestions will include CBA specific commands and snippets"
          type: "boolean"
          default: true
          order: 1
        includeAce:
          title: "Include ACE"
          description: "Autosuggestions will include ACE specific commands and snippets"
          type: "boolean"
          default: true
          order: 2

  activate: ->
    @subscriptions = new CompositeDisposable
    @subscriptions.add atom.commands.add 'atom-workspace',
      'language-arma-atom:build-dev': => buildProject.dev()
    @subscriptions.add atom.commands.add 'atom-workspace',
      'language-arma-atom:build-release': => buildProject.release()
    @subscriptions.add atom.commands.add 'atom-workspace',
      'language-arma-atom:open-latest-RPT-file': => openLatestRptFile.open()

    # If package is updated, copy required autosuggest files
    copyNewer "language-sqf-native*", "#{__dirname}/snippets", {
      cwd: "#{__dirname}/snippetsAvailable"
    }
    copyNewer "language-sqf-native*", "#{__dirname}/settings", {
      cwd: "#{__dirname}/settingsAvailable"
    }

    # Copy optional autosuggest files
    atom.config.observe 'language-arma-atom.autosuggest.includeCba', (checked) ->
      optionalAutosuggests.set('cba', checked)
    atom.config.observe 'language-arma-atom.autosuggest.includeAce', (checked) ->
      optionalAutosuggests.set('ace', checked)

  deactivate: ->
    @subscriptions.dispose()
