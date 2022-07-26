# LSP-marksman

An LSP server for Markdown that provides completion, go to definition, find references, diagnostics, etc. It also supports wiki-link-style references that enable Zettelkasten-like, note-taking.

Provided through [Marksman](https://github.com/artempyanykh/marksman).

### Installation

Currently, LSP-marksman is not on Package Control.

1. Install [LSP](https://packagecontrol.io/packages/LSP) via Package Control.
1. Clone LSP-marksman to your `Packages` folder.
    1. Run `sublime.packages_path()` in Sublime Text console. It will show the path of your `Packages` folder.
    1. Open terminal in the `Packages` folder and then run `git clone git@github.com:bitsper2nd/LSP-marksman.git`
1. Restart Sublime Text.

### Configuration

There are some ways to configure the package and the language server.

- From `Preferences > Package Settings > LSP > Servers > LSP-marksman`
- From the command palette `Preferences: LSP-marksman Settings`
