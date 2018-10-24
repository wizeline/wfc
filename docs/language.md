# Language Reference
[TOC]
## Language Basics

### Comments
Flow language supports inline comments to aid in script documentation, a comment
starts with `--` and finishes at the end of the line:

Example:
```
-- This is a comment
flow onboarding do
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
as       ask     call   change
define   do      done   empty
end      entity  equal  flow
given    has     if     include
install  intent  is     nil
not      null    open   read
reply    say     using  var
wait     when    with
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

A carousel definition represents the relationship between a set of object member names
with the slots of a carousel card set to the card content slots of a carousel

The valid slots in a carousel card are:

- _title_ (mandatory)
- _description_ (optional)
- _image\_url_ (optional)
- _buttons_ (optional, two or three buttons)

Dynamic Carousel Example
```
carousel contacts_carousel:
  set title contact_name,
  set description contact_phone,
  set image_url contact_avatar
end
```
Static Carousel Example
```
carousel options_carousel:
  card:
    set title 'Option 1',
    set description 'contact_phone',
    set image_url 'http://example-bucket.com/images/contact_avatar.jpg'
    button postback('Label', action:'action-text', id:'option-id'),
    button url('My Web Site', 'http://example.com')
end
```
Dynamic Carousel Example (with buttons)
```
carousel contacts_carousel:
  set title contact_name,
  set description contact_phone,
  set image_url contact_avatar
  button postback('Label', 'postback message'),
  button message('Say Hi', 'Hi')
end
```

#### Menu Definition

![Menu definition][menu-grammar]

Menus are lists of buttons indentified by a name. Once they're defined you can
use them later.

```
menu mainOptions:
  button message('Option One'),
  button postback('Option Two', 'clicked the second button'),
  button url('External Option', 'http://example.com/document.txt')
end
```

#### Intent and Entity Definition
![Intent and Entity definition][intent-entity-def]

Examples
```
define intent greeting "Hello", "Hi"
```
```
define entity person using "person-entity-def-file.json"
```

For details see [intents and entities][intents] documentation.

#### Command Definition

![commands grammar][commands-grammar]

The commands feature helps you to bypass the NLP and jump to any flow you want.

Examples
```
when read "/hi" do say_hi_flow

flow say_hi_flow do
  say "Hello World"
done
```

#### Flow Definition

A list of one or more dialogs see [flow](#flow) section for details.

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
- **entities**: `@identifier`
- **intents**: `#identifier`

Any of these symbols can have members:

- `$integration.method.member`
- `@entity.instance`
- `#intent.value`

#### Binary Operation
Let EXP be a **string**, **number**, **constant**, **variable**, **entity**, **intent**, then:

![Binary operation][expression-grammar]
![Operator][operator-grammar]

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
!['ask' action grammar][ask-grammar] <!-- TODO: update the grammar chart -->

Examples
```
ask "What can I do you for?" as variable
```
```
ask "What can I do you for?" as variable keeping context
```
```
ask "Do you want to continue?" as variable with:
    reply "Yes",
    reply "No"
```
```
ask "Would your like to recive offers? as variable with:
  reply "Sure!" as @yes,
  reply "Maybe later, thanks!" as @no
  fallback "I will ask you later"
```
```
ask "Would your like to recive offers? as variable with:
  reply @yes,
  reply @no
  fallback "I will ask you later"
```


#### Bot Waits
!['wait' action grammar][wait-grammar]

Example
```
wait variable
```

#### Set Variable

!['set variable' action grammar][var-grammar]

You can store values in custom variables. This operation supports basic
arithmetic and storing objects

Examples
```
var botNmae = 'Robotina'
```
```
var millenniumStartedOn = 2000
```
```
var year = 1955
var backToTheFuture = $year + 30
```
```
var persona = name: 'Max Power',
              age: 36
```
```
var nothing = empty
```
```
var none = nil
```

#### Change Flow
!['change flow' action grammar][change-grammar]

```
change flow menu
```


#### Open Flow
!['open flow' action grammar][open-grammar]

```
open flow menuFlow
```


#### Call Function
![Call function grammar][call-function-grammar]

Example
```
call outlook.get_collaborator_by_name(name, tag)
```

#### Show Components

![Show component grammar][show-component-grammar]
```
SHOW_COMPONENT: 'show' IDENTIFIER ['using' EXPRESSION]? ;
```

The supported components are carousels and menus. The `using EXPRESION` syntax
is valid for carousels only.

Examples
```
show contacts_carousel using $outlook.get_collaborators and pick name
```
```
show onboarding_options -- This is a menu
```

#### Open Flow

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
if $variable is empty
  ask "You did not specify a value" as variable
  say "Thank you!"
end
```

```
if $variable is empty:
  ask "You did not specify a value" as variable
else:
  say "The variable is {{$variable}}"
```

```
if $variable is empty
  say 'You did not enter the variable'
  ask 'Please enter a value' as variable
else:
  say "The variable is {{$variable}}"
```

```
if $variable is empty
  say 'You did not enter the variable'
  ask 'Please enter a value' as variable
else:
  say "The variable is {{$variable}}"
  say 'Thank you!'
end
```

### Flow
![Flow Grammar][flow-grammar]

Examples:
```
flow say_hi do
  say "Hello"
  ask "What's your name" as user_name
  say "Nice to meet you {{$user_name}}"
done
```
```
flow say_hi given #greeting do
  ask "What can I help you with?" as user_response
  if $user_response equals 'show menu' change dialog menu
done
```
```
fallback flow say_hi do
  say "Sorry, what did you mean?"
  say "These are the things I can help you with:"
  show stuff
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
[block-grammar]: img/grammar/block.svg
[call-function-grammar]: img/grammar/call-function.svg
[carousel-grammar]: img/grammar/carousel-definition.svg
[change-grammar]: img/grammar/change-flow.svg
[commands-grammar]: img/grammar/commands.svg
[control-grammar]: img/grammar/control.svg
[expression-grammar]: img/grammar/expression.svg
[flow-grammar]: img/grammar/flow.svg
[install-grammar]: img/grammar/install-integration.svg
[intent-entity-def]: img/grammar/intent-entity-def.svg
[intents]: #
[menu-grammar]: img/grammar/menu-definition.svg
[open-grammar]: img/grammar/open.svg
[operator-grammar]: img/grammar/operator.svg
[say-grammar]: img/grammar/say.svg
[show-component-grammar]: img/grammar/show-component.svg
[var-grammar]: img/grammar/var.svg
[wait-grammar]: img/grammar/wait.svg
