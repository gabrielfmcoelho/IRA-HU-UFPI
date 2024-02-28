![Banner Insuficiência Renal Aguda HU UFPI](images/banner.png)  

- [PT-BR](#pt-br-insuficiência-real-aguda-ira-em-pacientes-internados-pelo-setor-de-cardiologia-do-hu-ufpi)
- [EN](#en-acute-real-insufficiency-arf-in-patients-admitted-to-the-cardiology-department-of-hu-ufpi)

# PT-BR: Insuficiência Real Aguda (IRA) em pacientes internados pelo setor de Cardiologia do HU-UFPI

## Descrição do Projeto

Este projeto tem como objetivo o desenvolvimento de um modelo de Aprendizado de Máquina Supervisionado para inferência de Insuficiência Renal Aguda (IRA) de pacientes internados no Hospital Universitário da Universidade Federal do Piauí (HU-UFPI) no setor de cardiologia entre os anos de 2018 e 2022. Abordando aquisição, tratamento, análise, desenvolvimento, avaliação e implementação como WebApp.

## Versionamento
| Objeto | Versão | Data de Atualização |
|--------|--------|---------------------|
| Notebook | 2.5 | 27/02/2024 |
| WebApp | 1.5 | 27/02/2024 |

## Estrutura do Projeto

IRA-Analysis-HU-UFPI/  
|-- notebooks/  
|   |-- ira_analysis.ipynb  
|-- data/  
|   |-- raw/  
|   |   |-- creatinina_pacientes.csv  
|   |   |-- controle_pacientes.csv  
|   |-- processed/  
|   |   |-- ______.csv  
|   |-- final/  
|   |   |-- ______.csv  
|-- models/  
|   |-- modelo-1.pkl  
|-- reports/  
|   |-- _________.pdf  
|   |-- ...  
|-- src/  
|   |-- utils.py  
|-- app/  
|   |-- webapp.py  
|-- requirements.txt  
|-- Makefile
|-- README.md  

- **notebooks:** Contém o Jupyter Notebook principal para a análise dos dados e desenvolvimento dos modelos.
  
- **data:**
  - **raw:** Armazena os dados brutos extraídos do banco AGHU.
  - **processed:** Local para salvar dados processados durante a análise.
  - **final:** Destinado aos dados finais após a conclusão da análise.

- **models:** Contém os modelos de machine learning treinados, salvos em formato pickle (`.pkl`).

- **reports:** Armazena os relatórios e documentos gerados durante a análise, como o relatório final em PDF.

- **src:** Código-fonte e utilitários para a análise, como o arquivo `utils.py`.

- **app:** Possui arquivos relacionados a aplicação web para uso de validação do modelo, com o arquivo `webapp.py`.

- **requirements.txt:** Lista as dependências do projeto para replicação.

- **README.md:** Documentação principal do projeto, incluindo informações sobre a estrutura, configuração e execução do código.

## Preparação do Ambiente Virtual

Para a replicação do projeto, é necessário a criação de um ambiente virtual com as dependências necessárias.

- **dependencias basicas:**  
  - python >= 3.11
  - pip 20.0.2
  - git 2.25.1

Após assegurar que as dependências básicas estão instaladas, acesse o terminal e navegue até a pasta raiz do projeto. Em seguida, execute os seguintes comandos:

```bash
make prepare-env
```

## Execução do Web App

Para executar o web app, basta executar o seguinte comando no terminal dentro da pasta raiz do projeto:

```bash
make iniciar-webapp
```

O Web App estará disponível no endereço `http://localhost:8080/`.

## Autores

| Nome              | Lattes                   | Email                      |
|-------------------|--------------------------|----------------------------|
| Gabriel Feitosa Melo Coelho | [Link](http://lattes.cnpq.br/4697851599945993) | gabrielcoelho09gc@gmail.com |
| Francisco Luciani de Miranda Vieira | [Link](http://lattes.cnpq.br/4627829411266800) | email_mockup@gmail.com |


## Consentimento de Uso de Dados

Esta projeto foi desenvolvido como parte do projeto __________, encabeçada pela residente _______, sob orientação do prof. Dr. ______. Os dados utilizados são de propriedade do Hospital Universitário da UFPI e foram cedidos para o desenvolvimento desta análise.

# EN: Acute Real Insufficiency (ARF) in patients admitted to the Cardiology department of HU-UFPI
