from pydantic import BaseModel, ConfigDict


class AchievementBase(BaseModel):
    name: str
    description: str
    image: str


class Achievement(AchievementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
