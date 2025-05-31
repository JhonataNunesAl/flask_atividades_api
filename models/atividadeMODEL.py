from config import db
from services.verificacao_service import verificar_professor

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
        raise AtividadeNaoEncontrado(f'Atividade não encontrada.')
    return atividade.to_dict()

def adicionar_atividade(nova_atividade):
    professor_id = int(nova_atividade['professor_id'])

    if not verificar_professor(professor_id):
        raise AtividadeNaoEncontrado(f'Professor com ID {professor_id} não encontrado.')

    atividades = Atividades.query.all()
    for atividade in atividades:
        if atividade.professor_id == professor_id and atividade.atividade == nova_atividade['atividade']:
            raise AtividadeNaoEncontrado(f'Atividade já existe para o professor {professor_id} - atividade {nova_atividade["atividade"]}.')

    nova = Atividades(
        professor_id=professor_id,
        atividade=nova_atividade['atividade']
    )

    db.session.add(nova)
    db.session.commit()
    return {"message": "Atividade adicionada com sucesso!"}, 201

def atualizar_atividade(id_atividade, nova_atividade):
    atividade = Atividades.query.get(id_atividade)
    if not atividade:
        raise AtividadeNaoEncontrado('Atividade não encontrada.')

    atividade.atividade = nova_atividade['atividade']
    atividade.professor_id = nova_atividade['professor_id']
    
    db.session.commit()
    return {"message": "Atividade atualizada com sucesso!"}, 200

def excluir_atividade(id_atividade):
    atividade = Atividades.query.get(id_atividade)
    if not atividade:
        raise AtividadeNaoEncontrado('Atividade não encontrada.')

    db.session.delete(atividade)
    db.session.commit()
    return {"message": "Atividade excluída com sucesso!"}, 200
