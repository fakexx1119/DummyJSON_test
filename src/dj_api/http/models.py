from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

Order = Literal["asc", "desc"]


class PaginationQuery(BaseModel):
    limit: Optional[int] = Field(default=None, ge=0, description="限制返回数量；limit=0 表示不限制（返回所有）")
    skip: Optional[int] = Field(default=None, ge=0, description="跳过数量（分页）")

    def to_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if self.limit is not None:
            params["limit"] = self.limit
        if self.skip is not None:
            params["skip"] = self.skip
        return params


class SelectQuery(BaseModel):
    # 文档支持 select=key1,key2 或重复 select=key
    select: Optional[Union[str, List[str]]] = Field(default=None, description="返回字段筛选")

    def to_params(self) -> Dict[str, Any]:
        if self.select is None:
            return {}
        if isinstance(self.select, list):
            # 使用逗号拼接，兼容性更好
            return {"select": ",".join(self.select)}
        return {"select": self.select}


class DelayQuery(BaseModel):
    delay: Optional[int] = Field(default=None, ge=0, le=5000, description="模拟延迟（0-5000ms）")

    def to_params(self) -> Dict[str, Any]:
        return {} if self.delay is None else {"delay": self.delay}


class SortQuery(BaseModel):
    sortBy: Optional[str] = Field(default=None, description="排序字段名")
    order: Optional[Order] = Field(default=None, description="asc/desc")

    def to_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if self.sortBy:
            params["sortBy"] = self.sortBy
        if self.order:
            params["order"] = self.order
        return params


def merge_params(*parts: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for p in parts:
        for k, v in p.items():
            if v is None:
                continue
            merged[k] = v
    return merged

