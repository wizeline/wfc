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

2. Install the package with pip3, since this tool is writen using Python3

```sh
$ pip3 install /path/to/wfc-X.Y.zip
```

## Usage

### Command Line

With the snipet shown at [Hello World](#hello-world) section saved as `hellow.flow` do:

```sh
$ python -m wfc < hello.flow > hello.yaml
```

Or:

```sh
$ wfc < hello.flow > hello.yaml
```

And you'll get a new file `hello.yaml` with this contents:

```yaml
flows:
- actions:
  - id: b5db42a1-9601-4d4d-8fa2-8af3dfe3d834
    send_text:
      text: Hello World!
  - id: f87c73eb-40ca-46a6-b54d-71daa6c55b71
    send_text:
      text: I am a simple bot
  name: say_hi
version: 2.1.0
```

Or:

```sh
$ wfc -v 2.0.0 < hello.flow > hello.json
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
          "id": "2c3ab83b-a100-4bed-a68f-976c439ee945"
        },
        {
          "action": "send_text",
          "text": "I am a simple bot",
          "id": "c2666e82-e213-4b09-94eb-41ca7a47e2f5"
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
- `-V` or `--version` displays the version number

Examples:
```sh
$ wfc -o my-bot.json module1.flow module2.flow main.flow
```
```sh
$ wfc -v 2.1.0 -o my-bot.yaml module1.flow module2.flow main.flow
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
