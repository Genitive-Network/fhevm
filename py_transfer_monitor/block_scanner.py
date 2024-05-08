# -*- coding: utf-8 -*-
"""
区块数据循环扫描器
"""
import copy
import logging
import time

from data_fetcher import get_addr_logs_with_filter
from config import TOKEN_ADDRESS, EMIT_TOPIC, CORSS_CHAIN_DONE_DATA_PATH, \
    CORSS_CHAIN_PENDING_DATA_PATH
from crosschain_caller import cross_chain_mint
from persistence import load, save


def block_scanner(token_hash: str, emit_topic: str):
    """
    对所有区块进行遍历
    监控某个token向某个账户的流入情况
    :param token_hash:  目标token的合约地址
    :return:
    """
    # TODO 先获取token合约的部署tx
    # first_block_height = get_token_creation_block_height(token_hash)
    # block_height_ptr = first_block_height

    # 已完成跨链的tx
    cc_done_item_map = load(CORSS_CHAIN_DONE_DATA_PATH)

    # 仍需进行跨链的tx
    cc_pending_item_map = load(CORSS_CHAIN_PENDING_DATA_PATH)

    while True:
        # 监听新的跨链行为
        items = logs_view(get_addr_logs_with_filter(token_hash, emit_topic=emit_topic))
        for item in items:
            tx_hash = item['tx_hash']
            if tx_hash not in cc_done_item_map:
                # 发现新的跨链操作
                simple_view = logs_simple_view(item)
                logging.info("New Cross Chain Found：" + str(simple_view))
                # 请求目标链进行跨链
                if cross_chain_request(item):
                    logging.info("Cross Chain Succeed：" + str(simple_view))
                    cc_done_item_map[tx_hash] = item
                else:
                    # 记录失败项 后续进行重传
                    logging.info("Cross Chain Failed：" + str(simple_view))
                    cc_pending_item_map[tx_hash] = item
        # 显示当前已发现的txs
        # logging.info("Cross Chain Done List：" + str(cc_done_item_map))
        logging.info("Cross Chain Pending List：" + str(cc_pending_item_map))
        # 每轮扫描间隔10秒
        if save(cc_done_item_map, CORSS_CHAIN_DONE_DATA_PATH) and save(cc_pending_item_map,
                                                                       CORSS_CHAIN_PENDING_DATA_PATH):
            logging.info("数据持久化成功")
        time.sleep(10)

        # 对于失败的跨链操作进行重试
        tmp_list = []
        for hash in cc_pending_item_map:
            tmp_list.append(hash)
        for hash in tmp_list:
            # 请求目标链进行跨链
            item = cc_pending_item_map[hash]
            if cross_chain_request(item):
                simple_view = logs_simple_view(item)
                logging.info("Cross Chain Succeed：" + str(simple_view))
                cc_pending_item_map.pop(item["tx_hash"])
                cc_done_item_map[tx_hash] = item


def logs_view(items: list) -> list:
    result = []
    for item in items:
        new_item = {
            'tx_hash': item['tx_hash'],
            'address': item['topics'][1],
            'amount': item['data'],
            'block_number': item['block_number'],
            'block_hash': item['block_hash']
        }
        result.append(new_item)
    return result


def logs_simple_view(item: dict) -> dict:
    return {
        'address': item['address'],
        'amount': item['amount']
    }


def cross_chain_request(item: dict) -> bool:
    address = item["address"]
    address = "0x" + address[len(address) - 40:len(address)]
    amount = int(item["amount"], 16)
    return cross_chain_mint(to=address, amount=amount)


if __name__ == "__main__":
    token_hash = TOKEN_ADDRESS

    emit_topic = EMIT_TOPIC

    block_scanner(token_hash, emit_topic)

    # logging.debug("data=" + str(data))
