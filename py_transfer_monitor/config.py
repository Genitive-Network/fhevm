# -*- coding: utf-8 -*-
"""
公共配置参数
"""
import os

TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS") if os.getenv("TOKEN_ADDRESS") else "0x16456979482cC0EFFaF04b6eEb05BCA5aba09250"

EMIT_TOPIC = os.getenv("EMIT_TOPIC") if os.getenv("EMIT_TOPIC") else "0x0251d16288ef8058040c27892a01dac42c24f59d4d47117b7a71be12477ce190"

CORSS_CHAIN_BASE_URL = os.getenv("CORSS_CHAIN_BASE_URL") if os.getenv("CORSS_CHAIN_BASE_URL") else "http://localhost:8081"

CORSS_CHAIN_MINT_URL = os.getenv("CORSS_CHAIN_MINT_URL") if os.getenv("CORSS_CHAIN_MINT_URL") else CORSS_CHAIN_BASE_URL + "/api/mint"

CORSS_CHAIN_DONE_DATA_PATH = "data/done_data.json"
CORSS_CHAIN_PENDING_DATA_PATH = "data/pending_data.json"
