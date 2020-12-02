import sys
import MemoryManager  # Gerenciador de Memória
import IOManager	    # Gerenciador de Entrada/Saída
import FileManager    # Gerenciador de Arquivos
import ProcessData    # Classe de dados de processo

# Recebe e filtra a lista de argumentos do programa
if(len(sys.argv)<=1):
  print("\n -----------------------DISPATCHER SO PYTHON-----------------------\n  COMO USAR:\n  dispatcher.py [processos] [arquivos]\n    Processos: Arquivo com os dados dos processos\n    Arquivos: Arquivo com os dados do sistema de arquivos\n")
  exit()
else:
  FNAME_process = sys.argv[1]
  FNAME_files = sys.argv[2]

# DEBUG: Quais linhas ele está lendo do aqruivo
# FP_files = open(FNAME_files,'r')
# print(int(FP_files.readline()))  # Tamanho do disco
# print(int(FP_files.readline()))     # Segmentos ocupados
# for line in FP_files:
#   print(line)
# FP_files.close()

# Definição do Dispatcher
class Dispatcher:
  def __init__(self):
    self.process_queue = [] # Fila de processos prontos
    self.current_PID = 0

  def QueueProcess(self, line):
    current_process = line.split(',')
    # Armazena cada processo com seus parametros
    this_process = ProcessData.Process(self.current_PID, current_process)
    # Adiciona na fila
    self.process_queue.append(this_process)
    self.current_PID += 1

  def ReadProcessFile(self, FNAME_process):
    FP_process = open(FNAME_process,'r')
    for line in FP_process:
      self.QueueProcess(line)
    FP_process.close()
