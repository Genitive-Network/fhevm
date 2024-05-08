# -*- coding: utf-8 -*-
"""
命令目标链进行跨链操作
"""
import logging

import requests
import time

from config import CORSS_CHAIN_BASE_URL, CORSS_CHAIN_MINT_URL

BASE_URL = CORSS_CHAIN_BASE_URL


def cross_chain_mint(to: str, amount: int, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = CORSS_CHAIN_MINT_URL
            json_data = {"address": to, "amount": amount}
            logging.info("cross_chain_mint:" + str(json_data))
            response = requests.post(url, json={"address": to, "amount": amount})
            # print(response)
            return True
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return False


def cross_chain_transfer(to: str, amount: int, max_retries=3, wait_time=60):
    for retry in range(max_retries):
        try:
            url = BASE_URL + "/transfer"
            response = requests.post(url, json={"address": to, "amount": amount})
            # print(response)
            return True
        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
        print(f"Retrying {retry + 1}/{max_retries}: {error_msg}")
        if retry < max_retries - 1:
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    return False


if __name__ == "__main__":
    cross_chain_mint(to="0x6D8a1b1Ba7ce3844704c67b45f6B05E0bB4e536e", amount=5)
    # cross_chain_transfer(to="0x21b7356966eAef9C6CCBeB81a226630A9c916797", amount=5)
