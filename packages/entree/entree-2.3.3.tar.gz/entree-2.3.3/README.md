# entree

**entree** is a tool to jump start a programming project by creating all the files necessary to get started. **entree** can be used as a shell script, a [web service](http://entree.frenetic.be) or as a python package.

Here is the link to the [**entree** project on Pypi.org](https://pypi.org/project/entree/) and here is a link to the documentation for the [`entree` python package](http://frenetic-be.github.io/entree/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Installing

In order to install the `entree` shell script and the `entree` python package, simply use `pip`:

```
pip install entree
```

And that's it.

Or, download the .zip file from [GitHub](https://github.com/frenetic-be/entree) and navigate to the **entree** directory. For example,

```
cd ~/Downloads/entree-master/
```

Then install the package with

```
python setup.py install
```

**entree** was tested with Python 2.7 and Python 3.6.

### Testing the installation

If the installation was successful, you should now have an `entree` shell script. You can test it with the command

```
entree --version
```

The version number (for example `entree 2.3.3`) should then appear on the next line.

### How to use **entree**

#### How to use the `entree` shell script

The `entree` shell script is pretty straightforward. Here is a simple example to create a Python project called `foo`:

```
entree python foo
```

This will create a new directory `foo` in your current directory and will create all project files inside the `foo` directory. The previous example will create the following files:

```
foo/
|-- .gitignore
|-- License.md
|-- README.md
|-- foo/
    |-- __init__.py
|-- requirements.txt
|-- setup.py
|-- tests/
    |-- test_foo.py
```

It is possible to create the project files in another directory than the current directory using the `-d` option:

```
entree python -d path/to/other/directory/ foo
```

For complete usage information, type `entree -h` in a terminal.

#### How the use the web app

**entree** can be used online without installing anything. Visit [http://entree.frenetic.be](http://entree.frenetic.be) to check it out. Simply enter the project name and project type.

Optionally, you can add author information. All of the information entered on our web page is used to create the project files. We do not keep your data or share it with anyone else.

If there are files that you do not want to download, you can unselect the corresponding checkbox.

Finally, hit `Submit` and your download should start automatically.

### Supported project types

The following list contains the project types that are currently supported:

* HTML5
* Python
* Python - Flask
* Python - Large Flask App
* Python - SQLAlchemy

We hope to support more project types in the future. If there is a project type that you know well and you wish to add to the supported types, we'd love to hear from you. See below to see how you can contribute to this project.

## Configuration

The `entree` shell script and python package can be configured and customized. During installation, the following config file was created: `~/.config/entree_config.json`. The information in this file is used every time you run the `entree` command.

### Author information

In that config file, you can specify your name, email and url:

```json
{
    "author": "<UNDEFINED>",
    "author_email_prefix": "<UNDEFINED>",
    "author_email_suffix": "<UNDEFINED>",
    "author_url": "<UNDEFINED>",
}
```
### Default project type

You can specify a default project type:

```json
{
    "default_project_type": "python"
}
```

This default project type allows the shell script to run without a project type. For example,

```
entree foo
```

will create a Python project called `foo` if `"default_project_type": "python"`.

### Files to ignore

You can specify a list of files to ignore when creating a project:

```json
{
    "files_to_ignore": [
        ".DS_Store"
    ],
}
```

### Project-specific configuration

All of this can be configured per project type. For example, if you never want to have `License.md` and `requirements.txt` in your Python projects, you can use the following configuration:

```json
{
    "project_config": {

        "Flask": {},

        "Python": {
            "files_to_ignore": [
                "License.md",
                "requirements.txt",
            ]
        },

        "SQLAlchemy": {}
    }
}
```

#### Partial builts

You can also create custom partial builts for a given project if you often use a specific configuration. For example,

```json
{
    "project_config": {
        "Flask": {
            "partial_builds": {
                "tmpl": [
                    "static",
                    "static/css",
                    "static/css/style.css",
                    "static/js",
                    "static/js/app.js",
                    "templates",
                    "templates/index.html"
                ]
            }
        }
    }
}
```

Note that the files must match existing template files in the project `templates` directory.

This partial build can then be used with the following command:

```
entree flask -p tmpl foo
```

where `-p` allows to specify a partial build. The argument of the `-p` option is the name of the partial build you specified in the config file (`tmpl` in this case).


## Auto-completion

Along with the config file, the following file was created during installation: `~/.config/entree_autocomplete`. This is a simple shell script that enables auto-completion for the `entree` shell script. In order to use it, place the following code inside your `.bashrc` file or equivalent:

```bash
if [ -f ~/.config/entree_autocomplete ]; then
    source ~/.config/entree_autocomplete
fi
```

## Built With

The **entree** Python package and shell script were created using

* [Jinja2](http://jinja.pocoo.org/docs/2.10/)

The online tool was created using

* [Bootstrap](http://getbootstrap.com)
* [Flask](http://flask.pocoo.org)
* [gunicorn](http://gunicorn.org)
* [Heroku](heroku.com)

## Contributing

We'd love to expand our project types to other types and programming languages. Here's how to add project types:

1. Fork the repo.

2. In the `entree/projects/templates/` directory, add a directory for your new project type (e.g. `python-django`). Inside that directory, put all files that you want to see in the output. The file structure will be identical to what you put in this directory. 

    `.py` files should be renamed to end with `_py.template` to avoid confusion when installing the package (e.g. `setup.py` should be named `setup_py.template`).

    All files will be rendered using Jinja2 (see [Jinja2 cocumentation](http://jinja.pocoo.org/docs/2.10/)). This means that you can add strings like `'{{ modname }}'` to reference the project name and `'{{ config['somevariable'] }}'` to reference a variable defined in the config file.

3. Create a new project-specific module in the `projects` directory (e.g. `entree/projects/django.py`).

4. In this file, create a class that inherits from `entree.projects.base.ProjectBase` and that optionally redefines the following class attributes: 

    - project_type (str): project type (e.g. `'django'`)

    - project_long_name (str): long name for a project (e.g. `'Django App'`)

    - template_dir (str): path to the project template directory relative to
            the template root directory (e.g. `'python-django'`)

    - single_file (str): path to a single file that you want to create in
            single-file mode relative to the template root directory

    - replace (dict, default=None): dictionary mapping template file
            names that should be replaced when creating the files. For
            example, 
            
        ```
        {
            'sometemplatefile.md': 'newname.md',
            'src': {{ modname }},
            'unittest_py.template': 'test_{{ modname }}.py'
        }
        ```

    - version (str): version number

    See existing templates for examples.

5. Test or run unit tests to make sure the right files are created.

6. Once everything is tested and works, submit a pull request.

## Versioning

Releases:

- version 2.1:

    - Created the web service
    - Added support for Python, Flask and SQLAlchemy project types

- version 2.2:

    - Replaced common file functionality by simple symlinks (treated as regular files)
    - Added support for HTML5

- version 2.3:

    - Full path and file patterns are now supported for files_to_ignore per project type

## Authors

* **Julien Spronck** - *Initial work* - [frenetic.be](http://frenetic.be)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details