# 
## 合约部署地址
Token Address：0x16456979482cC0EFFaF04b6eEb05BCA5aba09250

Owner Address：0x21b7356966eAef9C6CCBeB81a226630A9c916797

Owner Private Key: b009e7bbd3b2103dc8f7f3ba14a6704fa929eaa9a490c005c479bae902c131bb

emit topic: 0x0251d16288ef8058040c27892a01dac42c24f59d4d47117b7a71be12477ce190
## 用户如何进行跨链操作
调用 'transfer(address to, bytes calldata encryptedAmount)'

其中"to"参数必须为 0x21b7356966eAef9C6CCBeB81a226630A9c916797（Owner Address）
## Bot Usage
1. 进入py_transfer_monitor目录
2. 执行如下命令：
```
export CORSS_CHAIN_BASE_URL="http://localhost:8006"
python main.py
```