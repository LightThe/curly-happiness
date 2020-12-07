# FIXME: Alguém por favor implemente isso aqui
# EDIT: Não seri quão bem isso rodará junto com o resto do código
class Memoria:
	def __init__(self):
		self.realtime = [0]*64
		self.user = [0]*960

def Criamem(self, pos, blocks, prioridade):		
	if(prioridade == 0):									# se for processo com prioridade máxima (Tempo real)
		for x in range(blocks):							# para o tamanho de blocos do processo
			self.realtime[pos] = 1						# setamos o valor para 1
			pos += 1									# sempre atualizando a posicao para a seguinte
	else:												# se for processo usuario
		for x in range(blocks):
			self.user[pos] = 1
			pos += 1
	# TODO: atualizar o context["mem_address"] no objeto do processo assim que for alocado
        
def retiraMemoria(self, offset, blocks, prioridade):		# funcao que retira da memoria processos ja executados
	if(prioridade == 0):
		for x in range(blocks):
			self.realtime[offset] = 0
			offset += 1
	else:
		for x in range(blocks):
			self.user[offset] = 0
			offset += 1        
