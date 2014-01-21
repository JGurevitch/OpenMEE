##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

import copy
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *


import ui_preferences
from ome_globals import *
#from ee_model import EETableModel

class PreferencesDialog(QDialog, ui_preferences.Ui_Dialog):
    def __init__(self,
                 get_init_params_fn,
                 reset_user_prefs_fn,
                 parent=None):
        super(PreferencesDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.get_init_params_fn = get_init_params_fn
        self.reset_user_prefs_fn = reset_user_prefs_fn
        
        init_params = get_init_params_fn()
        self.initializeDialog(init_params)

        
        
        self.color_buttons()
        # Connect buttons to color pickers
        
        buttons = [self.label_bg, self.label_fg,
                   self.cont_bg, self.cont_fg,
                   self.cat_bg, self.cat_fg,
                   self.count_bg, self.count_fg,
                   self.calc_bg, self.calc_fg,
                   self.default_bg]
        
        
        
        for btn in buttons:
            btn.clicked.connect(partial(self.get_new_color,btn))
        self.choose_font_btn.clicked.connect(self.set_font)
        self.reset_pushButton.clicked.connect(self._reset_everything)
        
    def initializeDialog(self, init_params):
        self.color_scheme = copy.deepcopy(init_params['color_scheme'])
        self.digits_spinBox.setValue(init_params['precision'])
        self.additional_values_checkBox.setChecked(init_params['show_additional_values'])
        self.analysis_selections_checkBox.setChecked(init_params['show_analysis_selections'])
        self.set_font(init_params['font_str'])
        
    def showEvent(self, show_event):
        QDialog.showEvent(self, show_event)
        
    def _reset_everything(self):
        choice = QMessageBox.warning(self, "Reset Preferences", "Are you sure you want to reset all the user preferences?", buttons=QMessageBox.Yes|QMessageBox.Cancel)

        if choice == QMessageBox.Yes:
            print("reseting everyfrom from prefereces dlg")
            self.reset_user_prefs_fn() # in main_form
            self.initializeDialog(init_params = self.get_init_params_fn())
        
    def get_new_color(self, btn):
        ''' Pops up a dialog to get the new color for the btn, then sets
        the color in the color scheme '''
        
        old_color = self.get_btn_color(btn)
        color = QtGui.QColorDialog.getColor(old_color, self)
        if color.isValid():
            # set new color
            self.set_color_for_btn(btn, color)
            
    def set_font(self, font=None):
        if font:
            ok=True
        else:
            font, ok = QFontDialog.getFont(QFont(self.font_preview_lbl.text()), self)
        if ok:
            print("Font family: '%s'" % str(font.family()))
            self.font_preview_lbl.setText(font.family())
            self.font_preview_lbl.setFont(font)
            self.font = font
            
    def get_btn_color(self, btn):
        if btn == self.label_bg:
            color = self.color_scheme['label'][BACKGROUND]
        elif btn == self.label_fg:
            color = self.color_scheme['label'][FOREGROUND]
        elif btn == self.cont_bg:
            color = self.color_scheme['variable'][CONTINUOUS][BACKGROUND]
        elif btn == self.cont_fg:
            color = self.color_scheme['variable'][CONTINUOUS][FOREGROUND]
        elif btn == self.cat_bg:
            color = self.color_scheme['variable'][CATEGORICAL][BACKGROUND]                                                      
        elif btn == self.cat_fg:
            color = self.color_scheme['variable'][CATEGORICAL][FOREGROUND]
        elif btn == self.count_bg:
            color = self.color_scheme['variable'][COUNT][BACKGROUND]
        elif btn == self.count_fg:
            color = self.color_scheme['variable'][COUNT][FOREGROUND]
        elif btn == self.calc_bg:
            color = self.color_scheme['variable_subtype']['DEFAULT_EFFECT'][BACKGROUND]
        elif btn == self.calc_fg:
            color = self.color_scheme['variable_subtype']['DEFAULT_EFFECT'][FOREGROUND]
        elif btn == self.default_bg:
            color = self.color_scheme['DEFAULT_BACKGROUND_COLOR']
        return color
    
    def set_color_for_btn(self, btn, color):
        if btn == self.label_bg:
            self.color_scheme['label'][BACKGROUND] = color
        elif btn == self.label_fg:
            self.color_scheme['label'][FOREGROUND] = color
        elif btn == self.cont_bg:
            self.color_scheme['variable'][CONTINUOUS][BACKGROUND] = color
        elif btn == self.cont_fg:
            self.color_scheme['variable'][CONTINUOUS][FOREGROUND] = color
        elif btn == self.cat_bg:
            self.color_scheme['variable'][CATEGORICAL][BACKGROUND] = color                                                   
        elif btn == self.cat_fg:
            self.color_scheme['variable'][CATEGORICAL][FOREGROUND] = color
        elif btn == self.count_bg:
            self.color_scheme['variable'][COUNT][BACKGROUND] = color
        elif btn == self.count_fg:
            self.color_scheme['variable'][COUNT][FOREGROUND] = color
        elif btn == self.calc_bg:
            self.color_scheme['variable_subtype']['DEFAULT_EFFECT'][BACKGROUND] = color
        elif btn == self.calc_fg:
            self.color_scheme['variable_subtype']['DEFAULT_EFFECT'][FOREGROUND] = color
        elif btn == self.default_bg:
            self.color_scheme['DEFAULT_BACKGROUND_COLOR'] = color
        
        # Actually apply the color change
        self.color_buttons()
        
    
    def color_buttons(self):
        ''' Colors the buttons with colors from the color scheme '''
        
        # Note: probably should replace all the self.color_scheme stuff with self.get_btn_color(btn). Too lazy now
        
        self.label_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['label'][BACKGROUND]))
        self.label_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['label'][FOREGROUND]))
        
        self.cont_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][CONTINUOUS][BACKGROUND]))
        self.cont_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][CONTINUOUS][FOREGROUND]))
        
        self.cat_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][CATEGORICAL][BACKGROUND]))
        self.cat_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][CATEGORICAL][FOREGROUND]))
        
        self.count_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][COUNT][BACKGROUND]))
        self.count_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable'][COUNT][FOREGROUND]))
        
        self.calc_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable_subtype']['DEFAULT_EFFECT'][BACKGROUND]))
        self.calc_fg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['variable_subtype']['DEFAULT_EFFECT'][FOREGROUND]))
        
        self.default_bg.setStyleSheet("background-color: %s;" % self._get_rgb_for_stylesheet(self.color_scheme['DEFAULT_BACKGROUND_COLOR']))
        
        if DEBUG_MODE:
            print("Set colors of buttons")
        
    def _get_rgb_for_stylesheet(self, color):
        r,g,b, alpha = color.getRgb()
        rgb_string = 'rgb(%d, %d, %d)' % (r,g,b) # stylesheet syntax
        return rgb_string
    
    def get_color_scheme(self):
        return self.color_scheme
    
    def get_precision(self):
        return self.digits_spinBox.value()
    
    def get_font(self):
        return self.font
    
    def get_show_additional_values(self):
        return self.additional_values_checkBox.isChecked()
    
    def get_show_analysis_selections(self):
        return self.analysis_selections_checkBox.isChecked()

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    form = PreferencesDialog(color_scheme=DEFAULT_COLOR_SCHEME)
    form.show()
    sys.exit(app.exec_())