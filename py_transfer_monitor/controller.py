"""
Controller层
基于模型层编写业务逻辑
"""
import logging
import time

from model import get_token_creation_block_height, get_stats_block_height, get_block_txs_by_height_with_filter


def block_scanner(token_hash: str, receiver_addr: str):
    """
    对所有区块进行遍历
    监控某个token向某个账户的流入情况
    :param token_hash:  目标token的合约地址
    :param receiver_addr:  目标账户
    :return:
    """
    # 先获取token合约的部署tx TODO 根据持久化配置进行变更
    first_block_height = get_token_creation_block_height(token_hash)

    # 循环获取目标数据
    items = []
    block_height_ptr = first_block_height
    while True:
        # 获取当前链上区块高度
        last_block_height = get_stats_block_height()
        last_block_height = int(last_block_height)
        # 判断是否有未扫描区块
        while block_height_ptr < last_block_height:
            logging.info("扫描区块：" + str(block_height_ptr))
            try:
                block_items = get_block_txs_by_height_with_filter(
                    block_height_ptr,
                    token_hash=token_hash,
                    receiver_addr=receiver_addr
                )
                items.extend(block_items)
            except Exception as e:
                # TODO 标记扫描失败的区块
                error_msg = "区块 " + str(block_height_ptr) + " 扫描失败"
                logging.error(error_msg)
                error_msg = f"Error occurred: {str(e)}"
                logging.error(error_msg)
            block_height_ptr += 1
        # 显示当前已发现的txs
        logging.info(items)
        # 每轮扫描间隔10秒
        time.sleep(10)
    # TODO 结果数据持久化
    logging.info(items)


if __name__ == "__main__":
    receiver_addr = "0xfCefe53c7012a075b8a711df391100d9c431c468"
    token_hash = "0x0F11a75185746f64B24b7444a68B5C5A72e342F7"
    block_height = 35647

    # data = get_blocks()

    block_scanner(token_hash, receiver_addr)

    # logging.debug("data=" + str(data))
