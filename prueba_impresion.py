import requests
import os
import platform
import subprocess
import tempfile
import time
import urllib3

# Suprimir advertencias de certificados SSL no verificados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
            # Usar lp (CUPS) en Linux/Raspberry Pi, o lpr como fallback
            try:
                subprocess.run(["lp", tmp_file], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback a lpr si lp no está disponible
                try:
                    subprocess.run(["lpr", tmp_file], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("Error: No se encontró comando de impresión (lp o lpr)")
                    raise
            
        time.sleep(5)
        
    else:
        print(f"Error: {response.status_code}")

except Exception as e:
    print(e)