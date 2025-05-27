from flask import Blueprint, request, jsonify,render_template,redirect, url_for
from datetime import datetime
from config import db
from models.atividadeMODEL import AtividadeNaoEncontrado, listar_atividades, adicionar_atividade, atualizar_atividade, excluir_atividade, atividade_por_id

atividades_blueprint = Blueprint('atividades', __name__)

@atividades_blueprint.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = listar_atividades()
    return jsonify(atividades)

@atividades_blueprint.route('/atividades', methods=['POST'])
def create_atividade():
    nova_atividade = request.json
    try:
        adicionar_atividade(nova_atividade)
        return jsonify(nova_atividade), 201
    
    except AtividadeNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 400


@atividades_blueprint.route('/atividades/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
        data = request.json
        try:
            atividade = atividade_por_id(id_atividade)
            if not atividade:
                return jsonify({'message': 'Sala não encontrado'}), 404
            atualizar_atividade(id_atividade, data)
            
            return jsonify(data),200
        except AtividadeNaoEncontrado as e:
            return jsonify({'message': str(e)}), 404
   
@atividades_blueprint.route('/atividades/<int:id_atividade>', methods=['DELETE'])
def delete_atividade(id_atividade):
        try:
            excluir_atividade(id_atividade)
            return jsonify({'message': 'Sala excluído com sucesso '}),200
        except AtividadeNaoEncontrado:
            return jsonify({'message': 'Sala não encontrado'}), 404