from fastapi import APIRouter, HTTPException, UploadFile, File

from app.schemas.alignment_schema import AlignmentRequest
from app.services.validation_service import (
    ValidationError,
    validate_score_parameters,
    validate_sequences,
)
from app.services.file_service import read_sequences_from_file
from app.services.alignment_service import execute_alignment

router = APIRouter(
    prefix="/api/alignment",
    tags=["Alignment"]
)


@router.post("/")
async def align(request: AlignmentRequest):

    try:
        seq1, seq2 = validate_sequences(
            request.seq1,
            request.seq2
        )

        match, mismatch, gap = validate_score_parameters(
            request.match,
            request.mismatch,
            request.gap
        )

        result = execute_alignment(
            seq1=seq1,
            seq2=seq2,
            match=match,
            mismatch=mismatch,
            gap=gap,
            mode=request.mode
        )

    except ValidationError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "method": request.mode,
        "seq1": seq1,
        "seq2": seq2,
        "parameters": {
            "match": match,
            "mismatch": mismatch,
            "gap": gap
        },
        "score": result["score"],
        "aligned_seq1": result["aligned_seq1"],
        "markers": result["markers"],
        "aligned_seq2": result["aligned_seq2"],
        "matrix": result["matrix"],
        "directions": result["directions"],
        "traceback": result["traceback"],
        "start_position": result["start_position"]
    }

@router.post("/file")
async def align_file(
    file: UploadFile = File(...)
):
    try:
        content = await file.read()

        seq1, seq2 = read_sequences_from_file(
            file.filename,
            content
        )

    except ValidationError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "message": "Arquivo válido.",
        "data": {
            "filename": file.filename,
            "seq1": seq1,
            "seq2": seq2
        }
    }