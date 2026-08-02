"""
Comparisons Module for GEOGIS Suite.
Provides functionalities to compare shapefiles, spreadsheets, and documents.
"""

from .controller import ComparisonsController

def get_controller(context):
    return ComparisonsController(context)
