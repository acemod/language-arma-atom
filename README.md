# Arma language support in Atom

This packages adds syntax highlighting and auto-completions for SQF files in Atom, including functions and macros from the [CBA](http://github.com/CBATeam/CBA_A3/) and [ACE3](http://github.com/acemod/ACE3/) projects. This package is maintained and developed by the [ACE3](http://ace3mod.com/) development team and the Arma community effort.

Support for the following file types used by the Real Virtuality engine has been added:
- sqf
- sqm
- cpp
- hpp
- ext
- cfg

### Syntax Highlighting

Syntax highlighting for all functions and script commands by Bohemia Interactive is supported. Next to that, functions and macros from CBA and ACE3 projects are also supported.

![Syntax Highlighting](https://raw.githubusercontent.com/acemod/language-arma-atom/master/rsc/images/syntax_highlighting.png)

### Autocomplete

With a goal of faster development in SQF, auto-completion for all BIS functions and script commands, as well as CBA and ACE3 functions and macros, is supported. All autocomplete assets also have a type, description and URL to their documentation.

![Autocomplete](https://raw.githubusercontent.com/acemod/language-arma-atom/master/rsc/images/autocomplete.png)

> CBA and ACE3 commands are optional, but enabled by default.

### Snippets

Quick development also requires writing a lot of different blocks or combinations of code. A handful of useful snippets ranging from BIS conditional structures and loops through CBA macros and ACE3 function headers were added to help you with this.

![Snippets](https://raw.githubusercontent.com/acemod/language-arma-atom/master/rsc/images/snippets.png)

> CBA and ACE3 snippets are optional, but enabled by default.

### Open Latest RPT File

Allows you to quickly open the latest Arma RPT log file with quick and easy access. Simply open the Command Palette and search for it or navigate to `Packages -> Language Arma Atom -> Open Latest RPT File`.

![Open Latest RPT](https://raw.githubusercontent.com/acemod/language-arma-atom/master/rsc/images/open_latest_rpt.png)

### Build Project Tools

*Only available if the project being worked on is based on a project framework like CBA's and ACE3's. The project must contain `build.py` and `make.py` tools.*

To ease development when working on projects with a framework like CBA's or ACE3's, quick options for building the project directly from Atom is supported. You have the ability to build a development version or a full release, simply open the Command Palette and search for it or navigate to `Packages -> Language Arma Atom -> Build Dev/Release`.

![Build Dev](https://raw.githubusercontent.com/acemod/language-arma-atom/master/rsc/images/build_dev.png)


## Contributing

Contributions are greatly appreciated. You can help out with the ongoing development by looking for potential bugs in our code base, or by contributing new features. To contribute something to the Arma Language Package, simply fork this repository and submit your pull requests for review by other collaborators (see [Contributing Guide](CONTRIBUTING.md)).

Please, use our [Issue Tracker](https://github.com/acemod/language-arma-atom/issues) to report a bug, propose a feature, or suggest changes to the existing ones.
