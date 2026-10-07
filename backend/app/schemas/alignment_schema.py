from enum import Enum

from pydantic import BaseModel, Field


class AlignmentMode(str, Enum):
    GLOBAL = "global"
    LOCAL = "local"


class AlignmentRequest(BaseModel):
    seq1: str = Field(
        ...,
        description="Primeira sequência de DNA"
    )
    seq2: str = Field(
        ...,
        description="Segunda sequência de DNA"
    )
    match: int = Field(
        ...,
        description="Pontuação para match"
    )
    mismatch: int = Field(
        ...,
        description="Pontuação para mismatch"
    )
    gap: int = Field(
        ...,
        description="Penalidade de gap"
    )
    mode: AlignmentMode = Field(
        ...,
        description="Modo de alinhamento: global ou local"
    )


class AlignmentParameters(BaseModel):
    match: int
    mismatch: int
    gap: int


class TracebackPosition(BaseModel):
    row: int
    column: int
    direction: str


class AlignmentResult(BaseModel):
    method: AlignmentMode

    seq1: str
    seq2: str

    parameters: AlignmentParameters

    score: int

    aligned_seq1: str
    markers: str
    aligned_seq2: str

    matrix: list[list[int]]

    directions: list[list[str | None]]

    traceback: list[TracebackPosition]

    start_position: TracebackPosition | None = None