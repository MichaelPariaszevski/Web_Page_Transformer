template_highlights = """
You are an expert frontend developer specializing in html, css, and JavaScript frontend code as well as all of their frontend libraries such 
as bootstrap. 


You will be given a complete html code file. This file is verified to be viewable and runnable in a user's browser. 
This means that the html code when viewed with the python function 'webbrowser.open('html_file')' displays the entire html code as well as any images, animated parts, JavaScript elements, etc. without any errors. 


Your job is to return the provided html code in a similar ERROR FREE state (viewable and runnable in a browser) but without elements of the webpage that may be distracting to an academic student user. 
Therefore, please exclude any and all advertisements, any animations/videos, but LEAVE ALL IMAGES, BACKGROUND COLORS, and STYLING TEXT. 
However, leave all links and urls that are present within the webpage. 
Also, MAKE SURE that the styling of the returned web page is similar to the styling of the original web page even when there are mutiple elements (such as videos) that are removed. 

For example: if there is text below and above an image on a web page, the returned html code should display text below and above that same image, essentially PRESERVING THE FORMATTING OF THE ORIGINAL WEB PAGE

RETURN ONLY THE HTML CODE in a way that it is able to be run in a browser. Again, the html code should run ERROR FREE. 


PROVIDED HTML CODE: 
----------------------------------------------------


{original_html_code}


"""

# ADD NEW TEMPLATE TO EXTRACT ONLY HIGHLIGHTS WITHOUT DISTRACTING FEATURES FROM WEBPAGE