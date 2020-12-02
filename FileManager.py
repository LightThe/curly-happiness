# Dados do arquivo
class File:
  def __init__(self, file_data):
    self.file_name = file_data[0]
    self.first_block = int(file_data[1])
    self.size = int(file_data[2])

# Sistema de arquivos e gerenciadores
class FileSystem:
  def __init__(self):
    # TODO: Montar o sistema de arquivos com base no tamanho do disco
    self.total_blocks = 0 
    self.used_segs = 0
    self.file_allocation = []
  
  # Aloca o arquivo no disco (nome, início, tamanho)
  def AllocateFile(self, line):
    file_data = line.split(',')
    file = File(file_data)
    self.file_allocation.append(file)
  
  # Carrega os dados do arquivo de texto
  def ReadFSFile(self, FNAME_files):
    FP_files = open(FNAME_files,'r')
    self.total_blocks = int(FP_files.readline())  # Tamanho do disco
    self.used_segs = int(FP_files.readline())     # Segmentos ocupados
    i = 0
    while i < (self.used_segs):
      line = FP_files.readline()
      self.AllocateFile(line)
      i += 1
    FP_files.close()
