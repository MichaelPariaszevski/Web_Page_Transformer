from bs4 import BeautifulSoup

def split_html(html_content, max_chunk_size=5000):
    soup = BeautifulSoup(html_content, 'html.parser')
    chunks = []
    current_chunk = ''
    current_size = 0

    # Iterate over direct children of the body
    for element in soup.body.contents:
        html_string = str(element)
        element_size = len(html_string)

        if current_size + element_size > max_chunk_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = ''
            current_size = 0

        current_chunk += html_string
        current_size += element_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks