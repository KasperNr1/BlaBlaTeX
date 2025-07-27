# BlaBlaTex
Is a Tool to write Boilerplate code to help you use your personal collection of $\LaTeX$ Templates.

## How To Use
### Setup
0. Install Git, Python, this Package, and probably LaTeX
1. Find or Create a public Git Repository with your LaTeX Templates
2. Run `blablatex set-repo <url>` to connect it to your Repository

### Usage
1. Run `blablatex init <templateName> [newFolderName]`

This will copy the folder called `templateName` from your repository into the current directory under the new name `newFolderName`

## Commands
This list can be displayed by running `blablatex --help`

- `set-repo`   Set the template repository URL.
- `path`       Get the full path of the local Repository
- `list`       List available templates.
- `init`       Copy a template to the current folder (optionally renaming the folder).
- `refresh`    Force refresh the local copy of the repo.                  