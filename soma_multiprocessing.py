import time
import numpy as np
from multiprocessing import Pool

def gerar_vetor(tamanho):
    return np.random.randint(1, 101, size=tamanho, dtype=np.int64)

def soma_parcial(subvetor):
    return np.sum(subvetor)

def soma_multiprocessing(vetor, num_processos):
    tamanho = len(vetor)
    parte = tamanho // num_processos
    subvetores = [vetor[i*parte : (i+1)*parte] for i in range(num_processos - 1)]
    subvetores.append(vetor[(num_processos - 1)*parte:])  # última parte

    with Pool(processes=num_processos) as pool:
        resultados = pool.map(soma_parcial, subvetores)

    return sum(resultados)

if __name__ == "__main__":
    tamanho_vetor = 100_000_000
    vetor = gerar_vetor(tamanho_vetor)

    # Soma serial com NumPy
    inicio = time.time()
    resultado_serial = np.sum(vetor)
    fim = time.time()
    tempo_serial = fim - inicio

    print(f"Soma serial: {resultado_serial}")
    print(f"Tempo serial: {tempo_serial:.4f} segundos\n")

    print("Processos | Tempo (s) | Speedup | Eficiência")
    print("---------------------------------------------")

    for num_processos in [1, 2, 4, 8]:
        inicio = time.time()
        resultado = soma_multiprocessing(vetor, num_processos)
        fim = time.time()
        tempo = fim - inicio
        speedup = tempo_serial / tempo
        eficiencia = speedup / num_processos

        ok = "(OK)" if resultado == resultado_serial else "(ERRO!)"
        print(f"{num_processos:^10} | {tempo:9.4f} | {speedup:7.2f} | {eficiencia:10.2f} {ok}")
