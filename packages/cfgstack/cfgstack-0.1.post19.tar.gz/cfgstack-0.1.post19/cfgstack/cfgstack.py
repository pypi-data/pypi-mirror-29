#! /usr/bin/env python

import copy, json, logtool, os, pprint, toml, yaml
from addict import Dict
from path import Path

DEFAULT_KEY = "_default_"
INCLUDE_KEY = "_include_"

#@logtool.log_call (log_args = False)
def _dictmerge (master, update):
  for k, v in update.items():
    if (k in master and isinstance (master[k], dict)
        and isinstance (update[k], dict)):
      _dictmerge (master[k], update[k])
    elif k not in master:
      master[k] = v

class CfgStack (object):

  """Note that dictionaries inside of lists are not expanded with
  respects to _default_ and _include_.  Only the immediate tree of
  dicts is munged.  The backing premise for this is that the purpose
  is configuration data, key value pairs, not arbitrary constructs.
  """

  # pylint: disable=too-few-public-methods

  @logtool.log_call
  def __init__ (self, fname, no_defaults = False,
                dirs = None, exts = None):
    # pylint: disable=too-many-nested-blocks,too-many-branches
    self.fname = fname
    self.dirs = [Path (d) for d in (["./"] if dirs is None else dirs)]
    self.exts = ("json", "yaml", "yml", "toml") if exts is None else exts
    self.read = self._load ()
    self.no_defaults = no_defaults
    self._do_includes ()
    if not no_defaults:
      self._do_defaults ()
    self.data = Dict (self.read)

  @logtool.log_call (log_rc = False)
  def _load (self):
    if not isinstance (self.fname, basestring):
      raise ValueError ("Name: %s is not a string" % self.fname)
    for d in self.dirs:
      for ext in self.exts:
        f = Path (d / "%s.%s" % (self.fname, ext))
        if f.isfile ():
          try:
            return json.loads (file (f).read ())
          except:
            try:
              return yaml.safe_load (file (f))
            except:
              return toml.loads (file (f).read ())
    else:
      raise IOError ("CfgStack: Cannot find/parse file for %s" % (self.fname))

  #@logtool.log_call (log_args = False, log_rc = False)
  def _do_nesting (self, d, stack):
    if isinstance (d, dict):
      for _, v in d.items ():
        if isinstance (v, dict):
          stack.append (v)

  #@logtool.log_call (log_args = False, log_rc = False)
  def _do_includes (self):
    stack = [self.read,]
    for d in stack:
      include = d.pop (INCLUDE_KEY, [])
      if isinstance (include, list):
        for f in include:
          for k, v in CfgStack (
              f, no_defaults = True).data.items ():
            if isinstance (d.get (k), dict) and isinstance (v, dict):
              _dictmerge (d[k], v)
            else:
              d[k] = v
      self._do_nesting (d, stack)

  #@logtool.log_call (log_args = False)
  def _do_defaults (self):
    stack = [self.read,]
    for d in stack:
      default = d.get (DEFAULT_KEY, {})
      if isinstance (default, dict):
        for k, v in d.items ():
          if (isinstance (v, dict) and isinstance (default, dict)
              and default != {}):
            _dictmerge (v, default)
          if isinstance (v, dict):
            stack.append (d[k])
      d.pop (DEFAULT_KEY, {})

  @logtool.log_call
  def as_yaml (self):
    return yaml.dump (self.data.to_dict (), width = 70, indent = 2,
                      default_flow_style = False)

  @logtool.log_call
  def as_json (self, indent = 2):
    return json.dumps (self.read, indent = indent)

  @logtool.log_call
  def as_pretty (self):
    return pprint.pformat (self.data.to_dict ())
