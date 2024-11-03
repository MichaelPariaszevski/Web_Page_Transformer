import os
import webbrowser
from pathlib import Path
from dotenv import load_dotenv, find_dotenv 
from langchain_core.prompts import ChatPromptTemplate
from Web_Page_Class_and_Tests_2.Web_Page_Download_Monolith.Monolith_Download import monolith_download_new_2, monolith_download_new_3
from Web_Page_Class_and_Tests_2.Web_Page_Prompt_Templates.Highlights_with_HTML_Text import template_highlights_with_html_text
from Web_Page_Class_and_Tests_2.Web_Page_Functions.Unstructured_HTML_Loader import unstructured_html_loader
from Web_Page_Class_and_Tests_2.Web_Page_Functions.LLM_Selection import llm_selection

load_dotenv(find_dotenv(), override = True)

class WebPage(): 
    def __init__(self, url, llm_model = "gpt-4o-mini"): 
        self.url = url 
        self.llm_model = llm_selection(model = llm_model)
        self.truncated_url = url.replace("https://", "")
        self.output_dir = f"html_links/{self.truncated_url}.html" 
        self.edited_page_dir = f"html_links/{self.truncated_url}_edited.html"
        self.html_text: str
    
    def path_exists(self) -> bool: 
        p = Path(self.output_dir) 
        return p.exists()
    
    def download_page(self) -> dict: 
        output_dir_2 = self.truncated_url + ".html"
        if not self.path_exists(): 
            self.output_dir = monolith_download_new_3(url = self.url, output_dir = output_dir_2)
        return self.output_dir
    
    def download_page_to_folder(self) -> dict: 
        output_dir_2 = self.truncated_url + ".html"
        if not self.path_exists(): 
            temp_dir = monolith_download_new_3(url = self.url, output_dir = output_dir_2)
            output_file = Path(self.output_dir)
            output_file.parent.mkdir(exist_ok = True, parents = True)
            with open(temp_dir, "r") as file_read: 
                html = file_read.read()
                output_file.write_text(html)
            if os.path.exists(output_dir_2): 
                os.remove(output_dir_2) 
                print("'output_dir_2' deleted successfully")
            else: 
                print("'output_dir_2' does not exist")
            return self.output_dir
        return "Page already downloaded", self.output_dir
    
    def html_text(self) -> str: 
        self.html_text = unstructured_html_loader(self.output_dir)
        return self.html_text
    
    def _html_var(self) -> str: 
        with open(self.output_dir, "r") as file: 
            html_output = file.read() 
        return html_output
            
    def llm_edit_page(self) -> str: 
        html_input = self._html_var()
        prompt_template = ChatPromptTemplate.from_template(template = template_highlights_with_html_text) 
        chain = prompt_template | self.llm_model 
        output = chain.invoke(input = {"html_text": self.html_text, "original_html_code": html_input}) 
        edited_html = output.content 
        with open(self.edited_page_dir, "w") as file: 
             file.write(edited_html) 
        return self.edited_page_dir, True
    
    def view_page(self) -> None: 
        if self.path_exists(): 
            webbrowser.open(url = self.output_dir)
        else: 
            raise AssertionError("the method 'download_page()' must first be executed before 'view_page()'")
        
    def view_edited_page(self) -> None: 
        webbrowser.open(url = self.edited_page_dir)
        
        
        