import requests
import argparse

def parse_request(request_template):
    lines = request_template.strip().split("\n")
    method, url, _ = lines[0].split(" ", 2)
    headers = {}
    body = ""
    is_body = False

    for line in lines[1:]:
        if not line.strip():  # Detecta la línea en blanco entre los headers y el body
            is_body = True
            continue
        
        if is_body:
            body += line + "\n"
        else:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value

    return method, url, headers, body.strip()

def fuzz_request(request_template, wordlist, placeholder, target_url):
    method, url, headers, body = parse_request(request_template)
    url = target_url  # Se usa la URL proporcionada en los argumentos
    
    with open(wordlist, "r", encoding="utf-8") as f:
        for word in f:
            word = word.strip()
            payload = body.replace(placeholder, word)
            print(f"[*] Probando: {word}")
            
            response = requests.request(method, url, headers=headers, data=payload, allow_redirects=False)
            print(f"[+] Código de respuesta: {response.status_code}\n")

            if response.status_code == 200:
                print(f"[!] Posible éxito con: {word}")
                break

def main():
    parser = argparse.ArgumentParser(description="Simple Intruder para fuzzing de credenciales en HTTP.")
    parser.add_argument("-r", "--request", required=True, help="Archivo con la solicitud HTTP en formato raw.")
    parser.add_argument("-w", "--wordlist", required=True, help="Archivo con la lista de palabras.")
    parser.add_argument("-p", "--placeholder", required=True, help="Marcador a reemplazar en la solicitud.")
    parser.add_argument("-u", "--url", required=True, help="URL objetivo.")
    
    args = parser.parse_args()
    
    with open(args.request, "r", encoding="utf-8") as f:
        request_template = f.read()
    
    fuzz_request(request_template, args.wordlist, args.placeholder, args.url)

if __name__ == "__main__":
    main()
