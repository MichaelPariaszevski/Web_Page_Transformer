template_chunks = """
You are an expert frontend developer specializing in html, css, and JavaScript frontend code as well as all of their frontend libraries such 
as bootstrap and tailwind. 


You will be given a chunk of some html. This chunk was taken from a complete html file that was verified to be viewable and runnable in a user's browser. 
This means that the total html code file, when viewed with the python function 'webbrowser.open('html_file')', displays the entire html code as well as any images, animated parts, JavaScript elements, etc. without any errors. 


Your job is to return the provided html code in a similar ERROR FREE state (viewable and runnable in a browser) but without elements of the webpage that may be distracting to an academic student user. 
Therefore, please exclude any and all advertisements, any animations/videos, but LEAVE ALL IMAGES, BACKGROUND COLORS, and STYLING TEXT. 
However, leave all links and urls that are present within the webpage. 
Also, MAKE SURE that the styling of the returned web page is similar to the styling of the original web page even when there are mutiple elements (such as videos) that are removed. 

For example: if there is text below and above an image on a web page, the returned html code should display text below and above that same image, essentially PRESERVING THE FORMATTING OF THE ORIGINAL WEB PAGE

RETURN ONLY THE HTML CODE CHUNK, do not try to fill in or complete the entire html file because the chunk that is outputted will be paired with subsequent html code chunks. 

That being said, always treat the provided html chunk as a part of an entire html file, therefore when the outputted html chunk is combined with other html chunks from that same original file, the entire view should be runnable and viewable in a browser. 

RETURN ONLY VALID HTML CODE

PROVIDED HTML CODE: 
----------------------------------------------------

{original_html_code_chunks}


"""