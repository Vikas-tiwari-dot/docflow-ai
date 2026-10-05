from pydantic import BaseModel
class IntegrationResponse(BaseModel):
    provider: str; connected: bool
