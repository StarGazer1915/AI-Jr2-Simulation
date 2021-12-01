"""
========== RUN FILE ==========
This file runs the server of MESA.
The simulation will run through it.
==============================
"""

from disease_server import server
server.port = 8521
server.launch()
