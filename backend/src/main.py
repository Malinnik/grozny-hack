import os
import uvicorn

from loguru import logger
from dotenv import load_dotenv
from core.app import create_app

if __name__ == "__main__":
    load_dotenv()
    logger.info("Starting app")

    app = create_app()

    uvicorn.run(app, forwarded_allow_ips="*", proxy_headers=True, port=int(os.getenv('APP_PORT', 80)), host="0.0.0.0")
