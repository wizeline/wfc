# Wizeline Flow
Language to simplify chatbot script development

**Contents**

1. [Install](#install)
1. [Usage](#usage)
1. [Language Reference][lang-ref]
1. [Hello World](#hello-world)

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

With the snipet shown at [Hello World](#hello-world) section do:

```sh
$ python -m wfc < hello.flow > hello.yaml
```

Or:

```sh
$ wfc < hello.flow > hello.json
```

And you'll get a new file `hello.json` with this contents:

```javascript
{
  "version": "2.1.0",
  "flows": [
    {
      "name": "helloWorld",
      "actions": [
        {
          "send_text": {
            "text": "Hello World, I am a Bot!"
          },
          "id": "15f644f7-69da-4278-91ab-f7284c9b93a7"
        }
      ]
    }
  ]
}
```

Or:

```sh
$ wfc -v 2.2.0 < hello.flow > hello.json
```

And you'll get a new file `hello.json` with this contents:

```javascript
{
  "version": "2.2.0",
  "flows": [
    {
      "name": "helloWorld",
      "actions": [
        {
          "send_text": {
            "text": "Hello World, I am a Bot!"
          },
          "id": "324e027c-7beb-42eb-b2ab-6f27c0ff757a"
        }
      ]
    }
  ]
}
```

There are some command line options available

- `-o` or `--output` specifies an output path to use rather than the standard
	output
- `-q` or `--quiet` runs the compiler in quiet mode, so it won't display any
	error message
- `-v` or `--outversion` specifies the output version format, currently it
  supports script versions 2.1.0 and 2.2.0. see [output versions][out-ver] for
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
$ wfc -v 2.2.0 -o my-bot.json module1.flow module2.flow main.flow
```

## Hello World

```
flow helloWorld do
  say 'Hello World, I am a Bot!'
done
```

For more details about Wizeline Flow, see the [language reference][lang-ref]

[wfc-zip]: docs/img/wfc-zip-package.png
[lang-ref]: docs/language.md
[venv]: https://github.com/wizeline/bots-platform-docs/blob/master/tools/venv.md
[out-ver]: docs/output.md
