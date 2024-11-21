from pydantic import BaseModel

class RuleBase(BaseModel):
    name: str
    condition: str
    action: str

class RuleCreate(RuleBase):
    pass

class Rule(RuleBase):
    id: int

    class Config:
        from_attributes = True 
