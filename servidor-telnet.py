import socket
import subprocess
import os
from datetime import datetime

# Função para enviar texto formatado corretamente para Telnet
def enviar_mensagem(cliente, mensagem):
    for linha in mensagem.splitlines():
        cliente.sendall((linha + '\r\n').encode('utf-8', errors='replace'))
    cliente.sendall(b'[FIM_DA_MENSAGEM]\r\n')  # Delimitador de fim de resposta

# Criação do socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('127.0.0.1', 1234))
servidor.listen(1)

# Conexão com o cliente
cliente, endereco_cliente = servidor.accept()
cliente.sendall(b'Bem-vindo(a)!\r\n')

# Menu alinhado
menu = """Menu:               \r\n
1. Dizer ola        \r\n
2. Ver horas        \r\n
3. Verificar faltas \r\n
4. Ver situacao     \r\n
5. Sair             \r\n
Escolha: """

cliente.sendall(menu.encode('utf-8', errors='replace'))

while True:
    opcao = cliente.recv(1024).decode('ascii').strip()

    if opcao == '1':
        enviar_mensagem(cliente, "\nOiii, cliente!")

    elif opcao == '2':
        hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        enviar_mensagem(cliente, f"\nHora atual: {hora_atual}")

    elif opcao == '3':
        enviar_mensagem(cliente, "\nVerificando faltas...")
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(base_dir, 'faltas_checker.py')
            subprocess.run(['python', script_path], cwd=base_dir, check=True)
            log_file = os.path.join(base_dir, 'logs', 'log_faltas.txt')

            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                enviar_mensagem(cliente, log_content)
            else:
                enviar_mensagem(cliente, "\nErro: Log de faltas nao encontrado.")
        except Exception as e:
            enviar_mensagem(cliente, f"\nErro: {str(e)}")

    elif opcao == '4':
        enviar_mensagem(cliente, "\nVerificando situacao curricular...")
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(base_dir, 'situacao_checker.py')
            subprocess.run(['python', script_path], cwd=base_dir, check=True)
            log_file = os.path.join(base_dir, 'logs', 'log_situacao.txt')

            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                enviar_mensagem(cliente, log_content)
            else:
                enviar_mensagem(cliente, "\nErro: Log da situacao nao encontrado.")
        except Exception as e:
            enviar_mensagem(cliente, f"\nErro: {str(e)}")

    elif opcao == '5':
        enviar_mensagem(cliente, "\nEncerrando conexao. Ate logo!")
        cliente.close()
        servidor.close()
        break

    else:
        enviar_mensagem(cliente, "\nOpção inválida.")

    # Exibe o menu novamente
    cliente.sendall(menu.encode('utf-8', errors='replace'))
