from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from models import Curso

app = FastAPI()

cursos = {
    1: {
        "titulo": "Programação",
        "aulas": 112,
        "horas": 58
    },
    2: {
        "titulo": "Algoritmo",
        "aulas": 87,
        "horas": 67
    }
} 

@app.put('/cursos/{curso_id}')
async def put(curso_id: int, curso: Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')

@app.delete('/cursos/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado.')

@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post(curso: Curso):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso

@app.get('/cursos')
async def get_cursos():
    return cursos

@app.get("/cursos/{id}")
async def get_cursos_by_id(id: int):
    try:
        curso = cursos[id]
        curso.update({"id": id})
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, 
                 reload=True)
