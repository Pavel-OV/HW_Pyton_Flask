from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import pandas as pd
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')
list_of_tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool = False


@app.post('/', response_model=Task)
async def create_task(task: Task):
    task.id = len(list_of_tasks)+1
    # task.id = task.id
    list_of_tasks.append(task)
    return task


@app.get('/', response_class=HTMLResponse)
async def show_task(request: Request):
    task_table = pd.DataFrame([vars(task) for task in list_of_tasks]).to_html()
    return templates.TemplateResponse('tasks.html', {'request': request, 'task_table': task_table})


@app.get('/tasks/{task_id}', response_class=HTMLResponse)
async def show_task(task_id: int):
    for i, task_step in enumerate(list_of_tasks):
        if task_step.id == task_id:
            task =list_of_tasks.pop(i)
            list_of_tasks.insert(i,task)          
            return pd.DataFrame((task)).to_html()
    # return list_of_tasks
            # return task_table


@app.put('/task/{task_id}', response_model=Task)
async def put_task(task_id: int, task: Task):
    for i, task_step in enumerate(list_of_tasks):
        if task_step.id == task_id:
            task.id = task_id
            list_of_tasks[i] = task
            return task


@app.delete('/task/{task_id}', response_class=HTMLResponse)
async def delete_task(task_id: int):
    for i, task_step in enumerate(list_of_tasks):
        if task_step.id == task_id:
            return pd.DataFrame((list_of_tasks.pop(i))).to_html()
