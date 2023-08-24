import time
import os
import msvcrt
import sqlite3
from colorama import init, Fore
from datetime import datetime
import pyperclip

init(autoreset=True)

valor_base = 3
valor_por_loop = 3
corrida_number = 0
intervalo_taximetro = 2  # Valor padrão, pode ser alterado na configuração

def exibir_menu():
    criar_tabela_corridas()
    total_ganhos = calcular_total_ganhos()

    print('[ADRP]' + Fore.YELLOW + 'Taxi-Tools 1.0'"\n")
    print("Bem-vindo ao Menu:\n")
    print('1.' + Fore.YELLOW + 'Taxímetro')
    print('2.' + Fore.GREEN + 'Cotação')
    print('3.' + Fore.RED + 'Em Breve')
    print('4.' + Fore.RED + 'Histórico de Corridas')
    print('5.' + Fore.RED + 'Sair')
    print('6.' + Fore.CYAN + 'Exibir Estatísticas')
    print('7.' + Fore.MAGENTA + 'Exibir Resumo Diário')
    print('8.' + Fore.YELLOW + 'Configuração Taxímetro')
    print(f'9. {Fore.YELLOW}Total que você ganhou com as corridas: US$ {total_ganhos:.2f}\n\n\n\n\n\n\n')
    print(f'Intervalo de atualização do Taxímetro: {intervalo_taximetro} segundos')
    print("|¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨|")
    print("|                                                     |")
    print("|                                                     |")
    print('|' + Fore.RED + '           Taxi-Tools AD-RP 1.0 by Naka e SKALLT     ' + Fore.WHITE + '|')
    print("|                                                     |")
    print("|_____________________________________________________|")

def configurar_taximetro():
    while True:
        try:
            segundos = int(input("Digite o intervalo de atualização do taxímetro em segundos: "))
            if segundos <= 0:
                print("O intervalo deve ser maior que zero.")
            else:
                global intervalo_taximetro
                intervalo_taximetro = segundos
                with open("configuracao.txt", "w") as config_file:
                    config_file.write(str(intervalo_taximetro))
                print("Intervalo de atualização configurado com sucesso.")
                input("Pressione Enter para continuar...")
                os.system('cls' if os.name == 'nt' else 'clear')
                return segundos
        except ValueError:
            print("Digite um valor válido.")

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

def criar_tabela_corridas():
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS corridas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        passageiros INTEGER,
                        data_hora TEXT,
                        valor_total REAL
                    )''')

    conn.commit()
    conn.close()

def salvar_corrida_banco_dados(num_passageiros, valor_total):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO corridas (passageiros, data_hora, valor_total)
                      VALUES (?, ?, ?)''', (num_passageiros, formatted_datetime, valor_total))

    conn.commit()
    conn.close()

def exibir_historico_corridas():
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM corridas ORDER BY data_hora DESC")
    corridas = cursor.fetchall()

    conn.close()

    if corridas:
        print("Histórico de Corridas:\n")
        for corrida in corridas:
            corrida_id, passageiros, data_hora, valor_total = corrida
            print(f"Corrida: {corrida_id} | Passageiros: {passageiros} | Data: {data_hora} | Valor: US$ {valor_total:.2f}")
    else:
        print("Nenhum histórico de corridas encontrado.")

def calcular_total_ganhos():
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(valor_total) FROM corridas")
    total_ganhos = cursor.fetchone()[0] or 0

    conn.close()

    return total_ganhos

def calcular_total_corridas():
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM corridas")
    total_corridas = cursor.fetchone()[0] or 0

    conn.close()

    return total_corridas

def calcular_total_ganhos_diarios(data):
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(valor_total) FROM corridas WHERE data_hora LIKE ?", (f"%{data}%",))
    total_ganhos_diarios = cursor.fetchone()[0] or 0

    conn.close()

    return total_ganhos_diarios

def calcular_total_corridas_diarias(data):
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM corridas WHERE data_hora LIKE ?", (f"%{data}%",))
    total_corridas_diarias = cursor.fetchone()[0] or 0

    conn.close()

    return total_corridas_diarias

def exibir_estatisticas():
    total_ganhos = calcular_total_ganhos()
    total_corridas = calcular_total_corridas()

    media_ganho_por_corrida = total_ganhos / total_corridas if total_corridas > 0 else 0

    print("Estatísticas:\n")
    print(f"Total de corridas realizadas: {total_corridas}")
    print(f"Total ganho: US$ {total_ganhos:.2f}")
    print(f"Média de ganho por corrida: US$ {media_ganho_por_corrida:.2f}\n")

def escrever_mensagem_taximetro(valor_total):
    mensagem = f"/do O taxímetro mostra o valor de US$ {valor_total:.2f}."
    pyperclip.copy(mensagem)

def exibir_resumo_diario():
    data_atual = datetime.now().strftime("%d/%m/%Y")
    total_ganhos_diarios = calcular_total_ganhos_diarios(data_atual)
    total_corridas_diarias = calcular_total_corridas_diarias(data_atual)

    print("Resumo Diário:\n")
    print(f"Data: {data_atual}")
    print(f"Total ganho hoje: US$ {total_ganhos_diarios:.2f}")
    print(f"Total de corridas hoje: {total_corridas_diarias}\n")

def executar_taximetro(num_passageiros, intervalo_atualizacao=5):
    global intervalo_taximetro, valor_base, valor_por_loop  # Adicione estas linhas

    intervalo_taximetro = intervalo_atualizacao

    valor_taximetro = calcular_tarifa_horario()
    if valor_taximetro is not None:
        valor_base = valor_taximetro
        valor_por_loop = valor_taximetro

    while True:
        valor_total = 0
        delay = 4

        while True:
            if msvcrt.kbhit():
                tecla = msvcrt.getch().decode('utf-8')
                if tecla.lower() == 'q':
                    delay = 0
                    break

            valor_total += valor_por_loop
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Taxímetro Iniciado!\n")
            print(f"Valor acumulado: US$ {valor_total:.2f}\n")
            print("Para parar o taxímetro, aperte a tecla 'Q'")
            time.sleep(intervalo_atualizacao)

            if delay == 0:
                break

        os.system('cls' if os.name == 'nt' else 'clear')

        if delay == 0:
            print("Aperte CTRL + V in game para colar automaticamente o /do")
            escrever_mensagem_taximetro(valor_total)
            print("Taxímetro Finalizado!")
            print(f"Valor total da última corrida: US$ {valor_total:.2f}\n")
            resposta_nova_corrida = input("Deseja iniciar uma nova corrida? (sim/não): ")
            if resposta_nova_corrida.lower().startswith("sim"):
                os.system('cls' if os.name == 'nt' else 'clear')
                num_passageiros = int(input("Digite o número de passageiros: "))
                executar_taximetro(num_passageiros)
                salvar_corrida_banco_dados(num_passageiros, valor_total)
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                salvar_corrida_banco_dados(num_passageiros, valor_total)
                os.system('cls' if os.name == 'nt' else 'clear')
                exibir_menu()
                os.system('cls' if os.name == 'nt' else 'clear')
                return
            break

def ler_intervalo_taximetro():
    global intervalo_taximetro
    try:
        with open("configuracao.txt", "r") as config_file:
            intervalo_taximetro = int(config_file.read().strip())
    except FileNotFoundError:
        intervalo_taximetro = 2  # Valor padrão, se o arquivo não existir
    except ValueError:
        intervalo_taximetro = 2  # Valor padrão, se não for possível converter para int


def executar_opcao(opcao):
    global intervalo_taximetro

    if opcao == 1:
        criar_tabela_corridas()
        num_passageiros = int(input("Digite o número de passageiros: "))
        executar_taximetro(num_passageiros, intervalo_taximetro)  # Passa o intervalo_taximetro como argumento
    elif opcao == 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("A cotação está funcionando da seguinte forma: ")
    elif opcao == 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Em Breve")
    elif opcao == 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_historico_corridas()
    elif opcao == 5:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Saindo do programa...")
        time.sleep(5)
    elif opcao == 6:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_estatisticas()
    elif opcao == 7:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_resumo_diario()
    elif opcao == 8:
        intervalo_taximetro = configurar_taximetro()  # Atualiza o intervalo_taximetro com o valor configurado

def main():
    ler_intervalo_taximetro()  # Chama a função para ler o intervalo de atualização do arquivo de configuração

    while True:
        exibir_menu()
        opcao = int(input("Digite o número da opção desejada: "))
        if opcao == 5:
            break
        executar_opcao(opcao)

if __name__ == "__main__":
    main()