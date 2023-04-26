# 企业工商信息抓取器

企业工商信息抓取器是一个用 Python 编写的命令行工具，它可以从企查查网站抓取企业的工商信息，并将结果保存为 Excel 文件。该工具可以帮助您快速获取企业工商信息，并进行必要的分析和处理。

## 安装

1. 克隆此仓库或将其下载为 ZIP 文件。
    ```
    git clone https://github.com/yourusername/enterprise-info-crawler.git
    ```

2. 进入项目目录，并创建一个 Python 虚拟环境（可选）。
    ```
    cd enterprise-info-crawler
    python -m venv venv
    ```

3. 激活虚拟环境（可选，在 Windows 上）  
    ```
    venv\Scripts\activate
    ```

4. 激活虚拟环境（可选，在 Linux 或 macOS 上）。
    ```
    source venv/bin/activate
    ```

5. 安装项目依赖项。
    ```
    pip install -r requirements.txt
    ```

## 使用

1. 在项目目录中创建一个包含统一社会信用代码的 Excel 文件（默认命名为 "统一社会信用代码.xlsx"）。  

2. 运行项目。
    ```
    python main.py
    ```

4. 如果一切顺利，您将在项目目录中看到一个名为 "企业工商信息.xlsx" 的新 Excel 文件，其中包含抓取的企业工商信息。

## 注意事项

- 您需要登录到企查查网站并获取您的 Cookie，才能在项目中进行抓取操作。请注意保护您的 Cookie 值，不要将其泄露给他人。