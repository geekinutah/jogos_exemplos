#!/bin/env python


############################################################
#
# Dado: uma sequencia de 4 cores
# 5 Cores: Azul, Amarelo, Laranja, Rosa, Preto #
#
# Objetivo: acertar a sequencia correta em seis tentativas
#
# Exemplo:
# Seq: P, R, L, L
# Tentativa #1: A, A, A, A
# Resultado #1: E, E, E, E
#
# Tentativa #2: P, P, P, P
# Resultado #2: C, E, E, E  (Ordem nao importa)

# Tentativa #3: P, P, L, L
# Resultado #3: C, C, C, E

# Tentativa #4: P, P, L, A
# Resultado #4: C, C, E, E

# Tentativa #5: P, L, R, L
# Resultado #5: C, C, P, P
#
############################################################


import itertools
import sys
import time
import termios
import tty

from random import randint
from termcolor import colored


TABULA_NUMEROS = {
        "A": 0,
        "a": 0,
        "V": 1,
        "v": 1,
        "R": 2,
        "r": 2,
        "C": 3,
        "c": 3,
        "B": 4,
        "b": 4,
        }

def azul(s):
    return colored(s,'blue', attrs=['bold'])

def verde(s):
    return colored(s,'green')

def roxa(s):
    return colored(s,'magenta')

def cinza(s):
    return colored(s,'grey', attrs=['bold'])

def branco(s):
    return colored(s,'white', attrs=['bold'])

def vermelho(s):
    return colored(s,'red', attrs=['bold'])

TABULA_CORES = {
        "A": azul("\bA "),
        "a": azul("\bA "),
        "V": verde("\bV "),
        "v": verde("\bV "),
        "R": roxa("\bR "),
        "r": roxa("\bR "),
        "C": cinza("\bC "),
        "c": cinza("\bC "),
        "B": branco("\bB "),
        "b": branco("\bB "),
        }

def getch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

def help():
  text=[]
  text.append(vermelho(" Voce tem seis chances de adivinhar minha senha!\n"))
  text.append(vermelho("Minha senha e uma sequencia de quatro cores,"))
  text.append(vermelho("se a adivinhar, voce ganha o premio!\n"))
  text.append(" Codigos de cores:\n")
  text.append(colored("   Azul   = A\n", 'blue', attrs=['bold']))
  text.append(colored("  Verde  = V\n", 'green'))
  text.append(colored("  Roxa   = R\n", 'magenta'))
  text.append(colored("  Cinza  = C\n", 'grey', attrs=['bold']))
  text.append(colored("  Branco = B\n", 'white', attrs=['bold']))
  for i in text:
      print i,

def spinner(segundos=1):
  t_end = time.time() + segundos
  delay = 0.1
  spinner = itertools.cycle(['-', '/', '|', '\\'])
  while time.time() < t_end:
    sys.stdout.write(spinner.next())  # write the next character
    sys.stdout.flush()                # flush stdout buffer (actual character display)
    time.sleep(delay)
    sys.stdout.write('\b')            # erase the last written char

def deletar_elemento_de_lista(l, e):
  i = l.index(e)
  del l[i]

def gerar_sequencia():
  '''Gerar cinco numeros aleatorios, retornar'''
  seq = []

  for i in range(0,4):
    positivo = randint(0,4)
    seq.append(positivo)

  return seq

def converter_cores_a_numeros(seq):
  # 5 Cores: Azul, Verde, Roxa, Cinza, Branco
  a_retornar = []

  for i in seq:
    a_retornar.append(TABULA_NUMEROS[i])

  return a_retornar

def procura_combinacoes(l1, l2):
  ''' Procurar elementos que tem o valor e ordem/posicao igual.

  exemplo:
      l1 = [1,0]
      l2 = [0,1]

  Nesse caso, a funcao retorna uma lista vazia.

  outro exemplo:
      l1 = [0,1,0,1]
      l2 = [1,1,0,0]

  A funcao retorna '[1,0]'
    '''
  return [i for i, j in zip(l1, l2) if i == j]

def comparar_sequencias(seq1, seq2):
  '''Compara duas sequencias

     O primeiro sequencia e o padrao, segunda e o que e comparada.

     Vai retornar um dicionario de valores tao grande quanto a sequencia padrao
     valores sendo:
       C = Correto
       E = Errado
       P = Correto, mas posicao errado
  '''
  assert len(seq1) == len(seq2)
  original_length = len(seq1)
  s1 = list(seq1)
  correta = procura_combinacoes(s1, seq2)
  #Procurar a primeria ocorrencia de todos os elementos de 'correta' em
  #ambos sequencias, deleta-os.

  for i in correta:
    deletar_elemento_de_lista(s1, i)
    deletar_elemento_de_lista(seq2, i)

  # Organiza a list e deleta elementos para nao fazer contagem duas vezes.
  s1.sort()
  seq2.sort()
  novas_combinacoes = procura_combinacoes(s1, seq2)

  combinacoes = len(procura_combinacoes(s1, seq2))

  if combinacoes > 0:
    for i in novas_combinacoes:
      deletar_elemento_de_lista(s1, i)
      deletar_elemento_de_lista(seq2, i)

  nao_combinacoes = 0

  for i in seq2:
    if i in s1:
      nao_combinacoes = nao_combinacoes + 1

  errado = abs(original_length - len(correta) - combinacoes - nao_combinacoes)

  return {"e": errado,
          "c": len(correta),
          "p": combinacoes + nao_combinacoes}


def advinha(seq, cores=4):
  '''
  1. Prompt for input
  2. Get input
  3. Validate input
  4. Record results
  5. Line Feed
  '''

  resultado = ""
  sys.stdout.write("Coloque os Codigos dos cores: ")
  sys.stdout.flush()

  i = 0
  while i < cores:
    c = getch()
    try:
      TABULA_CORES[c]
      resultado += c
      if i == 0:
        sys.stdout.write(" ")
      sys.stdout.write(TABULA_CORES[c])
      sys.stdout.flush()
      i = i + 1
    except KeyError:
      continue

  return list(resultado)

def mostra_resultados(c, s):
    for i in range(0,100):
        sys.stdout.write("\b")
        sys.stdout.flush()

    sys.stdout.write(vermelho(c['e']))
    sys.stdout.write(verde(c['c']))
    sys.stdout.write(branco(c['p']))
    sys.stdout.write("  ")
    for i in s:
        sys.stdout.write(TABULA_CORES[i])

    for i in range(0,79):
        sys.stdout.write(" ")

    sys.stdout.write("\n")

def start():
  seq_alvo = gerar_sequencia()
  spinner()
  help()
  print colored("Sequence generated!", "red", attrs=['bold'])
  while True:
    seq = advinha(seq_alvo)
    com = comparar_sequencias(seq_alvo, converter_cores_a_numeros(seq))
    spinner()
    mostra_resultados(com, seq)

if __name__ == "__main__":
    start()
