from config import *

if __name__ == "__main__":
    
    @app.route("/")
    def rota():
        print("Teste")