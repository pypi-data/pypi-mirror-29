
Models
######

hello
#####

*A "hello world" sample model*

This is a sample model that provides various operations for printing hello
world messages.

The message provided, either by default, by a flag, or a file (see each
operation for the applicable interface) is printed to standard output and
written to a file named `output` in the run directory.

Operations
==========

default
^^^^^^^

*Print a default message*

This operation doesn't support a user-defined message. Use the from-flag
operation with the 'message' flag to print an alternative message.

from-file
^^^^^^^^^

*Print a message from a file*

Use the 'file' flag to specify the file to print.

Flags
-----

**file**
  *File containing the message to print (default is 'msg.txt')*

from-file-output
^^^^^^^^^^^^^^^^

*Print output from last file-output operation*

This operation requires a completed file-output run.

from-flag
^^^^^^^^^

*Print a message*

Use the 'message' flag to specify the message to print.

Flags
-----

**message**
  *Message to print (default is 'Hello Guild, from a flag!')*



