# Wizeline Flow
Language to simplify chatbot script development

**Contents**

1. [Install](#install)
1. [Hello World](#hello-world)
1. [Usage](#usage)
1. [Language Reference][lang-ref]

## Install

### Install WFC
> Note: you can install this package inside a [virtual environment][venv] too ;)

1. Go to [WFC releases](https://github.com/wizeline/wfc/releases) and download
   the most recent release

2. Install the package with pip

```sh
$ pip install /path/to/wfc-X.Y.zip
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
  "version": "2.0.0",
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

There are some command line options available

- `-o` or `--output` specifies an output path to use rather than the standard
	output
- `-q` or `--quiet` runs the compiler in quiet mode, so it won't display any
	error message
- `-v` or `--outversion` specifies the output version format, currently it
  supports script versions 2.0.0 and 2.1.0. see [output versions][out-ver] for
  details.
- `-w` or `--workdir` sets the working directory, its the fault value is the
	current work directory
- `-h` or `--help` displays help information

Examples:
```sh
$ wfc -o my-bot.json module1.flow module2.flow main.flow
```
```sh
$ wfc -v 2.1.0 module1.flow module2.flow main.flow
```

### Python Library

```python
>>> import wfc.core as wfc
>>> script = 'flow say_hi do say "Hello World!" done'
>>> print(wfc.compile_text(script))
{
  "version": "2.0.0",
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
[venv]: https://github.com/wizeline/bots-platform-docs/blob/master/tools/venv.md
[out-ver]: docs/output.md
