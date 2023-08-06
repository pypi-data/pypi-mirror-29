# -*- coding: utf-8 -*-
import pandas as pd
import re
import difflib
from citableclass.base import Citable


class CorpusTextSearch(object):
    """
    This class is initialized with a searchstring, the name of the column,
    which contains the textstrings, and a path to a pickled dataframe.
    Optionally, a path to an excel file containing metadata can be provided.

    For other import formats change read_pickle and read_excel accordingly.

    Example:
            >>> search1 = SearchPhrases(
                            '[Ss]ol','text,'/path/to/kepler/dataframe'
                            )
            True
    """

    def __init__(
            self, pathDF,
            dataType='pickle', dataIndex='multi', colname='text',
            maxValues=2500, pathMeta=False, pathType=False
            ):

        self.datatype = dataType

        if pathType == 'DOI':
            pathDF = "http://dx.doi.org/{0}".format(pathDF)
        elif pathType == 'citable':
            self.citable = Citable(pathDF)
            self.dataframe = self.citable.digitalresource()

        if not pathType == 'citable':
            if self.datatype == 'pickle':
                self.dataframe = pd.read_pickle(pathDF)
            elif self.datatype == 'excel':
                self.dataframe = pd.read_excel(pathDF)
            elif self.datatype == 'csv':
                self.dataframe = pd.read_csv(pathDF, error_bad_lines=False)
            elif self.datatype == 'json':
                self.dataframe = pd.read_json(pathDF)
            else:
                raise ValueError(
                    'Please provide data in pickle,excel,csv or json format'
                    )

        self.dataindex = dataIndex

        self.colValueDictTrigger = []
        if self.dataindex == 'single':
            for col in self.dataframe.columns:
                if not self.dataframe[col].dtype.name in ['int', 'int64', 'float64']:
                    if len(self.dataframe[col].unique()) < maxValues:
                        self.colValueDictTrigger.append(col)
        elif self.dataindex == 'multi':
            for level in self.dataframe.index.names:
                if not self.dataframe.index.get_level_values(level).dtype.name in ['int', 'int64', 'float64']:
                    if len(self.dataframe.index.get_level_values(level).unique()) < maxValues:
                        self.colValueDictTrigger.append(level)

        self.extData = ''
        self.result = ''

        self.levelValues = {}

        self.column = colname

        if pathMeta:
            self.metaData = pd.read_excel(pathMeta)
        else:
            self.metaData = ''

    def resetColWidth(self):
        """ Reset pandas display option for max_colwidth"""
        pd.reset_option('display.max_colwidth')
        return

    def resetSearch(self):
        """Reset self.result to full dataframe."""
        self.result = ''
        return

    def search(self, value):
        """
        Search string in colname column.
        """
        if type(self.result) == str:
            self.result = self.dataframe[self.dataframe[self.column].str.contains(value)]
        elif isinstance(self.result, pd.DataFrame):
            self.result = self.result[self.result[self.column].str.contains(value)]
        return self

    def logicReduce(self, logicList):
        """
        Constructs complex searches for list of (part,value) tuples, connected
        via AND (&),OR (|),NOT (~&) logic. logicList has the format
        '[(part1,value1),&,(part2,value2),|,(part3,value3)]'.
        Evaluation is in order of apperance, e.g. for the above logicList,
        a boolean list is constructed for each (part,value) tuple.
        Then the first two tuples are compared with & yielding a temporary
        result temp1, which is compared with | with the last tuple.
        This creates a resulting boolean list res1,
        which is used to reduce the dataframe.
        """
        self.tempRes = []
        for part in logicList:
            if type(part) == tuple:
                res = self.boolList(part[0], part[1])
                self.tempRes.append(res)
            elif type(part) == str and part in ['&', '|', '~&']:
                self.tempRes.append(part)

        self.res = self.tempRes.pop(0)

        while self.tempRes:
            op = self.tempRes.pop(0)
            res2 = self.tempRes.pop(0)
            if op == '&':
                self.res = self.res & res2
            elif op == '|':
                self.res = self.res | res2
            elif op == '~&':
                self.res = self.res & np.invert(res2)
            else:
                pass

        if type(self.res) != str:
            self.result = self.dataframe[self.res]
        return self

    def boolList(self, level, value):
        """ Returns boolean list for dataframe[part]==value."""
        if self.dataindex == 'multi' and level != self.column:
            res = self.dataframe.index.get_level_values(level) == self._fuzzySearch(level, value)
        elif self.dataindex == 'single' and level != self.column:
            res = self.dataframe[level] == self._fuzzySearch(level, value)
        elif level == self.column:
            res = self.dataframe[level].str.contains(value) == True
        return res

    def _fuzzySearch(self, level, value):
        """Allow fuzzy search."""
        if level in self.colValueDictTrigger and level != self.column:
            if level not in self.levelValues.keys():
                if self.dataindex == 'multi':
                    self.levelValues[level] = self.dataframe.index.get_level_values(level).unique()
                elif self.dataindex == 'single':
                    self.levelValues[level] = self.dataframe[level].unique()
                else:
                    raise ValueError(
                        'DataIndex not "single" or "multi".'
                        )
            else:
                pass

            if value not in self.levelValues[level]:
                try:
                    closestMatch = difflib.get_close_matches(value, self.levelValues[level], 1)
                    if closestMatch:
                        searchValue = closestMatch[0]
                    else:
                        raise ValueError(
                            'Could not find matching expression to search.'
                            )
                except TypeError:
                    searchValue = value
            else:
                searchValue = value
        else:
            searchValue = value
        return searchValue

    def reduce(self, level, value):
        """ Return reduced dataframe for search tuple (level/column,value):
            a) as cross-section for multi-index dataframe:
               df.xs(value,level=level)
            b) as sub-dataframe for single-index dataframe:
               df[df.column == value]

            Result is in self.result, to be able to chain reductions.
            To view result use self.results()
        """

        searchValue = self._fuzzySearch(level, value)
        self._searchString(level, searchValue)
        return self

    def _searchString(self, level, value):
        """Helper function for reducing dataframes"""
        if self.dataindex == 'multi':
            if type(self.result) == str:
                self.result = self.dataframe.xs(self._assertDataType(level, value, self.dataframe), level=level, drop_level=False)
            else:
                self.result = self.result.xs(self._assertDataType(level, value, self.result), level=level, drop_level=False)
        elif self.dataindex == 'single':
            if type(self.result) == str:
                self.result = self.dataframe[self.dataframe[level] == self._assertDataType(level, value, self.dataframe)]
            else:
                self.result = self.result[self.result[level] == self._assertDataType(level, value, self.result)]

    def _assertDataType(self, level, value, dataframe):
        """Helper function to assert correct datatype for value at level"""
        intTypes = ['int8', 'int16', 'int32', 'int64', 'float', 'float64']
        valueType = type(value)
        if self.dataindex == 'multi':
            levelType = dataframe.index.get_level_values(level=level).dtype.name
        elif self.dataindex == 'single':
            levelType = self.dataframe[level].dtype.name
        if levelType == 'object' and valueType == str:
            return value
        elif levelType == 'object' and valueType == int:
            try:
                return str(value)
            except ValueError as err:
                raise('Can not cast {0} to type {1}'.format(value, levelType))
        elif levelType in intTypes and valueType == int:
            return value
        elif levelType in intTypes and valueType == float:
            return value
        elif levelType in intTypes and valueType == str:
            try:
                return int(value)
            except ValueError:
                raise('Can not cast {0} to type {1}'.format(value, levelType))
        else:
            raise ValueError('Can not cast {0} to type {1}'.format(value, levelType))

    def results(self):
        """Returns the search result as a single-index dataframe."""
        if self.dataindex == 'multi':
            self.indexLevels = list(self.result.index.names)
            formatedResult = self.result.reset_index(level=self.indexLevels)
        elif self.dataindex == 'single':
            formatedResult = self.result
        pd.set_option('display.max_colwidth', -1)
        return formatedResult

    def extResults(self, level):
        """
        Returns the search result as a single-index dataframe, extend with
        metadata on the desired level. The metadata is calculated for all other
        levels of multi-indexed dataframe.
        """
        if not self.dataindex == 'multi':
            print('Statistics for multiindexed dataframes only.')
            return
        self.extData = pd.merge(left=self.results(), right=self._metaData(level), on=level)
        cols = [x for x in self.extData.columns if x != self.column]
        cols = cols + [self.column]
        self.extData = self.extData[cols]
        pd.set_option('display.max_colwidth', -1)
        return self.extData

    def _countWords(self, level, value):
        """Helper function to count words on a given level."""
        text = ' '.join(self.dataframe.xs(value, level=level).text.tolist())
        numWords = len(re.findall('\w+', text))
        return numWords

    def _getStatistics(self, level):
        """Helper function to return statistics on given level."""
        retDict = {}
        subLevels = self.indexLevels.copy()
        try:
            subLevels.remove(level)
        except ValueError:
            print('{0} not in index'.format(level))

        for part in self.dataframe.index.get_level_values(level).unique():
            partDict = {}
            for subLevel in subLevels:
                num = len(self.dataframe.xs(part, level=level).index.get_level_values(subLevel).unique())
                if num > 1:
                    partDict['Num_' + subLevel] = num
            partDict['words'] = self._countWords(level, part)
            retDict[part] = partDict
        return retDict

    def _metaData(self, level):
        """Helper function to generate dataframe from statistics."""
        resDict = self._getStatistics(level)
        self.metaDataFrame = pd.DataFrame(resDict).fillna('1').astype('int').transpose().reset_index().rename({'index': level}, axis=1)
        return self.metaDataFrame
