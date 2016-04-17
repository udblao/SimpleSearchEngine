#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'aiwuxt'

class BooleanSearch(object):

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

    def boolean_search(self):
        content = self.__read_file(self.m_sDocIndexFile)
        content = content.split('\n')
        for line in content:
            if line:
                line = line.split('\t')
                self.m_docDocID2Path.setdefault(line[0], line[1])

        m_doc_word2list = {}
        content = self.__read_file(self.m_sWordIndexFile)
        content = content.split('\n')
        for line in content:
            if line:
                line = line.split('    ')
                ht_doc_ids = {}
                for id in line[1:]:
                    if id not in ht_doc_ids.keys():
                        ht_doc_ids.setdefault(id, None)
                self.m_docWord2List.setdefault(line[0], ht_doc_ids)

    def __search_with_single_keyword(self, skeyword):
        pList4Return = []
        if skeyword in self.m_docWord2List.keys():
            for docid in self.m_docWord2List[skeyword].keys():
                if docid not in pList4Return:
                    pList4Return.append(docid)
        return pList4Return

    def __construct_query_tree(self, s_query):
        sa_elements = s_query.lower().split(' ')
        lst_groups = []
        for i in range(0, len(sa_elements)):
            ob_node = ['', '', '']
            if sa_elements[i] == 'and':
                ob_node[0] = "AND"
                ob_pre_node = lst_groups[len(lst_groups) - 1]
                ob_node[1] = ob_pre_node
                lst_groups.pop(len(lst_groups)-1)

                ob_right_node = ['', '', '']
                ob_right_node[0] = sa_elements[i + 1]
                ob_right_node[1] = None
                ob_right_node[2] = None
                ob_node[2] = ob_right_node
                i += 1
            else:
                ob_node[0] = sa_elements[i]
                ob_node[1] = None
                ob_node[2] = None

            lst_groups.append(ob_node)

        ob_last_node = lst_groups[0]
        for i in range(0, len(lst_groups)):
            ob_current_node = lst_groups[i]

            ob_or_node = ['', '', '']
            ob_or_node[0] = 'OR'
            ob_or_node[1] = ob_last_node
            ob_or_node[2] = ob_current_node
            ob_last_node = ob_or_node

        return ob_last_node

    def __search_with_binary_tree(self, ob_root_node):
        lst_results2return = []
        s_node_value = str(ob_root_node[0])
        if s_node_value == 'AND':
            lst_left_child_results = self.__search_with_binary_tree(ob_root_node[1])
            lst_right_child_results = self.__search_with_binary_tree(ob_root_node[2])
            if lst_left_child_results:
                for result in lst_left_child_results:
                    if result in lst_right_child_results:
                        lst_results2return.append(result)
        elif s_node_value == 'OR':
            lst_left_child_results = self.__search_with_binary_tree(ob_root_node[1])
            lst_right_child_results = self.__search_with_binary_tree(ob_root_node[2])
            if lst_left_child_results:
                for result in lst_left_child_results:
                    if result not in lst_results2return:
                        lst_results2return.append(result)
            if lst_right_child_results:
                for result in lst_right_child_results:
                    if result not in lst_right_child_results:
                        lst_results2return.append(result)
        else:
            return self.__search_with_single_keyword(s_node_value)

        return lst_results2return

    def search(self, s_query):
        lst_ids = self.__search_with_binary_tree(self.__construct_query_tree(s_query))
        return lst_ids

    def get_document_path_by_id(self, s_doc_id):
        return str(self.m_docDocID2Path[s_doc_id])

    def get_content_by_path(self, s_doc_path):
        return self.__read_file(s_doc_path)




