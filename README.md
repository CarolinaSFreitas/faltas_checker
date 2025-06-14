# 📚 Faltas Checker + Situação Curricular Checker + Servidor Telnet 
Faltas Checker é um script em Python criado para automatizar a extração de faltas por disciplina diretamente do Portal do Aluno do Senac-RS. Ele foi pensado para facilitar a vida de estudantes que, assim como nós, precisam acessar o portal com frequência só para verificar a quantidade de faltas — algo essencial para o controle acadêmico e que, muitas vezes, passa despercebido.
Complementando essa funcionalidade, o Situação Curricular Checker automatiza a verificação da situação acadêmica no portal do aluno, trazendo um resumo detalhado do progresso do curso. Ele realiza login automaticamente e navega até a página de Situação Curricular, onde extrai informações importantes, como: total de disciplinas aprovadas, quantidade de disciplinas optativas já aprovadas e carga horária de atividades realizadas. om esses dados, o script calcula e exibe um panorama do progresso acadêmico.
Para tornar o acesso a essas informações ainda mais prático, desenvolvemos um Servidor Telnet em Python que permite consultar remotamente via terminal, bastando conectar-se ao servidor e escolher no menu o que o estudante deseja consultar sem precisar acessar o portal diretamente pelo navegador.

A proposta é tornar esse acompanhamento mais prático, rápido e confiável, gerando logs e alertas automáticos, evitando surpresas desagradáveis no final do semestre.

### 👥 Discentes:
- Carolina Soares Freitas
- Júlia Pereira Hallal

## ⚙️ Funcionalidades
### Faltas Checker
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

### Situação Curricular Checker
- 🔐 Login automático no portal acadêmico com CPF e senha via .env.

- 📂 Acesso automático à página de Situação Curricular.

- 🔽 Seleção do curso pelo dropdown para garantir a extração correta das informações.

- 📋 Extração de dados acadêmicos:

    - Total de disciplinas do curso.

    - Total de disciplinas aprovadas.

    - Quantidade de disciplinas optativas aprovadas.

    - Carga horária de atividades realizadas.

- ⏳ Cálculo automático do progresso do curso:

    - Horas restantes para conclusão.

    - Disciplinas restantes.

    - Optativas restantes.

📸 Captura de tela da página de situação curricular (capturas/4-situacao_curricular.png).

📄 Geração de log detalhado em logs/log_situacao.txt.

Tratamento de erros com screenshot automática (erro.png).

### Servidor Telnet
 - 🖥 Servidor local que permite acessar as funcionalidades via terminal remoto.
    
 - 📋 Menu interativo com opções:
    
    - Dizer “Olá”
    
    - Ver hora atual
    
    - Executar Faltas Checker e exibir log
    
    - Executar Situação Curricular Checker e exibir log
    
    - Sair

- 📡 Comunicação via socket TCP/IP (localhost:1234).

- Integração com scripts Python para execução sob demanda.

- Tratamento de erros para informar problemas na execução dos scripts.

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

O script Situação Curricular segue essa mesma base, com foco na extração de dados acadêmicos e cálculo do progresso do curso.

Já o servidor Telnet, implementado com a biblioteca socket, abre uma conexão local (porta 1234) para que o usuário possa executar os scripts remotamente via menu interativo. Ele:

- Recebe comandos do cliente Telnet.

- Executa os scripts faltas_checker.py e situacao_checker.py sob demanda.

- Responde com o horário atual se essa opção for solicitada.

- Envia os logs resultantes de volta ao cliente.

- Trata erros e mantém uma comunicação clara.

- Permite encerrar a conexão e o servidor de forma controlada.

## 🧾 Requisitos
1. Python 3.12 ou superior.

2. Selenium 
    ````
    pip install selenium
    ````
3. WebDriver compatível com seu navegador (exemplo: ChromeDriver para Google Chrome).

4. Telnet (cliente para conectar ao servidor Telnet)

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

4. Para rodar os scripts diretamente, execute:
Para verificar faltas:
````
python faltas_checker.py
````

Para verificar situação curricular:
````
python situacao_checker.py
````

5. Confira o terminal para ver os resultados e os avisos.

6. Verifique os arquivos de log gerados, como ``log_faltas.txt`` e ``logs/log_situacao.txt``, que armazenam o histórico das verificações.

7. Para usar o servidor Telnet:
Execute o servidor com:
````
python servidor_telnet.py
````

Em outro terminal, conecte-se via Telnet:
````
telnet 127.0.0.1 1234
````
O menu interativo permitirá executar os scripts remotamente e solicitar o horário atual, além de visualizar os logs gerados.

### 💡 Propósito do Projeto
Esse projeto surgiu da necessidade constante de acessar o Portal do Aluno apenas para consultar as faltas - uma informação crucial que muitas vezes é negligenciada no dia a dia. O Faltas Checker permite um acompanhamento mais simples, com alertas claros sobre o risco de reprovação por frequência, promovendo mais controle e responsabilidade acadêmica de forma prática e automatizada.
