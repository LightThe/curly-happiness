FP_Process = open("processes.txt",'r')
ProcessData = []
for line in FP_Process:
  CurrentProcess = line.split(',')
  Process = {
    "InitTime": int(CurrentProcess[0]),
    "Priority": int(CurrentProcess[1]),
    "CPUTime": int(CurrentProcess[2]),
    "MemorySpace": int(CurrentProcess[3]),
    "PrinterNo": int(CurrentProcess[4]),
    "ScannerNo": int(CurrentProcess[5]),
    "ModemNo": int(CurrentProcess[6]),
    "DiskNo": int(CurrentProcess[7]),
  }
  ProcessData.append(Process)
FP_Process.close()
FP_Files = open("files.txt",'r')
FP_Files.close()


# Para cada processo, os dados são
# tempo de inicializacao, prioridade, tempo de cpu, blocos (mem), impressora#, scanner?, modem?, disco# 