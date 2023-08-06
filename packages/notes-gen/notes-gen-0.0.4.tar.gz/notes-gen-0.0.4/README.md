# Notes Generator
A static site generator build specially for writing technical notes. You can see a live example here.

## Features

- Write notes in markdown and generate HTML, PDF and Latex.
- Divide single note in multiple markdown files with ```include``` directive.
- Easily customizable with custom plugins.
- Customizable website layout with user defined folder structure.

# Table of content
- [Getting started](#getting-started)
    + [Installation](#installation)
    + [Starting new project](#starting-new-project)
    + [Adding new notes](#adding-new-notes)
    + [Add Notes](#add-notes)
    + [Build](#build)
    + [Publish](#publish)
- [Folder Structure](#folder-structure)
- [Settings File](#settings-file)
- [Layouts](#layouts)
- [Include directive](#include-directive)
- [Plugins](#plugins)
- [Contributing](#contributing)
- [License](#license)

# Getting started
Notes generator is available as python package. 

### Installation
Install **notes-gen** command using pip.
```
pip install notes-gen
```
Notes generator needs pandoc and latex installed to work properly.
Install pandoc and latex using following command.
```shell
sudo apt install pandoc texlive-full
```
### Starting new project
To start a new project enter the following command
```
notes-gen startproject <project_name>
```
eg:
```shell
notes-gen startproject mynotes
```
where **mynote** is the name of the project.

This command will create a project folder with the name **mynotes** with some predefined folder structure.

### Adding new notes
To add new notes, cd into the project folder and  enter the following command. 
```shell
cd mynotes
notes-gen startnote
```
This command will ask you following questions
```
What name do u want for your note:  Single Variable Calculus #Give a title to your notes.

Give a small description of the note:  A small description about your new notes.

Give a comma seprated category: category1, category2, math, calculus

Folder for notes[single-variable-calculus.md]: math/calculus/single-variable-calculus.md  # Custom folder structure for notes if needed. 
```
### Add Notes
Now a file must be created in the **_notes** folder with the extension **.md**. You can edit that file and add your notes in markdown format.

### Build
To build notes run the following command
```
notes-gen build
```
This will create a **index.html** in the root folder of the project and all the html, pdf and latex file in the **_public** folder.

### Publish
You can publish the project folder as github page or on some server which servers static site.

# Folder Structure
By default **startproject** command creates the following folder structure.
```
<project_name>
	- _assets
		- index.css
		- index.js
		- notes.css
	- _layouts
		- index.html
		- notes.html
	- _notes
	- _plugins
	- _public
	- config.json
```
- **_assets**: This folder contains all the webiste assets like .css and js and images if needed.
- **_layouts**: Contains layout for index page and for individual notes page.
- **_notes**: This is directory where the notes are kept in markdown format.
- **_plugins**: All the custom plugins are kept under this directory.
-**_public**: Content of this directory is auto generated and deleted on every build. User should not add anything to this directory.
- **config.json**: Settings files for the project.

# Settings File
Settings file of the project must be in the project root directory and must be named **config.json**. 
Example of settings file looks like this
```js
{
  "folders": {  //All the folder for associated entity
    "assets": "_assets", 
    "public": "_public",
    "layout": "_layouts",
    "style": "_styles",
    "notes": "_notes",
    "plugins": "_plugins"
  },

  "root_index_page": true, //Generate index.html in the project root folder
  "generate_html": true, //Generate html form markdown
  "generate_pdf": true, //Generate pdf from markdown
  "generate_latex": true, //Generate latex from markdown.

  "pulgins_modules": [] //Array of custom plugins in the _plugins folder.
}

```
# Layouts
The **_layouts** folder contains layout for main index page and notes page. The project uses [Jinja](http://jinja.pocoo.org/) as its template render engine. For more on syntax used in templating please read [this](http://jinja.pocoo.org/docs/2.10/templates/).

Index.html receives a **site** object which contains an array of **notes** object describing details of each notes. 
Notes.html receives a **note** object containing detail of each node one at a time.

# Include directive
All the notes are written in **_notes** folder. You can write all the notes in single markdown file each or you can divide the content into multiple markdown files and combine it using include directive.
For example

You can have a ```chapter1.md``` file with following content
```markdown

# Chapter 1 heading
Something here

## Chapter 1 Sub heading 
Something here too

```

Can u can include it in the main file of the notes created using ```startnote``` command. 

```markdown
---
{
    "main": true,
    "title": "Single Variable Calculus",
    "description": "A small description about your new notes.",
    "category": ["category1","category2", "math", "calculus"]
}

---

# Main Heading

```include
chapter1.md 				//(this is comment) Here chapter1.md content will be added.
'''       //(this is comment) Using single apostipe instead of backtick for github markdown render

# Conclusion
Main conclusion here.
```

This way u can split the notes in multiple markdown and combine the together into a single note content.

# Plugins
Notes generator goes through following stages while build the site.
```
Pre Processing => Rendering => Post Processing => Cleanup
```
You can write custom plugins to be executed in any of this stages.

To write a custom plugins you must subclass following super classes. Each subclass of this super class we be ran at the respective stages.
```python
from notes_gen.core.preprocessors import BasePrePorcessor
from notes_gen.core.renders import BaseRender
from notes_gen.core.postprocessors import BasePostProcessor
from notes_gen.core.cleaners import BaseCleaner
```
Your subclass must be present in the **_pulgins** folder and you should register it in the **config.json** settings file under the key **pulgins_modules**.

For example u can create **myplugin.py** file in **_plugins** directory with following content
```python

from notes_gen.core.postprocessors import BasePostProcessor

class MyPostProcessor(BasePostProcessor):

	def execute(self, site):
		# Site object contains details for the site that is being generated.
		pass
```
And register this plugin in the **config.json** file.
```js
"pulgins_modules" : ["myplugins.MyPostProcessor"]
```
The execute function will be called by notes generator during the post processing phase.

# Contributing
This project was build for personal use, so I would only modify it if my needs arise. But your are free to fork it and make changes as per your need.

# License
This project is licensed under WTFPL license - For more info read [here](http://www.wtfpl.net/txt/copying/)  
