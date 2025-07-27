from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    title: str = Field(description="Название блюда")
    views: int = Field(ge=0, description="Количество просмотров рецепта")
    cooking_time: int = Field(gt=0, description="Время приготовления блюда")


class RecipeIn(BaseRecipe):
    ingredients: str = Field(description="Список ингредиентов")
    description: str = Field(description="Описание рецепта")


class RecipeDescr(BaseRecipe):
    id: int = Field(description="Номер рецепта")
    ingredients: str = Field(description="Список ингредиентов")
    description: str = Field(description="Описание рецепта")

    class Config:
        from_attributes = True
