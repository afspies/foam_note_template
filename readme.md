# Outline
## VSCode
### Foam
Foam is a VSCode library which will process all markdown notes in these folders and allow you to create links between files using backreferences (i.e. [[some link]] creates the file ```some_link.md```, by default in the root directory of this project - this can be changed using the ```"foam.openDailyNote.directory": "<path>``` setting).

You can also view the graph of all your connections by running the command ```>Foam: Show Graph```.

### Markdown Image
This is a lightweight extension which allows you to paste an image from your clipboard directly into a markdown file - it is saved as a .jpg at a path of your choosing. In our case, we change this setting to save all such images into ```./Attachments/pasted_images```. For example:

``` 
"markdown-image.local.path": "/Attachments/pased_images",
"markdown-image.base.fileNameFormat": "${YY}${MM}${DD}_${hh}${mm}${ss}",
```

## Python
We use a python script (to be executed from the root of the workspace) to place annotations annotations which have been exported by [highlights](highlights) as a textbundle into our existing collection.

The minimal functionality is to:
* Create a new markdown file in our folder of papers, which includes
  * (Using the arxiv API) Metadata such as arxiv link, title, abstract 
  * All of our annotations and corresponding images, which will have been moved to ```./Attachments/papers/<paper_title>/<id>.jpg```
  * (Through the Semantic Scholar API) the top K most influential papers which cite this paper, and a list of all references from the paper, instantiated as backlinks, with added links to the papers' Semantic Scholar entries.
* Add an entry to ```./Papers/index.md``` which links to the corresponding paper file (specific pathing information is not required, as foam checks the entire workspace for a matching file name).

The format of the output file is specified by choosing a template from ```./Autosort/templates/```, and papers which are to be sorted are placed within ```./Autosort/papers_to_sort```.

At present, there is no toggleable functionality for the different behaviours of the script, and it will fail if the Semantic Scholar api is not reachable. [TODO] This can be easily changed.

# Requirements
## VSCode
```
Foam
Markdown Image
```

## Python
```
semanticscholar
arxiv
```

# To Do
* Automate detection of textbundle, and switch to manual extraction in the style of https://gist.github.com/stevepowell99/e1e389a57ea9a2bcb988
* Make the sort.py script at least marginally robust and treat most user-specific vars as cmd line flags, rather than hard-coded
* Automatic folder substructure based on pre-defined rules or using arxiv tags
* ...