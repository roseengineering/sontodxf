
"""
    Copyright 2015 George Magiros

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import string
import sdxf 
import math

class Sonnet():
    """
    Parses Sonnet 'son' files for polygons.  Evaluating this class as a 
    string returns those polygons as a DXF file.
    """

    def rot(self, point):
        theta = self.theta * math.pi / 180
        x = point[0] * math.cos(theta) - point[1] * math.sin(theta) 
        y = point[0] * math.sin(theta) + point[1] * math.cos(theta) 
        return (x, y)

    def npoly(self, count):
        for i in range(count):
            self.polygon()
            self.file.next()

    def geo(self):
        for line in self.file:
            token = string.split(line)
            if len(token) == 2 and token[0] == "NUM":
                self.npoly(int(token[1]))
            if len(token) == 2 and token[0] == "END" and token[1] == "GEO":
                break

    def header(self):
        for line in self.file:
            token = string.split(line)
            if len(token) == 2 and token[0] == "END" and token[1] == "HEADER":
                break

    def dim(self):
        for line in self.file:
            token = string.split(line)
            if len(token) == 2 and token[0] == "END" and token[1] == "DIM":
                break

    def control(self):
        for line in self.file:
            token = string.split(line)
            if len(token) == 2 and token[0] == "END" and token[1] == "CONTROL":
                break

    def freq(self):
        for line in self.file:
            token = string.split(line)
            if len(token) == 2 and token[0] == "END" and token[1] == "FREQ":
                break

    def opt(self):
        for line in self.file:
            token = string.split(line)
            if len(token) == 2 and token[0] == "END" and token[1] == "OPT":
                break

    def varswp(self):
        for line in self.file:
            token = string.split(line)
            if len(token) == 2 and token[0] == "END" and token[1] == "VARSWP":
                break

    def varswp(self):
        for line in self.file:
            token = string.split(line)
            if len(token) == 2 and token[0] == "END" and token[1] == "QSG":
                break

    def polygon(self):
        token = string.split(self.file.next())
        nvertices = int(token[1])
        vertex = []
        for i in range(nvertices):
            token = string.split(self.file.next())
            point = self.rot((float(token[0]), float(token[1])))
            vertex.append(point)
        self.drawing.append(sdxf.LwPolyLine(vertex))

    ###### public methods #####

    def parse(self, filename=None):
        """ 
        Parse the Sonnet file named FILENAME.  If the 
        parameter is set to None, parse the standard input
        """
        self.file = open(filename) if filename is not None else sys.stdin
        for line in self.file:
            token = string.split(line)
            if len(token) == 1:
                if token[0] == "GEO": self.geo()
                if token[0] == "HEADER": self.header()
                if token[0] == "DIM": self.dim()
                if token[0] == "FREQ": self.freq()
                if token[0] == "OPT": self.opt()
                if token[0] == "CONTROL": self.control()
                if token[0] == "VARSWP": self.varswp()
                if token[0] == "QSG": self.qsg()

    def rotate(self, theta):
        """
        Rotate all the polygon points found by THETA degrees
        """
        self.theta = theta

    def __str__(self):
        return str(self.drawing)

    def __init__(self):
        self.theta = 0
        self.drawing = sdxf.Drawing()


def usage():
    print """Usage: sontodxy.py [OPTIONS] [file ...] 

Reads the Sonnet files named on the command line, or from standard input,
exporting any polygons found to standard output in DXF format.  This DXF output 
can be imported into the Eagle PCB software using the 'import-dxf' ULP script.  

Options:
  -r, --rotate NUM:   rotate polygons by NUM degrees
  -h, --help:         show this help message

Licensed under the GPL 3.0"""
    sys.exit()


if __name__ == '__main__':
    sonnet = Sonnet()
    filename = []
    n = 1
    while n < len(sys.argv):
        arg = sys.argv[n]
        n = n + 1
        if arg == "-h" or arg == "--help":
            usage()
        if arg == "-r" or arg == "--rotate":
            if n < len(sys.argv):
                sonnet.rotate(int(sys.argv[n]))
                n = n + 1
        else:
            filename.append(arg)

    for f in filename:
        sonnet.parse(f)
    if len(filename) == 0:
        sonnet.parse()
    print str(sonnet)

