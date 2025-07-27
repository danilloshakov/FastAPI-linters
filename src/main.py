from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import select, update

import schemas
from orm_models import Base, Recipes, Session, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Очистка при завершении
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post(
    "/recipes",
    response_model=schemas.RecipeIn,
    status_code=201,
    tags=["Рецепты"],
    summary="Создать новый рецепт",
)
async def add_recipe(recipe: schemas.RecipeIn):
    new_recipe = Recipes(
        title=recipe.title,
        views=recipe.views,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
        description=recipe.description,
    )
    async with Session() as session:
        session.add(new_recipe)
        await session.commit()
    return new_recipe


@app.get(
    "/recipes",
    status_code=200,
    summary="Получить список всех рецептов",
    tags=["Рецепты"],
    response_model=List[schemas.BaseRecipe],
)
async def get_all_recipes():
    async with Session() as session:
        order_stmt = Recipes.views.desc()
        res = await session.execute(select(Recipes).order_by(order_stmt))
    return [
        {"title": r.title, "views": r.views, "cooking_time": r.cooking_time}
        for r in res.scalars().all()
    ]


@app.get(
    "/recipes/{recipe_id}",
    status_code=200,
    summary="Получить детальную информацию о конкретном рецепте",
    tags=["Рецепты"],
    response_model=schemas.RecipeDescr,
)
async def get_description_recipe(recipe_id: int):
    async with Session() as session:
        where_stmt = Recipes.id == recipe_id
        res = await session.execute(select(Recipes).where(where_stmt))
        recipe = res.scalars().one_or_none()

        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        await session.execute(
            update(Recipes)
            .where(Recipes.id == recipe_id)
            .values(views=recipe.views + 1)
        )
        await session.commit()

    return recipe


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
