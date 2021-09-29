## assumptions

**data_assumptions**

Assuming the AccessError is a custom Exception already made (since it is not a standard Python Exception)

Assume that user data is stored in dictionaries in the code. (for now)

Assume that react information is contained in a database corresponding to messages (dictionary works for now)

Assume pinned messages for each channels are stored (dictionary works for now)

Assume that a reset code must be exactly 6 numbers.

Assume that channel IDs must be exactly 5 digits.

Assume that members will be referenced by u_id

Assume that is_public is determined by boolean operators “True” and “False”.

**misc_assumptions**

Assuming that the functions will raise errors (and tests can be made to verify these errors were raise when necessary)

Assuming that if a function has multiple conditions to throw an exception, each one is checked one at a time and the first condition that fails is used to identify the error. Other errors aren’t checked for once, a condition has failed.

Assume deltatime will be used for time control 

**auth_assumptions**

Assume that a token is unique not just to a user, but to a user’s particular login session

Assume that registering also results in logging in with the newly registered credentials

Assumptions of a valid email address:
* Has the structure of personal_info@domain_name.domain_extension (2 ascii strings separated by an @ symbol)
* personal_info can have alphanumeric (A-Z, a-z, 0-9) or underscores (_) in any order (and must have at least one of them). It can also have periods (.) or dashes (-) but can  not be consecutive and they can only be in between alphanumeric or underscore characters.
* Can only have 1 @ symbol between the personal_info and domain name
* The domain name has the same restrictions as personal_info (a valid example is “google)
* The domain extension is consisted of blocks that are each made up of a period (.) followed by 2 or 3 alphanumeric or underscore characters (such as .com or .au).
* There can be many of these blocks in the domain extension (example: .edu.au)


**channel_assumptions**

Assume that private channels are not visible to the public when listing channels.

Assume that all returned details of list channel functions are limited to the channel ID and the name of the channel.

Assume there will be a function that will check if the message is sent

**message_assumptions**

Assume that there is a checker for image URLs

Assume there is a function that return messages in a channel

Assume there is a function that return owners of a channel