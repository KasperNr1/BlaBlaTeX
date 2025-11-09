# BlaBlaTex
Is a Tool to write Boilerplate code to help you use your personal collection of $\LaTeX$ Templates.

It clones the specified repo into a hidden folder on your computer and copies subfolders from it to whereever you need it. This way you dont even need an internet connection after the first setup.

Since the tool copies subfolders of a repo, it is recommended to structure your templates in a way that no files outside their folder are required.

## How To Use
### Installation
You can install the app through python's package manager `pip` using
``` Shell
pip install blablatex
```

If you want to install a specific version, you can do that
```
pip install blablatex==1.x.x
```


### Setup
0. Install Git, Python, this Package, and probably LaTeX
1. Find or Create a public Git Repository with your LaTeX Templates
2. Run `blablatex set-repo <url>` to connect it to your Repository

### Usage
1. Run `blablatex init <templateName> [newFolderName]`

This will copy the folder called `templateName` from your repository into the current directory under the new name `newFolderName`

## Commands
This list can be displayed by running `blablatex --help`

- `init`       Copy a template to the current folder (optionally renaming the folder).
- `list`       List available templates.
- `path`       Get the full path of the local Repository
- `refresh`    Force refresh the local copy of the repo.          
- `set-repo`   Set the template repository URL.
- `version`    Display the version Number and Exit

## Changelog
### 1.1.1
#### Bugfix
Prevent a crash when cloning the Remote-Repo from Scratch. 

### 1.1.0
#### Features
- Add Command `version` to display current Version number
- Now Works offline with most recent status

#### Bugfixes
Fix a crash that is caused by failed pulls from Git Remote Repository.

### 1.0.0
Initial Release, add the following commands:

- `set-repo`   Set the template repository URL.
- `path`       Get the full path of the local Repository
- `list`       List available templates.
- `init`       Copy a template to the current folder (optionally renaming the folder).
- `refresh`    Force refresh the local copy of the repo.          
