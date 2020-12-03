class Process:
  # Para cada processo, os dados são
  # tempo de inicializacao, prioridade, tempo de cpu, 
  # blocos (mem), impressora#, scanner?, modem?, disco#
  def __init__(self, proc_ID, proc_data):
    self.PID = proc_ID
    self.init_time = int(proc_data[0])
    self.priority = int(proc_data[1])
    self.CPU_time = int(proc_data[2])
    self.memory_space = int(proc_data[3])
    self.printer_nmbr = int(proc_data[4])
    self.scanner_nmbr = int(proc_data[5])
    self.modem_nmbr = int(proc_data[6])
    self.disk_nmbr = int(proc_data[7])
  
  def Run(self): #TODO: implementar execução de processo
    exit()