import heapq
import os
import struct


class heapNode:
  def __init__(self, char, freq):
    self.char = char
    self.freq = freq
    self.left = None
    self.right = None

  def __lt__(self, other):
    return self.freq < other.freq

class huffmanCoding:
  def __init__(self, path=""):
    self.path = path
    self.frequency = {}
    self.heap = []
    self.codes = {}
    self.reverse_codes = {}

  def obtainFrequencies(self, text):
    for char in text:
      self.frequency[char] = self.frequency.get(char, 0) + 1

  def constructHeap(self):
    heapq.heapify(self.heap)
    for key in self.frequency:
      temp_heap_node = heapNode(key, self.frequency[key])
      heapq.heappush(self.heap, temp_heap_node)

  def buildTree(self): #Дерево
    pass

  def generateCodesHelper(self, root, curr_code): 
    pass

  def generateCodes(self):
    pass

  def encodedText(self, input):
    pass
    
  def getPaddedEncodedText(self, input):
    pass

  def get_byte_encoded(self, padded_encoded_text):
   pass

  def compress(self):
    pass

  
  def removePadding(self, input):
   pass

  def decode(self, input):
   pass

  def write_header(self, file): 
    pass

  def parse_header(self, input):  #Достает информацию
   pass

  def rawbytes(self, s):
    outlist = []
    for cp in s:
      num = ord(cp)
      if num < 256:
        outlist.append(struct.pack('B', num))
      elif num < 65535:
        outlist.append(struct.pack('>H', num))
      else:
        b = (num & 0xFF0000) >> 16
        H = num & 0xFFFF
        outlist.append(struct.pack('>bH', b, H))
    return b''.join(outlist)

  def decompress(self, input):
    pass

Huffman = huffmanCoding()
Huffman.compress()
Huffman.decompress()