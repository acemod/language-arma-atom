{CompositeDisposable} = require 'atom'
fs = require 'fs'
path = require 'path'
process = require 'process'

module.exports =
  subscriptions: null

  config:
    appDataFolder:
      title: "Arma 3 AppData Folder",
      description: "Location of the Arma 3 Application Data Folder (location of RPT files)",
      type: "string",
      default: "%localappdata%\\Arma 3\\"

  activate: ->
    @subscriptions = new CompositeDisposable
    @subscriptions.add atom.commands.add 'atom-workspace',
      'language-arma-atom:open-rpt-file': => @open()

  deactivate: ->
    @subscriptions.dispose()

  getLatestRptFile: (dir) ->
    (fs.readdirSync dir
      .filter (v) ->
        '.rpt' == path.extname (v)
      .map (v) ->
        return {
        name: dir+v,
        time: fs.statSync(dir + v).mtime.getTime()}
      .sort (a, b) -> b.time - a.time
      .map (v) -> v.name)[0]



  open: ->
    p = atom.config.get('language-arma-atom.appDataFolder').replace /%([^%]+)%/g, (_,n) -> process.env[n]
    atom.workspace.open(@getLatestRptFile p).done (rptView) ->
      rptView.moveToBottom()
      rptView.scrollToBottom()
      rptView.getBuffer().onDidReload (e) ->
        rptView.moveToBottom()
        rptView.scrollToBottom()
