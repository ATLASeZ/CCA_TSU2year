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

  def buildTree(self):  #Дерево
    while len(self.heap) > 1:
      min1 = heapq.heappop(self.heap)
      min2 = heapq.heappop(self.heap)
      tempNode = heapNode(None, min1.freq + min2.freq)
      tempNode.left = min1
      tempNode.right = min2
      heapq.heappush(self.heap, tempNode)

  def generateCodesHelper(self, root, curr_code):
    if not root:
      return
    if root.char:
      self.codes[root.char] = curr_code
      self.reverse_codes[curr_code] = root.char
    self.generateCodesHelper(root.left, curr_code + '0')
    self.generateCodesHelper(root.right, curr_code + '1')

  def generateCodes(self):
    root = heapq.heappop(self.heap)
    self.generateCodesHelper(root, '')

  def encodedText(self, input):
    output = ''
    for ele in input:
      output += self.codes[ele]
    return output

  def getPaddedEncodedText(self, input):
    length = len(input)
    required_padding = 8 - length % 8
    input = input + '0' * required_padding
    pad_info = '{0:08b}'.format(required_padding)
    input = pad_info + input
    return input

  def get_byte_encoded(self, padded_encoded_text):
    length = len(padded_encoded_text)
    if length % 8 != 0:
      print('Improper padding')
      exit(0)
    output = bytearray()
    for i in range(0, length, 8):
      byte = padded_encoded_text[i:i + 8]
      output.append(int(byte, 2))
    return output

  def compress(self):
    filename, extension = os.path.splitext(self.path)
    output_path = filename + '_compressed.bin'
    with open(self.path, 'r') as file, open(output_path, 'wb') as output:
      text = file.read() 
      text = text.rstrip()  
      self.obtainFrequencies(text)  
      self.constructHeap()  
      self.buildTree()  
      self.generateCodes() 
      encoded_text = self.encodedText(text) 
      padded_encoded_text = self.getPaddedEncodedText(encoded_text)  
      encoded_text_in_bits = self.get_byte_encoded(padded_encoded_text)  
      self.write_header(output)
      output.write(bytes(encoded_text_in_bits)) 
    print('Compressesd')
    return output_path

  def removePadding(self, input):
    pad_info = input[:8]
    input = input[8:]
    pad_info = int(pad_info, 2)
    input = input[:-1 * pad_info]
    return input

  def decode(self, input):
    output = ''
    curr_code = ''
    for ele in input:
      curr_code += ele
      if curr_code in self.reverse_codes:
        output += self.reverse_codes[curr_code]
        curr_code = ''
    return output

  def write_header(self, file):
    col_letters = (len(self.frequency.keys()) - 1).to_bytes(1, byteorder='little')
    file.write(col_letters)
    for letter, code in self.frequency.items():
      file.write(self.rawbytes(letter))
      file.write(code.to_bytes(4, byteorder='little'))

  def parse_header(self, input):  #Достает информацию
    col_letters = input[0] + 1
    header = input[1:5 * col_letters + 1]
    dict_chars = dict()
    for i in range(col_letters):
      dict_chars[chr(header[i * 5])] = int.from_bytes(header[i * 5 + 1:i * 5 + 5], byteorder='little')
    return dict_chars

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
    filename, extension = os.path.splitext(self.path)
    output_path = filename + '2.txt'
    with open(input, 'rb') as file, open(output_path, 'w') as output:
      ctx = file.read()
      ch_number = ctx[0] + 1
      body = ctx[5 * ch_number + 1:]
      self.frequency = self.parse_header(ctx)
      self.constructHeap()
      self.buildTree()
      self.generateCodes()
      bit_string = ''
      for i in range(len(body)):
        byte = body[i]
        bits = bin(byte)[2:].rjust(8, '0')
        bit_string += bits
      bit_string = self.removePadding(bit_string)
      decoded_text = self.decode(bit_string)
      output.write(decoded_text)
    print('Decompressed')
    return output_path


Huffman = huffmanCoding("1.txt")
Huffman.compress()
Huffman.decompress("1_compressed.bin")
