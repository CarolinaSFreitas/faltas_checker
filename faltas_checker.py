import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def carregar_credenciais():
    load_dotenv()
    return os.getenv("CPF"), os.getenv("SENHA")

def configurar_driver():
    options = Options()
    # options.add_argument("--start-maximized") # roda o script maximizado
    options.add_argument("--headless")  # para rodar sem abrir o navegador
    options.add_argument("--window-size=1920,1080")  # define tamanho da janela
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait

def fazer_login(driver, wait, cpf, senha):
    driver.get("https://apsweb.senacrs.com.br/modulos/aluno/login.php5?")
    wait.until(EC.element_to_be_clickable((By.ID, "usr-login"))).send_keys(cpf)
    wait.until(EC.element_to_be_clickable((By.ID, "usr-password"))).send_keys(senha)
    wait.until(EC.element_to_be_clickable((By.ID, "btnEntrar"))).click()

    ambiente = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "bg-aluno")))
    driver.save_screenshot("capturas/1-logada-antes-ambiente.png")
    print("📸 Screenshot após login tirada: 1-logada-antes-ambiente.png")

    ambiente.click()

def acessar_boletim(driver, wait):
    time.sleep(3)
    try:
        link_boletim = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Boletim")))
    except:
        print("Não encontrou link por texto 'Boletim', tentando buscar por href...")
        link_boletim = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'boletim')]")))
    link_boletim.click()
    print("📂 Acessando página do boletim...")
    time.sleep(5)

    seta = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "x-form-arrow-trigger")))
    driver.execute_script("arguments[0].scrollIntoView(true);", seta)
    time.sleep(1)
    seta.click()

    opcao = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(text(), '2025/1 - CST Anál Des Sist FPEL - 6º Semestre')]"
    )))
    opcao.click()

    time.sleep(3)
    time.sleep(10)
    driver.save_screenshot("capturas/2-entrada-boletim.png")
    print("📸 Screenshot ao entrar no boletim tirada: 2-entrada-boletim.png")

def extrair_faltas(driver):
    print("\n📋 FALTAS POR DISCIPLINA:")
    faltas_exibidas = set()
    tabelas = driver.find_elements(By.CLASS_NAME, "boletimTabelaNotas")

    # Cria pasta logs caso não exista
    os.makedirs("logs", exist_ok=True)

    caminho_arquivo = os.path.join("logs", "log_faltas.txt")
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_log:
        arquivo_log.write("📋 FALTAS POR DISCIPLINA:\n")
        for tabela in tabelas:
            linhas = tabela.find_elements(By.TAG_NAME, "tr")
            for linha in linhas:
                colunas = linha.find_elements(By.TAG_NAME, "td")
                if len(colunas) >= 4:
                    materia = colunas[0].text.strip()
                    faltas = colunas[3].text.strip()
                    if materia and materia.lower() not in ["disciplinas: média final faltas", "-", ""]:
                        if (materia, faltas) not in faltas_exibidas:
                            texto = f"- {materia}: {faltas} faltas"
                            print(texto)
                            arquivo_log.write(texto + "\n")
                            faltas_exibidas.add((materia, faltas))
                            gerar_aviso(arquivo_log, faltas)

def gerar_aviso(arquivo_log, faltas):
    try:
        faltas_num = int(faltas)
    except ValueError:
        return
    limite = 15
    faltas_por_dia = 3
    if faltas_num == 0:
        aviso = "  🎉 Muito bem, 0 faltas! Continue assim."
    elif faltas_num >= limite:
        aviso = f"  ⚠️ Atenção: Você ultrapassou o limite de {limite} faltas nesta matéria!"
    elif faltas_num >= limite - faltas_por_dia:
        aviso = f"  ⚠️ Cuidado: Você não pode mais faltar nenhum dia nesta matéria!"
    else:
        aviso = f"  🔔 Você está com {faltas_num} faltas. Lembre-se que o limite é {limite} faltas. Não perca a linha faltando as suas aulas!"
    print(aviso)
    arquivo_log.write(aviso + "\n")

def main():
    cpf, senha = carregar_credenciais()
    driver, wait = configurar_driver()

    try:
        fazer_login(driver, wait, cpf, senha)
        acessar_boletim(driver, wait)
        extrair_faltas(driver)
    except Exception as e:
        print(f"❌ Erro: {e}")
        driver.save_screenshot("erro.png")
        print("📸 Screenshot de erro tirada: erro.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
