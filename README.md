# auto selfreport
一个简单的SHU自动报告ncov的脚本。

### 使用
```bash
$ pip install -r requirements.txt
```

```bash
$ python main.py
```

由于selfreport开发的敏捷性，表单格式经常更新，需自行调整。作者不保证脚本的长期可用性。
如他人擅自改写或使用此脚本进行任何不受欢迎的行为，与作者无关。

### 原理
- 学校新sso做了一定的安全校验，但似乎并不会否认不带headers的访问
- 表单上传后端似乎只校验检验F_STATE的合法性，不检测它的正确性(现已改用base64)

### TODO
- [X] 添加检验上报是否成功的模块
- [ ] 添加查询排名的模块
