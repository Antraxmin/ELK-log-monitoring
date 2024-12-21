from fastapi import FastAPI, Request
import logging
import time
from datetime import datetime
import json

app = FastAPI()

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.get("/")
async def root(request: Request):
    start_time = time.time()
    response = {"message": "Hello, ELK!"}
    process_time = time.time() - start_time
    
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "client_ip": request.client.host,
        "method": request.method,
        "path": str(request.url.path),
        "status_code": 200,
        "process_time_ms": round(process_time * 1000, 2),
        "user_agent": str(request.headers.get("user-agent")),
        # 중첩된 딕셔너리도 문자열화
        "request_info": {
            "headers": dict(request.headers),
            "query_params": dict(request.query_params)
        }
    }
    
    # ensure_ascii=False로 설정하고, separators 옵션으로 공백 제거
    json_log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':'))
    logging.info("Request processed: " + json_log)
    return response

@app.get("/error")
async def trigger_error(request: Request):
    start_time = time.time()
    process_time = time.time() - start_time
    
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "client_ip": request.client.host,
        "method": request.method,
        "path": str(request.url.path),
        "status_code": 500,
        "process_time_ms": round(process_time * 1000, 2),
        "user_agent": str(request.headers.get("user-agent")),
        "error_type": "Internal Server Error",
        "request_info": {
            "headers": dict(request.headers),
            "query_params": dict(request.query_params)
        }
    }
    
    json_log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':'))
    logging.error("Error occurred: " + json_log)
    return {"message": "Error occurred"}, 500