#todo solves sudokus
# a methode that takes a 2d array of numbers and a sector size
# todo een methode maken die sudokus scraped van https://www.websudoku.com/ and solves them
# 3x3 areas are called sectors
# build up the already contians array at the same time as the sector map array
from pprint import pprint
from utils import log, log_return, get_timestamp


class Sudoku_Solver:
    # the sudoku is a 2d array that should bij evenly
    # divisable in both the x and y dir by sectorsize
    # it can contain numbers form 0 through 9 in which 0 means empty
    sudoku_list = []
    search_checks = 0
    hack = []

    def __init__(self, sudoku_array_list):
        # each sudokuarraylist contians a sudoku as an arrray in place 0
        # and it's sectorsize at place 1
        # todo add errorchecking (maybe)
        for item in sudoku_array_list:
            self.sudoku_list.append(self.Sudoku(item[0], item[1]))


    def solve(self):
        # for collums interate 1st coord
        # for rows interate 2nd coord
        sudoku = self.sudoku_list[0]

        while self._search_sweep(sudoku):
            pass

        #for i in range(10000):

        sudoku.log_sudoku()
        log(str(self.search_checks))

    def _search_sweep(self, sudoku):
        # does a search across the entire sudoku once
        made_change = False
        for i in range(len(sudoku.sector_array)):
            for j in range(len(sudoku.sector_array)):
                sector = sudoku.sector_array[i][j]
                # pprint(sector.sector)
                if self._search_sector(sector, sudoku):
                    made_change = True
                    # pprint(sector.sector)
                    # log_return()
        return made_change


    def _search_sector(self, sector, sudoku):
        changed_data = False
        coords = sector.coords

        #log("searching " + str(coords))
        gridsize = len(sudoku.sector_array)
        collum_sector_list = []
        row_sector_list = []
        for i in range(gridsize):
            if i is not coords[0]:
                collum_sector_list.append([i, coords[1]])
            if i is not coords[1]:
                row_sector_list.append([coords[0], i])
        # print("rowlist")
        # pprint(collum_sector_list)
        # print("collumlist")
        #pprint(row_sector_list)
        rows = sudoku.get_rows(row_sector_list)
        collums = sudoku.get_collums(collum_sector_list)

        for n in range(1, sudoku.places_per_sector+1):
            if n not in sector.contains:
                temp_bools = [list(i) for i in sector.bools]
                for j in range(len(temp_bools)):
                    if n in rows[j]:
                        temp_bools = self._mk_row_false(temp_bools, j)
                    if n in collums[j]:
                        temp_bools = self._mk_collum_false(temp_bools, j)
                    self.search_checks += 1

                b, coord = self._check_if_one_place(temp_bools)
                if b:
                    #log("data acessed added "+ str(n))
                    #log("coord = " + str(coord))
                    sector.change_value(n, coord)
                    changed_data = True

        return changed_data

    def _mk_collum_false(self, bools, x):
        for i in range(len(bools)):
            bools[i][x] = False
        return bools

    def _mk_row_false(self, bools, y):
        for i in range(len(bools[0])):
            bools[y][i] = False
        return bools

    def _check_if_one_place(self, temp_bools):
        # returns true and the coords if there was only one vart thats true in the array
        found_one = False
        coord = []
        for i in range(len(temp_bools)):
            for j in range(len(temp_bools[0])):
                if temp_bools[i][j]:
                    if not found_one:
                        found_one = True
                        coord = [i, j]
                    else:
                        return False, None
        if found_one:
            return found_one, coord
        else:
            log("no empty places, this is not suppused to happen.")
            return found_one, None


    class Sudoku:
        sector_array = ()
        places_per_sector = int

        def __init__(self, sudoku_array, sector_size):
            if len(sudoku_array) % sector_size == 0:
                if len(sudoku_array[0]) % sector_size == 0:
                    self.sudoku = sudoku_array
                    self.sector_size = sector_size
                else:  # todo make errorchecking better
                    log("sudoku not right size")
                    raise IOError
            else:
                log("sudoku not right size")
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
            self.places_per_sector = sector_size * sector_size

        def log_sudoku(self):
            ret = []
            sects = self.sector_array
            for j in range(len(sects)):
                for i in range(len(sects[0])):
                    ret.append([])
                for sector in sects[j]:
                    sector_height = len(sector.sector)

                    for row in range(len(sector.sector)):
                        index = row + j * sector_height
                        for item in sector.sector[row]:
                            ret[index].append(item)
            pprint(ret)

        def get_collums(self, sector_list):
            results = []
            for item in sector_list:
                results.append(
                    self.sector_array[item[0]][item[1]].get_sector_collums()
                )
            return self._merge_results(results)

        def get_rows(self, sector_list):
            results = []
            for item in sector_list:
                results.append(
                    self.sector_array[item[0]][item[1]].get_sector_rows()
                    )
            return self._merge_results(results)

        def _merge_results(self, results):
            ret = []
            for i in range(len(results[0])):
                ret.append([])
                for j in results:
                    for k in j[i]:
                        ret[i].append(k)
            return ret

        class Sector:
            sector = list
            bools = list
            contains = list
            coords = list
            places_in_sector = int

            def __init__(self, sector, coords, sector_size):
                # the sectormap five properties.
                # bools is is a 2d bool array of the sector where a filled in space if false and empty is true
                # sector is the numbers contained in the sector as a 2d tuple
                # contains is an array with all the numbers the sector already contains
                # coords is a tuple of the coords of the sector withing the sudoku
                # places in sector is the number of spots in the sector
                bools = []
                contains = []
                for i in range(len(sector[0])):
                    bools.append([])
                    row_int = len(bools) - 1
                    for j in range(len(sector)):
                        item = sector[i][j]
                        if item > 0:
                            bools[row_int].append(False)
                            contains.append(item)
                        else:
                            bools[row_int].append(True)

                self.sector = sector
                self.bools = bools
                self.contains = contains
                self.coords = coords
                self.items_per_sector = sector_size * sector_size

            def change_value(self, value, coord):
                if coord == []:#todo there's a bug here
                    log("no coord given")
                    log("coord = " + str(coord))
                    raise ValueError
                if value in self.contains:
                    log("sector " + str(self.coords) + " already contains " + str(value))
                    log("sector = " + str(self.sector))
                    log("contains = " + str(self.contains))
                    raise ValueError
                if value > self.items_per_sector:
                    log(str(value) + "is higher than the allowed in this sector.\n "
                                       "the maximum is " + str(self.items_per_sector))
                #todo more errorchecking (if i can be bothered)

                x = coord[0]
                y = coord[1]

                sector = self.sector
                bools = self.bools
                contains = self.contains
                sector[x][y] = value
                bools[x][y] = False
                contains.append(value)
                self.sector = sector
                self.bools = bools
                self.contains = contains

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

    pprint(sudoku)
    log_return()
    duku = Sudoku_Solver([[sudoku, 3]])
    duku.solve()



