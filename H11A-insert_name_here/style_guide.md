## Repo management
### File naming

* File names should encapsulate their contents
* Naming convention: snake_case, all lower case

## Git conventions
### Branch names

* Create branches for NEW things (check if a new branch NEEDS to be made)
* Branch names describe their contents and change being made
* Conventions: kebab-case, all lowercase, suffixed by initials
* **Example:** message-send-el

### Merge requests

* {branch-name} (merge)
* Convention: kebab-case, all lowercase
* Description: dot-pointed summary of commit history

**Notes**
* Thumbs up to approve merge request
* Author of merge request may *merge* only at consensus (3 thumbs up)
* Any errors/ambiguities should be raised with discussions

### Committing

* {change-part} ({change-type}): {brief description}
* Convention: kebab-case, all lower case
* Change types: add / rm (remove) / fix / merge
* *Example:* message-send (add): completed initial implementation of sending

**Notes**
* Commit after each block of code (push not necessary)
* Small frequent commits make merge conflicts much easier to resolve

## Code conventions

* Indent size of 4, using spaces

### Variables

* Convention: snake_case, all lowercase
* *Example*: `user_btn1` not `user_btn_1`

**Dummy variables/Constants**
* Convention: snake_case, all lowercase, prefixed with underscore
* **Example:** `_CHANNEL1`

**Notes**
* Underscore separates ONLY words

### Functions

* Convention: snake_case, all lower case
* **Example:** `def function_name(arg1, arg2):`
 
**Notes**
* No space between name and args, comma then space separates args
* Should be grouped by standard functions and helper functions
* Ordered by standard functions, then helper functions

### Imports

* Importing libraries, preferably `from {lib} import {module/s}`
* Importing global structures use `import {file} as {structure}`, except error
* **Example:** `import server.data as data`
* Importing global functions use `import {file} as {function}`
* **Example:** `import server.auth as auth`

### Comments

* Use comment sense
* Convention: only single line comments (no multiline), space after hash

**Notes**
* Before block for encapsulating desc, after code for brief desc


**Example:**
```py
# comment 1
# comment 1 cont.
if case 1:
    # comment 2
elif case2:
    # comment 3
```

* Personal comment should be suffixed with name and separated by newlines

**Example:**
```py
# EL comment
# my personal notes
```

**Helper functions**
* Should be seperated from standard functions by `#####   HELPER FUNCTIONS   #####`