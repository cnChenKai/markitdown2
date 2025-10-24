# MarkItDown Android App

这是一个基于微软MarkItDown项目的Android应用程序，使用Kivy和KivyMD框架开发。

## 功能特性

- 支持多种文件格式转换为Markdown：
  - PDF文档
  - Word文档 (.docx)
  - Excel表格 (.xlsx, .xls)
  - PowerPoint演示文稿 (.pptx)
  - 图片文件 (支持OCR)
  - 音频文件 (支持语音转文字)
  - HTML网页
  - 文本文件
  - ZIP压缩包
  - YouTube视频转录
  - EPub电子书
  - 更多格式...

- Material Design界面设计
- 便于操作的用户界面
- 支持文件选择器
- 结果复制功能
- 后台处理避免界面冻结

## 构建说明

### 使用GitHub Actions自动构建

1. 推送代码到GitHub仓库
2. GitHub Actions会自动构建APK
3. 在Actions页面下载构建好的APK文件

### 本地构建 (需要Linux环境)

```bash
# 安装依赖
pip install kivy kivymd buildozer

# 安装MarkItDown
cd packages/markitdown
pip install -e .[all]

# 构建APK
cd ..
buildozer android debug
```

## 项目结构

```
markitdown2/
├── main.py                 # 主应用程序
├── buildozer.spec         # Buildozer配置
├── .github/
│   └── workflows/
│       └── build-android.yml  # GitHub Actions工作流
└── packages/
    └── markitdown/        # MarkItDown核心库
```

## 依赖项

- Python 3.10+
- Kivy 2.3.1
- KivyMD 1.2.0
- MarkItDown (包含所有可选依赖)
- 其他Python库 (pillow, requests, beautifulsoup4等)

## Android权限

应用需要以下权限：
- INTERNET: 用于网络访问
- READ_EXTERNAL_STORAGE: 读取文件
- WRITE_EXTERNAL_STORAGE: 保存结果

## 架构

- 目标架构: arm64-v8a (64位Android设备)
- 最低API级别: 21 (Android 5.0)
- 目标API级别: 31 (Android 12)

## 使用方法

1. 启动应用
2. 点击"选择文件"按钮
3. 从文件浏览器中选择要转换的文件
4. 点击"转换为Markdown"按钮
5. 等待转换完成
6. 查看结果或点击"复制"按钮复制到剪贴板

## 注意事项

- 首次运行可能需要一些时间来加载
- 大文件转换可能需要较长时间
- 某些格式可能需要网络连接 (如YouTube转录)
- 确保设备有足够的存储空间

## 故障排除

如果构建失败：
1. 检查Python版本 (需要3.10+)
2. 确保所有依赖都正确安装
3. 检查buildozer.spec配置
4. 查看GitHub Actions日志获取详细错误信息

## 许可证

遵循MarkItDown项目的MIT许可证。