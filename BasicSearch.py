#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'aiwuxt'

class BasicSearch(object):

    def __init__(self):
        self.m_sDocDir = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\documents'
        self.m_sDocIndexFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\docIDs.txt'
        self.m_sWordIndexFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\wordIndex.txt'

        self.m_docWord2List = {}
        self.m_docDocID2Path = {}

    def __read_file(self, path):
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content

    def basci_serach(self):
        content = self.__read_file(self.m_sDocIndexFile)
        content = content.split('\n')
        for line in content:
            if line:
                line = line.split('\t')
                self.m_docDocID2Path.setdefault(line[0], line[1])

        content = self.__read_file(self.m_sWordIndexFile)
        content = content.split('\n')
        for line in content:
            if line:
                line = line.split('    ')
                ids = []
                for id in line[1:]:
                    ids.append(id)
                self.m_docWord2List.setdefault(line[0], ids)

    def search(self, s_query):
        if s_query in self.m_docWord2List.keys():
            return self.m_docWord2List[s_query]