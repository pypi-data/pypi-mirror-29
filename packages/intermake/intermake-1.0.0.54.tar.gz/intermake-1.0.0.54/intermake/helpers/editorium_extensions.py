"""
Creates and registers additional GUI editors.
"""

# (defer through function so we don't have to load Qt)
from typing import Tuple


def __get_editors() -> Tuple[type, type]:
    from intermake.hosts.frontends.gui_qt.editorium_extensions import Editor_Visualisable, Editor_VisualisablePath
    return Editor_Visualisable, Editor_VisualisablePath


import editorium
editorium.register( __get_editors )