# -*- coding: utf-8 -*-
import os
from ..base import CorpusTextSearch

from unittest import TestCase

DATA = os.path.join(os.path.dirname(__file__), 'data')


class TestCorpusTextSearch(TestCase):
    """Basic import test"""
    def setUp(self):
        self.test1 = CorpusTextSearch(
            pathDF=os.path.join(DATA, 'dfTest.csv'),
            dataType='csv',
            dataIndex='single'
            )
        self.test2 = CorpusTextSearch(
            pathDF=os.path.join(DATA, 'dfTest.pickle'),
            dataType='pickle'
            )

    def TestImportException(self):
        self.assertRaises(TypeError, CorpusTextSearch)

    def TestImport(self):
        expected_datatype_1 = 'csv'
        expected_datatype_2 = 'pickle'
        self.assertEqual(self.test1.datatype, expected_datatype_1)
        self.assertEqual(self.test2.datatype, expected_datatype_2)

    def TestReduceSingleIndex(self):
        testdt = self.test1.reduce('part', 'Einleitung').reduce('paragraph', '1') \
                    .reduce('page', 10).results()
        self.assertEqual(testdt.shape[0], 1)
        self.assertEqual(testdt.volume.values[0], 'Band_1')

    def TestReduceSingleIndexExtResults(self):
        testdt = self.test2.reduce('part', 'Einleitung').reduce('paragraph', '1') \
                    .reduce('page', 10).extResults('part')
        self.assertEqual(testdt.shape[0], 1)
        self.assertEqual(testdt.words.values[0], 117)

    def TestReduceMultiIndex(self):
        testdt = self.test2.reduce('part', 'Einleitung').reduce('paragraph', '1') \
                    .reduce('page', 10).results()
        self.assertEqual(testdt.shape[0], 1)
        self.assertEqual(testdt.volume.values[0], 'Band_1')

    def TestReduceMultiIndexExtResults(self):
        testdt = self.test2.reduce('part', 'Einleitung').reduce('paragraph', '1') \
                    .reduce('page', 10).extResults('part')
        self.assertEqual(testdt.shape[0], 1)
        self.assertEqual(testdt.words.values[0], 117)


if __name__ == '__main__':
    unittest.main()
