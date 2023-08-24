import os
import msvcrt
import time
import sqlite3
from colorama import init, Fore, Style
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
import pyrebase
import pyperclip

init(autoreset=True)

valor_base = 3
valor_por_loop  = 3
corrida_number = 0  # Counter for the number of rides

# Configurações do Firebase
firebase_config = {
    "apiKey": "AIzaSyCJexwdI0AuQ3SmC9ih986MgG0aGHimwZk",
    "authDomain": "taximetro-ad.firebaseapp.com",
    "databaseURL": "https://taximetro-ad-default-rtdb.firebaseio.com",
    "projectId": "taximetro-ad",
    "storageBucket": "taximetro-ad.appspot.com",
    "messagingSenderId": "422125042535",
    "appId": "1:422125042535:web:2ec6059dd793770eb60dc2",
    "measurementId": "G-X1NESHYTFK"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Configurações do Firebase Admin SDK
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "taximetro-ad",
    "private_key_id": "2ea1909432023154696eff53388f0bdef16a166f",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDe8Iek+rfuAwrA\n+ZfhHIggR/yBKxNhMjpYPFEt8Wo+woRJM1kPOwFuCaY59fEi0VLnNZbySPeacEYA\nSGStbESojmnKUFkhnnKlcM5Jgx1aEGAx4tysPH4/I/yb6+cTUz+nzN/V8v1SnhKl\n9oJUMnq8shmpg/Z4fuL/BWun16OL3okUhRVTUZ2vquD/L3rKGb6wmY7vtv1xbAtW\njZNMU1PxkLHzT+ef2GS04RqsFubBvSION1mJz4Y58CobDLMmH4nb6007oz3neKkF\nKhi4ie8iskyMzKms/OlvF+LlrceVxWRmF6FhGoHaCDL3WWx16XS1ZWnpcrzdl7UY\nfIJskXsjAgMBAAECggEAC4Ghlp/EF3o7t1sKfjlhQz1D6IzHGsijX0N5syPXJncW\nqcqHKbSTbdD8rdgmQnRIUZuf91BRyzxJOKGD5LmGT6bOCf2cpBIP+773Pq8QOEJJ\nHLoHRrJ2l56tXoTN797nlasK0HmSno1/C+bNsjfKwut0TJ39fhmacKwgctC75a+V\nd5QKpSmBl4NDwufCzMJSOEOOy6bJLsDKpbzSM8dO7wK3oKorlhTf62/DUJvNea1S\nPHaSNeIEiSyyopExveOIvn7uBNa5tF9ZYMj6p/+RCtc3oH3nNh1ti0lKvR2aCuKZ\n4cAMpYO8h23KVj3beMc8gg3cBukPStzQDKNwKP++gQKBgQD5ht8+7/5XoI1aHU37\n+7r1x/BDfxWjtxyu/DS7t4RH1n6hg6JtY1DkPcVpLUcd7ILgjCWR2AZzlDc/R0US\nUeuxlTOdMAxA7O6VnP0u/O+rGtGh+2stuqh7wqqSsg5yuWHUw7fpONom0pSuGRpQ\nbBdL/eAdPkwx4rZRMbGqOv5AgQKBgQDkuRbuBhJRX1AjdYAJfrQ7tuqHjgb351f/\nCGJOn8g4PjbWBHL+K/7RKIjixm/2bxHsTfnQIv2t3Ci3awI4y6EfOjdwyo8dIwar\nhVy/4aeVPxG2NRUQ7bPafY2qiX9hifViHy51BV69QQW4QUOPB4jgJu/kz2V/ENIb\n2rjFd3npowKBgQC9pcZzPVBgJUSJoxAsXkzglM+FXUeDIJ8KV+F0cqx1NQ8Vjsia\nvwsyDcjGgYU1txZZt+quCDQPEC1VSMO0gtLSK4YJCAWoKuvChojfd5pov39oz3/M\nR7vaJEAkMnRMuZ0jaoWTGoSjURVzpNydFyo1tYTqdPjQSXEsEMrpiODJAQKBgQDg\n4IYF4lxSOwb8xgLr0vJ7n505R8/cH03qRqD5MqnVen3JsDgrZLA1jsf/RyE/xvZ1\nQjkyhaSrMsGpjIFzu+mfXUqzD8Tj3dMqAoYtdjyhRZAxeEFNEph5YmZN3MAr80sa\nfRPdJDmAk5R/E1PMJZlS4ZWNfsgIxU3+6u4t4AkyRwKBgQCJtjHIgUFYqhZq4lGc\nQnprOqgVfySy8uAZbrUAxe0dNd5Dy472/jfXZ+ufcFuNi7XhUpI/jYxI5s69h/b0\nLG1nBsskNaSlSKzLXVa2WYJ1fsR2UAcHCPojkiVwwlszJ1OfXZvN8vGbTAVTIl+y\nzD9WeflYU3ZspFkrbmXzHqo8nQ==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-2ge5g@taximetro-ad.iam.gserviceaccount.com",
    "client_id": "113553896903210996604",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2ge5g%40taximetro-ad.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
})

firebase_app = initialize_app(cred)

db = firestore.client()

def mostrar_painel_login_cadastro():
    while True:
        print("\nTaxi Tools - Painel de Acesso\n")
        print("Escolha uma opção:")
        print("1. Login")
        print("2. Cadastro")
        print("3. Sair\n")

        opcao = int(input("Digite o número da opção desejada: "))

        if opcao == 1:
            user = login_usuario()
            if user is not None:
                return user
        elif opcao == 2:
            if cadastrar_usuario():
                print("Por favor, faça login com a nova conta.")
        elif opcao == 3:
            print("Saindo do programa...")
            return None
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")
    email = input("Digite o e-mail: ")
    senha = input("Digite a senha: ")

    try:
        user = auth.create_user_with_email_and_password(email, senha)
        print("Cadastro realizado com sucesso!")
        return True
    except Exception as e:
        print("Erro ao cadastrar usuário:", e)
        return False

def perguntar_url_foto():
    url = input("Digite o URL da foto do personagem: ")
    return url

def login_usuario():
    print("\n--- Login de Usuário ---")
    email = input("Digite o e-mail: ")
    senha = input("Digite a senha: ")

    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        user = auth.sign_in_with_email_and_password(email, senha)
        print("Login realizado com sucesso!")
        return user
    except Exception as e:
        print("Erro ao fazer login:", e)
        return None

def exibir_menu():
    print('[ADRP]' + Fore.YELLOW + 'Taxi Tools'"\n")
    print("Bem-vindo ao Menu:\n")
    print('1.' + Fore.YELLOW + 'Taxímetro')
    print('2.' + Fore.GREEN + 'Cotação')
    print('3.' + Fore.RED + 'Em Breve')
    print('4.' + Fore.RED + 'Histórico de Corridas')
    print('5.' + Fore.RED + 'Sair'"\n\n\n\n\n\n\n")
    print("|¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨|")
    print("|                                                     |")
    print("|                                                     |")
    print('|' + Fore.RED + '           Desenvolvido por  gabrielsam              ' + Fore.WHITE + '|')
    print("|                                                     |")
    print("|_____________________________________________________|")

def calcular_tarifa_horario():
    current_time = time.localtime()
    hour = current_time.tm_hour

    if 6 <= hour < 12:
          return 5
    elif 12 <= hour < 18:
        return 8
    elif 18 <= hour < 24:
        return 12
    elif 0 <= hour < 6:
        return 15

    return 0

valor_taximetro = calcular_tarifa_horario()

if valor_taximetro is not None:
    valor_base = valor_taximetro
    valor_por_loop = valor_taximetro

def salvar_corrida_atual(num_passageiros, valor_total, user_email):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

    data = {
        "passageiros": num_passageiros,
        "data_hora": formatted_datetime,
        "valor_total": valor_total,
        "email_usuario": user_email
    }

    try:
        db.collection("corridas").document(user_email).collection("corridas").add(data)
        print("Corrida salva no banco de dados.")
    except Exception as e:
        print("Erro ao salvar corrida no banco de dados:", e)

def escrever_mensagem_taximetro(valor_total):
    mensagem = f"/do O taxímetro mostra o valor de US$ {valor_total:.2f}."
    pyperclip.copy(mensagem)
def exibir_historico_corridas(user_id):
    try:
        corridas_ref = db.collection("corridas").document(user_id).collection("corridas")
        # Ordenar as corridas pela chave "data_hora" em ordem decrescente (do mais recente ao mais antigo)
        corridas = corridas_ref.order_by("data_hora", direction=firestore.Query.DESCENDING).get()
        if len(corridas) > 0:
            print("Histórico de Corridas:\n")
            for corrida in corridas:
                corrida_data = corrida.to_dict()
                print(f"Passageiros: {corrida_data['passageiros']} | Data: {corrida_data['data_hora']} | Valor: US$ {corrida_data['valor_total']:.2f}")
        else:
            print("Nenhum histórico de corridas encontrado.")
    except Exception as e:
        print("Erro ao buscar histórico de corridas:", e)

def executar_opcao(opcao, user_email):
    if opcao == 1:
        num_passageiros = int(input("Digite o número de passageiros: "))
        executar_taximetro(num_passageiros, user_email)  # Passa o email do usuário como parâmetro
    elif opcao == 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("A cotação está funcionando da seguinte forma: ")
        # Rest of the code...
    elif opcao == 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_historico_corridas(user_email)  # Passa o email do usuário como parâmetro
    elif opcao == 5:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Saindo do programa...")
        # Rest of the code...
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")


def executar_taximetro(num_passageiros, user_email):
    valor_total = 0

    while True:
        if msvcrt.kbhit():
            tecla = msvcrt.getch().decode('utf-8')
            if tecla.lower() == 'q':
                salvar_corrida_atual(num_passageiros, valor_total, user_email)
                break

        valor_total += valor_por_loop
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Taxímetro Iniciado!\n")
        print(f"Valor acumulado: US$ {valor_total:.2f}\n")
        print("Para parar o taxímetro, aperte a tecla 'Q'")
        time.sleep(4)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Aperte CTRL + V in game para colar automaticamente o /do\n")
    print("Taxímetro Finalizado!")
    print(f"Valor total da última corrida: US$ {valor_total:.2f}\n")
    escrever_mensagem_taximetro(valor_total)
    resposta_nova_corrida = input("Deseja iniciar uma nova corrida? (sim/não): ")
    if resposta_nova_corrida.lower() != "sim":
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    user_email = None
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        user = mostrar_painel_login_cadastro()
        if user is not None:
            user_email = user['email']
            break

    while True:
        exibir_menu()
        opcao = int(input("Digite o número da opção desejada: "))
        executar_opcao(opcao, user_email)  # Pass both arguments here
        if opcao == 5:
            break

if __name__ == "__main__":
    main()
