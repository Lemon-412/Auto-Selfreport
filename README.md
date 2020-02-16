# auto selfreport
一个简单的SHU自动报告ncov的脚本。

### 使用
```bash
$ pip install -r requirements.txt
```

```bash
$ python main.py
```

该脚本为个人使用。如他人擅自改写或使用此脚本进行任何不受欢迎的行为，与本人无关。

### 原理
- 学校新sso做了一定的安全校验，但似乎并不会否认不带headers的访问
- 表单上传后端似乎只校验检验F_STATE的合法性，不检测它的正确性

### TODO
- [X] 添加检验上报是否成功的模块
- [ ] 添加查询排名的模块
