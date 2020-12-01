# TODO(Theo): Receber nomes de arquivo como argumento.
# Lista de processos
FP_process = open("processes.txt",'r')
process_data = [] # Fila de processos prontos
current_PID = 0
# TODO(Theo): Separar a função para adicionar o processo na fila
for line in FP_process:
  current_process = line.split(',')
  # Armazena cada processo com seus parametros
  # Para cada processo, os dados são
  # tempo de inicializacao, prioridade, tempo de cpu, 
  # blocos (mem), impressora#, scanner?, modem?, disco# 
  this_process = {
    "PID": current_PID,
    "InitTime": int(current_process[0]),
    "Priority": int(current_process[1]),
    "CPUTime": int(current_process[2]),
    "MemorySpace": int(current_process[3]),
    "PrinterNo": int(current_process[4]),
    "ScannerNo": int(current_process[5]),
    "ModemNo": int(current_process[6]),
    "DiskNo": int(current_process[7]),
  }
  current_PID += 1
  # Adiciona na fila
  process_data.append(this_process)
FP_process.close()

# SISTEMA DE ARQUIVOS
FP_files = open("files.txt",'r')

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