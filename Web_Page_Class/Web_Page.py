from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from Web_Page_Download.web_page_download_using_subprocess import download_web_page, download_web_page_mozilla_auth
import webbrowser
from pathlib import Path

template_images_removed = """
You are an expert frontend developer specializing in html, css, and JavaScript frontend code as well as all of their frontend libraries such 
as bootstrap. 


You will be given a complete html code file. This file is verified to be viewable and runnable in a user's browser. 
This means that the html code when viewed with the python function 'webbrowser.open('html_file')' displays the entire html code as well as any images, animated parts, JavaScript elements, etc. without any errors. 


Your job is to return the provided html code in a similar ERROR FREE state (viewable and runnable in a browser) but without elements of the webpage such as images, animations, and pictures that may be distracting to an academic student user. 
RETURN ONLY THE HTML CODE in a way that it is able to be run in a browser. Again, the html code should run ERROR FREE and without elements of the web page, ONLY images, animations, and pictures, that may be distracting to a student user. 

PROVIDED HTML CODE: 
----------------------------------------------------


{original_html_code}


"""

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
            self.downloaded, self.output_dir = self.download_page()
        elif download and path_exists_bool: 
            self.downloaded = True 
            self.output_dir = self.expected_output_dir
        else: 
            self.downloaded = False 
            self.output_dir = None
        # self.output_dir = f"./wget_web_page/{url}/index.html"
    
    def path_exists(self): 
        p = Path(self.expected_output_dir) 
        return p.exists()
    
    def download_page(self) -> dict: 
        output_dict = download_web_page_mozilla_auth(url = self.url)
        return output_dict["is_successful"], output_dict["web_page_dir"]
    
    def html_var(self, output_dir) -> str: 
        with open(output_dir, "r") as file: 
            html_output = file.read() 
        return html_output
        
    def view_page(self) -> None: 
        webbrowser.open(url = self.output_dir)
        
    def llm_edit_page(self) -> str: 
        html_original = self.html_var(self.output_dir)
        prompt_template_images_removed = ChatPromptTemplate.from_template(template = template_images_removed) 
        html_editor_chain_images_removed = prompt_template_images_removed | llm
        html_editor_chain_images_removed.invoke(input = {"original_html_code": html_original})
        
# web_page_example = WebPage(url = "https://www.selenium.dev")
        