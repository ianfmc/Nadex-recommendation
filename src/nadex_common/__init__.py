"""
nadex_common package - Common utilities for LIVEWELL Nadex workflow
"""

# Import key functions from modules to make them available at package level
from .strategy_rsi import (
    rsi_wilder,
    macd,
    sma,
    generate_rsi_signals,
    apply_guardrails,
    calculate_signal_confidence
)

from .utils_s3 import (
    create_s3_clients,
    get_bucket,
    append_runlog_s3,
    save_dataframe_to_s3,
    save_text_to_s3,
    upload_df_to_s3_with_validation,
    assert_allowed_bucket
)

__all__ = [
    # strategy_rsi exports
    "rsi_wilder",
    "macd",
    "sma",
    "generate_rsi_signals",
    "apply_guardrails",
    "calculate_signal_confidence",
    # utils_s3 exports
    "create_s3_clients",
    "get_bucket",
    "append_runlog_s3",
    "save_dataframe_to_s3",
    "save_text_to_s3",
    "upload_df_to_s3_with_validation",
    "assert_allowed_bucket"
]
