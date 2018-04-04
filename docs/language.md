# Language Reference
[TOC]
## Language Basics

### Comments
Flow language supports inline comments to aid in script documentation, a comment
starts with `--` and finishes at the end of the line:

Example:
```
-- This is a comment
dialog onboarding do
  say 'Hi' -- This is a comment too
done
```


### Identifiers

Identifiers are a sequence of alphanumeric symbols and the underscore (`_`).
They must start with alphabetical or underscore symbol.

Example

**Valid identifiers**
```
_name
```
```
name
```
```
this_is_an_identifier24
```

**Invalid identifiers**
```
1invalid
```
```
Hi!_
```

### Reserved Words

```
as         ask        call      change    define
define     dialog     do        done      empty
entity     equal      given     has       if
include    install    intent    intent    is
nil        not        null      reply     say
using      wait       when      with
```

### Script Sections

#### Integration install

![integration install grammar][install-grammar]

Example
```
install outlook using "outlook-configuration.json"
```

> **NOTE** Although the grammar is defined, no code is generated... yet.

#### Carousel Definition

![Carousel definition grammar][carousel-grammar]

Example
```
carousel contacts_carousel:
  set name contact_name,
  set phone contact_phone
```

For details see [carousels](#) documentation.

#### Intent and Entity Definition
![Intent and Entity definition][intent-entity-def]

Examples
```
define intent greeting "Hello", "Hi"
```
```
define entity person using "person-entity-def-file.json"
```

For details see [intents and entities](#) documentation.


#### Dialog Definition

A list of one or more dialogs see [dialog](#dialog) section for details.

### Expressions

Syntactically, an expression can be either a **string**, **number**,
**constant**, **variable**, **entity**, **intent** or a **binary operation**:

#### Strings

Text strings are arbitrary sequences of characters bounded by single or double
quotes.

Examples
```
"This is a valid string"
```
```
'This is a valid string too'
```

#### Numbers

Right now there is support for integer numbers only

#### Constants

- **empty**
- **null**
- **nil**



#### Objects

The identifiers are used to express more complex symbols like:

- **variables**: `$identifier`
- **entities**: `#identifier`
- **intents**: `@identifier`

Any of these symbols can have members:

- `$integration.method.member`
- `#entity.instance`
- `@intent.value`

#### Binary Operation
Let EXP be a **string**, **number**, **constant**, **variable**, **entity**, **intent**, then:

![Binary Operation grammar][binary-op-grammar]

## Statements
### Actions
![action grammar][action-grammar]


#### Bot Says
!['say' action grammar][say-grammar]

Examples
```
say "Hello, I am a simple bot"
```
```
say 'Hello, I am a 'sample' bot, '
    'nice to meet you'
```


#### Bot Asks
!['ask' action grammar][ask-grammar]

Examples
```
ask "What can I do you for?" as variable
```
```
ask "Do you want to continue?" as variable with:
    reply "Yes",
    reply "No"
```
```
ask  "Would your like to recive offers? as variable
with: reply "Sure!" as @yes,
      reply "Maybe later, thanks!" as @no
```


#### Bot Waits
!['wait' action grammar][wait-grammar]

Example
```
wait variable
```

#### Change Dialog
!['change dialog' action grammar][change-grammar]

```
change dialog menu
```


#### Call Function
![Call function grammar][call-function-grammar]

Example
```
call outlook.get_collaborator_by_name(name, tag)
```

#### Send Menu
![Send menu grammar][send-menu-grammar]

Example
```
TODO: Add example
```

#### Send Carousel
![Send carousel grammar][send-carousel-grammar]

Example
```
SEND_CAROUSEL: 'show' IDENTIFIER 'using' EXPRESSION 'and' 'pick' IDENTIFIER;
```
```
show contacts_carousel using $outlook.get_collaborators and pick name
```


#### Send Media
![Send media grammar][send-media-grammar]

Example
```
TODO: Add example
```
#### Open Flow
> **THIS ACTION IS NOT SUPPORTED YET**

![Open flow grammar][open-flow-grammar]

Example
```
TODO: Add example
```
### Blocks
![Block grammar][block-grammar]

Example:
```
do
  say "hi"
done
```

### Control statements
![Control statements][control-grammar]

Examples:
```
if $identity equals "The Boss":
  say "Hey, you're the boss!"
```
```
if $variable is empty: do
  ask "You did not specify a value" as variable
  say "Thank you!"
done
```
```
when @role equals "boss": say "Hey, you're the boss!"
```


### Dialog
![Dialog Grammar][dialog-grammar]

Examples:
```
dialog say_hi do
  say "Hello"
  ask "What's your name" as user_name
  say "Nice to meet you {$user_name}"
done
```
```
dialog say_hi given @greeting do
  ask "What can I help you with?" as user_response
  if $user_response equals 'show menu' change dialog menu
done
```

### Including code

It is possible to split the conversation script in several files and include
them from a _root_ script using the `%include` directive.

```
%include module
```

When a like lake the one above is find by the compiler, it will look for a file
`module.flow` in the current work directory and replace the line by the file's
contents before the compilation process starts.

[action-grammar]: img/grammar/action.svg
[ask-grammar]: img/grammar/ask.svg
[binary-op-grammar]: img/grammar/binary-operation.svg
[block-grammar]: img/grammar/block.svg
[call-function-grammar]: img/grammar/call-function.svg
[carousel-grammar]: img/grammar/carousel-definition.svg
[change-grammar]: img/grammar/change-dialog.svg
[control-grammar]: img/grammar/control.svg
[dialog-grammar]: img/grammar/dialog.svg
[install-grammar]: img/grammar/install-integration.svg
[intent-entity-def]: img/grammar/intent-entity-def.svg
[open-flow-grammar]: #
[say-grammar]: img/grammar/say.svg
[send-carousel-grammar]: img/grammar/send-carousel.svg
[send-media-grammar]: #
[send-menu-grammar]: #
[wait-grammar]: img/grammar/wait.svg
