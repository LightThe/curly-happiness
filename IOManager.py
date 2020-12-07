import Constantes as cons

class IOManager:
  def __init__(self):
    # Uma fila por dispositivo
    self.scan0_queue = []
    self.prnt0_queue = []
    self.prnt1_queue = []
    self.modm0_queue = []
    self.disk0_queue = []
    self.disk1_queue = []
    # Fila de processos com IO finalizada (signal)
    self.io_done=[]
  
  # Recebe pedidos para operações de IO e coloca os processos na fila de dispositivo
  def RequestIOForProcess(self, process_obj):
    if process_obj.scanner_nmbr != 0:
      self.scan0_queue.append(process_obj)
    elif process_obj.printer_nmbr == 1:
      self.prnt0_queue.append(process_obj)
    elif process_obj.printer_nmbr == 2:
      self.prnt1_queue.append(process_obj)
    elif process_obj.modem_nmbr != 0:
      self.modm0_queue.append(process_obj)
    elif process_obj.disk_nmbr == 1:
      self.disk0_queue.append(process_obj)
    elif process_obj.disk_nmbr == 2:
      self.disk1_queue.append(process_obj)
    else:
      return cons.ERR_NOT_FOUND
    return cons.RESULT_SUCCESS
  
  # Copia o resultado das operações de IO para a fila de destino
  def GetIOResults(self, destination):
    while len(self.io_done) > 0:
      item = self.io_done.pop(0)
      item.init_time = len(destination)+1
      destination.append(item)
  
  # Realiza as operações de IO no começo da fila
  def RunIOOperations(self):
    if len(self.scan0_queue) > 0:
      scanning = self.scan0_queue.pop(0)
      scanning.scanner_nmbr = 0
      self.io_done.append(scanning)
    if len(self.prnt0_queue) > 0:
      printing0 = self.prnt0_queue.pop(0)
      printing0.printer_nmbr = 0
      self.io_done.append(printing0)
    if len(self.prnt1_queue) > 0:
      printing1 = self.prnt1_queue.pop(0)
      printing1.printer_nmbr = 0
      self.io_done.append(printing1)
    if len(self.modm0_queue) > 0:
      networking = self.modm0_queue.pop(0)
      networking.modem_nmbr = 0
      self.io_done.append(networking)
    if len(self.disk0_queue) > 0:
      disking0 = self.disk0_queue.pop(0)
      disking0.disk_nmbr = 0
      self.io_done.append(disking0)
    if len(self.disk1_queue) > 0:
      disking1 = self.disk1_queue.pop(0)
      disking1.disk_nmbr = 0
      self.io_done.append(disking1)
  
  def IODEBUG(self):
    print("Scanner:",self.scan0_queue)
    print("Printer 1:",self.prnt0_queue)
    print("Printer 2:",self.prnt1_queue)
    print("Modem:",self.modm0_queue)
    print("Disk 1:",self.disk0_queue)
    print("Disk 2:",self.disk0_queue)