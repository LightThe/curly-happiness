# Dados do arquivo
class File:
  def __init__(self, file_data):
    self.file_name = file_data[0]
    self.first_block = int(file_data[1])
    self.size = int(file_data[2])
    self.owner = -1 # Se nenhum número de processo criou, o arquivo é acessível por todos (-1)

# Sistema de arquivos e gerenciadores
class FileSystem:
  def __init__(self):
    self.total_blocks = 0 
    self.used_segs = 0
    self.disk = []
  
  # Alocação de arquivo no disco
  def AllocateFile(self, file_obj):
    # Novo arquivo (primeiro bloco = -1), necessario procurar o índice do primeiro bloco, first-fit
    if file_obj.first_block == -1:
      for i in self.disk:
        if self.disk[i] == 0:
          livres = 0 # Contador de blocos sequenciais livres
          for j in range(file_obj.size):
            if self.disk[i+j] == 0:
              livres += 1 # Mais um bloco livre na sequencia de i até o tamanho
            else:
              i = i+(j-1) # move o índice para o próximo bloco ocupado, para recomeçar o teste
          if livres == (file_obj.size): # Se houver algum bloco ocupado, essa conta não bate e tentamos o próximo espaço
            file_obj.first_block = i
            break # Encontramos o índice inicial do arquivo, termina o loop
      # Se o índice não for alterado, não há espaço contíguo para armazenar o arquivo
      if file_obj.first_block == -1:
        print("Não há espaço suficiente para armazenar o arquivo")
    
    # Ao final, armazena o arquivo
    if file_obj.first_block != -1:
      for i in range(file_obj.size):
        self.disk[file_obj.first_block + i] = str(file_obj.file_name)
  
  # Carrega os dados do arquivo de texto
  def InitializeFS(self, FNAME_files):
    FP_files = open(FNAME_files,'r')
    self.total_blocks = int(FP_files.readline())  # Tamanho do disco
    self.used_segs = int(FP_files.readline())     # Segmentos ocupados
    
    # Inicialização do disco
    for i in range(self.total_blocks):
      self.disk.append(0)
    
    # Inicialização dos arquivos existentes
    i = 0
    while i < (self.used_segs):
      line = FP_files.readline()
      file_data = line.split(',')
      file = File(file_data)
      self.AllocateFile(file)
      i += 1
    #TODO: Ler operações de arquivo para manipular o disco.
    FP_files.close()
  
  def DeleteFile(self, file_obj, caller_PID):
    # Se o arquivo não tem dono ou o processo é dono do arquivo, autoriza a exclusão
    if (file_obj.owner != -1) or (file_obj.owner == caller_PID):
      for i in range(file_obj.size):
        self.disk[file_obj.first_block+i] = 0
    else:
      print("Não foi possível completar a operação (permissão negada)")