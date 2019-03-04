### 文档说明

#### 运行环境
* python 3.6

####运行脚本（项目文件夹下运行）
```
pip3.6 install -r requirements.txt
python3.6 WikiTag.py
```
#### 运行说明

* 目前 端口设置 为5000， 可以自行带代码中更改
* 目前取了长度2-3的短语词条， 如果需要增加长度，可以修改代码第7行的max_length变量， 需要内存16G,初始化时间30分钟左右
* 请求示例: http://127.0.0.1:5000/?sentence=thisissentence&page=1&per_page=1.  其中sentence 是 待匹配句子，page 是当前页数， per_page 是每页显示数量。 sentence 和 page 是必填参数。 