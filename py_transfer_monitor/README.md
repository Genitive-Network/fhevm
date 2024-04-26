# 
## 计算逻辑
 - 根据token address计算first block height
 - 从first block height开始 按block height顺序获取所有block的数据
 - 对每个block中的所有transaction进行遍历 按照token和address进行筛选
 - 数据持久化：链上数据落地，便于数据重刷；聚合数据checkpoint。
## 难点
 - rpc api默认单词查询最多返回50个transaction，当单个block中的transaction超过50时，如何获取完整数据。
 - 当节点分叉时，如何保证数据正确性（延迟确认，等待X个节点确认/checkpoint+回溯）。