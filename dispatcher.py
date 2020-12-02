import sys
import MemoryManager  # Gerenciador de Memória
import IOManager	    # Gerenciador de Entrada/Saída
import FileManager    # Gerenciador de Arquivos
import ProcessData    # Classe de dados de processo

# Recebe a lista de argumentos do programa
if(len(sys.argv)<=1):
  print("\n -----------------------PYTHON OS DISPATCHER-----------------------\n  COMO USAR:\n  dispatcher.py [processos] [arquivos]\n    Processos: Arquivo com os dados dos processos\n    Arquivos: Arquivo com os dados do sistema de arquivos\n")
  exit()
else:
  FNAME_process = sys.argv[1]
  FNAME_files = sys.argv[2]

# Lista de processos
FP_process = open(FNAME_process,'r')
process_queue = [] # Fila de processos prontos
current_PID = 0
# TODO(Theo): Separar a função para adicionar o processo na fila
for line in FP_process:
  current_process = line.split(',')
  # Armazena cada processo com seus parametros
  this_process = ProcessData.Process(current_PID, current_process)
  # Adiciona na fila
  process_queue.append(this_process)
  current_PID += 1
FP_process.close()

# SISTEMA DE ARQUIVOS
FP_files = open(FNAME_files,'r')
# L1: Tamanho do disco (blocos)
# L2: Segementos ocupados no disco (arquivos)
total_blocks = int(FP_files.readline())
used_segments = int(FP_files.readline())
file_data = []
#Leitura de arquivos
for i in range(0, used_segments):
  current_line = FP_files.readline()
  current_file = current_line.split(',')
  file_formatted = {
    "FileName": current_file[0],
    "FirstBlock": int(current_file[1]),
    "Size": int(current_file[2]),
  }
  file_data.append(file_formatted)
FP_files.close()