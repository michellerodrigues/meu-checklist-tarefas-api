from __future__ import annotations

import json

from fastapi import HTTPException
from fastapi import status
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from models.questionario import OpcaoModel
from models.questionario import PerguntaModel
from models.questionario import QuestionarioModel
from models.questionario import RespostaModel
from models.usuario import UsuarioModel
from schemas.converters import QuestionarioConverter
from schemas.questionario import ResponderQuestionarioRequest
from schemas.questionario import ResponderQuestionarioResponse


async def criar_questionario(questionario: ResponderQuestionarioRequest, db: Session):
    try:

        respostas_para_inserir = []

        for resposta in questionario.respostas:
            if not resposta.opcoes_selecionadas:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Todas as perguntas devem ser respondidas',
                )

            for opcao_id in resposta.opcoes_selecionadas:
                respostas_para_inserir.append(
                    {'questionario_id': questionario.id, 'opcao_id': int(opcao_id)},
                )

        if respostas_para_inserir:
            try:
                with db.begin():
                    deletar_questionario_stmt = delete(RespostaModel.__table__).where(
                        RespostaModel.__table__.c.questionario_id == questionario.id,
                    )
                    db.execute(deletar_questionario_stmt)

                    inserir_novo_stmt = insert(RespostaModel.__table__).values(
                        respostas_para_inserir,
                    )
                    db.execute(inserir_novo_stmt)
                    db.commit()

            except SQLAlchemyError as e:
                db.rollback()

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro na transação: {str(e)}",
                ) from e

        opcoes_ids = [resposta['opcao_id'] for resposta in respostas_para_inserir]
        tags_unicas = __get_tags_unicas(db, opcoes_ids)

        return ResponderQuestionarioResponse(
            mensagem='Questionário salvo com sucesso',
            questionario_id=questionario.id,
            tags_usuario=tags_unicas,
        )

    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro de formato nos dados: {str(e)}",
        ) from e

    except HTTPException as he:
        raise he

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}",
        ) from e


def get_db_usuario_by_email(email: str, db: Session):

    usuario = db.execute(select(UsuarioModel).where(UsuarioModel.email == email))
    usuario = usuario.scalars().first()

    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    return usuario


def obter_questionario_usuario(email: str, db: Session):

    usuario = get_db_usuario_by_email(email, db)

    questionario = db.execute(
        select(QuestionarioModel)
        .where(QuestionarioModel.usuario_id == usuario.id)
        .order_by(QuestionarioModel.data_criacao.desc())
        .limit(1),
    )
    questionario = questionario.scalars().first()

    if not questionario:
        return None

    perguntas = db.execute(
        select(PerguntaModel).options(
            selectinload(PerguntaModel.opcoes).selectinload(OpcaoModel.respostas),
        ),
    )

    return QuestionarioConverter.to_schema(perguntas, questionario.id)


def get_tags_do_usuario(questionarioRespondido):
    selected_tags = set()

    for pergunta in questionarioRespondido:
        for opcao in pergunta['opcoes']:
            if opcao['selecionada']:
                formatted_tags = [
                    tag.lower().replace(' ', '-') for tag in opcao['tags']
                ]
                selected_tags.update(formatted_tags)

    return sorted(list(selected_tags))


def __get_tags_unicas(db: Session, opcoes_ids: list[int]) -> list[str]:

    resultados = db.query(OpcaoModel.tags).filter(OpcaoModel.id.in_(opcoes_ids)).all()

    tags_unicas = set()

    for (tags_str,) in resultados:
        try:
            tags_list = json.loads(tags_str)
            tags_unicas.update(tags_list)
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON: {tags_str}")

    return list(tags_unicas)
