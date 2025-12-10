import requests
import os
import platform
import subprocess
import tempfile
import time
import urllib3

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
            printer_name = None
            
            try:
                result = subprocess.run(
                    ["lpstat", "-d"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in result.stdout.split('\n'):
                    if 'system default destination:' in line:
                        printer_name = line.split('system default destination:')[1].strip()
                        break
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            
            if not printer_name:
                try:
                    result = subprocess.run(
                        ["lpstat", "-p"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    for line in result.stdout.split('\n'):
                        if line.startswith('printer '):
                            printer_name = line.split()[1]
                            # Preferir impresora Zebra si está disponible
                            if 'ZTC' in printer_name or 'Zebra' in printer_name:
                                break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
            
            try:
                if printer_name:
                    print(f"Imprimiendo en: {printer_name}")
                    subprocess.run(["lp", "-d", printer_name, tmp_file], check=True)
                else:
                    subprocess.run(["lp", tmp_file], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                try:
                    if printer_name:
                        subprocess.run(["lpr", "-P", printer_name, tmp_file], check=True)
                    else:
                        subprocess.run(["lpr", tmp_file], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print(f"Error: No se pudo imprimir. Impresora: {printer_name or 'no encontrada'}")
                    raise
            
        time.sleep(5)
        
    else:
        print(f"Error: {response.status_code}")

except Exception as e:
    print(e)

#editor del cup: http://localhost:631/printers/ZTC-GK420t
#manual https://support-new.zebra.com/es/article/Install-CUPS-Driver-for-Zebra-Printer-in-Mac-OS?language=en_US