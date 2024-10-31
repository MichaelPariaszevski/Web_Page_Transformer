from langchain_community.document_loaders import UnstructuredHTMLLoader

def unstructured_html_loader(file_path): 
        loader = UnstructuredHTMLLoader(file_path = file_path) 
        data = loader.load()
        return data[0].page_content