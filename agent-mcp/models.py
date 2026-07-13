from pydantic import BaseModel, Field


class NoteRfqRequest(BaseModel):
    """Note RFQ request payload, field names match the Java MCP contract."""

    undelryingRetutersCode: str = Field(description="Underlying Reuters code")
    payoffCode: str = Field(description="Payoff code")
    currencyCode: str = Field(description="Currency code")
