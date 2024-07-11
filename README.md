# HTML-Data-Extractor

Este repositório contém um script em Python que utiliza as bibliotecas BeautifulSoup e Pandas para extrair dados específicos de arquivos HTML, realizar o tratamento dos dados e gerar uma saída em formato HTML.

## Funcionalidades

- **Extração de Dados:** Identificação e extração de informações específicas de tabelas contidas em arquivos HTML.
- **Tratamento de Dados:** Manipulação e padronização dos dados extraídos, incluindo a remoção de duplicatas e o preenchimento de valores ausentes.
- **Exportação:** Geração de um arquivo HTML consolidado contendo os dados processados.

## Estrutura do Código

- **Importação de Bibliotecas:** Importação das bibliotecas necessárias, como BeautifulSoup, Pandas, os e re.
- **Funções Auxiliares:** Definição de funções para encontrar CNPJ, resultados e extrair dados de tabelas.
- **Processamento de Arquivos HTML:** Iteração sobre os arquivos HTML no diretório especificado, leitura e conversão para objetos BeautifulSoup.
- **Armazenamento e Manipulação de Dados:** Armazenamento dos dados extraídos em uma lista de dicionários e manipulação dos dados utilizando Pandas.
- **Exportação de Dados:** Criação de um arquivo HTML contendo os dados processados e organizados em formato tabular.

## Utilização

1. **Configuração do Diretório:** Especifique o diretório onde os arquivos HTML estão localizados.
2. **Execução do Script:** Execute o script para processar os arquivos HTML, extrair os dados e gerar a saída em HTML.
3. **Verificação da Saída:** O arquivo HTML gerado estará localizado no mesmo diretório do script, contendo os dados extraídos e tratados.
