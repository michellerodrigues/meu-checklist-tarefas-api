class DatasetTarefas:
    def __init__(self):
        self.tarefa = []
        self.categoria = []

    def to_dict(self):
        return {'tarefa': self.tarefa, 'categoria': self.categoria}