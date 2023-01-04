# Importação das bibliotecas necessárias
import os, hashlib, shutil
import tkinter as tk
from tkinter import filedialog 
from collections import defaultdict
import timeit
import csv

print('Bem vindo ao programa localizador de arquivos idêntidos')
print('-------------------------------------------------------\n\n')
print('Para começar, selecione a pasta de pesquisa...')

# Função para a seleção da pasta com o Tkinter
def seleciona_pasta (title = 'Selecione a pasta...', initialdir = '.'):
    root=tk.Tk()
    root.withdraw() # Esconde a janela root do Tkinter
    pasta_escolhida = filedialog.askdirectory(title = title, initialdir = initialdir)
    return pasta_escolhida

# Seleção da pasta de pesquisa
pasta_de_pesquisa = seleciona_pasta('Selecione a pasta de pesquisa...')
print('Aguarde...')
print('A leitura dos arquivos e o cálculo dos hashes pode demorar.')

# Medição de tempo com timeit para a escolha do algoritmo de hash
start = timeit.default_timer()

# Criação de um dicionário de arquivos únicos (a chave será o hash)
arquivos_unicos = dict()

# Criação de um dicionário de listas de arquivos repetidos (a chave será o hash)
# Observe o uso da classe 'defautdict' para a estruturação do dicionário
repetidos = defaultdict(list)

# Percorrendo todos os arquivos da pasta escolhida e suas subpastas
arquivos = os.walk(pasta_de_pesquisa)

total_arquivos = 0
for dirpath, dirname, files in arquivos:
    for file in files:
        arquivo = os.path.join(dirpath, file)
        hash = hashlib.sha1(open(arquivo, 'rb').read()).hexdigest()   
        total_arquivos += 1

        # Os dicionários de arquivos_unicos e repetidos relacionarão o hash
        # com o 'path' completo dos arquivos, facilitando as demais operações
        if hash not in arquivos_unicos:
            arquivos_unicos[hash] = arquivo # Add da 1a. ocorrência de um arquivo no dicionário de arquivos únicos
        else:
            repetidos[hash].append(arquivo) 

# Estatística
print(f'Pasta "top level" da pesquisa: {pasta_de_pesquisa}')
print(f'Arquivos encontrados: {total_arquivos} ')
print(f'Arquivos únicos: {len(arquivos_unicos)}')
print(f'Arquivos repetidos: {total_arquivos - len(arquivos_unicos)}')

with open ('repetidos.csv', 'w') as arquivo_csv:
    csv.writer(arquivo_csv, delimiter=',').writerow(['hash', 'arquivo original', 'arquivo(s) repetido(s)'])
    for hash in repetidos:
        csv.writer(arquivo_csv, delimiter=',').writerow([hash, arquivos_unicos[hash], repetidos[hash]])

print(f'Arquivo csv gravado em {os.getcwd()}.')

# Medição de tempo com timeit
end1 = timeit.default_timer()
tempo_parcial = end1 - start
print (f"Tempo de processamento até aqui (medido com timeit): {tempo_parcial}")

# Mover arquivos repetidos
def move_repetidos(repetidos, destino):
    n = 0
    for hash in repetidos:
        for arquivo in repetidos[hash]:
            nome_do_arquivo = arquivo.split('\\')[-1]
            shutil.move(arquivo, destino +'\\'+ str(n) + '_' + nome_do_arquivo)
        n += 1

resp = input('Deseja mover os arquivos repetidos? [s,n] ')
if resp == 'S' or resp =='s':
    # Seleção da pasta de destino
    pasta_de_destino = seleciona_pasta('Selecione a pasta de destino...')
    new_start = timeit.default_timer()
    print('Aguarde...')

    move_repetidos(repetidos, pasta_de_destino)
    end2 = timeit.default_timer()
    tempo_parcial_1 = end2 - new_start
    print (f"Tempo de processamento total: {tempo_parcial + tempo_parcial_1}")

os.system("pause")
print('Programa concluído!')