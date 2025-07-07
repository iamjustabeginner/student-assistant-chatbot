import os
import html2text

# Specify the folder containing the HTML files
folder_path = "data"

# Create a folder to store the Markdown files
markdown_folder = "markdown_files"
os.makedirs(markdown_folder, exist_ok=True)

# Iterate over each file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):
        file_path = os.path.join(folder_path, file_name)

        # Read the contents of the file
        with open(file_path, "r") as file:
            html_content = file.read()

        # Convert HTML to Markdown
        markdown_converter = html2text.HTML2Text()
        markdown_converter.wrap_links = False  # Disable link wrapping
        markdown_converter.inline_links = True  # Enable inline links
        markdown_converter.ignore_images = True  # Ignore images
        markdown_converter.ignore_tables = True  # Ignore tables
        markdown_converter.single_line_break = True  # Use single line breaks

        markdown_content = markdown_converter.handle(html_content)

        # Create a new file to store the Markdown content
        markdown_file_path = os.path.join(
            markdown_folder, f"{os.path.splitext(file_name)[0]}.md"
        )
        with open(markdown_file_path, "w") as markdown_file:
            markdown_file.write(markdown_content)

        print(f"Converted {file_name} to Markdown and saved as {markdown_file_path}")
