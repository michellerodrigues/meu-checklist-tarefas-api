from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.questionario import criar_questionario, obter_questionario_usuario
from database.database import SessionLocal
from schemas.questionario import QuestionarioResponse, ResponderQuestionarioRequest, ResponderQuestionarioResponse



router = APIRouter(prefix="/questionarios", tags=["Questionários"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{email}", response_model=QuestionarioResponse,
            summary="Obtem o questionário do usuário pelo email dele",
            response_description="Devolve o esquema completo do questionário com as perguntas e as opções disponiiveis. " \
            "As opções selecionadas com suas respectivas tags." \
            "Se o usuário acabou de fazer o login pela 1a vez, o questionário ainda não tem respostas")
def obter_questionarios_por_email(email: str, db: Session = Depends(get_db)):
    questionarioUsuario = obter_questionario_usuario(email, db)
        
    if questionarioUsuario is None:
        raise HTTPException(status_code=400, detail="Questionario não respondido")
    
    return questionarioUsuario


@router.post("/", response_model = ResponderQuestionarioResponse,
            summary="Enviar Resposta para questionário do usuário",
            response_description="Devolve o id do questionário com as tags que filtrarão as categorias")
async def criar_novo_questionario( questionario: ResponderQuestionarioRequest, db: Session = Depends(get_db)):

    return await criar_questionario(questionario, db)
    