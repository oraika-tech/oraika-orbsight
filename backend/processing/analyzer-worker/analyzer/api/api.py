import logging

import uvicorn
from fastapi import FastAPI, HTTPException, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from analyzer.api.tiyaro_exception import TiyaroException
from analyzer.model.api_request_response import AnalyzerAPIResponse, AnalyzerAPIRequest
from analyzer.model.data_store_request import DBStoreRequest, ObserverInfo, EntityInfo
from analyzer.model.structure_data_request import UnstructuredDataRequest
from analyzer.service.structure_data_extractor import StructuredDataExtractor
from analyzer.service.processed_data_entity_manager import ProcessedDataEntityManager

logger = logging.getLogger(__name__)
PORT = 8080


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


app = FastAPI(
    title="Analyzer Worker",
    debug=True,
    description="Analyzer worker api"
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_error_handler)

router = APIRouter()
app.include_router(router)

structure_data_extractor: StructuredDataExtractor = StructuredDataExtractor()
structured_data_store: ProcessedDataEntityManager = ProcessedDataEntityManager()


@app.on_event("startup")
def app_init():
    logger.info(f"Open http://127.0.0.1:{PORT}/redoc")


@app.post(
    "/v1/job/analyzer/ingestion",
    response_model=AnalyzerAPIResponse,
    response_model_exclude_unset=True,
    tags=["worker", "analyzer", "processing"]
)
def update_workflow(request: AnalyzerAPIRequest):
    try:
        structured_data = structure_data_extractor.extract_structure_fast(
            UnstructuredDataRequest(
                company_id=request.company_id,
                raw_text=request.text_data.raw_text
            )
        )
        structured_data_identifier = structured_data_store.insert_structure_data(
            data_request=DBStoreRequest(
                structured_data=structured_data,
                raw_data_identifier=request.text_data.identifier,
                company_id=request.company_id,
                event_time=request.text_data.event_time,
                observer_info=ObserverInfo(
                    identifier=request.observer.identifier,
                    name=request.observer.name,
                    type=request.observer.type.name,
                    regulated_entity_type=request.observer.regulated_entity_type,
                ),
                entity_info=EntityInfo(
                    identifier=request.entity.identifier,
                    simple_name=request.entity.simple_name,
                    country=request.entity.country,
                    city=request.entity.city
                )
            )
        )
        return AnalyzerAPIResponse(identifier=structured_data_identifier)
    except TiyaroException as ex:
        logger.error(f"Tiyaro Exception occur: {ex}")
        raise HTTPException(status_code=500, detail=f"Tiyaro error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
