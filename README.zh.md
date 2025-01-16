# Notion-Auto-Format

> 查看英文文档：**[README in English](README.md)**

Notion-Auto-Format 是一款能够自动格式化指定 Notion 文档的工具。它目前支持在文档标题和正文中将中文与英文、中文与数字之间添加空格。

## 特性

- 自动在中文与英文之间添加空格。
- 自动在中文与数字之间添加空格。

## 需求

- **Python**: 版本 3.x
- **依赖项**:
  - `notion-client`

## 限制

由于 Notion API 的频率限制以及编辑接口的性能限制，默认情况下最多可以并发修改 3 个块。如果遇到编辑冲突错误，工具将自动重试。

## 安装

1. 克隆这个仓库：
   ```bash
   git clone https://github.com/ideadsnow/notion-auto-format.git
   ```

2. 进入项目目录：
   ```bash
   cd notion-auto-format
   ```

3. 安装所需的依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. **配置 Notion Token**：
   请确保在代码中手动将 `NOTION_TOKEN = "your_integration_token"` 的值替换为您自己的 Notion 集成的 TOKEN。您可以在这个地址创建自己的集成并获得 TOKEN：[创建 Notion 集成](https://www.notion.so/profile/integrations)。

## 使用

要使用 Notion-Auto-Format，可以通过运行以下命令查看使用说明：
```bash
python auto_format.py -h
```
具体的使用方式为：
```bash
usage: auto_format.py [-h] page_id
```

**从哪里找到我的文档 ID？**
> 在 Notion 中打开页面。使用 "共享 "菜单复制链接。现在将链接粘贴到文本编辑器中，以便仔细查看。URL 以页面 ID 结尾。
它应该是一个 32 个字符的长字符串。按照以下模式插入连字符 (-) 来格式化该值：8-4-4-4-12（每个数字是连字符之间的字符长度）。
例如：1429989fe8ac4effbc8f57f56486db54 变为 1429989fe8ac-4eff-bc8f-57f56486db54。
该值就是您的页面 ID。

## 许可证

该项目根据 MIT 许可证授权。详见 [LICENSE](LICENSE) 文件。