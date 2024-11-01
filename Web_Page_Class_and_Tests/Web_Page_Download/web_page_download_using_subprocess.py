import subprocess

def download_web_page(url: str, output_dir: str = "wget_web_page"): 
    try:
        command = ["wget", "-p", "-k", url, "-P", f"./{output_dir}/"]
        subprocess.run(command) 
        url_new = url.replace("https://", "")
        web_page_dir = f"./{output_dir}/{url_new}/index.html"
        return {"is_successful": True, "web_page_dir": web_page_dir}
    except Exception: 
        raise Exception
    
def download_web_page_mozilla_auth(url: str, output_dir: str = "wget_web_page"): 
    try:
        command = ["wget", "--no-proxy", "-p", "-k", "-U", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4", url, "-P", f"./Web_Page_Class_and_Tests/{output_dir}/"]
        subprocess.run(command) 
        url_new = url.replace("https://", "")
        web_page_dir = f"./{output_dir}/{url_new}/index.html"
        return {"is_successful": True, "web_page_dir": web_page_dir}
    except Exception: 
        raise Exception