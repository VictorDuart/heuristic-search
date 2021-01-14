# -- coding: utf-8 --
author = "Victor Duarte"

import sys
import csv
from math import sqrt
from math import pow

custo_total = 0

# Dada uma matriz e um valor, encontra as coordenadas (i,j) 
# que contenham o valor procurado e os retorna em uma lista.
def encontraPosicoes (matriz, M, N, valor):
	posicoes = []
	for i in range(0, M):
		for j in range(0, N):
			if matriz[i][j] == valor:
				posicoes.append((i, j))
	return posicoes


# Dado um estado inicial e uma lista de estados finais, ordena
# a lista de estados finais com base na distância euclidiana  
# em uma nova lista e a retorna.
def ordenaEstados (estado_inicial, estados_finais):
	x = estado_inicial[0]
	y = estado_inicial[1]
	estados_ordenados = {}

	for estado_final in estados_finais:
		x_estado_final = estado_final[0]
		y_estado_final = estado_final[1]
		diff1 = x_estado_final - x
		diff2 = y_estado_final - y
		somaDiffs = pow(diff1, 2) + pow(diff2, 2)
		distancia_atual = sqrt(somaDiffs)
		estados_ordenados[estado_final] = distancia_atual
		estados_finais_ordenados = {}
		keys_ordenadas = {}
	
	i = 0
	for item in sorted(estados_ordenados, key = estados_ordenados.get):
		estados_finais_ordenados[i] = estados_ordenados[item]
		keys_ordenadas[i] = item
		i = i + 1
	return list(keys_ordenadas.values())


# Dada uma matriz e a posicao atual pelas coordenadas (i,j), 
# encontra os estados sucessores com 1 passo de (i,j).
def encontra_estados_sucessores (matriz, M, N, posicao_atual):
	i = posicao_atual[0]
	j = posicao_atual[1]
	estados_sucessores = []
	if i > 0: # Move para cima na matriz.
		estados_sucessores.append ((i-1, j))
	if i+1 < M: # Move para baixo na matriz.
		estados_sucessores.append ((i+1, j))
	if j > 0: # Move para esquerda na matriz.
		estados_sucessores.append ((i, j-1))
	if j+1 < N: # Move para direita na matriz.
		estados_sucessores.append ((i, j+1))
	return estados_sucessores

# Dado um estado considerado final, uma lista de predecessores e um numero de iteracao,
# apresenta em qual iteracao foi encontrada a solucao e como partir do estado inicial 
# e chegar ate o estado final a partir da solucao parcial armazenada em predecessores,
# além disso, apresta o custo de caminho parcial para aquele caminho. 
def apresenta_solucao (matriz, estado, predecessores, iteracao):
	custo = 0
	caminho = []
	caminho.append(estado)
	print("Solucao encontrada na iteracao " + str(iteracao) + ":")
	while predecessores[estado] != None:
		caminho.append(predecessores[estado])
		estado = predecessores[estado]
	caminho = caminho[::-1]
	print("Caminho encontrado: ")
	print(caminho)
	for elemento in caminho:
		x = elemento[0]
		y = elemento[1]
		custo = custo + int(matriz[x][y])
	custo -= 20
	global custo_total 
	custo_total += custo
	print("\nCusto do caminho: ")
	print(custo)
	print("\n\n")
		
		
# Dado um estado qualquer e um conjunto de estados finais, 
# calcula a distancia do estado qualquer ate um estado final mais proximo.
def calcula_distancia_euclidiana (estado, estados_finais):
	x = estado[0]
	y = estado[1]
	distancia_minima = 1000000000

	for estado_final in estados_finais:
		x_estado_final = estado_final[0]
		y_estado_final = estado_final[1]
		diff1 = x_estado_final - x
		diff2 = y_estado_final - y
		somaDiffs = pow(diff1, 2) + pow(diff2, 2)
		distancia_atual = sqrt(somaDiffs)
		if distancia_atual < distancia_minima:
			distancia_minima = distancia_atual
	return distancia_minima

# Dado um conjunto de nós e uma funcao heuristica, 
# encontra o estado com menor valor nesse conjunto.
def encontra_estado_mais_promissor (nodes, heuristica_estados):
	valor_mais_promissor = 1000000000
	indice_mais_promissor = 0
	indice = 0
	for estado in nodes:
		if heuristica_estados[estado] < valor_mais_promissor:
			valor_mais_promissor = heuristica_estados[estado]
			indice_mais_promissor = indice
		indice = indice + 1
	return indice_mais_promissor

# Algoritmo de Busca A*
def busca_a_estrela (matriz, M, N, estado_inicial, estados_finais):
	distancia_euclidiana = {}
	distancia_percorrida = {}
	heuristica = {}
	predecessores = {}
	estados_expandidos = []
	solucao_encontrada = False

	print("\nAlgoritmo A*\n")

	# inicializacao da distancia percorrida (f), distancia ate a meta (g) e heuristica (h = f+g).
	distancia_percorrida[estado_inicial] = 0
	distancia_euclidiana[estado_inicial] = calcula_distancia_euclidiana (estado_inicial, estados_finais) 
	heuristica[estado_inicial] = distancia_percorrida[estado_inicial] + distancia_euclidiana[estado_inicial]
	predecessores[estado_inicial] = None
	print("Heuristica da Distância no Estado Inicial: " + str(heuristica[estado_inicial]))
	nodes = []
	nodes.append(estado_inicial)
	iteracao = 1
	while len(nodes) != 0:
		indice_mais_promissor = encontra_estado_mais_promissor(nodes, heuristica)
		estado = nodes.pop(indice_mais_promissor)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores(matriz, M, N, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):	
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in nodes:
				nodes.append(sucessor)
				if sucessor not in heuristica.keys():
					linha = sucessor[0]
					coluna = sucessor[1]
					distancia_euclidiana[sucessor] = calcula_distancia_euclidiana(sucessor, estados_finais)
					distancia_percorrida[sucessor] = distancia_percorrida[estado] + int(matriz[linha][coluna])
					heuristica[sucessor] = distancia_euclidiana[sucessor] + distancia_percorrida[sucessor]
					predecessores[sucessor] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		# print(distancia_percorrida)
		apresenta_solucao (matriz, estado, predecessores, iteracao)
	else:
		print("Nao foi possivel encontrar uma solucao para o problema.")

def main():
	if len(sys.argv) == 2:
		count = 0
		problema = sys.argv[1]

		# carrega o arquivo csv contendo a representacao do mapa
		with open (problema, 'r') as csv_file:
			leitor_problema = csv.reader(csv_file)
			entrada = list(leitor_problema)
	
		M = int(entrada[0][0]) # numero de linhas.
		N = int(entrada[0][1]) # numero de colunas.
		matriz = entrada[1:]   # mapa representado como matriz.

		# calcula os estados iniciais e finais com base no parâmetro
		estado_inicial = encontraPosicoes (matriz, M, N, '1')
		estados_finais = encontraPosicoes (matriz, M, N, '0')

		# encontra os melhores caminhos para cada pingente
		while(count < 3):
			print("Estado Inicial: " + str(estado_inicial))
			print("Estado Final: " + str(estados_finais))

			estado_final = ordenaEstados(estado_inicial[0], estados_finais)
			busca_a_estrela (matriz, M, N, estado_inicial[0], [tuple(estado_final[0])])
			estado_inicial = [estado_final[0]]

			if(len(estados_finais) > 0):
				estados_finais.remove(estado_inicial[0])
				matriz[estado_inicial[0][0]][estado_inicial[0][1]] = 20
			count = count + 1
	
		# encontra o melhor caminho para a Master Sword
		estados_finais = encontraPosicoes (matriz, M, N, '2')
		busca_a_estrela(matriz, M, N, estado_inicial[0], estados_finais)

		print("Custo total: ")
		print(custo_total)
			
	else:
		print("Forneca um arquivo CSV para os algoritmos de busca.")

if __name__ == "__main__":
    main()
