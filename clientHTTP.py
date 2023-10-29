import socket
import sys
from PIL import Image
from io import BytesIO

USER_AGENTS_MAP = {
    1 : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3",
    2: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    3: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class HttpClient:
    def __init__(self, host, url, port, user_agent, encoding, connection):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.url = url
        self.port = port
        self.user_agent = user_agent
        self.encoding = encoding
        self.connection = connection
        self.accept = "text/html"
        self.accept_charset = "utf-8, iso-8859-1;q=0.7, *;q=0.9"
        self.language = "*"
        
    def connect(self):
        self.sock.connect((self.host, self.port))
        
    def close(self):
        self.sock.close()
    
    def send_request(self, url):
        self.sock.send(url)
        
    def make_TCPrequest(self, http_method):
        if http_method not in ['GET', 'HEAD']:
            raise ValueError("El método debe ser GET o HEAD, no se permite otro")
        
        self.connect()
        
        url_request = f"{http_method} {self.url} HTTP/1.1\r\nHost: {self.host}\r\nUser-Agent: {self.user_agent}\r\nAccept: {self.accept}\r\nAccept-Charset: {self.accept_charset}\r\n Accept-Language: {self.language}\r\n\r\n"
        url_encoded = url_request.encode("utf-8")
        self.send_request(url_encoded)
        
        response = b""
        while True:
            chunk = self.sock.recv(1024)
            if len(chunk) == 0:    
                break
            response = response + chunk
            
        self.close()
        
        headers, content = response.split(b"\r\n\r\n", 1)
        
        is_image = False
        
        
        if b"200 OK" in headers:
            content_type = headers.lower().decode('utf-8')
            if "content-type: image/" in content_type:
                is_image = True
        else:
            return f"Problema al conectar con el host: {self.host}"
                
        if is_image:
            image = Image.open(BytesIO(content))
            image.show()
            
            return "La respuesta es una imagen, por lo cual intentar hacer un decode() con la respuesta causaría un error\n por lo cual sólo se muestra la imagen"
                    
        return response.decode("utf-8")
    
def use_message():
    msg = "\n\nPara usar el programa se debe correr de la siguiente manera:\n"
    msg += '\t python3 http_client.py host http_method url user_agent encoding connection\n\n'
    
    msg += "Los campos de host, http_method, url, enconding y connection tienen que ser proporcionados por el usuario\n\n"
    msg += "Los métodos que se puede poner en el campo de http_method son únicamente: GET y HEAD\n\n"
    
    msg += "Para el campo de user_agent se debe poner un número entre 1 y 3, los cuales corresponden a las opciones disponibles. A continuación se muestran:\n\n"
    
    for i in range(1, 4):
        msg += f"\t {i} : {USER_AGENTS_MAP[i]}\n"
    
    msg += "\n"
    msg += "Un ejemplo de como usar el programa se muestra a continuación:\n\n"
    msg += "\t python3 http_client.py mail7.unam.mx GET / 1 identity close"
    
    return msg
    
def get_args():
      
    args_map = {
        "host": sys.argv[1],
        "http_method" : sys.argv[2],
        "url" : sys.argv[3],
        "user_agent" : sys.argv[4],
        "encoding" : sys.argv[5],
        "connection" : sys.argv[6]
    }
    
    return args_map


if __name__ == '__main__':
    if len(sys.argv) != 7:
        print(use_message())
    else:
        args_map = get_args()
        
        client = HttpClient(args_map["host"], args_map["url"], 80, USER_AGENTS_MAP[int(args_map["user_agent"])], args_map["encoding"], args_map["connection"])
        response = client.make_TCPrequest(args_map["http_method"])
        
        print(response)