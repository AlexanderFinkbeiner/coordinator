# coding=utf-8
"""Common functionality used by regression tests."""

import sys
import logging
from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QMainWindow, QDialog, QWindow
from time import sleep
from qgis._core import QgsCoordinateReferenceSystem


LOGGER = logging.getLogger('QGIS')
QGIS_APP = None  # Static variable used to hold hand to running QGIS app
CANVAS = None
PARENT = None
IFACE = None


def get_qgis_app():
    """ Start one QGIS application to test against.

    :returns: Handle to QGIS app, canvas, iface and parent. If there are any
        errors the tuple members will be returned as None.
    :rtype: (QgsApplication, CANVAS, IFACE, PARENT)

    If QGIS is already running the handle to that app will be returned.
    """

    try:
        from PyQt5 import QtGui, QtCore
        from qgis.core import QgsApplication
        from qgis.gui import QgsMapCanvas
        from .qgis_interface import QgisInterface
    except ImportError as error:
        print("Failed to import QGIS libs %s"  % error)
        return None, None, None, None

    global QGIS_APP  # pylint: disable=W0603



    
    if QGIS_APP is None:
        gui_flag = True  # All test will run qgis in gui mode
        #noinspection PyPep8Naming    
        
        try:
            sysargsUtf8 = [sysarg.encode("utf-8") for sysarg in sys.argv]
        except AttributeError:
            sysargsUtf8 = []

        QGIS_APP = QgsApplication(sysargsUtf8, gui_flag)

        # Make sure QGIS_PREFIX_PATH is set in your env if needed!
        QGIS_APP.initQgis()
        s = QGIS_APP.showSettings()
        LOGGER.debug(s)
        

    global PARENT  # pylint: disable=W0603
    if PARENT is None:
        
        #noinspection PyPep8Naming
        PARENT = QWidget()


    global CANVAS  # pylint: disable=W0603
    if CANVAS is None:
        #noinspection PyPep8Naming
        CANVAS = QgsMapCanvas(PARENT)
        CANVAS.resize(QtCore.QSize(400, 400))
        CANVAS.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))

    global IFACE  # pylint: disable=W0603
    if IFACE is None:
        # QgisInterface is a stub implementation of the QGIS plugin interface
        #noinspection PyPep8Naming
        IFACE = QgisInterface(CANVAS)
    
    return QGIS_APP, CANVAS, IFACE, PARENT
