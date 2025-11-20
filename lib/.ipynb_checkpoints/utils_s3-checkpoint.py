# utils_s3.py
from __future__ import annotations
import io, csv, datetime as dt
from typing import Iterable, Optional
import pandas as pd
from botocore.exceptions import ClientError  # from boto3

RUNLOG_FIELDS = ["date","start_time","end_time","status",
                 "files_processed","files_skipped","files_error",
                 "run_id","notes"]

def append_runlog_s3(s3_client, bucket: str, key: str, *, start_time: Optional[dt.datetime]=None,
                     status: str="success", files_processed: int=0, files_skipped: int=0,
                     files_error: int=0, run_id: str="", notes: str=""):
    now = dt.datetime.now()
    start = start_time or now
    row = {"date": now.date().isoformat(),
           "start_time": start if isinstance(start, str) else start.isoformat(timespec="seconds"),
           "end_time": now.isoformat(timespec="seconds"),
           "status": status,
           "files_processed": int(files_processed),
           "files_skipped": int(files_skipped),
           "files_error": int(files_error),
           "run_id": run_id,
           "notes": notes}
    buf = io.StringIO(); need_header = False
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        buf.write(obj["Body"].read().decode("utf-8"))
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("NoSuchKey","404","NoSuchBucket"):
            need_header = True
        else:
            raise
    if buf.tell() == 0: need_header = True
    writer = csv.DictWriter(buf, fieldnames=RUNLOG_FIELDS)
    if need_header: writer.writeheader()
    if buf.getvalue() and not buf.getvalue().endswith("\n"): buf.write("\n")
    writer.writerow(row)
    s3_client.put_object(Bucket=bucket, Key=key, Body=buf.getvalue().encode("utf-8"), ContentType="text/csv")

def save_dataframe_to_s3(s3_client, df: pd.DataFrame, bucket: str, key: str, *, index: bool=False, na_rep: str=""):
    csv_bytes = df.to_csv(index=index, na_rep=na_rep).encode("utf-8")
    s3_client.put_object(Bucket=bucket, Key=key, Body=csv_bytes, ContentType="text/csv")

def save_text_to_s3(s3_client, text: str, bucket: str, key: str, content_type: str="text/plain; charset=utf-8"):
    s3_client.put_object(Bucket=bucket, Key=key, Body=text.encode("utf-8"), ContentType=content_type)

def assert_allowed_bucket(bucket: str, allowed_buckets: Iterable[str]):
    if bucket not in set(allowed_buckets or []):
        raise ValueError(f"Bucket '{bucket}' not in allowed set: {set(allowed_buckets or [])}")
