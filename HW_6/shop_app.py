import uvicorn
import random
from typing import List
from fastapi import FastAPI, Path
from datetime import datetime, timedelta
from flask import app

from HW_6.database import *
from HW_6.model_base import *




app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return {"Сообщение": "Тестовый сервер интернет магизина запущен"}

@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int = Path(..., ge=1)):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname,
                                  email=user.email, password=user.password)
    actual_id = await database.execute(query)
    return {**user.model_dump(), 'id': actual_id}


@app.put('/users/{user_id}', response_model=User)
async def update_user(new_user: UserIn, user_id: int = Path(..., ge=1)):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), 'id': user_id}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(..., ge=1)):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'Сообщение': f'Пользователь с идентификатором {user_id} был удален.'}


@app.get('/goods/', response_model=List[Goods])
async def get_all_goods():
    query = goods.select()
    return await database.fetch_all(query)


@app.get('/goods/{product_id}', response_model=Goods)
async def get_goods(product_id: int = Path(..., ge=1)):
    query = goods.select().where(goods.c.id == product_id)
    return await database.fetch_one(query)


@app.post('/goods/', response_model=Goods)
async def create_product(product: GoodsIn):
    query = goods.insert().values(title=product.title,
                                  description=product.description, price=product.price)
    actual_id = await database.execute(query)
    return {**product.model_dump(), 'id': actual_id}


@app.put('/goods/{product_id}', response_model=Goods)
async def update_product(new_product: GoodsIn, product_id: int = Path(..., ge=1)):
    query = goods.update().where(goods.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), 'id': product_id}


@app.delete('/goods/{product_id}')
async def delete_product(product_id: int = Path(..., ge=1)):
    query = goods.delete().where(goods.c.id == product_id)
    await database.execute(query)
    return {'Сообщение': f'Пользователь с идентификатором {product_id} был удален.'}


@app.get('/orders/', response_model=List[Order])
async def get_all_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get('/orders/{order_id}', response_model=Order)
async def get_order(order_id: int = Path(..., ge=1)):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(order_date=order.order_date, status=order.status,
                                   user_id=order.user_id, goods_id=order.goods_id)
    actual_id = await database.execute(query)
    return {**order.model_dump(), 'id': actual_id}


@app.put('/orders/{order_id}', response_model=Order)
async def update_order(new_order: OrderIn, order_id: int = Path(..., ge=1)):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), 'id': order_id}


@app.delete('/orders/{order_id}')
async def delete_order(order_id: int = Path(..., ge=1)):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'Сообщение': f'Пользователь с идентификатором {order_id} был удален.'}


@app.get('/test_users/{count}')
async def create_users(count: int):
    for i in range(count):
        query = users.insert().values(name=f'Имя{i}',
                                      surname=f'Фамилия{i}',
                                      email=f'email{i}@mail.ru',
                                      password=f'qwerty{i}')
        await database.execute(query)
    return {'Сообщение': f'{count}: Тестовые пользователи были добавлены в базу данных.'}


@app.get('/test_goods/{count}')
async def create_goods(count: int):
    for i in range(count):
        query = goods.insert().values(title=f'Наименование товара {i}',
                                      description='Описание товара',
                                      price=f'{random.randint(1, 100000):.2f}')
        await database.execute(query)
    return {'Сообщение': f'{count}: Тестовые товары были добавлены в базу данных.'}


@app.get('/test_orders/{count}')
async def create_orders(count: int):
    for i in range(count):
        query = orders.insert().values(order_date=datetime.strptime("2020-01-24", "%Y-%m-%d").date() + timedelta(days=i ** 2),
                                       status=random.choice(
                                           ['в работе', 'выполнен', 'отмененный']),
                                       user_id=random.randint(1, 10),
                                       goods_id=random.randint(1, 10))
        await database.execute(query)
    return {'Сообщение': f'{count}: Тестовые заказы были добавлены в базу данных.'}


if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=8000, reload=True)
