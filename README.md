# Wizeline Flow
Language to simplify chatbot script development

**Contents**

1. [Install](#install)
1. [Hello World](#hello-world)
1. [Usage](#usage)
1. [Language Reference][lang-ref]

## Install

1. Download the package in a `.zip` archive

![Package download][wfc-zip]

2. Install the package with pip

```sh
$ pip install /path/to/wfc-development.zip
```

## Hello World

```
dialog say_hi do
  say "Hello World!"
  say "I am a simple bot"
done
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
>>> script = 'dialog say_hi do say "Hello World!" done'
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

For more details about Wizeline Flow, see the [language reference][lang-ref]

[wfc-zip]: docs/img/wfc-zip-package.png
[lang-ref]: docs/language.md
