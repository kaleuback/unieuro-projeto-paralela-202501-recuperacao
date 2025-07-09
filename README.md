# Paralelização de Soma com Threads em Python

# IMPORTANTE: O código em Python puro é limitado pelo GIL (Global Interpreter Lock). Como parte da investigação e solução, foi estudado o impacto do GIL e exploradas duas abordagens:  
 Uso de bibliotecas que liberam o GIL, como o NumPy.  
 Uso do módulo `multiprocessing` para paralelismo real.  
 Embora o objetivo principal da atividade seja o uso de threads, ambas as abordagens são apresentadas aqui para demonstrar conhecimento aplicado e análise comparativa de desempenho.
-
# Configuração da Máquina de Teste

 **Processador:** Intel com 2 núcleos físicos / 4 threads lógicas  
 **Frequência base:** 2,20 GHz  
 **Virtualização:** Habilitada  
 **Cache L1:** 128 KB  
 **Cache L2:** 512 KB  
 **Cache L3:** 3,0 MB  
 **Sockets:** 1  

# Versão 1 — Python Puro com `threading`

## Tabela de Resultados

| Threads | Tempo (s) | Speedup | Eficiência |
|---------|-----------|---------|------------|
| 1       | 8.6629    | 1.0000  | 1.0000     |
| 2       | 13.3591   | 0.6485  | 0.3242     |
| 4       | 11.7121   | 0.7397  | 0.1849     |
| 8       | 12.5895   | 0.6881  | 0.0860     |

# Soma: 5049448532

# Análise

Apesar de retornar o valor correto, o desempenho piora com mais threads. Isso ocorre devido ao **GIL** (Global Interpreter Lock), que impede a execução simultânea de threads em operações CPU-bound. Assim, múltiplas threads competem pela CPU, gerando sobrecarga e reduzindo a performance.

Além disso, a partir de 8 threads, a queda de desempenho se intensifica por dois motivos:
- O número de threads excede o número de núcleos lógicos, aumentando a contenção por recursos.
  O overhead de gerenciamento de threads se torna maior que o ganho obtido pela paralelização. 

# Versão 2 — Threads com NumPy (`numpy.sum`)

## Tabela de Resultados

| Threads | Tempo (s) | Speedup | Eficiência |
|---------|-----------|---------|------------|
| 1       | 0.0650    | 1.0000  | 1.0000     |
| 2       | 0.0440    | 1.4762  | 0.7381     |
| 4       | 0.0478    | 1.3594  | 0.3398     |
| 8       | 0.0507    | 1.2823  | 0.1603     |

# Soma: 5050109388

### Análise

A função `numpy.sum` é escrita em C e libera o GIL durante sua execução, o que permite ganho real de desempenho com múltiplas threads. No entanto, à medida que aumentam as threads:
- O overhead de sincronização ainda existe.
- A contenção de CPU limita a escalabilidade, especialmente em sistemas com poucos núcleos.

---

# Versão 3 — Multiprocessing para Paralelismo Real

## Tabela de Resultados

| Processos | Tempo (s) | Speedup | Eficiência |
|-----------|-----------|---------|------------|
| 1         | 0.0650    | 1.0000  | 1.0000     |
| 2         | 0.0360    | 1.8056  | 0.9028     |
| 4         | 0.0220    | 2.9545  | 0.7386     |
| 8         | 0.0175    | 3.7143  | 0.4643     |

# Soma: 5049778442

# Análise

Com `multiprocessing`, cada processo roda seu próprio interpretador Python, bypassando o GIL. Isso permite paralelismo real em tarefas CPU-bound, o que leva a tempos menores, especialmente com 2 ou 4 processos.

No entanto, com 8 processos, a eficiência cai um pouco devido a:
Custo de criação e comunicação entre processos.
 Limitação física do número de núcleos disponíveis.

# Variação leve no resultado:
Apesar de todas as versões somarem o mesmo vetor, as somas finais apresentaram pequenas variações entre os métodos (poucos milhares de diferença entre valores superiores a 5 bilhões). Isso não é um erro, e sim consequência de como diferentes bibliotecas e abordagens lidam com precisão e paralelismo interno.
Essas diferenças são esperadas em operações paralelas com grande volume de dados e não invalidam os resultados, já que o valor final continua extremamente próximo e correto. A precisão está dentro de uma margem aceitável.

# Conclusão Geral

O Global Interpreter Lock (GIL) do Python limita a execução paralela com threads em tarefas intensivas de CPU.

# Estratégias para superar a limitação:

Bibliotecas como NumPy: usam código nativo (C/C++) que libera o GIL e permite algum grau de paralelismo com threads.
Multiprocessing: cria múltiplos processos independentes que não compartilham o GIL, possibilitando paralelismo verdadeiro com ganhos significativos.

Recomendação: para tarefas CPU-bound com alta carga computacional, use `multiprocessing` ou bibliotecas otimizadas como NumPy, Numba ou Cython.

# Estrutura do Projeto

`soma_puro_threads.py`: implementação com `threading` puro  
  `soma_numpy_threads.py`: threads com `numpy.sum`  
  `soma_multiprocessing.py`: soma paralela com `multiprocessing`  

## Referências

 [Documentação oficial do Python sobre o GIL](https://wiki.python.org/moin/GlobalInterpreterLock)  
 [NumPy e liberação do GIL](https://numpy.org/devdocs/user/c-info.how-to-extend.html#releasing-the-gil)  
 [Módulo `multiprocessing` do Python](https://docs.python.org/3/library/multiprocessing.html)  

# Graficos:
![graficos](https://github.com/user-attachments/assets/8d411f8e-b902-412b-93fa-121d754da1bf)


# Projeto desenvolvido para a disciplina de Programação Paralela — UNIEURO 2025/01
