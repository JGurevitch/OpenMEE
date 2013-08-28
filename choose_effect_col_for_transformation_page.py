from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

import ui_choose_effect_col_for_transformation_page



class ChooseEffectColForTransformationPage(QWizardPage, ui_choose_effect_col_for_transformation_page.Ui_WizardPage):
    def __init__(self, model, parent=None):
        super(ChooseEffectColForTransformationPage, self).__init__(parent)
        
        self.model = model
        self.chosen_column = None
        
        # get columns that contain effect sizes
        self.effect_size_columns = self.model.get_continuous_columns()
        effect_size_subtypes = [TRANS_EFFECT, RAW_EFFECT]
        self.effect_size_columns = [col for col in self.effect_size_columns if self.model.get_variable_assigned_to_column(col).get_subtype() in effect_size_subtypes]
        
        # populate combo box
        self._populate_combo_box(self.comboBox, self.effect_size_columns)
        
        self.current_scale_lbl.setText("None")
        self.new_scale_lbl.setText("None")
        
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"), self._update_current_selection)
        
        
    def initializePage(self):
        self.wizard().get_chosen_column = self.get_chosen_column
    
    def selected_column(self, combo_box):
        item_data = combo_box.itemData(combo_box.currentIndex())
        selected_column = item_data.toInt()[0]
        if selected_column == -1:
            return None
        return selected_column
    
    def _update_current_selection(self):
        self.chosen_column = self.selected_column(self.comboBox)
        
        var = self.model.get_variable_assigned_to_column(self.chosen_column)
        subtype = var.get_subtype()
        if subtype == TRANS_EFFECT:
            self.current_scale_lbl.setText("Transformed Scale")
            self.new_scale_lbl.setText("Raw Scale")
        elif subtype == RAW_EFFECT:
            self.current_scale_lbl.setText("Raw Scale")
            self.new_scale_lbl.setText("Transformed Scale")
        else:
            raise Exception("unrecognized subtype")

        self.completeChanged.emit()
        
    def get_chosen_column(self):
        return self.chosen_column
    
    def isComplete(self):
        if self.chosen_column is None:
            return False
        return True
        
    def _populate_combo_box(self, box, columns):
        box.blockSignals(True)
        box.clear()
        box.addItem("", QVariant(-1)) # -1 meaning no choice
        key_fn = lambda col: self.model.get_variable_assigned_to_column(col).get_label() # sort by column label
        for col in sorted(columns, key=key_fn):
            var = self.model.get_variable_assigned_to_column(col)
            box.addItem(var.get_label(), col) # store the chosen col
        box.setCurrentIndex(0)
        box.blockSignals(False)
        