# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/intermake/intermake/hosts/frontends/gui_qt/designer/frm_arguments_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(917, 747)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LBL_PLUGIN_NAME = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LBL_PLUGIN_NAME.sizePolicy().hasHeightForWidth())
        self.LBL_PLUGIN_NAME.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        self.LBL_PLUGIN_NAME.setFont(font)
        self.LBL_PLUGIN_NAME.setObjectName("LBL_PLUGIN_NAME")
        self.verticalLayout.addWidget(self.LBL_PLUGIN_NAME)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.GRID_ARGS_OWNER = QtWidgets.QWidget()
        self.GRID_ARGS_OWNER.setGeometry(QtCore.QRect(0, 0, 893, 652))
        self.GRID_ARGS_OWNER.setObjectName("GRID_ARGS_OWNER")
        self.GRID_ARGS = QtWidgets.QGridLayout(self.GRID_ARGS_OWNER)
        self.GRID_ARGS.setContentsMargins(0, 0, 0, 0)
        self.GRID_ARGS.setObjectName("GRID_ARGS")
        self.scrollArea.setWidget(self.GRID_ARGS_OWNER)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CHK_HELP = QtWidgets.QCheckBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CHK_HELP.sizePolicy().hasHeightForWidth())
        self.CHK_HELP.setSizePolicy(sizePolicy)
        self.CHK_HELP.setCheckable(True)
        self.CHK_HELP.setObjectName("CHK_HELP")
        self.horizontalLayout.addWidget(self.CHK_HELP)
        self.CHK_DONT_ASK_AGAIN = QtWidgets.QCheckBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CHK_DONT_ASK_AGAIN.sizePolicy().hasHeightForWidth())
        self.CHK_DONT_ASK_AGAIN.setSizePolicy(sizePolicy)
        self.CHK_DONT_ASK_AGAIN.setCheckable(True)
        self.CHK_DONT_ASK_AGAIN.setObjectName("CHK_DONT_ASK_AGAIN")
        self.horizontalLayout.addWidget(self.CHK_DONT_ASK_AGAIN)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/resource_files/app.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.LBL_PLUGIN_NAME.setText(_translate("Dialog", "TextLabel"))
        self.LBL_PLUGIN_NAME.setProperty("style", _translate("Dialog", "title"))
        self.CHK_HELP.setText(_translate("Dialog", "Help"))
        self.CHK_DONT_ASK_AGAIN.setText(_translate("Dialog", "Don\'t ask again"))
        self.pushButton.setText(_translate("Dialog", "Execute"))


