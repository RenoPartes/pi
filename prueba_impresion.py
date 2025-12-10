import requests
import os
import platform
import subprocess
import tempfile
import time

url = "https://cc.paquetexpress.com.mx:8082/wsReportPaquetexpress/GenCartaPorte?trackingNoGen=111229071587&measure=4x6"

try:
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        tmp_file = tempfile.mktemp(suffix=".pdf")
        
        with open(tmp_file, "wb") as f:
            f.write(response.content)

        system_name = platform.system()

        if system_name == "Windows":
            os.startfile(tmp_file, "print")
        else:
            subprocess.run(["lpr", tmp_file])
            
        time.sleep(5)
        
    else:
        print(f"Error: {response.status_code}")

except Exception as e:
    print(e)