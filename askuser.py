from Qt.QtWidgets import QDialog, QVBoxLayout 
from Qt.QtWidgets import QLineEdit, QListWidget

import re

def ask_filter(options):
  options = list(options)

  dialog = QDialog()
  layout = QVBoxLayout()
  lineedit = QLineEdit()
  qlist = QListWidget()
  
  # dump the things in the thing in the thing
  layout.addWidget(lineedit)
  layout.addWidget(qlist)
  dialog.setLayout(layout)

  def update_list_values(filt = ''):
    qlist.clear()
    filtc = re.compile('.*'+'.*'.join(filt.lower())+'.*')
    matches = options if not filt else [
      option for option in options if filtc.match(
        option.lower()
      )
    ]
    qlist.addItems(matches)

  #set initial values
  update_list_values()

  # signals
  def option_select(item):
    if not item: return
    dialog.reslt = item.text()
    dialog.accept()
  qlist.itemPressed.connect(option_select)

  lineedit.textChanged.connect(update_list_values)
  lineedit.returnPressed.connect(lambda: option_select(qlist.item(0)))
  
  if dialog.exec_():
    return dialog.reslt 
