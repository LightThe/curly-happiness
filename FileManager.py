# Dados do arquivo
class File:
  def __init__(self, file_data):
    self.file_name = file_data[0].strip()
    self.first_block = int(file_data[1])
    self.size = int(file_data[2])
    self.owner = -1 # Se nenhum número de processo criou, o arquivo é acessível por todos (-1)

  def SetOwnership(self, owner):
    self.owner = int(owner)

# Sistema de arquivos e gerenciadores
class FileSystem:
  def __init__(self):
    self.total_blocks = 0 
    self.used_segs = 0
    self.disk = []
    self.file_op_list = []
  
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
    
    # Leitura das operações do disco
    for line in FP_files:
      operation = line.split(',')
      operation_parameters = {
        "altering_PID": int(operation[0]),
        "opcode": int(operation[1]),
        "file_name": operation[2].strip(),
        "create_blocks": int(operation[1]),
      }
      self.file_op_list.append(operation_parameters)
    FP_files.close()
  
  def DeleteFile(self, file_obj, caller_PID):
    # Se o arquivo não tem dono ou o processo é dono do arquivo, autoriza a exclusão
    if (file_obj.owner != -1) or (file_obj.owner == caller_PID):
      for i in range(file_obj.size):
        self.disk[file_obj.first_block+i] = 0
    else:
      print("Não foi possível completar a operação (permissão negada)")

  def FileOperations(self, process_list):
    copyof_process_list = process_list.copy()
    process_exist = 0

    for current_op in self.file_op_list:
      # Verifica a existência do processo
      for process in copyof_process_list:
        if current_op["altering_PID"] == process.PID:
          process_exist = 1
      if process_exist == 0:
        return 1 # TODO: Processo não existe, erro 1
      
      # Verifica o tipo de operação
      if current_op["opcode"] == 0: #FILEMODE_CREATE
        file_data = [current_op["file_name"], 0, current_op["create_blocks"]]
        new_file = File(file_data)
        new_file.SetOwnership(current_op["altering_PID"])
        self.AllocateFile(new_file)
      elif current_op["opcode"] == 1: #FILEMODE_DELETE
        file_data = [current_op["file_name"], 0, 0]
        del_file = File(file_data)
        self.DeleteFile(del_file, current_op["altering_PID"])

