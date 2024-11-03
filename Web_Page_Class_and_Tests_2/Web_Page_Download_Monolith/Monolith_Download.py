import os 
import subprocess
import warnings

def monolith_download_new_2(url: str, output_dir: str): # does not display certain visual elements such as windows and animations when using "-I" or "-k"; use "-b <url> -n" instead
    command = ["chromium", "--headless", "--window-size=1920,1080", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=9000", "--incognito", "--dump-dom", url, "|", "monolith", "-", "-b", url, "-n", "-o", output_dir]
    env = os.environ.copy()
    env["DBUS_SESSION_BUS_ADDRESS"] = ""
    with warnings.catch_warnings(): 
        warnings.simplefilter("ignore")
        subprocess.run(" ".join(command), capture_output=True, text=True, env=env, shell=True)
    return output_dir 

def monolith_download_new_3(url: str, output_dir: str): # does not display certain visual elements such as windows and animations when using "-I" or "-k"; use "-b <url> -n" instead
    command = ["chromium", "--headless", "--window-size=1920,1080", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=9000", "--incognito", "--dump-dom", url, "|", "monolith", "-", "-b", url, "-o", output_dir]
    env = os.environ.copy()
    env["DBUS_SESSION_BUS_ADDRESS"] = ""
    with warnings.catch_warnings(): 
        warnings.simplefilter("ignore")
        subprocess.run(" ".join(command), capture_output=True, text=True, env=env, shell=True)
    return output_dir

# monolith_download_new_3 displays more visual elements compared to monolith_download_new_2 
# monolith_download_new_3 uses only "-b" and "-o"
# monolith_download_new_2 uses "-b", "-o", and "-n"