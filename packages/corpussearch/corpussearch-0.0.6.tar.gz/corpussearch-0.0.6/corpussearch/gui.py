# -*- coding: utf-8 -*-
import pandas as pd
import re
import ipywidgets as widgets
from IPython.display import clear_output


from citableclass.base import Citable
from .base import CorpusTextSearch
# from corpussearch.base import CorpusTextSearch


class SearchWordGUI(widgets.HBox):
    def __init__(self, optionList, colName):
        super(SearchWordGUI, self).__init__()
        self.optList = optionList
        self.column = colName
        if self.column not in self.optList:
            self.optList.extend([colName])

        #############
        # Functions #
        #############
        def chgTxt(change):
            self._text.value = change['new']

        ###########
        # Widgets #
        ###########
        self._text = widgets.Text(description='Search for:', placeholder='Enter search word')
        self._text.layout.margin = '0 0 0 20px'

        self._select = widgets.Dropdown(
            description='Values:',
            options=self.optList,
            value=self.column,
        )
        ###########
        # Actions #
        ###########
        self._select.observe(
            chgTxt,
            names='value'
        )

        children = [self._text, self._select]
        self.children = children

    @property
    def value(self):
        return self._text.value

    @property
    def part(self):
        return self._select.value


class CorpusGUI(CorpusTextSearch):

    def __init__(
            self, pathDF,
            dataType='pickle', dataIndex='multi', colname='text',
            maxValues=2500, pathMeta=False, pathType=False
            ):

        super(CorpusGUI, self).__init__(pathDF, dataType, dataIndex, colname, maxValues, pathMeta, pathType)
        self.initSearch = SearchWordGUI(self.colValueDictTrigger, self.column)
        self.accordion = widgets.Accordion(children=[self.initSearch])
        self.accordion.set_title(0, 'Enter search term')

        self.extendSearch = widgets.ToggleButtons(options=['more', 'less'])
        self.extendSearch.on_msg(self._addSearchField)

        self.searchButton = widgets.Button(
            description='Search',
            button_style='danger'
        )

        self.searchButton.on_msg(self._searchLogic)

        self.direction = widgets.ToggleButtons(options=['previous', 'next'])

        self.direction.on_msg(self._setSentence)

        self.outInfo = widgets.Output()

        self.outSentence = widgets.Textarea(
            value='',
            layout=widgets.Layout(flex='0 1 auto', height='200px', min_height='40px', width='500px'),
            placeholder='Sentence'
        )

        self.outMeta = widgets.Textarea(
            placeholder='Result',
            description='Result:',
            value=''
        )

    def _setDescription(self):
        res = 'number {0}\n'.format(self.counter) + '\n'.join(
             ["{0}. {1}".format(x,y) for x,y in self.displayResult.iloc[self.counter].to_dict().items() if x != self.column]
        )
        return res

    def _setSentence(self, widget, content, buffers):
        if widget.value == 'previous':
            self.counter = self.counter - 1
        elif widget.value == 'next':
            self.counter = self.counter + 1
        if self.counter < self.displayResult.shape[0] and self.counter > -1:
            self.outSentence.value = self.displayResult[self.column].iloc[self.counter]
            self.outMeta.value = self._setDescription()
        else:
            self.outSentence.value = 'End of found results. Enter new search.'
        return

    def _addSearchField(self, widget, content, buffers):
        child = self.initSearch
        children = []
        for ch in self.accordion.children:
            children.append(ch)
        if self.extendSearch.value == 'more':
            children.append(
                widgets.Dropdown(
                    description='Select logic to connect words',
                    options={'and': '&', 'or': '|', 'not': '~&'},
                    value='&'
                )
            )
            children.append(child)
            self.accordion.children = children
            self.accordion.set_title(len(children)-2, 'and/or/not')
            self.accordion.set_title(len(children)-1, 'add term')
        elif self.extendSearch.value == 'less':
            if len(children) >= 3:
                lesschildren = children[:-2]
                self.accordion.children = lesschildren
            else:
                pass
            pass
        return

    def _searchLogic(self, widget, content, buffers):
        self.tempRes = []
        self.tempList = []
        self.counter = 0
        for ch in self.accordion.children:
            if ch.value not in ['&', '|', '~&']:
                self.tempList.append((ch.part, ch.value))
            else:
                self.tempList.append(ch.value)
        self.outputResult = self.logicReduce(self.tempList)

        self.displayResult = self.outputResult.results()

        if self.displayResult.shape[0] > 0:
            # TODO: Add plotting logic in handle_submit(sender)
            # handle_submit(sender)

            self.outSentence.value = re.sub('\n|\s+', ' ', self.displayResult[self.column].iloc[self.counter])
            self.outMeta.value = self._setDescription()
            with self.outInfo:
                clear_output()
                print('Found {} entries.'.format(self.displayResult.shape[0]))
        else:
            with self.outInfo:
                clear_output()
                print('Found no entries. Try changing search!')

    def displayGUI(self):
        searchControl = widgets.HBox([self.extendSearch, self.searchButton, self.outInfo])
        textControl = widgets.HBox([self.direction])
        sentenceFields = widgets.HBox([self.outMeta, self.outSentence])
        searchBox = widgets.VBox([self.accordion, searchControl, textControl, sentenceFields])

        return display(searchBox)
