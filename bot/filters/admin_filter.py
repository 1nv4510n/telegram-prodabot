from typing import Union, List

from aiogram.filters import BaseFilter
from aiogram.types import Message

class AdminFilter(BaseFilter):
    def __init__(self, admin_id: Union[int, List[int]]) -> None:
        super().__init__()
        self.admin_id = admin_id
    
    async def __call__(self, message: Message) -> bool:
        if isinstance(self.admin_id, int):
            return message.from_user.id == self.admin_id
        else:
            return message.from_user.id in self.admin_id