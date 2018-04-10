# Wizeline Flow
Language to simplify chatbot script development

**Contents**

1. [Install](#install)
1. [Hello World](#hello-world)
1. [Usage](#usage)
1. [Language Reference][lang-ref]

## Install

### Create a virtual envirionment

You can use a virtual envrironment to install the package without having
super user privileges:

**Create a virtual environment using venv module**
```sh
$ python3 -m venv ~/.venvs/wfc-testing
```
**Activate the virtual environment**
```
$ source ~/.venvs/wfc-testing/bin/activate
```
**Upgrade the python package manager**
```
$ pip install --upgrade pip
```

### Install WFC
1. Download the package in a `.zip` archive

![Package download][wfc-zip]

2. Install the package with pip

```sh
$ pip install /path/to/wfc-development.zip
```

## Usage

### Command Line

With the snipet shown at [Hello World](#hello-world) section saved as `hellow.flow` do:

```sh
$ python -m wfc < hello.flow > hello.json
```

Or:

```sh
$ wfc < hello.flow > hello.json
```

And you'll get a new file `hello.json` with this contents:

```javascript
{
  "version": "1.0.0",
  "intentions": [],
  "entities": [],
  "dialogs": [
    {
      "name": "say_hi",
      "actions": [
        {
          "action": "send_text",
          "text": "Hello World!",
          "id": "2bc394e5-cf6e-465a-aa70-44bff7b33546"
        },
        {
          "action": "send_text",
          "text": "I am a simple bot",
          "id": "70cacd6e-090c-40ef-ba64-6ec4f61ae811"
        }
      ]
    }
  ],
  "qa": []
}
```

### Python Library

```python
>>> import wfc.core as wfc
>>> script = 'flow say_hi do say "Hello World!" done'
>>> print(wfc.compile_string(script))
{
  "version": "1.0.0",
  "intentions": [],
  "entities": [],
  "dialogs": [
    {
      "name": "say_hi",
      "actions": [
        {
          "action": "send_text",
          "text": "Hello World!",
          "id": "8cfa6bc1-868f-4f7c-a90c-4ddb91e8f5cf"
        }
      ]
    }
  ],
  "qa": []
}
>>>
```

## Hello World

```
flow say_hi do
  say "Hello World!"
  say "I am a simple bot"
done
```

For more details about Wizeline Flow, see the [language reference][lang-ref]

[wfc-zip]: docs/img/wfc-zip-package.png
[lang-ref]: docs/language.md
