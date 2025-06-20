import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Carrega o CPF e a senha do arquivo .env
def carregar_credenciais():
    load_dotenv()
    return os.getenv("CPF"), os.getenv("SENHA")

# Configura o ChromeDriver com opções para rodar em modo headless (sem abrir o navegador)
def configurar_driver():
    options = Options()
    # options.add_argument("--start-maximized") # roda o script maximizado
    options.add_argument("--headless")  # para rodar sem abrir o navegador
    options.add_argument("--window-size=1920,1080")  # define tamanho da janela virtual
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait

# Realiza o login no portal do aluno
def fazer_login(driver, wait, cpf, senha):
    driver.get("https://apsweb.senacrs.com.br/modulos/aluno/login.php5?")
    wait.until(EC.element_to_be_clickable((By.ID, "usr-login"))).send_keys(cpf)
    wait.until(EC.element_to_be_clickable((By.ID, "usr-password"))).send_keys(senha)
    wait.until(EC.element_to_be_clickable((By.ID, "btnEntrar"))).click()

    # Acessa o ambiente acadêmico após o login
    ambiente = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "bg-aluno")))
    driver.save_screenshot("capturas/1-logada-antes-ambiente.png")
    print(" Screenshot apas login tirada: 1-logada-antes-ambiente.png")

    ambiente.click()

# Acessa a página de boletim e seleciona o semestre atual
def acessar_boletim(driver, wait):
    time.sleep(3) # tempo extra de espera para estabilidade
    try:
        link_boletim = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Boletim")))
    except:
        # Caso não encontre o link direto, tenta buscar por parte do href
        print("Nao encontrou link por texto 'Boletim', tentando buscar por href...")
        link_boletim = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'boletim')]")))
    link_boletim.click()
    print(" Acessando pagina do boletim...")
    time.sleep(5)

    # Seleciona o semestre atual no dropdown
    seta = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "x-form-arrow-trigger")))
    driver.execute_script("arguments[0].scrollIntoView(true);", seta)
    time.sleep(1)
    seta.click()

    opcao = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(text(), '2025/1 - CST Anál Des Sist FPEL - 6º Semestre')]"
    )))
    opcao.click()

    time.sleep(12) # tempo para carregar todos os dados
    driver.save_screenshot("capturas/2-entrada-boletim.png")
    print(" Screenshot ao entrar no boletim tirada: 2-entrada-boletim.png")

# Extrai as faltas por disciplina e salva em um txt de logs
def extrair_faltas(driver):
    print("\n FALTAS POR DISCIPLINA:")
    faltas_exibidas = set()
    tabelas = driver.find_elements(By.CLASS_NAME, "boletimTabelaNotas")

    # Cria pasta logs caso não exista
    os.makedirs("logs", exist_ok=True)

    caminho_arquivo = os.path.join("logs", "log_faltas.txt")
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_log:
        arquivo_log.write(" FALTAS POR DISCIPLINA:\n")
        for tabela in tabelas:
            linhas = tabela.find_elements(By.TAG_NAME, "tr")
            for linha in linhas:
                colunas = linha.find_elements(By.TAG_NAME, "td")
                if len(colunas) >= 4:
                    materia = colunas[0].text.strip()
                    faltas = colunas[3].text.strip()
                        # Filtra entradas inválidas ou repetidas
                    if materia and materia.lower() not in ["disciplinas: media final faltas", "-", ""]:
                        if (materia, faltas) not in faltas_exibidas:
                            texto = f"- {materia}: {faltas} faltas"
                            print(texto)
                            arquivo_log.write(texto + "\n")
                            faltas_exibidas.add((materia, faltas))
                            gerar_aviso(arquivo_log, faltas)

# Gera mensagens com base na quantidade de faltas
def gerar_aviso(arquivo_log, faltas):
    try:
        faltas_num = int(faltas)
    except ValueError:
        return
    limite = 15
    faltas_por_dia = 3
    # Define mensagens diferentes conforme o nível de alerta
    if faltas_num == 0:
        aviso = "   Muito bem, 0 faltas! Continue assim."
    elif faltas_num >= limite:
        aviso = f"   Atencao: Voce ultrapassou o limite de {limite} faltas nesta materia!"
    elif faltas_num >= limite - faltas_por_dia:
        aviso = f"   Cuidado: Voce nao pode mais faltar nenhum dia nesta materia!"
    else:
        aviso = f"   Voce esta com {faltas_num} faltas. Lembre-se que o limite e {limite} faltas. Nao perca a linha faltando as suas aulas!"
    print(aviso)
    arquivo_log.write(aviso + "\n")

# Função principal que orquestra a execução do script
def main():
    cpf, senha = carregar_credenciais()
    driver, wait = configurar_driver()

    try:
        fazer_login(driver, wait, cpf, senha)
        acessar_boletim(driver, wait)
        extrair_faltas(driver)
    except Exception as e:
        print(f" Erro: {e}")
        driver.save_screenshot("erro.png")
        print(" Screenshot de erro tirada: erro.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
