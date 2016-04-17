#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'aiwuxt'
import math

class VectorSpaceSearch(object):

    def __init__(self):
        self.sTermFrequencyFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\termFrequency.txt'
        self.sVectorFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\tfIdfVectors.txt'
        self.sBasisWordsFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\basisWords.txt'
        self.m_sDocIndexFile = 'G:\\2016_Spring\\SimpleSearchEngine\\static\\docIDs.txt'

        self.m_dicWord2DocFrequency = {}
        self.m_lstBaisWords = []
        self.m_dicDocId2Vector = {}
        self.m_docDocID2Path = {}

    def __read_file(self, path):
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content

    def vector_space_search(self):
        content = self.__read_file(self.sTermFrequencyFile)
        content = content.split('\n')
        for line in content:
            if line:
                line = line.split('    ')
                self.m_dicWord2DocFrequency.setdefault(line[0], len(line))

        content = self.__read_file(self.sBasisWordsFile)
        content = content.split('\n')
        for line in content:
            if line:
                self.m_lstBaisWords.append(line)

        content = self.__read_file(self.sVectorFile)
        content = content.split('\n')
        for line in content:
            if line:
                line = line.split('	')
                daVector = []
                for vec in line[1:]:
                    if vec:
                    #print(vec)
                        daVector.append(float(vec))
                self.m_dicDocId2Vector.setdefault(line[0], daVector)

        content = self.__read_file(self.m_sDocIndexFile)
        content = content.split('\n')
        for line in content:
            if line:
                line = line.split('\t')
                self.m_docDocID2Path.setdefault(line[0], line[1])

    def __represent_query_as_vector(self, s_query):
        sa_terms = str(s_query).lower().split(' ')
        d_doc_length = len(sa_terms)
        dic_word2count = {}
        for i in range(0, len(sa_terms)):
            if sa_terms[i] not in dic_word2count.keys():
                dic_word2count.setdefault(sa_terms[i], 1)
            else:
                dic_word2count[sa_terms] += 1
        da_qvector = []
        for i in range(0, len(self.m_lstBaisWords)):
            s_current_basis_word = self.m_lstBaisWords[i]
            if s_current_basis_word not in dic_word2count.keys():
                pass
            else:
                dTf = int(dic_word2count[s_current_basis_word])
                dTf /= d_doc_length
                dIdf = math.log(len(self.m_docDocID2Path) / (self.m_dicWord2DocFrequency[s_current_basis_word]+1))
                da_qvector.append(dTf * dIdf)
        return da_qvector

    def __get_vector_similarity(self, da_vector1, da_vector2):
        d_length_vector1 = 0
        for i in range(0, len(da_vector1)):
            d_length_vector1 += math.pow(da_vector1[i], 2)
        if d_length_vector1 == 0:
            return 0
        d_length_vector1 = math.sqrt(d_length_vector1)

        d_length_vector2 = 0
        for i in range(0, len(da_vector2)):
            d_length_vector2 += math.pow(da_vector2[i], 2)
        if d_length_vector2 == 0:
            return 0
        d_length_vector2 = math.sqrt(d_length_vector2)

        d_inner_product = 0
        for i in range(0, len(da_vector1)):
            d_inner_product += da_vector1[i] * da_vector2[i]

        return d_inner_product / (d_length_vector1 * d_length_vector2)

    def search(self, s_query):
        da_query_vector = self.__represent_query_as_vector(s_query)
        da_similarities = []
        sa_doc_ids = []
        for s_doc_id in self.m_dicDocId2Vector.keys():
            da_doc_vector = self.m_dicDocId2Vector[s_doc_id]

            da_similarities.append(self.__get_vector_similarity(da_query_vector, da_doc_vector))
            sa_doc_ids.append(s_doc_id)

        temp = [(similarities, doc_ids) for similarities, doc_ids in zip(da_similarities, sa_doc_ids)]
        temp.sort()
        sa_doc_ids = [doc_ids for similarities, doc_ids in temp]
        sa_doc_ids.reverse()
        return sa_doc_ids

