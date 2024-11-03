from typing_extensions import TypedDict
from typing import Annotated 
from operator import add
from Web_Page_Class_and_Tests.Web_Page import WebPage

class Web_Page_Transformer_State(TypedDict): 
    url: str
    web_page_object: WebPage
    html_original: str 
    html_original_text: str 
    improvement_instructions: Annotated[list[str], add] 
    html_edited: str
    html_edited_final_dir: str 
    finished_improvements: bool 