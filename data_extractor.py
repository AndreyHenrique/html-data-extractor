from bs4 import BeautifulSoup
import pandas as pd
import os 
import re

# Lista para armazenar as linhas da coluna com os dados extraidos
dados_extraidos = []
 
# Caso o nome dos arquivos não contenham o cnpj, pode se usar a função abaixo para procurar eles dentros dos htmls
def encontra_cnpj(soup):
    # Procurando o texto com o CNPJ
    string_com_cnpj = soup.find('font', string=re.compile(r'CPF ou CNPJ do Depositante'))

    if string_com_cnpj:
        # Extraindo o cnpj com o regex
        cnpj_modelo = r'\b\d{14}\b'  # CNPJ possui 14 dígitos
        cnpj = re.search(cnpj_modelo, string_com_cnpj.text)
        if cnpj:
            cnpj = cnpj.group()
            return cnpj
    return 'n/a'
    
def encontra_resultado(soup):
    texto_completo = None

    # Procura a string com o resultado
    string_com_resultado = re.compile(r'Foram encontrados', re.IGNORECASE)
    encontrados = soup.find_all(string=string_com_resultado)
    
    # Verifica se foi encontrado a string "Forma encontrados"
    if encontrados:
        # Encontra o elemento html da string
        for encontrado in encontrados:
            # Acessando o elemento pai do texto encontrado
            texto_completo = encontrado.find_parent()

    # Encontrando o número de resultados
    if texto_completo:
        texto_completo = str(texto_completo)
        soup2 = BeautifulSoup(texto_completo, "lxml")

        # Procurando a tag <b>
        tag_b = soup2.find('font', class_='normal',).find('b')

        # Retirando a tag <b>
        numero_de_resultados = str(tag_b).replace('<b>', '')
        numero_de_resultados = str(numero_de_resultados).replace('</b>', '')
        return numero_de_resultados
     
    return 0
    
def extracao_da_tabela(tabela):
    pedidos = []

    # Encontra parte do arquivo html que é contido pelas tags "<tr></tr>"", ou seja as, "linhas" das tabelas, e as coloca em uma lista
    linhas = tabela.find_all('tr') if tabela else []

    # Percorre todas as "linhas"
    for linha in linhas:
        
        # Encontra parte do arquivo html que é contido pelas tags "<td></td>", ou seja, as "colunas" da tabela
        colunas = linha.find_all('td')

        if len(colunas) >= 4:
            numero_do_pedido = colunas[0].get_text(strip=True)
            data_do_deposito = colunas[1].get_text(strip=True)
            titulo = colunas[2].get_text(strip=True)
            ipc = colunas[3].get_text(strip=True)

            pedidos.append((numero_do_pedido, data_do_deposito, titulo, ipc))
        else:
            while len(colunas) < 4:
                colunas.append(BeautifulSoup('<td>n/a</td>', 'lxml').td)
            numero_do_pedido = colunas[0].get_text(strip=True)
            data_do_deposito = colunas[1].get_text(strip=True)
            titulo = colunas[2].get_text(strip=True)
            ipc = colunas[3].get_text(strip=True)
            pedidos.append((numero_do_pedido, data_do_deposito, titulo, ipc))

    return pedidos

# Direrório onde se encontram os arquivos html
diretorio = 'C:/Users/greyc/Desktop/Python Files/API/OpenSense Project/PATENTES'

# Retorna uma lista dos nomes dos arquivos html no diretorio
arquivos_das_patentes = os.listdir(diretorio)

# Retornando o caminho de cada arquivo html 
for cada_arquivo in arquivos_das_patentes:
    caminho_do_arquivo = os.path.join(diretorio, cada_arquivo)
    
    # Retorna o conteúdo de cada html no arquivo de PATENTES
    with open(caminho_do_arquivo, 'r', encoding='latin1') as arquivo:
        conteudo_do_html = arquivo.read()

        # Facilita a leitura do html, transformando ele em "soup". Interessante para pegar dados especificos dentro de arquivos html
        soup = BeautifulSoup(conteudo_do_html, "lxml")

        # Dados que devem ser encontrados dentro do soup

        nome_do_arquivo = cada_arquivo

        # O cnpj está no nome do arquivo, só precisa estar formatado da forma correta.
        cnpj = nome_do_arquivo.replace('.html', '').replace('-', '')

        resultado = int(encontra_resultado(soup))

        if resultado > 0:
            # Procura a tabela em que estão os dados do resultado
            tabela = soup.find('tbody', id="tituloContext")
            pedidos = extracao_da_tabela(tabela)

        else:
            # Coloca os dados como (n/a) dos arquivos que não possuem resultados
            pedidos = [('n/a'),('n/a'),('n/a'),('n/a')]

        # Coloca nos dados extraidos, as linhas da futura tabela
        for pedido in pedidos:
            dados_extraidos.append({
                'Arquivo': nome_do_arquivo,
                'CNPJ': cnpj,
                'Resultado': resultado,
                'Número do Pedido': pedido[0] if len(pedido) > 0 else 'n/a',
                'Data do Depósito': pedido[1] if len(pedido) > 1 else 'n/a',
                'Título': pedido[2] if len(pedido) > 2 else 'n/a',
                'IPC': pedido[3] if len(pedido) > 3 else 'n/a'
                })

# Transforma os dicionários python em um data frame em pandas
df = pd.DataFrame(dados_extraidos)

# Retira as linhas duplicadas
df = df.drop_duplicates()

# Reorganiza o index 
df = df.reset_index(drop=True)

# Tira as inconsistências do código
inconsistencia = ['a', 'n', '', '/', '-']
df.replace(inconsistencia, 'n/a', inplace=True)

# Cria um arquivo html para a tabela
df.to_html('C:/Users/greyc/Desktop/Python Files/API/OpenSense Project/PATENTES.HTML', index=False)