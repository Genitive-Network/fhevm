# -*- coding: utf-8 -*-
"""
API交互层
"""
import requests
import time
from log import logging

BASE_URL = "https://main.explorer.zama.ai/api/v2"


def modify_next_page_url(url: str, next_page_params=None):
    if next_page_params is not None:
        url += "?"
        for key, value in next_page_params.items():
            url += str(key) + "=" + str(value) + "&"
            # print(key, " : ", value)
    if url.endswith("&"):
        url = url[0:len(url) - 1:1]
    # print("url : ", url)
    return url


def api_get_addr(addr_hash: str, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/addresses/" + addr_hash
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            return data
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


def api_get_addr_txs(addr_hash: str, next_page_params=None, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/addresses/" + addr_hash + "/transactions"
            url = modify_next_page_url(url, next_page_params)
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            items = data["items"]
            next_page_params = data["next_page_params"]
            return [items, next_page_params]
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


def api_get_addr_logs(addr_hash: str, next_page_params=None, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/addresses/" + addr_hash + "/logs"
            url = modify_next_page_url(url, next_page_params)
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            items = data["items"]
            next_page_params = data["next_page_params"]
            return [items, next_page_params]
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


def api_get_token_txs(addr_hash: str, token_hash: str, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/addresses/" + addr_hash + "/token-transfers?token=" + token_hash
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            items = data["items"]
            next_page_params = data["next_page_params"]
            # print("next_page_params : ", next_page_params)
            return items
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


def api_get_block_info_by_height(height: int, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/blocks/" + str(height)
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            return data
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


def api_get_block_txs_by_height(height: int, next_page_params=None, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/blocks/" + str(height) + "/transactions"
            url = modify_next_page_url(url, next_page_params)
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            items = data["items"]
            next_page_params = data["next_page_params"]
            # print("next_page_params : ", next_page_params)
            # items：当前分页
            # next_page_params：下一个分页的必备参数
            return [items, next_page_params]
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return [None, None]


def api_get_blocks(next_page_params=None, max_retries=3, wait_time=60):
    """获取所有block的info"""
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/blocks"
            url = modify_next_page_url(url, next_page_params)
            # print("url : ", url)

            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            items = data["items"]
            next_page_params = data["next_page_params"]
            # print("next_page_params : ", next_page_params)
            # items：当前分页
            # next_page_params：下一个分页的必备参数
            return [items, next_page_params]
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return [None, None]


def api_get_tx(tx_hash: str, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/transactions/" + tx_hash
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            return data
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


def api_get_stats(max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/stats/"
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            return data
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


def api_get_token_info(token_hash:str, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/tokens/" + token_hash
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            return data
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


def api_get_token_transfer(addr_hash:str, token_hash:str, next_page_params=None, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/addresses/" + addr_hash + "/token-transfers?filter=to&token=" + token_hash
            url = modify_next_page_url(url, next_page_params)
            # print("url : ", url)
            transactions = requests.get(url)
            # print("transactions : ", transactions)
            data = transactions.json()
            # print("data : ", data)
            items = data["items"]
            next_page_params = data["next_page_params"]
            # print("next_page_params : ", next_page_params)
            # items：当前分页
            # next_page_params：下一个分页的必备参数
            return [items, next_page_params]
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return None


if __name__ == "__main__":
    addr_hash = "0x390DCAAc12e5Bf1bd9c44EeA3707728A2F851125"
    token_hash = "0x0F11a75185746f64B24b7444a68B5C5A72e342F7"
    block_height = 106893

    # data = api_get_txs(wallet_addr)

    # data = api_get_token_txs(wallet_addr, token_addr)

    # data = api_get_block_info_by_height(block_height)

    # data = api_get_block_txs_by_height(block_height)

    # data = api_get_blocks(next_page_params={'block_number': 107065, 'items_count': 50})

    # data = api_get_addr(token_hash)

    # data = api_get_stats()

    # data = api_get_token_info(token_hash)

    # data = api_get_addr_txs(addr_hash)

    data = api_get_addr_logs(addr_hash)

    logging.info("data: " + str(data))
