# I will create a procedural asset generator of a low-poly tree

# Parameters include:
# - Trunk height
# - Trunk width/radius
# - Tree lean/tilt angle
# - Branch count stemming from trunk
# - Canopy number
# - Canopy shape(s)?
# - Canopy size(s)
# - Leaf scale
# - "Squash" scale

import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance

def get_maya_main_win():
    """Returns Maya Main Window"""
    main_win_address = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win_address), QtWidgets.QWidget)

class polyTreeWin(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.lowPolyTree = lowPolyTree()
        self.setWindowTitle("Low Poly Tree Generator")
        self._make_main_layout()
        self._connect_signals()
    
    def _make_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout() # Creates vertical box layout
        # self._mk_trunk_options_ui()
        # Example of how to make UI's
        self.setLayout(self.main_layout) # Directs Dialog Window to main layout

    def _make_buttons_layout(self):
        self.generate_button = QtWidgets.QPushButton("Generate") # Creates button
        self.main_layout.addWidget(self.generate_button) # Adds build button to box
        self.cancel_button = QtWidgets.QPushButton("Cancel") # Creates cancel button
        self.main_layout.addWidget(self.cancel_button)
    
    def _connect_signals(self):
        self.cancel_button.clicked.connect(self.close)
        self.generate_button.clicked.connect(self.generate_tree)

    def _make_trunk_options(self):
        self.trunk_options_layout = QtWidgets.QHBoxLayout()
        self.trunk_height_label = QtWidgets.QLabel("Trunk Height")
        self.trunk_height_dspnbx = QtWidgets.QDoubleSpinBox()
        self.trunk_height_dspnbx.setMinimumWidth(100)
        self.trunk_height_dspnbx.setValue(1.0)
        self.trunk_height_dspnbx.setSingleStep(1)
        self.trunk_options_layout.addWidget(self.trunk_height_label)
        self.trunk_options_layout.addWidget(self.trunk_height_dspnbx)
        self.main_layout.addLayout(self.trunk_options_layout)


class lowPolyTree():

    trunk_height = 3.0
    trunk_radius = 1.0
    tree_tilt = 0
    branch_count = 3.0
    canopy_shape = round
    canopy_size = 1.0
    leaf_scale = 1.0
    squash = 1.0

    def generate_trunk(self):
        obj_name = cmds.polyCylinder(height=self.trunk,
                                     radius=self.trunk_radius,
                                     name="trunk")[0]
        # Set pivot to the bottom
        cmds.xform(obj_name, pivots=[0, -self.trunk_height/2.0, 0])
        # Move trunk to floor
        cmds.xform(obj_name, translation=[0, self.trunk_height/2.0, 0])
        # Set trunk angle if specified
        cmds.xform(obj_name, rotateAxis=[self.tree_tilt, 0, 0])
        # Create branches from trunk (cones)

        return obj_name
    
    def generate_leaves(self):
        # Create a canopy on top of the trunk and every stemming branch

        # Create spheres for leaves based on inputted scale on every canopy
        # Figure out a ratio to canopy size and leaf number
        