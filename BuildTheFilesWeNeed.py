#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'aiwuxt'
import math
class BuildTheFilesWeNeed(object):

    def __init__(self):
        self.sDocDir = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\documents'
        self.sDocIndexFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\docIDs.txt'
        self.sWordIndexFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\wordIndex.txt'
        self.sTermFrequencyFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\termFrequency.txt'
        self.sVectorFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\tfIdfVectors.txt'
        self.sBasisWordsFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\basisWords.txt'

    def __read_file(self, path):
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content

    def build_document_index(self):
        pass

    def build_word_index(self):
        pass

    def build_term_frequency_file(self):
        content = self.__read_file(self.sWordIndexFile)
        content = content.split('\n')
        file = open(self.sTermFrequencyFile, 'w')
        for line in content:
            if line:
                line = line.split('    ')
                tempdic = {}
                for id in line[1:]:
                #print(id)
                    if id not in tempdic.keys():
                        tempdic.setdefault(id, 0)
                    tempdic[id] += 1
                termfrequency = {}
                termfrequency.setdefault(line[0], '')
                for id in tempdic.keys():
                    termfrequency[line[0]] += '    ' + str(id) + '-' + str(tempdic[id])
                file.write(line[0] + termfrequency[line[0]] + '\n')
        file.close()

    def build_tfidvector_file(self):
        content = self.__read_file(self.sTermFrequencyFile)
        dic_word2doc_frequency = {}
        dic_term_frequency = {}
        dic_document2length = {}
        lst_words = []
        content = content.split('\n')
        for line in content:
            if line:
                line = line.split('    ')
                dic_word2doc_frequency.setdefault(line[0], len(line[1:]))
                for freq in line[1:]:
                    freq = freq.split('-')
                    dic_term_frequency.setdefault(line[0]+'@'+freq[0], freq[1])
                    lst_words.append(line[0])

                    if freq[0] not in dic_document2length.keys():
                        dic_document2length.setdefault(freq[0], 0)
                    dic_document2length[freq[0]] += int(freq[1])

        file = open(self.sVectorFile, 'w')
        for doc_id in dic_document2length.keys():
            daTfIdf = []
            for word in lst_words:
                sPariKey = word + '@' + doc_id
                if sPariKey in dic_term_frequency.keys():
                    dTf = int(dic_term_frequency[sPariKey])
                else:
                    dTf = 0
                dTf /= int(dic_document2length[doc_id])
                dIdf = math.log(len(dic_document2length) / int(dic_word2doc_frequency[word]))
                daTfIdf.append(dTf * dIdf)

            file.write(doc_id + '\t')
            for i in daTfIdf:
                file.write(str(i) + '\t')
            file.write('\n')
        file.close()

        file = open(self.sBasisWordsFile, 'w')
        #print(lst_words)
        for word in lst_words:
            file.write(word + '\n')
        file.close()

