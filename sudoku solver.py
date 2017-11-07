# a methode that takes a 2d array of numbers and a sector size
# todo een methode maken die sudokus scraped van https://www.websudoku.com/ and solves them
# 3x3 areas are called sectors
# build up the already contians array at the same time as the sector map array
import urllib
from pprint import pprint

import bs4
import urllib3

from utils import log, log_return, get_timestamp
from Sudoku import Sudoku

class Sudoku_Scraper:

    def __init__(self):
        self.url = "https://show.websudoku.com/?"
        self.http = urllib3.PoolManager()

    def get_sudokus(self, n):
        # n is the number of sudokus that get returned
        pass

    def test(self):

        pprint(bs4.BeautifulSoup(self.http.request("GET", self.url).data, 'html.parser'))

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
            self.sudoku_list.append(Sudoku(item[0], item[1]))

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
    test = Sudoku_Scraper()
    test.test()
    # pprint(sudoku)
    # log_return()
    # duku = Sudoku_Solver([[sudoku, 3]])
    # duku.solve()



