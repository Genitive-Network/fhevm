# 
## 合约部署地址
Token Address：0x390DCAAc12e5Bf1bd9c44EeA3707728A2F851125
Owner Address：0x21b7356966eAef9C6CCBeB81a226630A9c916797
emit topic: 0x0251d16288ef8058040c27892a01dac42c24f59d4d47117b7a71be12477ce190
## 用户如何进行跨链操作
调用 'cross_chain_transfer(bytes calldata encryptedAmount)'
## 计算逻辑
 - 根据token address计算first block height
 - 从first block height开始 按block height顺序获取所有block的数据
 - 对每个block中的所有transaction进行遍历 按照token和address进行筛选
 - 数据持久化：链上数据落地，便于数据重刷；聚合数据checkpoint。
## 难点
 - rpc api默认单词查询最多返回50个transaction，当单个block中的transaction超过50时，如何获取完整数据。
 - 当节点分叉时，如何保证数据正确性（延迟确认，等待X个节点确认/checkpoint+回溯）。