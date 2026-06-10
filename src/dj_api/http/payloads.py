from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class FlexibleModel(BaseModel):
    # DummyJSON 的 add/update 示例经常写 “other ... data”
    # 这里允许额外字段，避免“参数写进脚本”时被模型限制住
    model_config = ConfigDict(extra="allow")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)


class ProductUpsertPayload(FlexibleModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    discountPercentage: Optional[float] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    brand: Optional[str] = None
    tags: Optional[List[str]] = None
    sku: Optional[str] = None
    weight: Optional[float] = None


class CartProductItem(FlexibleModel):
    id: int
    quantity: int = Field(ge=1)


class CartUpsertPayload(FlexibleModel):
    userId: Optional[int] = None
    merge: Optional[bool] = None
    products: Optional[List[CartProductItem]] = None


class UserUpsertPayload(FlexibleModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class PostUpsertPayload(FlexibleModel):
    title: Optional[str] = None
    body: Optional[str] = None
    userId: Optional[int] = None
    tags: Optional[List[str]] = None


class CommentUpsertPayload(FlexibleModel):
    body: Optional[str] = None
    postId: Optional[int] = None
    userId: Optional[int] = None


class TodoUpsertPayload(FlexibleModel):
    todo: Optional[str] = None
    completed: Optional[bool] = None
    userId: Optional[int] = None


class RecipeUpsertPayload(FlexibleModel):
    name: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[List[str]] = None
    prepTimeMinutes: Optional[int] = None
    cookTimeMinutes: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    cuisine: Optional[str] = None
    caloriesPerServing: Optional[int] = None
    tags: Optional[List[str]] = None
    userId: Optional[int] = None
    image: Optional[str] = None
    mealType: Optional[List[str]] = None

