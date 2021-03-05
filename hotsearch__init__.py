from .askuser import ask_filter
import nuke
from itertools import chain
import yaml

rankings_file = "/home/kshepherd/.nuke/hotrankings.yaml"

def rank_sort(seq):
  with open(rankings_file) as fil:
    rankdata = yaml.safe_load(fil) or {}
  return sorted(seq, key=lambda x: (-rankdata.get(x, 0), x))

def incr_rank(option):
  """ Increment ranking of given option, each record decays the other rankings for that class"""
  with open(rankings_file) as fil:
    rankdata = yaml.safe_load(fil) or {}
  rankdata = {k:v*0.95 for k,v in rankdata.items() if v>0.1} # decay
  rankdata[option] = rankdata.get(option, 0)+1
  with open(rankings_file, 'w') as fil:
    yaml.safe_dump(rankdata, fil)

def pnam(knob):
  print knob.name()

def fmt_opt(knob, opt):
  return "({}) {} -> {}".format(knob.node().Class(), knob.name(), opt)

def get_searchable_options(node):
  for knob in node.knobs().values():
    if type(knob) is nuke.Link_Knob:
      knob = knob.getLinkedKnob()
    if type(knob) is nuke.Format_Knob:
      for opt in map(nuke.Format.name, nuke.formats()):
          yield fmt_opt(knob, opt), lambda k=knob, o=opt: k.setValue(o)
    if type(knob) in (nuke.PyScript_Knob, nuke.Script_Knob): 
      yield fmt_opt(knob, 'PUSH'), lambda k=knob: k.execute()
    if type(knob) in (nuke.Channel_Knob, nuke.ChannelMask_Knob): #layers
      for opt in nuke.layers(node) if 'in' in knob.name() else nuke.layers():
        yield fmt_opt(knob, opt), lambda k=knob, o=opt: k.setValue(o)
    if type(knob) in (nuke.Boolean_Knob, nuke.Disable_Knob):
      yield fmt_opt(knob, 'ON'), lambda k=knob: k.setValue(True)
      yield fmt_opt(knob, 'OFF'), lambda k=knob: k.setValue(False)
    if type(knob) is nuke.Enumeration_Knob:
      for opt in knob.values():
        yield fmt_opt(knob, opt), lambda k=knob, o=opt: k.setValue(o)
  #for preset in getAllUserPresets():

def change_node():
  nodes = nuke.selectedNodes()

  options = dict()
  for opt_name, func in chain(*map(get_searchable_options, nodes)):
    options.setdefault(opt_name, []).append(func)

  selected_option = ask_filter(rank_sort(options))
  if selected_option in options:
    incr_rank(selected_option)
    for func in options[selected_option]:
      func()
  


nuke.menu('Nuke').addCommand('HotSearch', change_node, shortcut='E')


