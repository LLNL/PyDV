# Copyright (c) 2011-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by Mason Kwiat, Douglas S. Miller, and Kevin Griffin
# e-mail: dougmiller@llnl.gov or griffin28@llnl.gov
# LLNL-CODE-507071
# All rights reserved.

# This file is part of PDV.  For details, see <URL describing code and
# how to download source>. Please also read "Additional BSD Notice".

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the disclaimer below.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the disclaimer (as noted below)
# in the documentation and/or other materials provided with the
# distribution.  Neither the name of the LLNS/LLNL nor the names of
# its contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL LAWRENCE
# LIVERMORE NATIONAL SECURITY, LLC, THE U.S. DEPARTMENT OF ENERGY OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# Additional BSD Notice

# 1. This notice is required to be provided under our contract with
# the U.S.  Department of Energy (DOE).  This work was produced at
# Lawrence Livermore National Laboratory under Contract
# No. DE-AC52-07NA27344 with the DOE.

# 2. Neither the United States Government nor Lawrence Livermore
# National Security, LLC nor any of their employees, makes any
# warranty, express or implied, or assumes any liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents
# that its use would not infringe privately-owned rights.

# 3.  Also, reference herein to any specific commercial products,
# process, or services by trade name, trademark, manufacturer or
# otherwise does not necessarily constitute or imply its endorsement,
# recommendation, or favoring by the United States Government or
# Lawrence Livermore National Security, LLC.  The views and opinions
# of authors expressed herein do not necessarily state or reflect
# those of the United States Government or Lawrence Livermore National
# Security, LLC, and shall not be used for advertising or product
# endorsement purposes.

import sys
sys.path.append("../")
import os
import os.path

import unittest
import pydvpy as pydvif

class Test_PYPDVPY(unittest.TestCase):
    def setUp(self):
        self.x = [1, 2, 3, 4]
        self.y = [5, 6, 7, 8]
        self.plotfname = 'myPlot'
        self.ftype = 'png'
        self.fullfname = self.plotfname + '.' + self.ftype

    def tearDown(self):
        self.x = None
        self.y = None

    def test_span(self):
        c = pydvif.span(1, 10, 10)
        self.assertEqual(10, len(c.x))

    def test_makecurve(self):
        c = pydvif.makecurve(self.x, self.y, 'Line', 'myfile')
        self.assertEqual(c.name, 'Line')
        self.assertEqual(c.filename, 'myfile')
        self.assertEqual(len(c.x), 4)
        self.assertEqual(len(c.y), 4)

    def test_create_plot(self):
        self.assertTrue(True)
        # curves = pydvif.read('testData.txt')
        # pydvif.create_plot(curves, fname=self.plotfname, ftype=self.ftype, title='My Title',
        #                    xlabel='X', ylabel='Y', legend=True, stylename='ggplot', xls=True, yls=True)
        # self.assertTrue(os.path.isfile(self.fullfname))
        # os.remove(self.fullfname)


    def test_save(self):
        c = pydvif.makecurve(self.x, self.y, 'Line', 'myfile')
        pydvif.save('mysave.txt', c)
        self.assertTrue(os.path.isfile('mysave.txt'))
        os.remove('mysave.txt')

    def test_savecsv(self):
        c = pydvif.makecurve(self.x, self.y, 'Line', 'myfile')
        pydvif.savecsv('mysave.csv', c)
        self.assertTrue(os.path.isfile('mysave.csv'))
        os.remove('mysave.csv')

    def test_read(self):
        curves = pydvif.read('testData.txt')
        self.assertEqual(len(curves), 2)
        self.assertEqual(curves[0].name, 'darkness')
        self.assertEqual(curves[1].name, 'lightness')

    def test_readcsv(self):
        curves = pydvif.readcsv('testData.csv')
        self.assertEqual(len(curves), 1)
        self.assertEqual(len(curves[0].x), 5)


if __name__ == '__main__':
    unittest.main()
