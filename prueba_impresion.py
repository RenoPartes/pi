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
            # Detectar impresora disponible en Linux/Raspberry Pi
            printer_name = None
            
            # Intentar obtener impresora por defecto
            try:
                result = subprocess.run(
                    ["lpstat", "-d"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                # Buscar "system default destination: nombre_impresora"
                for line in result.stdout.split('\n'):
                    if 'system default destination:' in line:
                        printer_name = line.split('system default destination:')[1].strip()
                        break
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            
            # Si no hay impresora por defecto, buscar impresoras disponibles
            if not printer_name:
                try:
                    result = subprocess.run(
                        ["lpstat", "-p"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    # Buscar impresoras disponibles (líneas que empiezan con "printer")
                    for line in result.stdout.split('\n'):
                        if line.startswith('printer '):
                            printer_name = line.split()[1]
                            # Preferir impresora Zebra si está disponible
                            if 'ZTC' in printer_name or 'Zebra' in printer_name:
                                break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
            
            # Intentar imprimir con lp
            try:
                if printer_name:
                    print(f"Imprimiendo en: {printer_name}")
                    subprocess.run(["lp", "-d", printer_name, tmp_file], check=True)
                else:
                    # Intentar sin especificar impresora (usará la predeterminada si existe)
                    subprocess.run(["lp", tmp_file], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                # Fallback a lpr si lp no está disponible
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