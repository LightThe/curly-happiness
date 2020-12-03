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
    #FIXME: As filas devem suportar no maximo 1000 processos
    self.input_queue = [] # Fila de processos de entrada
    self.current_PID = 0
    self.P0 = []
    self.P1 = []
    self.P2 = []
    self.P3 = []

  def SchedulerMessage():
    exit()

  def QueueProcess(self, destination, process_obj):
    if (len(destination) < 1000) or (destination == self.input_queue):
      destination.append(process_obj)
    else:
      print(f"não foi possível alocar o processo {process_obj.PID}, não há espaço na fila {process_obj.priority}")

  def Boot(self, FNAME_process):
    FP_process = open(FNAME_process,'r')
    for line in FP_process:
      current_process = line.split(',')
      process = ProcessData.Process(self.current_PID, current_process)
      self.QueueProcess(self.input_queue, process)
      self.current_PID += 1
    FP_process.close()
  
  def FilterProcesses(self):
    if len(self.input_queue) == 0:
      return
    self.input_queue.sort(key=lambda process: process.init_time) # Ordena a fila por tempo de inicialização
    while len(self.input_queue) > 0:
      filtered_process = self.input_queue.pop(0)
      print(filtered_process.priority)
      if filtered_process.priority == 0:
        self.QueueProcess(self.P0, filtered_process)
      elif filtered_process.priority == 1:
        self.QueueProcess(self.P1, filtered_process)
      elif filtered_process.priority == 2:
        self.QueueProcess(self.P2, filtered_process)
      else: # Tudo que não for prioridade 0, 1 ou 2 é 3; Impede que processos não sejam alocados por erro de prioridade
        self.QueueProcess(self.P3, filtered_process)

  def ScheduleNext(self):
    if len(self.P0) > 0:
      scheduled_proc = self.P0.pop(0)
      scheduled_proc.run()
    elif len(self.P1) > 0:
      scheduled_proc = self.P1.pop(0)
      scheduled_proc.run() # FIXME: processos não sofrem preempção nunca
    elif len(self.P2) > 0:
      scheduled_proc = self.P2.pop(0)
      scheduled_proc.run()
    elif len(self.P3) > 0:
      scheduled_proc = self.P3.pop(0)
      scheduled_proc.run()
    else:
      exit() #TODO: finalizar o sistema quando não houver mais nada pra escalonar


# No início não havia nada, e então o sistema inicializou
# Também conhecido como MAIN():
sistema = Dispatcher()
sistema.Boot(FNAME_process)
sistema.FilterProcesses()
print(sistema.input_queue) # Imprime a fila de processos pra ver se funciona
print(sistema.P0)
print(sistema.P1)
print(sistema.P2)
print(sistema.P3)

