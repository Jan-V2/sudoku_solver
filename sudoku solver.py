#todo solves sudokus
# a methode that takes a 2d array of numbers and a sector size
# todo een methode maken die sudokus scraped van https://www.websudoku.com/ and solves them
# 3x3 areas are called sectors
# build up the already contians array at the same time as the sector map array
from pprint import pprint

items_in_sector = 0

class Sudoku_Solver:
    # the sudoku is a 2d array that should bij evenly
    # divisable in both the x and y dir by sectorsize
    # it can contain numbers form 0 through 9 in which 0 means empty
    sudoku_list = list

    def __init__(self, sudoku_array_list):
        # each sudokuarraylist contians a sudoku as an arrray in place 0
        # and it's sectorsize at place 1
        # todo add errorchecking (maybe)
        sudoku_list = []
        for item in sudoku_array_list:
            sudoku_list.append(self.Sudoku(item[0], item[1]))

    def solve(self):
        self._search_pulse()

    class Sudoku:
        sector_array = ()

        def __init__(self, sudoku_array, sector_size):
            if len(sudoku_array) % sector_size == 0:
                if len(sudoku_array[0]) % sector_size == 0:
                    self.sudoku = sudoku_array
                    self.sector_size = sector_size
                else:  # todo make errorchecking better
                    print("sudoku not right size")
                    raise IOError
            else:
                print("sudoku not right size")
                raise IOError

            # generates the sector_data_array
            # the sector_data_array is a 2d array of 2d arrays
            sector_data_array = []
            for a in range(len(sudoku_array[0]) // sector_size):
                sector_data_array.append([])
                for b in range(len(sudoku_array) // sector_size):
                    x_min = a * sector_size - 1
                    x_max = (a + 1) * sector_size
                    y_min = b * sector_size - 1
                    y_max = (b + 1) * sector_size
                    sector_data = []
                    for i in range(len(sudoku_array[0])):
                        if x_min < i < x_max:
                            sector_data.append([])
                            for j in range(len(sudoku_array)):
                                if y_min < j < y_max:
                                    sector_data[len(sector_data) - 1].append(self.sudoku[i][j])
                    sector_data_array[len(sector_data_array) - 1].append(sector_data)

            sector_array = []
            for i in range(len(sector_data_array)):
                sector_array.append([])
                for j in range(len(sector_data_array[0])):
                    sector_array[i].append(self.Sector(sector_data_array[i][j], [i, j], sector_size))
            self.sector_array = tuple(sector_array)

        def get_collums(self, sector_list):
            pass

        def get_rows(self, sector_list):
            pass

        class Sector:
            sector = tuple
            bools = tuple
            contains = tuple
            coords = tuple
            items_in_sector = tuple

            def __init__(self, sector, coords, sector_size):
                # the sectormap three properties.
                # the fist item is a 2d bool array of the sector where a filled in space if false and empty is true
                # the second item is an array with all the numbers the sector already contains
                # the third item is a tuple of the coords
                bools = []
                contains = []
                for i in range(len(sector[0])):
                    bools.append([])
                    row_int = len(bools) - 1
                    for j in range(len(sector)):
                        item = sector[j][i]
                        if item > 0:
                            bools[row_int].append(False)
                            contains.append(item)
                        else:
                            bools[row_int].append(True)

                self.sector = tuple(sector)
                self.bools = tuple(bools)
                self.contains = tuple(contains)
                self.coords = tuple(coords)
                self.items_per_sector = tuple(sector_size * sector_size)

            def change_value(self, value, x, y):
                if value in self.contains:
                    print("sector " + str(self.coords) + "already contains " + str(value))
                    raise ValueError
                if value > self.items_per_sector:
                    print(str(value) + "is higher than the allowed in this sector.\n "
                                       "the maximum is " + str(self.items_per_sector))
                #todo more errorchecking (if i can be bothered)

                sector = [list(i) for i in self.sector]
                bools = [list(i) for i in self.bools]
                contains = [list(i) for i in self.contains]
                sector[x][y] = value
                bools[x][y] = False
                contains.append(value)
                self.sector = (tuple(i) for i in sector)
                self.bools = (tuple(i) for i in bools)
                self.contains = (tuple(i) for i in contains)

            def get_sector_rows(self):
                rows = []
                for i in self.sector:
                    rows.append(list(i))
                return rows

            def get_sector_collums(self):
                collums = []
                width = len(self.sector[0])
                for i in range(width):
                    collums.append([])
                    index = len(collums) -1
                    for row in self.sector:
                        collums[index].append(row[index])
                return collums


    def _check_sector(self, sector):
        pass


    def _search_pulse(self):
        sectorlist = self.sector_list
        for a in range(len(sectorlist[0])):
            for b in range(len(sectorlist)):
                sector = self.Sector(sectorlist[b][a], (b, a))
                for i in range(1, self.items_per_sector+1):
                    if i not in sector.contains:
                        pass

        #self.sector_list = sectorlist




sudoku = [[0, 0, 8, 0, 0, 0, 9, 0, 0],
          [5, 0, 0, 0, 6, 0, 0, 2, 1],
          [4, 1, 7, 3, 9, 2, 0, 0, 6],
          [0, 4, 9, 2, 0, 0, 6, 0, 0],
          [7, 0, 0, 0, 0, 0, 0, 0, 3],
          [0, 0, 1, 0, 0, 5, 4, 8, 0],
          [2, 0, 0, 6, 4, 9, 3, 1, 8],
          [9, 8, 0, 0, 2, 0, 0, 0, 7],
          [0, 0, 6, 0, 0, 0, 2, 0, 0]]

if __name__ == '__main__':
    duku = Sudoku_Solver([sudoku, 3])
    duku.solve()



