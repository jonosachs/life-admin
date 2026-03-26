from functions.run_pipeline.pipeline import lambda_handler as run_pipeline
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    run_pipeline(None, None)
