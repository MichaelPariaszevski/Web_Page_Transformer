from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from Web_Page_Download.web_page_download_using_subprocess import download_web_page, download_web_page_mozilla_auth
import webbrowser
from pathlib import Path
from Prompt_Templates_Dir.prompt_template_org import template_original
from Prompt_Templates_Dir.prompt_template_img import template_images_removed
from Prompt_Templates_Dir.prompt_template_highlights import template_highlights
from Prompt_Templates_Dir.prompt_template_highlights_with_html_text import template_highlights_with_html_text
from Web_Page_Class_Functions.Unstructured_HTML_Loader_Function import unstructured_html_loader

llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)

class WebPage(): 
    template_images_removed: str
    llm: ChatOpenAI
    
    def __init__(self, url, download = True): 
        self.url = url
        # self.expected_output_dir = f"./wget_web_page/{self.url}/index.html"
        self.truncated_url = url.replace("https://", "")
        self.expected_output_dir = f"./wget_web_page/{self.truncated_url}/index.html"
        path_exists_bool = self.path_exists()
        if download and not path_exists_bool: 
            self.downloaded, self.output_dir, self.html_text = self.download_page()
        elif download and path_exists_bool: 
            self.downloaded = True 
            self.output_dir = self.expected_output_dir
            self.html_text = unstructured_html_loader(self.output_dir)
        else: 
            self.downloaded = False 
            self.output_dir = None
        # self.output_dir = f"./wget_web_page/{url}/index.html"
        self.edited_page_dir = f"./wget_web_page/{self.truncated_url}/index_edited.html"
    
    def path_exists(self) -> bool: 
        p = Path(self.expected_output_dir) 
        return p.exists()
    
    def download_page(self) -> dict: 
        output_dict = download_web_page_mozilla_auth(url = self.url)
        html_text = unstructured_html_loader(output_dict["web_page_dir"])
        # self.html_text = html_text
        return output_dict["is_successful"], output_dict["web_page_dir"], html_text
    
    
    def html_var(self, output_dir) -> str: 
        with open(output_dir, "r") as file: 
            html_output = file.read() 
        return html_output
        
    def view_page(self) -> None: 
        webbrowser.open(url = self.output_dir)
        
    def view_edited_page(self) -> None: 
        webbrowser.open(url = self.edited_page_dir)
        
    def llm_edit_page(self) -> str: 
        html_original = self.html_var(self.output_dir)
        html_text = self.html_text
        prompt_template = ChatPromptTemplate.from_template(template = template_highlights_with_html_text) 
        html_editor_chain_images_removed = prompt_template | llm
        output = html_editor_chain_images_removed.invoke(input = {"html_text": html_text, "original_html_code": html_original})
        edited_html = output.content
        with open(self.edited_page_dir, "w") as file: 
            file.write(edited_html)
        return self.edited_page_dir
        
        
        