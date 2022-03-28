import uvicorn
from fastapi import FastAPI

from observer.domain.observer_job_handler import ObserverJobHandler
from observer.presentation.model.observer_job_event import ObserverJobEvent

app = FastAPI()
observer_job_handler = ObserverJobHandler()


@app.post("/v1/job/observer/ingestion")
def consume_job_event(observer_job_event: ObserverJobEvent):
    count = observer_job_handler.handle_job(observer_job_event)
    return {
        "identifier": observer_job_event.observer_identifier,
        "type": observer_job_event.observer_type.name,
        "count": count
    }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
