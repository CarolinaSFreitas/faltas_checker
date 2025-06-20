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
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait

def fazer_login(driver, wait, cpf, senha):
    driver.get("https://apsweb.senacrs.com.br/modulos/aluno/login.php5?")
    wait.until(EC.element_to_be_clickable((By.ID, "usr-login"))).send_keys(cpf)
    wait.until(EC.element_to_be_clickable((By.ID, "usr-password"))).send_keys(senha)
    wait.until(EC.element_to_be_clickable((By.ID, "btnEntrar"))).click()

    ambiente = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "bg-aluno")))
    driver.save_screenshot("capturas/3-logada-antes-ambiente.png")
    print(" Screenshot apos login tirada: 3-logada-antes-ambiente.png")
    ambiente.click()
    time.sleep(5)

def acessar_situacao_curricular(driver, wait):
    # Clica no link "Situação Curricular"
    link_situacao = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href,'consultaHistorico.php5')]")
    ))
    link_situacao.click()
    print(" Acessando Situação Curricular...")
    time.sleep(5)
def selecionar_curso_dropdown(driver, wait):
    # Espera e pega a seta (trigger) do dropdown pelo id ext-gen75
    seta_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "ext-gen75")))
    
    # Garante que o elemento está visível na tela para clicar sem erro
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seta_dropdown)
    time.sleep(3)
    
    # Clica na seta para abrir o dropdown
    seta_dropdown.click()

    # Espera e clica na opção desejada no dropdown
    opcao_curso = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class,'x-combo-list-item') and contains(text(),'CST Anál Des Sist FPEL')]")
    ))
    opcao_curso.click()

    time.sleep(5)

def extrair_informacoes(driver):
    infos = {}

    def buscar_valor_por_label(label_text):
        try:
            label_td = driver.find_element(By.XPATH, f"//td[@class='label' and contains(text(),'{label_text}')]")
            valor_td = label_td.find_element(By.XPATH, "./following-sibling::td")
            return valor_td.text.strip()
        except:
            return None

    infos["Total de disciplinas do curso"] = buscar_valor_por_label("Total de disciplinas do curso:")
    infos["Total de disciplinas aprovadas"] = buscar_valor_por_label("Total de disciplinas aprovadas:")
    infos["Optativas aprovadas"] = buscar_valor_por_label("Optativas aprovadas:")
    infos["Carga horária de atividades realizadas"] = buscar_valor_por_label("Carga horária de atividades realizadas:")

    return infos
def main():
    cpf, senha = carregar_credenciais()
    driver, wait = configurar_driver()

    try:
        fazer_login(driver, wait, cpf, senha)
        acessar_situacao_curricular(driver, wait)
        selecionar_curso_dropdown(driver, wait)
        infos = extrair_informacoes(driver)

        print("\n Informacoes coletadas:")
        for k, v in infos.items():
            print(f"{k}: {v if v else 'Nao encontrado'}")

        carga_total = 1740  # horas totais do curso
        total_optativas_necessarias = 5

        def extrair_horas(texto):
            if texto is None:
                return 0
            import re
            numeros = re.findall(r"\d+", texto.replace(".", ""))
            if numeros:
                return int("".join(numeros))
            return 0

        def extrair_numero(texto):
            if texto is None:
                return 0
            import re
            numeros = re.findall(r"\d+", texto)
            if numeros:
                return int(numeros[0])
            return 0

        horas_realizadas = extrair_horas(infos.get("Carga horaria de atividades realizadas"))
        disciplinas_total = extrair_numero(infos.get("Total de disciplinas do curso"))
        disciplinas_aprovadas = extrair_numero(infos.get("Total de disciplinas aprovadas"))
        optativas_aprovadas = extrair_numero(infos.get("Optativas aprovadas"))

        horas_faltando = carga_total - horas_realizadas
        disciplinas_faltando = disciplinas_total - disciplinas_aprovadas
        optativas_faltando = total_optativas_necessarias - optativas_aprovadas

        print()
        resultado = ""

        if horas_faltando > 0:
            resultado += f" Faltam {horas_faltando} horas para voce completar sua graduacao! Se mantenha firme :)\n"
        else:
            resultado += " Parabens! Voce ja completou a carga horaria do curso!\n"

        if disciplinas_faltando > 0:
            resultado += f" Faltam {disciplinas_faltando} disciplinas para voce concluir o curso.\n"
        else:
            resultado += " Parabens! Voce ja completou todas as disciplinas do curso!\n"

        if optativas_faltando > 0:
            resultado += f" Voce ja aprovou {optativas_aprovadas} optativas. Faltam {optativas_faltando} optativas para completar as 5 necessarias para se formar.\n"
        else:
            resultado += " Parabens! Voce ja completou todas as optativas necessárias para a formacao.\n"

        print(resultado)

        # Salvar screenshot da página final
        driver.save_screenshot("capturas/4-situacao_curricular.png")
        print(" Screenshot da situacao curricular tirada: 4-situacao_curricular.png")

        # Criar pasta de logs, se ainda não existir
        os.makedirs("logs", exist_ok=True)

        # Salvar resultado no log
        with open("logs/log_situacao.txt", "w", encoding="utf-8") as f:
            f.write(" Informacoes coletadas:\n")
            for k, v in infos.items():
                f.write(f"{k}: {v if v else 'Nao encontrado'}\n")
            f.write("\n" + resultado)

        print(" Log salvo em logs/log_situacao.txt")

    except Exception as e:
        print(f" Erro: {e}")
        driver.save_screenshot("erro.png")
        print(" Screenshot de erro tirada: erro.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
