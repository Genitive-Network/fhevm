# -*- coding: utf-8 -*-
from config import TOKEN_ADDRESS, EMIT_TOPIC
from controller import block_scanner

token_hash = TOKEN_ADDRESS

emit_topic = EMIT_TOPIC

block_scanner(token_hash, emit_topic)