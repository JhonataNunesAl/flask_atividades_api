from flask import Blueprint, request, jsonify
from models.atividadeMODEL import (
    AtividadeNaoEncontrado, listar_atividades, adicionar_atividade,
    atualizar_atividade, excluir_atividade, atividade_por_id
)

atividades_blueprint = Blueprint('atividades', __name__)

@atividades_blueprint.route('/atividades', methods=['GET'])
def get_atividades():
    """
    Lista todas as atividades
    ---
    responses:
      200:
        description: Lista de atividades
    """
    atividades = listar_atividades()
    return jsonify(atividades)

@atividades_blueprint.route('/atividades', methods=['POST'])
def create_atividade():
    """
    Cria uma nova atividade
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Atividade
          required:
            - professor_id
            - atividade
          properties:
            professor_id:
              type: integer
            atividade:
              type: string
    responses:
      201:
        description: Atividade criada
      400:
        description: Erro na criação
    """
    nova_atividade = request.json
    try:
        adicionar_atividade(nova_atividade)
        return jsonify(nova_atividade), 201
    except AtividadeNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 400

@atividades_blueprint.route('/atividades/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
    """
    Atualiza uma atividade
    ---
    parameters:
      - in: path
        name: id_atividade
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          id: Atividade
          required:
            - professor_id
            - atividade
          properties:
            professor_id:
              type: integer
            atividade:
              type: string
    responses:
      200:
        description: Atividade atualizada
      404:
        description: Atividade não encontrada
    """
    data = request.json
    try:
        atividade_por_id(id_atividade)
        atualizar_atividade(id_atividade, data)
        return jsonify(data), 200
    except AtividadeNaoEncontrado as e:
        return jsonify({'message': str(e)}), 404

@atividades_blueprint.route('/atividades/<int:id_atividade>', methods=['DELETE'])
def delete_atividade(id_atividade):
    """
    Deleta uma atividade
    ---
    parameters:
      - in: path
        name: id_atividade
        type: integer
        required: true
    responses:
      200:
        description: Atividade deletada
      404:
        description: Atividade não encontrada
    """
    try:
        excluir_atividade(id_atividade)
        return jsonify({'message': 'Atividade excluída com sucesso'}), 200
    except AtividadeNaoEncontrado:
        return jsonify({'message': 'Atividade não encontrada'}), 404
