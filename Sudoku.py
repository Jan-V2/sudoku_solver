from utils import log, log_return
import pprint

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
        for i in ret:
            print(i)# pprint didn't work here?

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
            if coord == []:  # todo there's a bug here
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
            # todo more errorchecking (if i can be bothered)

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
                index = len(collums) - 1
                for row in self.sector:
                    collums[index].append(row[index])
            return collums
