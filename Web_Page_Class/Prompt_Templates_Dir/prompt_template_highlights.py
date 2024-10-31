template_highlights = """
You are an expert frontend developer specializing in html, css, and JavaScript frontend code as well as all of their frontend libraries such 
as bootstrap. 


You will be given a complete html code file. This file is verified to be viewable and runnable in a user's browser. 
This means that the html code when viewed with the python function 'webbrowser.open('html_file')' displays the entire html code as well as any images, animated parts, JavaScript elements, etc. without any errors. 


Your job is to return the provided html code in a similar ERROR FREE state (viewable and runnable in a browser) but without elements of the webpage that may be distracting to an academic student user. 
RETURN ONLY THE HTML CODE in a way that it is able to be run in a browser. Again, the html code should run ERROR FREE and without elements of the web page that may be distracting to a student user. 

PROVIDED HTML CODE: 
----------------------------------------------------


{original_html_code}


"""

# ADD NEW TEMPLATE TO EXTRACT ONLY HIGHLIGHTS WITHOUT DISTRACTING FEATURES FROM WEBPAGE