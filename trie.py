# -*- coding: utf-8 -*-
'''
Created on 14 сент. 2016 г.
Префиксное дерево
@author: igor
'''

import codecs
import readline
from operator import itemgetter
import time

class Node(object):
    """Узел префиксного дерева
    """
    def __init__(self):
        self.children = {}
        self.word = None
    
    def __getitem__(self, key):
        if key in self.children:
            return self.children[key]
        return None
    
    def __setitem__(self, key, value):
        self.children[key] = value
    
    def __contains__(self, key):
        return key in self.children

class Trie(object):
    """Префиксное дерево
    """
    def __init__(self):
        self.root = Node()
    
    def add(self, word):
        word = word.strip().lower()
        if word:
            node = self.root
            for ch in word:
                if ch not in node:
                    node[ch] = Node()
                node = node[ch]
            node.word = word
               
    def  __contains__(self, word):
        node = self.root
        for ch in word.strip().lower():
            if ch in node:
                node = node[ch]
            else:
                return False
        return node.word is not None
    
              
    def spell(self, word, maxCost):
        
        word = word.strip().lower()
        
        # build first row
        currentRow = range(len(word) + 1)
        results = []
        
        def recursive(node, letter, word, previousRow, results):

            columns = len(word) + 1
            currentRow = [previousRow[0] + 1]
        
            # Build one row for the letter, with a column for each letter in the target
            # word, plus one for the empty string at column 0
            for column in xrange(1, columns):
        
                insertCost = currentRow[column - 1] + 1
                deleteCost = previousRow[column] + 1
        
                if word[column - 1] != letter:
                    replaceCost = previousRow[column - 1] + 1
                else:                
                    replaceCost = previousRow[column - 1]
        
                currentRow.append(min(insertCost, deleteCost, replaceCost))
        
            # if the last entry in the row indicates the optimal cost is less than the
            # maximum cost, and there is a word in this trie node, then add it.
            if currentRow[-1] <= maxCost and node.word != None:
                results.append((node.word, currentRow[-1]))
        
            # if any entries in the row are less than the maximum cost, then 
            # recursively spell each branch of the trie
            if min(currentRow) <= maxCost:
                for letter in node.children:
                    recursive(node.children[letter], letter, word, currentRow, results)
        
        # recursively spell each branch of the trie
        for letter in self.root.children:
            recursive(self.root.children[letter], letter, word, currentRow, results)
    
        return results

trie = Trie()

with codecs.open('word.txt', mode='r', encoding='utf-8') as f:
    for line in f:
        if line:
            trie.add(line)

while True:
    word = raw_input('Найти: ').decode('utf-8')
    if not word:
        break
    beg = time.time()
    res = sorted(trie.spell(word, 3), key = itemgetter(1))[:10]
    print 'Выполнено за %f сек' % (time.time() - beg)
    for tup in res:
        print tup[0], tup[1]


    

        
  

    

 
