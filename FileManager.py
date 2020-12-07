# Dados do arquivo
import Constantes as cons

class File:
  def __init__(self, file_data):
    self.file_name = file_data[0].strip()
    self.first_block = int(file_data[1])
    self.size = int(file_data[2])
    self.owner = cons.ERR_UNDEFINED # Se nenhum número de processo criou, o arquivo é acessível por todos

  def SetOwnership(self, owner):
    self.owner = int(owner)

# Sistema de arquivos e gerenciadores
class FileSystem:
  def __init__(self):
    # Parâmetros do sistema de arquivos
    self.total_blocks = 0 
    self.used_segs = 0
    self.disk = []
    self.file_op_list = []
  
  # Alocação de arquivo no disco
  def AllocateFile(self, file_obj):
    # Novo arquivo (primeiro bloco undefined), necessario procurar o índice do primeiro bloco, first-fit
    if file_obj.first_block == cons.ERR_UNDEFINED:
      for i in range(len(self.disk)):
        if self.disk[i] == 0:
          livres = 0 # Contador de blocos sequenciais livres
          for j in range(file_obj.size):
            if i+j<len(self.disk):
              if self.disk[i+j] == 0:
                livres += 1 # Mais um bloco livre na sequencia de i até o tamanho
              else:
                i = i+(j-1) # move o índice para o próximo bloco ocupado, para recomeçar o teste
            else:
              return cons.ERR_NO_FREE_SPACE
          if livres == (file_obj.size): # Se houver algum bloco ocupado, essa conta não bate e tentamos o próximo espaço
            file_obj.first_block = i
            break # Encontramos o índice inicial do arquivo, termina o loop
      
      # Se o índice não for alterado, não há espaço contíguo para armazenar o arquivo
      if file_obj.first_block == cons.ERR_UNDEFINED:
        return cons.ERR_NO_FREE_SPACE
    
    # Ao final, armazena o arquivo
    if file_obj.first_block != cons.ERR_UNDEFINED:
      for i in range(file_obj.size):
        self.disk[file_obj.first_block + i] = file_obj #str(file_obj.file_name)
      return cons.RESULT_SUCCESS    
  
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
      if int(operation[1]) == cons.FILEMODE_CREATE:
        blocks = int(operation[3])
      else:
        blocks = 0
      operation_parameters = {
        "altering_PID"  : int(operation[0]),
        "opcode"        : int(operation[1]),
        "file_name"     : operation[2].strip(),
        "create_blocks" : blocks,
        "result"        : cons.ERR_UNDEFINED
      }
      self.file_op_list.append(operation_parameters)
    FP_files.close()
  
  def DeleteFile(self, file_name, caller_PID):
    file_start = cons.ERR_UNDEFINED

    # Procura pelo arquivo por nome
    for index in range(len(self.disk)):
      if self.disk[index].file_name == file_name:
        # Ao encontrar um bloco que seja do arquivo, recupera o endereço inicial dele.
        file_start = self.disk[index].first_block
        break
    
    # Se não encontrou depois do loop, o arquivo não está no disco (não existe)
    if file_start == cons.ERR_UNDEFINED:
      return cons.ERR_NOT_FOUND
    
    # Se o arquivo foi encontrado, recupera os dados dele no disco
    file_obj = self.disk[file_start]

    # Se o arquivo não tem dono ou o processo é dono do arquivo, autoriza a exclusão
    if (file_obj.owner == cons.ERR_UNDEFINED) or (file_obj.owner == caller_PID):
      for i in range(file_obj.size):
        self.disk[file_obj.first_block+i] = 0
    else:
      return cons.ERR_NOT_AUTHORIZED # Permissão negada (não é o dono do arquivo)
    return cons.RESULT_SUCCESS

  def FileOperations(self, process_list):
    copyof_process_list = process_list.copy()

    for current_op in self.file_op_list:
      # Verifica a existência do processo
      process_exists = 0
      for process in copyof_process_list:
        if current_op["altering_PID"] == process.PID:
          process_exists = 1
      if process_exists == 0:
        current_op["result"] = cons.ERR_NO_PROCESS
        continue
      # Verifica o tipo de operação
      if current_op["opcode"] == cons.FILEMODE_CREATE:
        file_data = [current_op["file_name"],cons.ERR_UNDEFINED, current_op["create_blocks"]]
        new_file = File(file_data)
        new_file.SetOwnership(current_op["altering_PID"])

        current_op["result"] = self.AllocateFile(new_file)
      elif current_op["opcode"] == cons.FILEMODE_DELETE:
        current_op["result"] = self.DeleteFile(current_op["file_name"], current_op["altering_PID"])
      else:
        current_op["result"] = cons.ERR_NOT_FOUND
        continue


