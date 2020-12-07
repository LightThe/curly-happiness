import Constantes as cons

class IOManager:
  def __init__(self):
    self.scan0_queue = []
    self.prnt0_queue = []
    self.prnt1_queue = []
    self.modm0_queue = []
    self.disk0_queue = []
    self.disk1_queue = []
    self.io_done=[]
  
  def RequestIOForProcess(self, process_obj, IO_request):
    if IO_request == "scan0":
      self.scan0_queue.append(process_obj)
    elif IO_request == "print0":
      self.prnt0_queue.append(process_obj)
    elif IO_request == "print1":
      self.prnt1_queue.append(process_obj)
    elif IO_request == "modem0":
      self.modm0_queue.append(process_obj)
    elif IO_request == "disk0":
      self.disk0_queue.append(process_obj)
    elif IO_request == "disk1":
      self.disk1_queue.append(process_obj)
    else:
      return cons.ERR_NOT_FOUND
    return cons.RESULT_SUCCESS
  
  def GetIOResults(self, destination):
    while len(self.io_done) > 0:
      item = self.io_done.pop(0)
      destination.append(item)
  
  def RunIOOperations(self):
    scanning = self.scan0_queue.pop(0)
    printing0 = self.prnt0_queue.pop(0)
    printing1 = self.prnt1_queue.pop(0)
    networking = self.modm0_queue.pop(0)

    scanning.scanner_nmbr = 0
    printing0.printer_nmbr = 0
    printing1.printer_nmbr = 0
    networking.modem_nmbr = 0

    self.io_done.append(scanning)
    self.io_done.append(printing0)
    self.io_done.append(printing1)
    self.io_done.append(networking)
