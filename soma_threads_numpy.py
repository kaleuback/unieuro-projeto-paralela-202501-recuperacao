import time
import numpy as np
import threading

def gerar_vetor(tamanho):
    return np.random.randint(1, 101, size=tamanho, dtype=np.int64)

def soma_serial(vetor):
    return np.sum(vetor)

def soma_parcial(vetor, inicio, fim, resultados, indice):
    resultados[indice] = np.sum(vetor[inicio:fim])

def soma_paralela(vetor, num_threads):
    tamanho = len(vetor)
    threads = []
    resultados = [0] * num_threads
    parte = tamanho // num_threads

    for i in range(num_threads):
        inicio = i * parte
        fim = tamanho if i == num_threads - 1 else (i + 1) * parte
        t = threading.Thread(target=soma_parcial, args=(vetor, inicio, fim, resultados, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(resultados)

def medir_performance(vetor, num_threads_list):
    tempo_serial = None
    resultados = []

    for num_threads in num_threads_list:
        inicio = time.time()
        if num_threads == 1:
            resultado = soma_serial(vetor)
        else:
            resultado = soma_paralela(vetor, num_threads)
        fim = time.time()
        tempo = fim - inicio

        if tempo_serial is None:
            tempo_serial = tempo

        speedup = tempo_serial / tempo
        eficiencia = speedup / num_threads

        resultados.append({
            'threads': num_threads,
            'tempo': tempo,
            'speedup': speedup,
            'eficiencia': eficiencia,
            'resultado': resultado
        })

    return resultados

if __name__ == "__main__":
    tamanho_vetor = 100_000_000
    vetor = gerar_vetor(tamanho_vetor)
    num_threads_list = [1, 2, 4, 8]

    resultados = medir_performance(vetor, num_threads_list)

    print(f"{'Threads':<10}{'Tempo (s)':<15}{'Speedup':<15}{'Eficiência':<15}")
    for r in resultados:
        print(f"{r['threads']:<10}{r['tempo']:<15.4f}{r['speedup']:<15.4f}{r['eficiencia']:<15.4f}")

    print(f"\nSoma com 1 thread: {resultados[0]['resultado']}")
    for r in resultados[1:]:
        print(f"Soma com {r['threads']} threads: {r['resultado']}  {'(OK)' if r['resultado'] == resultados[0]['resultado'] else '(ERRO!)'}")

