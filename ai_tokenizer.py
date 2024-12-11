from collections import Counter
from typing import List, Dict, Set, Tuple
import re
import json
import math
from dataclasses import dataclass
import heapq
from itertools import combinations

@dataclass
class Phrase:
    words: Tuple[str, ...]
    count: int
    total_chars: int
    compressed_chars: int
    
    @property
    def savings(self) -> int:
        """Calculate space savings for this phrase"""
        # Original size: words + spaces between them, times number of occurrences
        original_size = self.total_chars * self.count
        # Compressed size: replacement token * occurrences + one-time definition cost
        compressed_size = self.compressed_chars * self.count + self.total_chars + len(str(len(self.words)))
        return original_size - compressed_size
    
    def __lt__(self, other):
        return self.savings < other.savings

class AdaptiveCompressor:
    def __init__(self, min_phrase_len: int = 2, max_phrase_len: int = 6, 
                 min_occurrences: int = 3, max_phrases: int = 1000):
        self.min_phrase_len = min_phrase_len
        self.max_phrase_len = max_phrase_len
        self.min_occurrences = min_occurrences
        self.max_phrases = max_phrases
        self.compression_dict: Dict[Tuple[str, ...], str] = {}
        self.decompression_dict: Dict[str, Tuple[str, ...]] = {}
        self.next_token_id = 0
        
    def _tokenize(self, text: str) -> List[str]:
        """Split text into words while preserving important whitespace and punctuation"""
        return re.findall(r'\S+|\s+', text)
        
    def _generate_token(self) -> str:
        """Generate a unique token for compression"""
        token = f"@T{self.next_token_id}@"
        self.next_token_id += 1
        return token
        
    def _find_phrases(self, words: List[str]) -> List[Phrase]:
        """Find repeated phrases in text"""
        # First pass: count all possible phrases
        phrase_counts: Dict[Tuple[str, ...], int] = Counter()
        phrase_chars: Dict[Tuple[str, ...], int] = {}
        
        for i in range(len(words)):
            for length in range(self.min_phrase_len, min(self.max_phrase_len + 1, len(words) - i + 1)):
                phrase = tuple(words[i:i+length])
                # Only count phrases that don't cross sentence boundaries
                if not any(w.strip() in '.!?' for w in phrase[:-1]):
                    phrase_counts[phrase] += 1
                    if phrase not in phrase_chars:
                        phrase_chars[phrase] = sum(len(w) for w in phrase)
        
        # Filter and create Phrase objects
        phrases = []
        for phrase, count in phrase_counts.items():
            if count >= self.min_occurrences:
                total_chars = phrase_chars[phrase]
                compressed_chars = len(self._generate_token())  # simulate token generation
                phrases.append(Phrase(
                    words=phrase,
                    count=count,
                    total_chars=total_chars,
                    compressed_chars=compressed_chars
                ))
        
        # Sort by savings and return top phrases
        return sorted(phrases, key=lambda x: -x.savings)[:self.max_phrases]
    
    def _build_compression_dict(self, phrases: List[Phrase]):
        """Build compression dictionary from identified phrases"""
        self.compression_dict.clear()
        self.decompression_dict.clear()
        
        for phrase in phrases:
            if phrase.savings > 0:  # Only include if it actually saves space
                token = self._generate_token()
                self.compression_dict[phrase.words] = token
                self.decompression_dict[token] = phrase.words
    
    def compress(self, text: str) -> Tuple[str, dict]:
        """Compress text by identifying and replacing common phrases"""
        words = self._tokenize(text)
        
        # Find repeated phrases
        phrases = self._find_phrases(words)
        
        # Build compression dictionary
        self._build_compression_dict(phrases)
        
        # Compress text by replacing phrases
        compressed_words = []
        i = 0
        stats = {
            'original_length': len(text),
            'phrases_found': len(phrases),
            'phrases_used': len(self.compression_dict),
            'replacements': Counter()
        }
        
        while i < len(words):
            replaced = False
            # Try to match longest phrases first
            for length in range(self.max_phrase_len, self.min_phrase_len - 1, -1):
                if i + length <= len(words):
                    phrase = tuple(words[i:i+length])
                    if phrase in self.compression_dict:
                        compressed_words.append(self.compression_dict[phrase])
                        stats['replacements'][' '.join(phrase)] += 1
                        i += length
                        replaced = True
                        break
            if not replaced:
                compressed_words.append(words[i])
                i += 1
        
        compressed_text = ''.join(compressed_words)
        stats['compressed_length'] = len(compressed_text)
        stats['compression_ratio'] = 1 - (len(compressed_text) / len(text))
        
        return compressed_text, stats
    
    def decompress(self, text: str) -> str:
        """Decompress text by replacing tokens with original phrases"""
        # Sort tokens by length (longest first) to avoid partial matches
        tokens = sorted(self.decompression_dict.keys(), key=len, reverse=True)
        pattern = '|'.join(re.escape(token) for token in tokens)
        
        def replace_func(match):
            token = match.group(0)
            return ''.join(self.decompression_dict[token])
            
        if tokens:  # Only try to replace if we have tokens
            text = re.sub(pattern, replace_func, text)
        return text
    
    def save_compression_map(self, file):
        """Save compression mapping to file"""
        mapping = {
            'compression': {' '.join(k): v for k, v in self.compression_dict.items()},
            'decompression': {k: list(v) for k, v in self.decompression_dict.items()}
        }
        # Handle both filenames and file objects
        if isinstance(file, str):
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(mapping, f, indent=2)
        else:
            json.dump(mapping, file, indent=2)
    
    def load_compression_map(self, filename: str):
        """Load compression mapping from file"""
        with open(filename, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        self.compression_dict = {tuple(k.split()): v for k, v in mapping['compression'].items()}
        self.decompression_dict = {k: tuple(v) for k, v in mapping['decompression'].items()}
        self.next_token_id = max(int(re.search(r'\d+', token).group()) for token in self.decompression_dict.keys()) + 1

def main():
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Adaptive text compression utility')
    
    # Add the help epilog
    parser.epilog = """
    Single-file Usage (for Claude):
        When only input_file is provided, outputs a complete package to stdout containing:
        1. Instructions for Claude
        2. Compression mapping
        3. Compressed text
        This output can be directly pasted to Claude for decompression.

    Two-file Usage:
        When both input_file and output_file are provided, operates in normal mode:
        - Compressing: Creates compressed output and optional mapping file
        - Decompressing: Requires mapping file to restore original text
    """
    parser.add_argument('input_file', help='Input file to process')
    parser.add_argument('output_file', nargs='?', help='Output file for processed text. If omitted, writes Claude-ready package to stdout')
    parser.add_argument('--decompress', action='store_true', help='Decompress instead of compress')
    parser.add_argument('--min-phrase-len', type=int, default=2, help='Minimum phrase length')
    parser.add_argument('--max-phrase-len', type=int, default=6, help='Maximum phrase length')
    parser.add_argument('--min-occurrences', type=int, default=3, help='Minimum phrase occurrences')
    parser.add_argument('--max-phrases', type=int, default=1000, help='Maximum number of phrases to use')
    parser.add_argument('--compression-map', help='File to save/load compression mapping')
    
    args = parser.parse_args()
    
    compressor = AdaptiveCompressor(
        min_phrase_len=args.min_phrase_len,
        max_phrase_len=args.max_phrase_len,
        min_occurrences=args.min_occurrences,
        max_phrases=args.max_phrases
    )
    
    # Read input file
    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if args.output_file is None:
        # Single-file mode: output Claude-ready package to stdout
        compressed, stats = compressor.compress(text)
        
        # Create temporary mapping file in memory
        import io
        map_file = io.StringIO()
        compressor.save_compression_map(map_file)
        mapping_content = map_file.getvalue()
        
        # Output the complete package
        print("Decompress this text, then just answer with 'Text successfully decompressed` "
              "if so, otherwise respond with whatever problem. The compression mapping:")
        print(mapping_content)
        print("\nCompressed text:")
        print(compressed)
        
        # Print stats to stderr so they don't interfere with the Claude-ready output
        print("\nCompression Statistics:", file=sys.stderr)
        print(f"Original length: {stats['original_length']} characters", file=sys.stderr)
        print(f"Compressed length: {stats['compressed_length']} characters", file=sys.stderr)
        print(f"Compression ratio: {stats['compression_ratio']:.2%}", file=sys.stderr)
        print(f"Phrases found: {stats['phrases_found']}", file=sys.stderr)
        print(f"Phrases used: {stats['phrases_used']}", file=sys.stderr)
        
        if stats['replacements']:
            print("\nTop 10 most replaced phrases:", file=sys.stderr)
            for phrase, count in sorted(stats['replacements'].items(), key=lambda x: (-x[1], x[0]))[:10]:
                print(f"- '{phrase}' replaced {count} times", file=sys.stderr)
    
    else:
        # Two-file mode: normal operation
        if args.decompress:
            if not args.compression_map:
                parser.error("Decompression requires --compression-map")
            compressor.load_compression_map(args.compression_map)
            result = compressor.decompress(text)
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Text decompressed and saved to {args.output_file}")
        else:
            compressed, stats = compressor.compress(text)
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(compressed)
            
            if args.compression_map:
                compressor.save_compression_map(args.compression_map)
            
            print("\nCompression Statistics:")
            print(f"Original length: {stats['original_length']} characters")
            print(f"Compressed length: {stats['compressed_length']} characters")
            print(f"Compression ratio: {stats['compression_ratio']:.2%}")
            print(f"Phrases found: {stats['phrases_found']}")
            print(f"Phrases used: {stats['phrases_used']}")
            
            if stats['replacements']:
                print("\nTop 10 most replaced phrases:")
                for phrase, count in sorted(stats['replacements'].items(), key=lambda x: (-x[1], x[0]))[:10]:
                    print(f"- '{phrase}' replaced {count} times")

if __name__ == "__main__":
    main()
    