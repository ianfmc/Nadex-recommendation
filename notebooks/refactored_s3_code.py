# Refactored S3 Functions to Use s3.yaml Configuration
# Copy these into your Jupyter notebook cells

# ============================================================================
# CELL: Define a function to upload the recommendations to S3
# ============================================================================
import io
import boto3
import pandas as pd
from botocore.exceptions import ClientError
from botocore import UNSIGNED
from botocore.config import Config

from typing import Iterable, List, Dict

def create_s3_clients(
    profile: str = "default", region: str = None
) -> Dict[str, boto3.client]:
    """
    Create S3 clients for public and private access.
    Now uses region from s3.yaml if not explicitly provided.
    """
    session = boto3.Session(profile_name=profile, region_name=region)
    return {
        "public": session.client(
            "s3",
            config=Config(signature_version=UNSIGNED),
            region_name=region,
        ),
        "private": session.client("s3"),
        "resource": session.resource("s3"),
    }

def get_bucket(resource: boto3.resource, name: str):
    return resource.Bucket(name)

def upload_df_to_s3(
    df: pd.DataFrame,
    bucket: str,
    key: str,
    region: str = None) -> None:
    """
    Uploads a DataFrame to S3 as CSV. Verifies bucket existence first.
    
    Parameters
    ----------
    df : pd.DataFrame
    bucket : str
        Name of the S3 bucket (no leading/trailing spaces).
    key : str
        S3 object key, e.g. "csv/2025-06-28-results.csv"
    region : str, optional
        AWS region where the bucket resides.
    """
    bucket = bucket.strip()
    s3 = boto3.client('s3', region_name=region)

    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError as e:
        code = e.response['Error']['Code']
        msg = e.response['Error']['Message']
        raise RuntimeError(
            f"Could not access bucket '{bucket}' (region={region}): {msg} (code {code})"
        ) from e

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    try:
        s3.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())
        print(f"✅ Uploaded to s3://{bucket}/{key}")
    except ClientError as e:
        raise RuntimeError(
            f"Failed to upload CSV to s3://{bucket}/{key}: "
            f"{e.response['Error']['Message']}"
        ) from e


# ============================================================================
# CELL: Define a function to run the Pipeline
# ============================================================================
import pandas as pd
from datetime import date, datetime

from typing import List

import boto3
from botocore import UNSIGNED
from botocore.config import Config

def run_recommendation_pipeline(tickers: List,
                               bucket_name: str,
                               period: str,
                               interval: str,
                               mapping_file: str,
                               region: str = None) -> pd.DataFrame:
    """
    Fetch price, compute indicators, load strikes,
    and return a DataFrame of trade signals.
    
    Now accepts region parameter from s3.yaml config.
    """
    clients = create_s3_clients(region=region)
    public_s3 = clients["public"]
    private_s3 = clients["private"]
    s3_resource = clients["resource"]
    buckets = {
        "daily":  get_bucket(s3_resource, bucket_name),
    }

    ticker_price_data = [
        (ticker, fetch_price(ticker, period, interval))
        for ticker in tickers
    ]

    processed = {
        ticker: (
            df
              .pipe(compute_macd)
              .pipe(compute_rsi)
              .pipe(compute_atr)
        )
        for ticker, df in ticker_price_data
    }
    strikes_df = load_strikes(mapping_file)
    signals_df = generate_detailed_signals(processed, strikes_df)

    today_str = date.today().strftime('%Y%m%d')

    s3_key = f"{RECS_PREFIX}/{today_str}.csv"
    upload_df_to_s3(
        signals_df,
        bucket_name,
        s3_key,
        region=region  # Now passing region to upload
    )
    return signals_df


# ============================================================================
# CELL: Run recommendation pipeline
# ============================================================================
TICKERS = {
    'CL=F',
    'ES=F',
    'GC=F',
    'NQ=F',
    'RTY=F',
    'YM=F',
    'NG=F',
    'AUDUSD=X',
    'EURJPY=X',
    'EURUSD=X',
    'GBPJPY=X',
    'GBPUSD=X',
    'USDCAD=X',
    'USDCHF=X',
    'USDJPY=X'
}

successful_run = show_interesting_trades(
    run_recommendation_pipeline(
        tickers=TICKERS,
        period="90d",
        interval="1d",
        bucket_name=BUCKET,
        mapping_file=MAPPING_FILE,
        region=REGION  # Now passing region from s3.yaml
    )
)

run_start = dt.datetime.now()

# Generate a run_id (timestamp) for provenance (no Git required)
run_id = run_start.strftime("%Y%m%dT%H%M%S")

# After run: append run log with counters
append_runlog_s3(
    BUCKET, RUNLOG_KEY,
    start_time=run_start,
    status=successful_run,
    files_processed=0,
    files_skipped=0,
    files_error=0,
    run_id=run_id,
    notes='Recommendation run'
)
