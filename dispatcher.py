import sys
import asyncio

import MemoryManager  # Gerenciador de Memória
import IOManager	    # Gerenciador de Entrada/Saída
import FileManager    # Gerenciador de Arquivos
import ProcessData    # Classe de dados de processo
import Constantes as cons


# Definição do Dispatcher
class Dispatcher:
  def __init__(self):
    self.input_queue = [] # Fila de processos de entrada
    self.out_queue = [] # Fila de processos para redirecionar para IO
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
    # Ordena a fila por tempo de inicialização
    self.input_queue.sort(key=lambda process: process.init_time)
    while len(self.input_queue) > 0:
      filtered_process = self.input_queue.pop(0)
      if filtered_process.priority == 0:
        self.QueueProcess(self.P0, filtered_process)
      elif filtered_process.priority == 1:
        self.QueueProcess(self.P1, filtered_process)
      elif filtered_process.priority == 2:
        self.QueueProcess(self.P2, filtered_process)
      else: 
        # Tudo que não for prioridade 0, 1 ou 2 é 3
        # Impede que processos não sejam alocados por erro de prioridade
        self.QueueProcess(self.P3, filtered_process)

  def PrintProcInfo(self, process_obj):
    # Essa função precisa fazer um monte de conversão de formato para imprimir as infos, por isso é uma bagunça
    args = [
      process_obj.PID,
      process_obj.context["mem_addr"],
      process_obj.memory_space,
      process_obj.priority,
      process_obj.CPU_time-process_obj.context["instruction"],
      process_obj.printer_nmbr,
      process_obj.scanner_nmbr,
      process_obj.modem_nmbr,
      process_obj.disk_nmbr,
      ]
    print("\n------------------- DISPATCHER SCHEDULING -------------------")
    print("\n|PID|OFFSET|BLOCKS|PRIORITY|TIME|PRINTER|SCANNER|MODEM|DRIVE|")
    print("|{0:02d} |{1:002d}   |{2:02d}    |{3:02d}      |{4:02d}  |{5:02d}     |{6:02d}     |{7:02d}   |{8:02d}   |".format(
      args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8]
      ))
    print("\n-------------------------------------------------------------\n")


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
      return cons.ERR_NO_PROCESS

    # Retira o processo da fila e executa
    scheduled_proc = source_queue.pop(0)
    if scheduled_proc.printer_nmbr != 0 or scheduled_proc.scanner_nmbr != 0 or scheduled_proc.modem_nmbr != 0 or scheduled_proc.disk_nmbr != 0:
      self.out_queue.append(scheduled_proc)
    else:
      self.PrintProcInfo(scheduled_proc)
      if scheduled_proc.priority == 0:
        scheduled_proc.RunRealtime() #Prioridade 0: tempo real
      else:
        try:
          # Processos de usuário, escalonados com quantum de 1s
          await asyncio.wait_for(scheduled_proc.Run(),timeout=1.0) 
        except asyncio.TimeoutError:
          if scheduled_proc.priority < 3: 
            scheduled_proc.priority += 1 #Aumenta a prioridade se < 3
          if scheduled_proc.CPU_time - scheduled_proc.context["instruction"] != 0:
            #Ajusta o tempo de inicialização para manter a fila ordenada
            scheduled_proc.init_time = len(self.input_queue)+1 
            self.QueueProcess(self.input_queue, scheduled_proc)
      

def DebugShow(label, variable):
  print("\n--------------------------------------DEBUG-------------------------------------")
  print("\t",label,">>>",variable)
  print("\n--------------------------------------------------------------------------------")

def PrintFSInfo(file_sys):
  print("\n------------------------ FILE SYSTEM ------------------------")
  # Lista de operações
  opnum=1
  for item in file_sys.file_op_list:
    print("\nOperacao",opnum, end=' ')
    opnum +=1
    if item["result"] == cons.RESULT_SUCCESS:
      print("sucesso: o arquivo",item["file_name"],"foi",end=' ')
      if(item["opcode"] == cons.FILEMODE_CREATE):
        print("criado.")
      else:
        print("excluído.")
    elif item["result"] == cons.ERR_NOT_FOUND:
      print("falhou: o arquivo",item["file_name"],"não existe.")
    elif item["result"] == cons.ERR_NO_PROCESS:
      print("falhou: o PID",item["altering_PID"],"não existe.")
    elif item["result"] == cons.ERR_NO_FREE_SPACE:
      print("falhou: Não há espaço para alocação do arquivo",item["file_name"])
    elif item["result"] == cons.ERR_NOT_AUTHORIZED:
      print("falhou: o PID",item["altering_PID"],"não possui permissão para alterar o arquivo",item["file_name"])
    else:
      print(item["result"])
  
  # Cria mapa do disco
  diskmap = []
  for item in file_sys.disk:
    disk_pos = ""
    if item != 0:
      disk_pos = item.file_name
    else:
      disk_pos = "0"
    diskmap.append(disk_pos)
  
  print("\n------------------------- DISK MAP --------------------------")
  print(diskmap)
  print("\n-------------------------------------------------------------\n")


# No início não havia nada, e então o sistema inicializou
# Também conhecido como MAIN():

print("\t ____        _   _                    ___  ____")
print("\t|  _ \\ _   _| |_| |__   ___  _ __    / _ \\/ ___|")
print("\t| |_) | | | | __| '_ \\ / _ \\| '_ \\  | | | \\___ \\")
print("\t|  __/| |_| | |_| | | | (_) | | | | | |_| |___) |")
print("\t|_|    \\__, |\\__|_| |_|\\___/|_| |_|  \\___/|____/")
print("\t       |___/")
print("--------------------------------------------------------------------------------")

# Recebe e filtra a lista de argumentos do programa
if(len(sys.argv)<=1):
  print("  COMO USAR:")
  print("  dispatcher.py [processos] [arquivos]\n    Processos: Arquivo com os dados dos processos")
  print("    Arquivos: Arquivo com os dados do sistema de arquivos\n    (Insira o nome dos arquivos com extensão)")
  exit()
else:
  FNAME_process = sys.argv[1]
  FNAME_files = sys.argv[2]


# Inicializa os recursos do sistema
dsptc = Dispatcher()
fsmgr = FileManager.FileSystem()
iomgr = IOManager.IOManager()

# Inicializa o sistema
dsptc.Boot(FNAME_process)
fsmgr.InitializeFS(FNAME_files)

# Processa as operações de arquivo usando a fila inicial de processos
fsmgr.FileOperations(dsptc.input_queue)


print("processos>>>", dsptc.input_queue)

# Fluxo principal, escalonamento de processos
dsptc_exit = cons.RESULT_SUCCESS
while dsptc_exit != cons.ERR_NO_PROCESS:
  # Procura pelo sinal de IO concluída
  iomgr.GetIOResults(dsptc.input_queue)
  # Reorganiza filas de prioridade
  dsptc.FilterProcesses()
  # Executa escalonamento
  dsptc_exit = asyncio.run(dsptc.ScheduleNext())
  # Chama proximas operações de IO
  for item in dsptc.out_queue:
    res = iomgr.RequestIOForProcess(item)
  iomgr.RunIOOperations()


#Imprime resultado das operações de arquivo
PrintFSInfo(fsmgr)

iomgr.IODEBUG()
