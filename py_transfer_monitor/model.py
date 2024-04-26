"""
模型层
保存读取数据的逻辑
依赖API交互层
"""
import logging

from api import api_get_blocks, api_get_block_txs_by_height, api_get_tx, api_get_addr, api_get_stats, \
    api_get_token_transfer


def get_block_txs_by_height_with_filter(height: int, token_hash: str, receiver_addr: str) -> list | None:
    """
        获取所有block的transaction
        filter : 用于过滤transaction
    """

    def default_filter(items: list):
        return token_transfer_filter(
            items,
            token_hash=token_hash,
            receiver_addr=receiver_addr
        )

    return get_block_txs_by_height(height, tx_filter=default_filter)


def token_transfer_filter(items: list, token_hash: str, receiver_addr: str) -> list:
    """
    仅过滤出特定的token transfer对象
    :param items:
    :param token_hash: 过滤条件 token合约地址
    :param receiver_addr: 过滤条件
    :return: 包含token_transfer的数组
    """
    result = []
    for item in items:
        try:
            # 过滤token_hash tx必须发送至token合约地址
            if item["to"]["hash"] != token_hash:
                continue
            tx_hash = item["hash"]
            tx = api_get_tx(tx_hash)
            token_transfers = tx["token_transfers"]

            # 过滤receiver_addr token必须发送至目标账户地址
            for token_transfer in token_transfers:
                if token_transfer["to"]["hash"] == receiver_addr:
                    # 满足过滤条件要求
                    result.append(token_transfers)
                    logging.debug("发现满足要求的item：" + str(item))


        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
            logging.error(error_msg)
    return result


def get_block_txs_by_height(height: int, tx_filter=None, max_query_time=5) -> list | None:
    """
        获取所有block的transaction
        filter : 用于过滤transaction
    """
    result = []
    try:
        # 第一次 获取next_page_params
        [items, next_page_params] = api_get_block_txs_by_height(height)
        if items is not None:
            if tx_filter is not None:
                items = tx_filter(items)
            result += items
        logging.debug("items = " + str(items))
        logging.debug("next_page_params = " + str(next_page_params))
        logging.debug("result = " + str(result))
        # 迭代查询 直到next_page_params=None
        counter = 1
        while next_page_params is not None:
            if counter > max_query_time:
                break
            logging.debug("查询次数" + str(counter))
            counter += 1
            [items, next_page_params] = api_get_block_txs_by_height(height, next_page_params)
            if items is not None:
                if tx_filter is not None:
                    items = tx_filter(items)
                result += items
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        logging.error(error_msg)
        return None
    return result


def get_blocks(max_query_time=5) -> list | None:
    """
        获取所有block的info
    """
    result = []
    try:
        # 第一次 获取next_page_params
        [items, next_page_params] = api_get_blocks()
        if items is not None:
            result += items
        logging.debug("items = " + str(items))
        logging.debug("next_page_params = " + str(next_page_params))
        logging.debug("result = " + str(result))
        # 迭代查询 直到next_page_params=None
        counter = 1
        while next_page_params is not None:
            if counter > max_query_time:
                break
            logging.debug("查询次数" + str(counter))
            counter += 1
            [items, next_page_params] = api_get_blocks(next_page_params)
            if items is not None:
                result += items
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        logging.error(error_msg)
        return None
    return result


def get_token_creation_block_height(token_hash: str) -> int | None:
    """
    获取token创建时的block 的height
    :param token_hash:
    :return:
    """
    try:
        token_addr_info = api_get_addr(token_hash)
        creation_tx_hash = token_addr_info["creation_tx_hash"]
        creation_tx_info = api_get_tx(creation_tx_hash)
        block_height = creation_tx_info["block"]
        return block_height
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        logging.error(error_msg)
        return None


def get_stats_block_height() -> int | None:
    """
    获取当前集群的区块高度
    :rtype: object
    :return:
    """
    try:
        stats = api_get_stats()
        block_height = stats["total_blocks"]
        return block_height
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        logging.error(error_msg)
        return None


def get_token_transfer(addr_hash: str, token_hash: str, max_query_time: int = 3) -> list | None:
    """

    :param addr_hash:
    :param token_hash:
    :param max_retries:
    :param wait_time:
    :return:
    """
    result = []
    try:
        # 第一次 获取next_page_params
        [items, next_page_params] = api_get_token_transfer(addr_hash, token_hash)
        if items is not None:
            result += items
        logging.debug("items = " + str(items))
        logging.debug("next_page_params = " + str(next_page_params))
        logging.debug("result = " + str(result))
        # 迭代查询 直到next_page_params=None
        counter = 1
        while next_page_params is not None:
            if counter > max_query_time:
                break
            logging.debug("查询次数" + str(counter))
            counter += 1
            [items, next_page_params] = api_get_block_txs_by_height(height, next_page_params)
            if items is not None:
                result += items
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        logging.error(error_msg)
        return None
    return result


if __name__ == "__main__":
    receiver_addr = "0xfCefe53c7012a075b8a711df391100d9c431c468"
    token_hash = "0x0F11a75185746f64B24b7444a68B5C5A72e342F7"
    block_height = 35647

    # data = get_blocks()

    # data = get_block_txs_by_height_with_filter(height=block_height, token_hash=token_hash, receiver_addr=receiver_addr)

    # data = get_token_creation_block_height(token_hash)

    # data = get_stats_block_height()
    data = get_token_transfer(addr_hash=receiver_addr, token_hash=token_hash)

    logging.debug("data=" + str(data))
