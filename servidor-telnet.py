import socket
import subprocess
import os
from datetime import datetime

# Create the socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind address and port
servidor.bind(('127.0.0.1', 1234))

# Listen for connections
servidor.listen(1)

# Accept connections
cliente, endereco_cliente = servidor.accept()

# Send welcome message
cliente.sendall(b'Bem-vindo ao servidor!\r\n')

# Menu atualizado
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
        cliente.sendall('\nOla, cliente!\r\n'.encode('utf-8', errors='replace'))

    elif opcao == '2':
        hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cliente.sendall(f'\nHora: {hora_atual}\r\n'.encode('utf-8', errors='replace')
)

    elif opcao == '3':
        cliente.sendall('\nVerificando faltas...\r\n'.encode('utf-8', errors='replace')
)
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(base_dir, 'faltas_checker.py')
            subprocess.run(['python', script_path], cwd=base_dir, check=True)
            log_file = os.path.join(base_dir, 'logs', 'log_faltas.txt')

            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                log_content = log_content.encode('ascii', 'replace').decode('ascii')
                cliente.sendall(log_content.encode('utf-8', errors='replace')
 + b'\r\n')
            else:
                cliente.sendall('\nErro: Log nao encontrado.\r\n'.encode('utf-8', errors='replace')
)
        except Exception as e:
            cliente.sendall(f'\nErro: {str(e)}\r\n'.encode('utf-8', errors='replace')
)

    elif opcao == '4':
        cliente.sendall('\nVerificando situacao curricular...\r\n'.encode('utf-8', errors='replace')
)
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(base_dir, 'situacao_checker.py')
            subprocess.run(['python', script_path], cwd=base_dir, check=True)
            log_file = os.path.join(base_dir, 'logs', 'log_situacao.txt')

            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                log_content = log_content.encode('ascii', 'replace').decode('ascii')
                cliente.sendall(log_content.encode('utf-8', errors='replace')
 + b'\r\n')
            else:
                cliente.sendall('\nErro: Log da situacao nao encontrado.\r\n'.encode('utf-8', errors='replace')
)
        except Exception as e:
            cliente.sendall(f'\nErro: {str(e)}\r\n'.encode('utf-8', errors='replace')
)

    elif opcao == '5':
        cliente.sendall('\nEncerrando...\r\n'.encode('utf-8', errors='replace')
)       
        cliente.close()
        servidor.close()
        break

    else:
        cliente.sendall('\nOpcao invalida.\r\n'.encode('utf-8', errors='replace')
)
    
    # Send the menu again
    cliente.sendall(menu.encode('utf-8', errors='replace'))

