util = require('util')

describe "SQF grammar", ->
  grammar = null
  workspaceElement = atom.views.getView(atom.workspace)

#  executeCommand = (callback) ->
#    atom.commands.dispatch(workspaceElement, 'language-arma-atom:toggle')
#    waitsForPromise ->
#      activationPromise
#    grammar = atom.grammars.grammarForScopeName("source.sqf")
#    runs(callback)

#  beforeEach ->
    ## active our sqf package
#    activationPromise  = atom.packages.activatePackage("language-arma-atom")

#  it "parses the grammar", ->
#    executeCommand >
#      expect(grammar).toBeDefined()
#      expect(grammar.scopeName).toBe "source.sqf"

#  it "tokenizes multi-line strings", ->
#    executeCommand >
#      tokens = grammar.tokenizeLines('"12"')
#      expect(tokens[0][0].value).toBe '"'
#      expect(tokens[0][1].value).toBe '12'
#      expect(tokens[0][2].value).toBe '"'
