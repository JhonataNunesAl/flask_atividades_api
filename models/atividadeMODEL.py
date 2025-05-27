from datetime import datetime, date
from config import db


class AtividadeNaoEncontrado(Exception):
    pass

class Atividades(db.Model):
    __tablename__ = "atividades"
    
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, nullable=False)
    atividade = db.Column(db.String(100), nullable=False)

    def __init__(self, professor_id, atividade):
        self.professor_id = professor_id
        self.atividade = atividade

    def to_dict(self):
        return {
            'id': self.id,
            'professor_id': self.professor_id,
            'atividade': self.atividade
        }

def listar_atividades():
    atividades = Atividades.query.all()
    return [atividade.to_dict() for atividade in atividades]

def atividade_por_id(id_atividade):
    atividade = Atividades.query.get(id_atividade)
    if not atividade:
        raise AtividadeNaoEncontrado(f'atividade não encontrado.')
    return atividade.to_dict()

def adicionar_atividade(nova_atividade):
    professor_id=int(nova_atividade['professor_id'])
    atividades = Atividades.query.all()
    for atividade in atividades:
        if atividade.professor_id == nova_atividade['professor_id'] and atividade.atividade == nova_atividade['atividade']:
            raise AtividadeNaoEncontrado(f'Atividade já existe para o professor {nova_atividade["professor_id"]} - atividade {nova_atividade["atividade"]}.')
    
    nova_atividade = Atividades(
        professor_id=int(nova_atividade['professor_id']),
        atividade=nova_atividade['atividade']       
    )

    db.session.add(nova_atividade)
    db.session.commit()
    return {"message": "Atividade adicionada com sucesso!"}, 201

def atualizar_atividade(id_atividade, nova_atividade):
    atividade = Atividades.query.get(id_atividade)
    if not atividade:
        raise AtividadeNaoEncontrado
    
    atividades = Atividades.query.all()
    for atividade_for in atividades:
        if atividade_for.professor_id == nova_atividade['professor_id'] and atividade_for.atividade == nova_atividade['atividade']:
            raise AtividadeNaoEncontrado(f'atividade já existe para o professor {nova_atividade["professor_id"]} na atividade {nova_atividade["atividade"]}.')

    atividade.atividade = nova_atividade['atividade']
    atividade.professor_id = nova_atividade['professor_id']
    
    db.session.commit()
    return {"message": "Atividade atualizado com sucesso!"}, 200

def excluir_atividade(id_atividade):
    atividade = Atividades.query.get(id_atividade)
    if not atividade:
        raise AtividadeNaoEncontrado(f'Atividade não encontrado.')

    db.session.delete(atividade)
    db.session.commit()
    return {"message": "Atividade excluida com sucesso!"}, 200
