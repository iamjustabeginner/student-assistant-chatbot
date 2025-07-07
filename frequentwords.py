import os
import glob
from collections import Counter
import re

def count_words_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        words = re.findall(r'\b\w+\b', content.lower())  # Extract words and convert to lowercase
        return words

def count_words_in_directory(directory_path):
    total_words = []
    # Get all markdown files in the directory
    markdown_files = glob.glob(os.path.join(directory_path, '**/*.md'), recursive=True)
    
    for md_file in markdown_files:
        total_words.extend(count_words_in_file(md_file))
    
    return total_words

def get_top_frequent_words(words, top_n=10):
    word_count = Counter(words)
    return word_count.most_common(top_n)

# Specify the directory where your markdown files are stored
directory_path = '/home/subin/Desktop/subin/ritsu_bot/markdown_files'

# Get all words from the dataset
all_words = count_words_in_directory(directory_path)

# Get total word count
total_word_count = len(all_words)
print(f"Total number of words in the dataset: {total_word_count}")

# Get top 10 most frequent words
top_10_words = get_top_frequent_words(all_words, top_n=10)
print("Top 10 most frequent words:")
for word, count in top_10_words:
    print(f"{word}: {count} times")
