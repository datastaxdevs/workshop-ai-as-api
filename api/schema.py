from pydantic import BaseModel
from typing import Optional, List

class SingleTextQuery(BaseModel):
    text: str
    skip_cache: bool = False


class MultipleTextQuery(BaseModel):
    texts: List[str]
    echo_input: bool = True
    skip_cache: bool = False
