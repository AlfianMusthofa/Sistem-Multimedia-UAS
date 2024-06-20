import heapq
from collections import defaultdict

# Huffman Node class
class HuffmanNode:
    def __init__(self, left=None, right=None, symbol=None, freq=0):
        self.left = left
        self.right = right
        self.symbol = symbol
        self.freq = freq
    
    def __lt__(self, other):
        return self.freq < other.freq

# Function to build the Huffman Tree
def build_huffman_tree(symbols_with_freqs):
    heap = [HuffmanNode(symbol=symbol, freq=freq) for symbol, freq in symbols_with_freqs.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left=left, right=right, freq=left.freq + right.freq)
        heapq.heappush(heap, merged)
    
    return heap[0]

# Function to build the Huffman Codes
def build_huffman_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.symbol is not None:
            codebook[node.symbol] = prefix
        build_huffman_codes(node.left, prefix + "0", codebook)
        build_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encoding(data):
    if data.size == 0:
        return "", {}

    # Calculate frequency of each symbol
    symbol_freqs = defaultdict(int)
    for symbol in data.flatten():
        symbol_freqs[symbol] += 1

    # Build Huffman Tree
    huffman_tree = build_huffman_tree(symbol_freqs)
    
    # Build Huffman Codes
    huffman_codes = build_huffman_codes(huffman_tree)
    
    # Encode data
    encoded_data = ''.join(huffman_codes[symbol] for symbol in data.flatten())
    
    return encoded_data, huffman_codes

def arithmetic_encoding(data):
    if data.size == 0:
        return "", {}

    # Calculate frequency of each symbol
    symbol_freqs = defaultdict(int)
    for symbol in data.flatten():
        symbol_freqs[symbol] += 1
    
    total_symbols = sum(symbol_freqs.values())
    probabilities = {symbol: freq / total_symbols for symbol, freq in symbol_freqs.items()}
    
    # Calculate cumulative probabilities
    cumulative_prob = {}
    cum_prob = 0
    for symbol, prob in sorted(probabilities.items()):
        cumulative_prob[symbol] = cum_prob
        cum_prob += prob
    
    low = 0.0
    high = 1.0
    for symbol in data.flatten():
        range_width = high - low
        high = low + range_width * (cumulative_prob[symbol] + probabilities[symbol])
        low = low + range_width * cumulative_prob[symbol]
    
    return (low + high) / 2, probabilities
