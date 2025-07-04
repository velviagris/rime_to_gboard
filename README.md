# rime_to_gboard

![GitHub](https://img.shields.io/github/license/cgcel/rime_to_gboard)
![Github all releases](https://img.shields.io/github/downloads/cgcel/rime_to_gboard/total.svg)
![GitLab latest release](https://badgen.net/github/release/cgcel/rime_to_gboard)
[![CodeQL](https://github.com/cgcel/rime_to_gboard/actions/workflows/codeql.yml/badge.svg?branch=master)](https://github.com/cgcel/rime_to_gboard/actions/workflows/codeql.yml)

## 简介

借助 Rime 输入法的 `userdb.txt` 用户词库, 让 Gboard 的输入体验媲美旧时的 Google Pinyin.

本脚本可将 Rime `xxx.userdb.txt` (测试于 [Weasel](https://github.com/rime/weasel)) 转换为 Gboard `PersonalDictionary.zip` 格式, 便于将词库导入 Gboard.

## 适用输入方案

- 全拼
- 小鹤双拼, [参考链接](https://github.com/bcaso/pinyin_to_double_pinyin)

> Rime 小鹤双拼模式下的 `userdb.txt` 中编码仍为全拼, 脚本原理是将全拼转为双拼后写入 `PersonalDictionary.zip`.

## 脚本依赖

- Python 3.8-3.10
  - OpenCC 1.1.9
  - tqdm 4.67.1

## 使用方法

### 命令行启动

1. 安装 python 以及依赖:
    ```shell
    pip install -r requirements.txt
    ```
2. 运行脚本, 按照提示将你的待转换的 `userdb.txt` 拖拽入命令行, 或输入文件路径.

> userdb.txt 路径相关疑问见 [Q&A](#qa)

3. 根据指引, 确认输入方案, 输入文件文本繁简类型.
4. 回车, 等待数秒, `.zip` 压缩文件将自动生成.

  ![](https://gitee.com/cgcel/image/raw/master/img/202312191012716.png)

5. 将 `.zip` 压缩文件导入手机存储中, 在 Gboard 设置 - 字典 - 个人字典 - 中文 (简体) - 点击右上角 *导入* - 选择 `.zip` 压缩文件.

  ![](https://gitee.com/cgcel/image/raw/master/img/202312191017762.jpg)

### 使用应用程序

1. [下载](https://github.com/cgcel/rime_to_gboard/releases) 应用程序, 保存至本地.
2. 打开 rime2gboard.exe, 按照提示将待转换的 `*.userdb.txt` 拖入窗口, 或直接输入文件路径.
3. 按照后续提示确认输入方案, 输入繁简类型后回车.
4. 与 [上述](#命令行) 第5步操作一致.

## Q&A

### userdb.txt 所在路径

以小狼毫为例, 在 Rime 用户目录, 打开 `installation.yaml`:

![](https://gitee.com/cgcel/image/raw/master/img/202312191009385.png)

```yaml
distribution_code_name: Weasel
distribution_name: "小狼毫"
distribution_version: 0.15.0.0
install_time: "Thu Sep  7 09:37:03 2023"
installation_id: "rime-weasel-cgc"
rime_version: 1.9.0
sync_dir: "D:\\NutBackup\\RimeSync"
update_time: "Mon Dec 18 09:12:35 2023"
```

记下 `sync_dir` 的路径, 然后右键右下角 Rime 菜单栏图标, 点击 `用户资料同步`, 进入 `sync_dir` 的路径, 找到对应的 `*.userdb.txt`.

![](https://gitee.com/cgcel/image/raw/master/img/202312191011023.png)

## License

**rime_to_gboard** is licensed under the MIT license. Refer to [LICENSE](https://github.com/cgcel/rime_to_gboard/blob/master/License.txt) for more information.
