import xlrd
import os

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')

class DataReader:

    _default_datafile = os.path.join(PROJECT_DIR,'data','matingassay.xlsx')

    def __init__(self):
        pass

    def load(self,file_=_default_datafile):
        book = xlrd.open_workbook(file_)
        res = {}
        for i in range(book.nsheets):
            sheet = book.sheet_by_index(i)
            res[sheet.name] = self._parseSheet(sheet)
        return res

    def _parseSheet(self,sheet):
        res = {}
        for c in range(sheet.ncols):
            name = sheet.cell_value(0,c).lower().strip()
            try:
                res[name] = [k if c == 0 else self._transform(k) for k in sheet.col_values(c,1,sheet.nrows)]
            except ValueError:
                raise ValueError('Some values in sheet "{0}", column "{1}" are not numbers.'.format(sheet.name,name))
        return res

    def _transform(self,x):
        if isinstance(x,basestring) and len(x.strip()) == 0:
            return None
        try:
            return int(x)
        except ValueError:
            return float(x)


