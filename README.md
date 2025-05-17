# 📚 Faltas Checker
Faltas Checker é um script em Python criado para automatizar a extração de faltas por disciplina diretamente do Portal do Aluno do Senac-RS. Ele foi pensado para facilitar a vida de estudantes que, assim como nós, precisam acessar o portal com frequência só para verificar a quantidade de faltas — algo essencial para o controle acadêmico e que, muitas vezes, passa despercebido.

A proposta é tornar esse acompanhamento mais prático, rápido e confiável, gerando logs e alertas automáticos, evitando surpresas desagradáveis no final do semestre.

### 👥 Discentes:
- Carolina Soares Freitas
- Júlia Pereira Hallal

## ⚙️ Funcionalidades
- 🔐 Acesso automático ao portal acadêmico com login via CPF e senha (utilizando .env).

- 📊 Extração das faltas por disciplina.

- 🧠 Avisos personalizados conforme a quantidade de faltas:

    - 🎉 0 faltas: Mensagem positiva de incentivo.

    - ⚠️ Próximo do limite (15 faltas): Alerta para não faltar mais.

    - 🚨 Acima do limite: Alerta crítico.

- 📄 Geração de um log (`log_faltas.txt`) com todas as informações exibidas no terminal.

- 🔁 Prevenção de registros duplicados no log.

- 📸 Armazenamento automático de capturas de tela:
    - Após o login no portal.
    - Ao acessar o boletim no sistema.

    - As screenshots são salvas com os seguintes nomes:
        `1-logada-antes-ambiente.png` – após o login e antes de entrar no ambiente do estudante.
        `2-entrada-boletim.png` – ao acessar o boletim com as disciplinas.
        `erro.png` – se ocorrer algum erro durante a execução.
        - As imagens são armazenadas por padrão na subpasta capturas/.

## 🛠️ Detalhes Técnicos
O script foi desenvolvido em Python utilizando a biblioteca Selenium WebDriver, que permite controlar o navegador programaticamente. Optamos pelo modo ``headless``, que executa a automação sem abrir a interface visual do navegador, otimizando recursos e possibilitando rodar em servidores sem interface gráfica.

Para garantir estabilidade em páginas com carregamento dinâmico, como o Portal do Aluno, utilizamos esperas explícitas (``WebDriverWait``), que aguardam até que os elementos estejam visíveis ou clicáveis antes de prosseguir com as ações. Isso evita erros comuns de sincronização.

Um desafio técnico importante foi a seleção do semestre correto no boletim, que exigiu o uso do método ``scrollIntoView`` para garantir que o elemento da seta de seleção estivesse visível na tela.

O código está organizado em funções para modularizar o fluxo da automação, incluindo:
 - Carregamento seguro das credenciais via arquivo `.env`.
 - Configuração e inicialização do driver.
 - Login e navegação até o boletim.
 - Extração e filtragem dos dados de faltas.
 - Geração de logs e alertas baseados na quantidade de faltas.

Além disso, o script conta com tratamento de exceções para capturar erros inesperados, salvar screenshots de erro para facilitar a depuração e garantir o encerramento adequado do driver para liberar recursos do sistema.

## 🧾 Requisitos
1. Python 3.12 ou superior.

2. Selenium 
    ````
    pip install selenium
    ````
3. WebDriver compatível com seu navegador (exemplo: ChromeDriver para Google Chrome).

## ▶️ Como usar
1. Clone ou baixe o repositório.

2. Crie um arquivo .env com suas credenciais do portal:
- Crie um arquivo .env com suas credenciais do portal:
````
CPF=seu_cpf_aqui
SENHA=sua_senha_aqui
````

3. Instale as dependências necessárias:
````
pip install selenium python-dotenv
````

4. Execute o script:
````
python faltas_checker.py
````

5. Confira o terminal para ver os resultados e os avisos.

6. Verifique o arquivo ``log_faltas.txt`` com o histórico das faltas e alertas.

### 💡 Propósito do Projeto
Esse projeto surgiu da necessidade constante de acessar o Portal do Aluno apenas para consultar as faltas - uma informação crucial que muitas vezes é negligenciada no dia a dia. O Faltas Checker permite um acompanhamento mais simples, com alertas claros sobre o risco de reprovação por frequência, promovendo mais controle e responsabilidade acadêmica de forma prática e automatizada.
