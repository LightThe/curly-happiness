"""
  Constantes.py
  Uma tentativa de padronizar os códigos de erro entre as classes de programa
  Importe esse arquivo e use os códigos listados sempre que necessário retornar algum erro

  dispatcher.py é o responsável pela impressão dos erros gerados por outros módulos
"""

# Codigos de sucesso 100 - 199
RESULT_SUCCESS = 100

# Erros gerais 200 - 299
ERR_NOT_FOUND = 200
ERR_NOT_AUTHORIZED = 201

# Erros de arquivo 300 - 399
ERR_NO_FREE_SPACE = 300

# Erros de Processo 400 - 499
ERR_NO_PROCESS = 400

# Operações de arquivo (CODIGOS ESPECIAIS)
FILEMODE_CREATE = 0
FILEMODE_DELETE = 1