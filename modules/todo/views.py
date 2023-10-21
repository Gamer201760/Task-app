from uuid import UUID

from fastapi import APIRouter, status

from modules.todo.crud import Task
from modules.todo.schemas.request import TaskRequestSchema, TaskRequestUpdateSchema
from modules.todo.schemas.response import TaskResponeSchema

router = APIRouter(prefix='/task')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(task: TaskRequestSchema):
    return await Task().create(task=task)


@router.put('/{id}')
async def update(id: UUID, task: TaskRequestUpdateSchema):
    return await Task().create(task=task, id=id)


@router.get('/', response_model=list[TaskResponeSchema])
async def get():
    return await Task().get()


@router.get('/{id}', response_model=TaskResponeSchema)
async def get_by_id(id: UUID):
    task = await Task().get(id=str(id))
    return task[0]


@router.delete('/{id}')
async def delete(id: UUID):
    return {'success': await Task().delete(id=str(id))}
