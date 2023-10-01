from pydantic import BaseModel, Extra, NoneStr


class ExampleModel(BaseModel):
    """
    Example Pydantic model for validating json
    """

    example_id: int
    example_message: NoneStr = None

    class Config:
        extra = Extra.forbid
