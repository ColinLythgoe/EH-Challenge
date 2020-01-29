import collections
import time
from typing import List
from typing import Set


class TrieNode():
    def __init__(self):
        self.children = collections.defaultdict(TrieNode) #Make the node children a defaultdict so we automatically get a new TrieNode if an unknown key is added
        self.finishedWord = False

#We'll use a trie to be able to deal with all the words optimally
class Trie():
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            node = node.children[char]
        node.finishedWord = True #Mark the end of a word so we can check it individually before trying to use it as the root of a larger word


#Loads up Shakespeare text into a unordered set, 10ms faster than trying to load a list with duplicates into the trie
def loadShakespeare(file: List[str], wordSet: Set[str]):
    for line in file:
        for word in line.split():
            wordSet.add(word.casefold())


#Function to make sure all the characters in the grid conform to being lowercase
def casefoldGrid(charGrid: List[List[str]]):
    for i in range(len(charGrid)):
        for j in range(len(charGrid[0])):
            charGrid[i][j] = charGrid[i][j].casefold()


#First function of the solution itself
def findLongestWord(charGrid: List[List[str]], wordList: List[str]) -> str:
    if not wordList or not charGrid:
        return "Failed: Invalid Inputs"

    retList = [""] #List object to hold the longest word
    trie = Trie()  #Initializing the trie to hold all the words

    #Loading all the words into the trie, while making sure everything in the grid and words is lowercase
    #print(len(wordList))
    casefoldGrid(charGrid)
    for word in wordList:
        trie.insert(word.casefold())

    #Iterating through the character grid, starting up a recursive DFS through the trie if there exist any potential words
    for i in range(len(charGrid)):
        for j in range(len(charGrid[0])):
            dfs(charGrid, trie.root, i, j, "", retList)

    return retList[0]


def dfs(charGrid: List[List[str]], node: TrieNode, i: int, j: int, path: str, retList: List[str]):
    #If we're at a finished word and it is longer than the previous word, take the new longer word
    if node.finishedWord and len(path) > len(retList[0]):
        retList[0] = path
        #print(retList[0])

    #Make sure we're in bounds, leave if we're not
    if i < 0 or i >= len(charGrid) or j < 0 or j >= len(charGrid[0]):
        return

    #Pick up the character on our current grid location so we can check if it continues any words
    nextChar = charGrid[i][j]
    node = node.children.get(nextChar)
    if not node: #If it didn't continue a word then we leave
        return

    #Continue moving around the grid per the rules, allowing for reuse of positions
    dfs(charGrid, node, i + 2, j + 1, path + nextChar, retList)
    dfs(charGrid, node, i + 2, j - 1, path + nextChar, retList)
    dfs(charGrid, node, i - 2, j + 1, path + nextChar, retList)
    dfs(charGrid, node, i - 2, j - 1, path + nextChar, retList)
    dfs(charGrid, node, i + 1, j + 2, path + nextChar, retList)
    dfs(charGrid, node, i - 1, j + 2, path + nextChar, retList)
    dfs(charGrid, node, i + 1, j - 2, path + nextChar, retList)
    dfs(charGrid, node, i - 1, j - 2, path + nextChar, retList)


#Driver function to deal with the grids, files, wordlists
def main():
    print("Starting...")

    words = ["algol", "fortran", "simula"]
    words2 = set()

    grid = [
        ['q', 'w', 'e', 'r', 't', 'n', 'u', 'i'],
        ['o', 'p', 'a', 'a', 'd', 'f', 'g', 'h'],
        ['t', 'k', 'l', 'z', 'x', 'c', 'v', 'b'],
        ['n', 'm', 'r', 'w', 'f', 'r', 't', 'y'],
        ['u', 'i', 'o', 'p', 'a', 's', 'd', 'f'],
        ['g', 'h', 'j', 'o', 'l', 'z', 'x', 'c'],
        ['v', 'b', 'a', 'm', 'q', 'w', 'e', 'r'],
        ['t', 'y', 'u', 'i', 'o', 'p', 'a', 's']
    ] #fortran

    grid2 = [
        ['e', 'x', 't', 'r', 'a', 'h', 'o', 'p'],
        ['n', 'e', 't', 'w', 'o', 'r', 'k', 's'],
        ['q', 'i', 'h', 'a', 'c', 'i', 'q', 't'],
        ['l', 'f', 'u', 'n', 'u', 'r', 'x', 'b'],
        ['b', 'w', 'd', 'i', 'l', 'a', 't', 'v'],
        ['o', 's', 's', 'y', 'n', 'a', 'c', 'k'],
        ['q', 'w', 'o', 'p', 'm', 't', 'c', 'p'],
        ['k', 'i', 'p', 'a', 'c', 'k', 'e', 't']
    ] #honorificabilitudinitatibus

    with open('shakespeare.txt') as file:
        loadShakespeare(file, words2)

    t1 = time.perf_counter_ns() #Timer for performance checking
    print("Longest word is:", findLongestWord(grid2, words2))
    print("Execution time:", (time.perf_counter_ns() - t1), "ns")
    print("Finished.")

    x = 2
    y = 3
    if x < y: if x > 10: print('foo')


if __name__ == "__main__":
    main()