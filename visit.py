import re
import math


class reader:
    def __init__(self):
        pass

    def read_csv(self):
        pass

    def read_sel(self, filename):
        self.filename = filename
        file = open(self.filename)
        self.values = file.read().split("\n")
        self.data = []

        for key in self.values:
            self.value = re.findall(r"[-+]?\d*\.\d+|\d+", key)

            if len(self.value) == 5:
                self.value[3] = (10 ** float(self.value[4])) * float(self.value[3])
                del self.value[4]
                # print(self.value)
            if self.value != []:
                self.data.append(self.value)
        # print(self.data)
        return self.data

    def _read_cart(self, filename):
        self.filename = filename
        file = open(self.filename)
        self.values = file.read().split("\n")
        self.data = []

        for key in self.values:
            self.value = re.findall(r"[-+]?\d*\.\d+|\d+", key)

            if self.value != []:
                self.data.append(self.value)

        return self.data


class plot:
    def __init__(self, data):
        self.data = data  # [col-1::18]
        # self.index=0
        self.data_cart = []
        # self.data_cart=[]
        # self.size=size
        # self.column=column

    def _hex_cornerX(self, centerX, i):
        self.centerX = centerX
        self.i = i
        self.angle_deg = 60 * i + 30
        self.angle_rad = math.pi / 180 * self.angle_deg
        return self.centerX + self.size * math.cos(self.angle_rad)

    def _get_max_num(self, i):
        self.max = 0
        self.i = i
        for index in range((len(self.data))):
            while self.max < int(self.data[index][i]):
                self.max = int(self.data[index][i])
        return self.max

    def _read_cart(self):
        self.readcart = reader()
        self.data_cart = self.readcart._read_cart("./Cart.txt")

    def _check_mask(self, maskPos):
        for i in range(round(len(self.data_cart) / 6)):
            for item in self.data_cart[i]:
                if int(item) == maskPos:
                    return True
        return False

    def _num_of_cells(self):
        self.max_Mask = 0
        for i in range(round(len(self.data_cart) / 6)):
            for item in self.data_cart[i]:
                if self.max_Mask < int(item):
                    self.max_Mask = int(item)
        return self.max_Mask

    def _hex_cornerY(self, centerY, i):
        self.centerY = centerY
        self.i = i
        self.angle_deg = 60 * i + 30
        self.angle_rad = math.pi / 180 * self.angle_deg
        return self.centerY + self.size * math.sin(self.angle_rad)

    def _column(self, matrix, i):
        return [float(row[i]) for row in matrix]

    def _rings(self, matrix):
        self.matrix = matrix
        return (1 + (1 + 4 * ((self.matrix) - 1) / 3) ** (1 / 2)) / 2

    def plt2d_2(self, size, col):
        self._read_cart()

        self.size = size
        self.data = self.data[col - 1::self._get_max_num(0)]
        self.points = self._column(self.data, -1)  # 2+self.index)
        # print(self.points)
        self.num = self._num_of_cells() + 1
        # print(self.num)
        self.r = math.ceil(self._rings(self.num))
        # print(self.r)

        self.stepX = self.size / 2 * math.cos(math.pi / 3)
        self.stepY = self.size / 2 * math.sin(math.pi / 3)
        self.centerX = 0
        self.centerY = 0
        self.shiftY = 0
        self.shiftX = 0

        self.ring = 0
        self.width = self.size * 2
        self.vert = self.width * 3 / 4
        self.height = self.width ** (3 / 2)
        self.k = 0
        self.MaskPos = 0
        with open('2d.vtk', 'w', encoding='utf-8') as f:
            f.write("# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\nPOINTS " + str(
                6 * self.num) + " float\n")  # str(len(points))
            # print(self.r)
            for j in range(int(self.r)):

                if (j == 0):
                    f.write(str(self._hex_cornerX(self.centerX, 0)) + " " + str(self._hex_cornerY(self.centerY, 0)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 1)) + " " + str(
                        self._hex_cornerY(self.centerY, 1)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 2)) + " " + str(
                        self._hex_cornerY(self.centerY, 2)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 3)) + " " + str(
                        self._hex_cornerY(self.centerY, 3)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 4)) + " " + str(
                        self._hex_cornerY(self.centerY, 4)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 5)) + " " + str(
                        self._hex_cornerY(self.centerY, 5)) + \
                            " 0.0\n")  # +str(points[index])+" 0.0" + "\n")
                    self.MaskPos += 1
                for index in range(j * 3):
                    if self._check_mask(self.MaskPos):
                        f.write(
                            str(self._hex_cornerX(self.centerX, 0)) + " " + str(self._hex_cornerY(self.centerY, 0)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 1)) + " " + str(
                                self._hex_cornerY(self.centerY, 1)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 2)) + " " + str(
                                self._hex_cornerY(self.centerY, 2)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 3)) + " " + str(
                                self._hex_cornerY(self.centerY, 3)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 4)) + " " + str(
                                self._hex_cornerY(self.centerY, 4)) + \
                            " 0.0\n" + str(self._hex_cornerX(self.centerX, 5)) + " " + str(
                                self._hex_cornerY(self.centerY, 5)) + " 0.0\n")  # +str(points[index])+" 0.0" + "\n")
                    # else:
                    # print(1234567)
                    if self._check_mask(self.MaskPos + 3 * j):
                        f.write(
                            str(-self._hex_cornerX(self.centerX, 0)) + " " + str(-self._hex_cornerY(self.centerY, 0)) + \
                            " 0.0\n" + str(-self._hex_cornerX(self.centerX, 1)) + " " + str(
                                -self._hex_cornerY(self.centerY, 1)) + \
                            " 0.0\n" + str(-self._hex_cornerX(self.centerX, 2)) + " " + str(
                                -self._hex_cornerY(self.centerY, 2)) + \
                            " 0.0\n" + str(-self._hex_cornerX(self.centerX, 3)) + " " + str(
                                -self._hex_cornerY(self.centerY, 3)) + \
                            " 0.0\n" + str(-self._hex_cornerX(self.centerX, 4)) + " " + str(
                                -self._hex_cornerY(self.centerY, 4)) + \
                            " 0.0\n" + str(-self._hex_cornerX(self.centerX, 5)) + " " + str(
                                -self._hex_cornerY(self.centerY, 5)) + " 0.0\n")  # +str(points[index])+" 0.0" + "\n")
                    # else:
                    # print(1234567)
                    self.MaskPos += 1
                    self.centerX -= self.width / 2
                    self.centerY += self.vert + self.size / 4  # height/5#**2/3#-size**(3/2)#-size**(3/2)**2

                    if (index >= j):
                        self.centerX -= self.width / 2
                        self.centerY -= self.vert + self.size / 4  # height/5#**2/3#-size**(3/2)#-size**(3/2)**3/2
                    if (index >= 2 * j):
                        self.centerX += self.width / 2
                        self.centerY -= self.vert + self.size / 4  # height/5#**2/3#-size**(3/2)#-size**(3/2)**3/2
                self.MaskPos += 3 * j
                self.shiftX += self.width
                self.centerX = self.shiftX
                self.centerY = self.shiftY
            f.write("POLYGONS " + str(self.num) + " " + str(self.num * 7) + "\n")
            for index in range(self.num):
                f.write("6 " + str(0 + index * 6) + " " + str(1 + index * 6) + " " + str(2 + index * 6) + " " + str(
                    3 + index * 6) + " " + str(4 + index * 6) + " " + str(5 + index * 6) + "\n")
            f.write("\nCELL_DATA " + str(self.num) + "\n\nSCALARS p float\n" + "\nLOOKUP_TABLE default\n")
            for j in range(int(self.r)):
                if (j == 0):
                    f.write(str(self.points[self.k]) + "\n")
                    self.k += 1
                for index in range(j * 3):
                    if self._check_mask(self.k):
                        f.write(str(self.points[self.k]) + "\n")
                    if self._check_mask(self.k + 3 * j):
                        f.write(str(self.points[self.k + 3 * j]) + "\n")
                    #                     else:
                    #                         print(123)
                    self.k += 1
                self.k += 3 * j

    def plt2d_1(self, i):
        self.i = i
        # print(self.data)
        self.data = self.data[self._get_max_num(1) * (self.i - 1):self._get_max_num(1) * self.i]
        # print(self.data)
        self.plt1d_1()

    def plt1d_1(self):
        self.points = self._column(self.data, -1)
        # print(self.points)
        with open('1d.vtk', 'w', encoding='utf-8') as f:
            f.write("# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\nPOINTS " + str(
                len(self.points)) + " float\n")
            for index in range(len(self.points)):
                if index == 0:
                    f.write(str(index) + "0.0 " + str(self.points[index]) + " 0.0" + "\n")
                else:
                    f.write(str(index) + "0.0 " + str(self.points[index]) + " 0.0" + "\n")
            f.write("LINES " + str(len(self.points) - 1) + " " + str(2 * len(self.points)) + "\n")
            for index in range(len(self.points) - 1):
                f.write("2" + " " + str(index) + " " + str(index + 1) + "\n")

    def plt3d_2(self, col3d, col2d, size):
        self.col3d = col3d
        self.col2d = col2d
        self.size = size
        self.data = self.data[
                    (self.col3d - 1) * self._get_max_num(1) * self._get_max_num(0):self.col3d * self._get_max_num(
                        1) * self._get_max_num(0):1]
        self.plt2d_2(self.size, self.col2d)

    def plt3d_1(self, col3d, col1d):
        self.col3d = col3d
        self.col1d = col1d
        self.data = self.data[
                    (self.col3d - 1) * self._get_max_num(1) * self._get_max_num(0):self.col3d * self._get_max_num(
                        1) * self._get_max_num(0):1]
        self.plt2d_1(self.col1d)