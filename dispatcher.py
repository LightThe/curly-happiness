import sys
import asyncio

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
    self.input_queue = [] # Fila de processos de entrada
    self.current_PID = 0
    self.P0 = []
    self.P1 = []
    self.P2 = []
    self.P3 = []

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
      if filtered_process.priority == 0:
        self.QueueProcess(self.P0, filtered_process)
      elif filtered_process.priority == 1:
        self.QueueProcess(self.P1, filtered_process)
      elif filtered_process.priority == 2:
        self.QueueProcess(self.P2, filtered_process)
      else: # Tudo que não for prioridade 0, 1 ou 2 é 3; Impede que processos não sejam alocados por erro de prioridade
        self.QueueProcess(self.P3, filtered_process)

  async def ScheduleNext(self):
    # Seleciona a fila para retirar o processo
    source_queue = []
    if len(self.P0) > 0:
      source_queue = self.P0
    elif len(self.P1) > 0:
      source_queue = self.P1
    elif len(self.P2) > 0:
      source_queue = self.P2
    elif len(self.P3) > 0:
      source_queue = self.P3
    else:
      return 1

    # Retira o processo da fila e executa
    scheduled_proc = source_queue.pop(0)
    if scheduled_proc.priority == 0:
      scheduled_proc.RunRealtime() #Prioridade 0: tempo real
    else:
      try:
        await asyncio.wait_for(scheduled_proc.Run(),timeout=1.0) # Processos de usuário, 
      except asyncio.TimeoutError:
        if scheduled_proc.priority < 3: 
          scheduled_proc.priority += 1 #Aumenta a prioridade se < 3
        if scheduled_proc.context["instruction"] < scheduled_proc.CPU_time:
          scheduled_proc.init_time = len(self.input_queue)+1 #Ajusta o tempo de inicialização para manter a fila ordenada
          self.QueueProcess(self.input_queue, scheduled_proc)
      


# No início não havia nada, e então o sistema inicializou
# Também conhecido como MAIN():
#TODO: finalizar o sistema quando não houver mais nada pra escalonar
sistema = Dispatcher()
sistema.Boot(FNAME_process)
print("Entrada:",sistema.input_queue) # Imprime a fila de processos pra ver se funciona
sistema.FilterProcesses()
exit_flag = 0
limit=0
while exit_flag != 1 and limit < 200:
  exit_flag = asyncio.run(sistema.ScheduleNext())
  sistema.FilterProcesses()
  limit+=1

