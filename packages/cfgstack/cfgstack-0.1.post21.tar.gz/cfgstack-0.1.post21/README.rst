CfgStack
========

CfgStack is a configfile system reader.  System?  Yeah.  In reading
and parsing one file, CfgStack can be directed to go read other files
and to incorporate their contents into the growing dataset.

::

  CfgStack ("somefile")
  
Attempts to load the named file as JSON/YAML/TOML with default
extensions of json/yaml/yml/toml (can be over-ridden).  The loaded
object must be a dictionary.  The "data" member of the resulting
object is an addict Dict of the loaded dataset.  So far so simple.

::

  _include_:
    - file1
    - file2
  _default_:
    zero: 0
    one: 1
  foo:
    this: that
    zero: null
  var: value
  bar:
    _default_:
      inner: inside_bar
    inside: 
      oh: boy
      yep: really
  baz:
    _include_:
      - file3

A few things going on here:

- "_include_" keys are assumed to list additional data files which
  will be loaded and their contents merged with the dictionary at the
  same level.  If multiple files are listed, they will be applied in
  order from the top down.  Files are searched for in the CWD or
  optionally in a list of passed paths.

- "_default_" keys provide default key:value pairs for all
  dictionary values at the current level
  
Note that all includes are applied first, then all defaults. Higher
level values override lower level values, across both includes and
defaults (includes first) and both for contents and data-type.  
