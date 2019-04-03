## PDV is a 1D graphics and data analysis tool, heavily based on the ULTRA plotting tool.

To use it, download the source, and run with Python.  You need pyside or pyqt4, matplotlib and numpy installed.

### PyDV Importable Interface Module ###
You can now call most of PyDV's functionality from within a Python script. Below is an example of how to do this.
        
        import sys
        sys.path.append("/usr/gapps/pydv/2.0")
        import pydvpy as pydvif

        curves = list()
        curves.appedn(pydvif.span(1,10,6))
        pydvif.save('myFile.txt', curves)

## License

PyDV is distributed under the terms of the [BSD-3 License](LICENSE)

All new contributions must be made under the [BSD-3 License](LICENSE)

See [LICENSE](LICENSE) for details.

LLNL-CODE-507071
