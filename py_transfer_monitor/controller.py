"""
Controller层
基于模型层编写业务逻辑
"""
import logging
import time

from model import get_token_creation_block_height, get_stats_block_height, get_block_txs_by_height_with_filter, \
    get_addr_logs_with_filter


def block_scanner(token_hash: str, emit_topic: str):
    """
    对所有区块进行遍历
    监控某个token向某个账户的流入情况
    :param token_hash:  目标token的合约地址
    :return:
    """
    # 先获取token合约的部署tx TODO 根据持久化配置进行变更
    # first_block_height = get_token_creation_block_height(token_hash)
    # block_height_ptr = first_block_height

    # 循环获取目标数据
    item_map = {}

    while True:
        items = cross_chain_logs_view(get_addr_logs_with_filter(token_hash, emit_topic=emit_topic))
        for item in items:
            tx_hash = item['tx_hash']
            if tx_hash not in item_map:
                # TODO 发现新的跨链操作
                logging.info("发现新的跨链操作：" + str(item))
                item_map[tx_hash] = item
        # 显示当前已发现的txs TODO 结果数据持久化
        logging.info("当前已发现的跨链操作：" + str(item_map))
        # 每轮扫描间隔10秒
        time.sleep(10)
    logging.info(items)


def cross_chain_logs_view(items: list) -> list:
    result = []
    for item in items:
        new_item = {
            'tx_hash': item['tx_hash'],
            'from_addr': item['topics'][1],
            'amount': item['data'],
            'block_number': item['block_number'],
            'block_hash': item['block_hash']
        }
        result.append(new_item)
    return result


if __name__ == "__main__":
    token_hash = "0x390DCAAc12e5Bf1bd9c44EeA3707728A2F851125"

    emit_topic = "0x0251d16288ef8058040c27892a01dac42c24f59d4d47117b7a71be12477ce190"

    block_scanner(token_hash, emit_topic)

    # logging.debug("data=" + str(data))
