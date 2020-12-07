import asyncio

import Constantes as cons

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
    self.context = {"instruction": 0, "mem_addr": cons.ERR_UNDEFINED}
  
  async def Run(self): 
    while (self.priority != 0) and (self.context["instruction"] < self.CPU_time):
      print(f"P{self.PID+1} INSTRUCTION", (self.context["instruction"]+1))
      self.context["instruction"] += 1
      await asyncio.sleep(1)
  
  def RunRealtime(self): 
    while (self.context["instruction"] < self.CPU_time):
      print(f"P{self.PID+1} INSTRUCTION", (self.context["instruction"]+1))
      self.context["instruction"] += 1