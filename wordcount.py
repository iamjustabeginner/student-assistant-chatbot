import os
import glob

def count_words_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return len(content.split())

def count_words_in_directory(directory_path):
    total_words = 0
    # Get all markdown files in the directory
    markdown_files = glob.glob(os.path.join(directory_path, '**/*.md'), recursive=True)
    
    for md_file in markdown_files:
        total_words += count_words_in_file(md_file)
    
    return total_words

# Specify the directory where your markdown files are stored
directory_path = '/home/subin/Desktop/subin/ritsu_bot/markdown_files'

total_word_count = count_words_in_directory(directory_path)
print(f"Total number of words in the dataset: {total_word_count}")
