# Iteration 2 SEP Review

## Reflection
At the beginning of iteration 3, we took a step back before commencing any development or changes to reflect on our code base up until that point. We believed that the first step in improving our code would be through a retrospective evaluation, as this would allow us to identify our shortcomings and areas for change for both past code as well as considerations for future development.

At our first meeting in preparation for iteration 3, we drafted up a list of issues that we saw throughout our respective development in iterations 1 and 2. This already set up a guideline to begin plans but we next need peer-reviewed one another's code to get a fresh outlook upon the flaws within our code. We quickly noticed how effective this was, as we identified many more issues than the initial ones. This was a consequence of being "tunnel-visioned" when you become too involved with your task. At the conclusion of our review, we had a large list of issues and proposed solutions which gave us a significant starting point in bettering our *SEP*.

## Key Issues
Some notable issues that we identified from our review are listed below titled by design smells, alongside examples and proposed solutions.

### rigidity, immobility, opacity, needless repetition
**Issue:** Many of our functions were long and did not follow *SRP*, making for changes to be much harder to implement as the whole function would need to be changed.

```py
def test_message_sendlater():
    # sending later normally
    ...
    # sending message later to a channel you haven't joined
    ...
    # sending a message later over 1000 characters
    ...
    # sending later to a non-existent channel
    ...
    # sending later for a past date
    ...
```

**Solution:** Begin by abstracting where appropriate, and attempt to make each function have a *Single Responsibility* and use constants when variables are reused often to reduce *redundancy*. 

**Improvements:** *maintainability*, *understandability*.

### fragility, immobility, needless complexity, coupling
**Issue:** As frontend worked with HTTP requests, their functions always received data as strings. This caused issues with the backend which sometimes operated on other data types, particularly ids. Previously data was only converted when needed, this created problems when strings were treated as integers for example.

```py
def message_send(token, channel_id, message):
    channel_id = int(channel_id)
```

**Solution:** Have frontend handle all data conversion, assuring that backend functions are given inputs in the appropriate format. This once again follows *SRP* as backend functions should only be concerned with their primary tasks which subsequently improves their *coupling* with the frontend. 

**Improvements:** *maintainability*, *testability*.

### rigidity, needless repetition, coupling
**Issue:** Our previous method of saving data involved invoking `data.save_...()` function call within every function that modified related data. This was very *repetitive* and made it harder than necessary to *maintain* code.

```py
def channels_create(token, name, is_public):
    ...
    data.save_channels()
    return {'channel_id': channel_id}
```

**Solution:** Create decorator functions that wrap over any functions that involve data modification, allowing for better *SRP* and overall *readability* between the coupled functions.

**Improvements:** *maintainability*, *reusability*, *extensibility*.

## Plans
As outlined above, we used code smells to identify our main issues to be *rigidity*, *needless repetition*, and *coupling*. This was of no surprise to us, as we had not made any previous refactorings nor maintenance efforts towards our codebase. For iteration 3, aside from our assigned tasks, we made it of utmost importance to make a significant effort in refactoring our code to better follow *SEP*.

### Refactoring
Make changes to the problems we identified from our review, such as; abstracting where appropriate and having more extensive use of constants. Through the appropriate abstraction of code, we can better follow *SRP* which will assist in future *maintenance*, *reusability* and *extensibility*. In addition to this, increased use of constants will contribute to prior factors as well but these changes will in large reduce *opacity* and improve overall *understandability*.

### Consistency
Make constant updates to the style guide to reflect changing team requirements for the project. Notify the team when changes are made to the style guide, and constantly update oneself with style guide. Be more diligent with following the style guide, bring up with the team when ambiguities arise to reach a consensual solution. We also plan to improve our overall pylint score by conforming to their conventions appropriately, which will be discussed more in-depth next. This will help with consistency throughout the codebase and subsequently better align with *SEP* by improving *maintainability* and *understandability*.

#### Pylint
We use Pylint to identify any major issues with our code but for the most part, Pylint will point out style issues and pythonic conventions that don't agree with PEP8, the style pylint enforces. However, some of the conventions outlined by PEP8 conflict with our own style guide which everyone was both familiar and comfortable with, and to drastically change that now is relatively redundant. As a team, we did not see the need to fully commit in conforming to PEP8 as there it was not necessary to be overly pedantic as the point of style is to improve overall *understandability* and ease of *maintainability*. With that in mind, as long as the team unanimously understands and enforces our style, there would be no major issues.

As a result, while Pylint gives an indicator of our general style, we chose to follow some different standards that deviate from PEP8 which unfortunately results in a much lower Pylint score. However, we can still be assured of our *SEP* since we do have our own enforced style guide and we reflect it by filtering out appropriate PEP8 criteria:

- constant-name (C0103): We decided to separate our variables into static constants and run-time constants, where static constants would bare an uppercase styling prefixed by an underscore and run-time constants (usually testing variables) to bare no specific styling.
- missing-module-docstring (C0114): We opted to not use docstrings and stick with general comments.
- missing-function-docstring (C0116): As above, we don’t use docstrings.
- line-too-long (C0103): While it is a general practice to not have excessively long lines, we evaluated **all** violators of this and deemed that it would be unfeasible and in most cases be worse with any resolution.
- too-many-arguments (R0913): This was out of our control, as the specifications outlined it to be implemented as such
- protected-access (W0212): We are using the underscore prefix to indicate constants rather than to show protected members of a class which PEP8 assumes
- global-statement (W0603): While Pylint discourages the use of global variables, it is fine to use when done so with precaution as we have done. We decided on the use of global variables all stored in a single file for easy data manipulation.
- redefining-built-in (W0622): This was our exact intention to redefine built-in errors to better suit our project purposes.

So for our purposes we run Pylint with the command `pylint --disable=C0103,C0114,C0116,C0301,R0913,W0212,W0603,W0622`. Running this, our final pylint score was 9.99/10, losing marks on too-many-local-variables (R0914) and similar-lines (R0801).

### Coverage
Improve overall testing suites by increasing coverage, multiple (not redundant, there's a difference) tests for each case. We started off with a very simple goal by setting a minimum 95% threshold coverage for every member to first reach. Alongside the standard tests, we plan to develop volume and stress tests by having multiple tests for each case and test as many edge cases as possible respectively. Overall, this will most definitely improve *testability* as well as assisting with future *maintenance*.

# Iteration 3 SEP Changes
With the conclusion of iteration 3, we will discuss the notable changes we have made throughout the iteration as it would be irrational and unfeasible to cover every change. The following changes are titled by subject and include an outline, code example, and discussion on *SEP* covered.

### Wildcard Imports
**Outline:** The first task on our agenda was to update our import style, previously we used `from {file} import *` which was both bad practice and *opaque*. We updated our entire codebase to the new convention of importing each module as a descriptor, `import {file} as {descriptor}` and subsequent uses would be `{descriptor}.{function}`.

```py
import auth as auth
auth.auth_register(email, password, name_first, name_last)
```

**Discussion:** This greatly reduced the *fragility* of our code, as unnecessary imports were not made and conflicts that occurred when multiple functions/data shared common names were negated. As a consequence, *maintainability* and *reusability* were improved, however, it did have the consequence of bringing *needless repetition* and reducing *readability* when using module functions, which will be discussed next.

### Function Names
**Outline:** This arose as a consequence of changing our import style where there would be redundancy when using module data and functions. We planned to solve this *needless repetition* and *opacity* by doing a mass refactor of all our code to rename data and functions where appropriate. So instead of `def {module}_{function}`, we would use `def {function}` instead.

```py
# auth.py file
def register(...):

# XXX.py file
import auth as auth
auth.register(...)
```

**Discussion:** Prior to this change, our code was very *opaque* but introducing the new implementations improved overall *clarity* and *understandability* which subsequently reduced the initial issues surrounding *opacity* and *needless repetition*. However, these changes also inadvertently improved *testability* and *maintainability* as test suites can make better and more extensive use of module functions as well as having much more *readable* code.

### File Management
**Outline:** Previously, our standup and search function were under the "miscellaneous" module which came with its own whole set of issues involving *coupling* between message and standup which were dependent on one another. This was because standup was invoked by message send and upon conclusion, standup would send a message. Due to this interdependency, we encountered issues with circular imports. Our initial solution involved moving all the miscellaneous functions into the message module. However, this went slightly against our modular approach as it didn't exactly align with message functionality. When it was found that standup did not need to invoked by message, we abstracted standup functions into their own "standup" module which much better aligned with *SEP* as well as our conventions.

```py
# standup.py
import message as message
def start(...):
    ...
    send_messages(standup_messages)
def send_messages(...):
    ...
    message.send(...)
```

**Discussion:** Making this change clearly outlined the design smell of *coupling*, as multiple issues arose from the interdependence between components. However, resolving this had a profound impact, as it not only directly improved *maintainability* and *reusability* through abstraction but it also led us to realise the importance of *SEP*. The problems that this particular issue gave rise to were arguably the most difficult ones (circular imports), so we experienced the consequences of poor *SEP*.

## Conclusion
As there weren't many new components to implement in iteration 3, it was clear that it's main focus was on *SEP* and to improve the project's overall quality through extensive refactoring while keeping *SEP* in mind. Throughout our experience with iteration 3, we came to realise the many flaws that existed with not only our codebase but also our development style. Being able to rethink and change accordingly led us to understand the importance of having good *SEP* as we were able to have the first-hand experience with consequences that poor *SEP* yields.

Making our changes accordingly really elucidated how much impact *SEP* had on our project as we saw the exponential development progress with each *SEP* improvement. We believe that iteration 3 was very informative as it taught us about not only the repercussions of poor *SEP* but also the benefits of good *SEP* and general practices.
