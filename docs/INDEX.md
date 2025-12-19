# 📚 SIGI 项目文档索引

欢迎查阅 SIGI (思想钢印) 项目文档！

---

## 🚀 快速开始

- **[AI_README.md](AI_README.md)** - AI 助手快速指引（必读！）
- **[../README.md](../README.md)** - 项目主说明文档
- **[../QUICK_START.md](../QUICK_START.md)** - 快速开始指南

---

## 📖 核心文档

### Git 相关
- **[GIT_WORKFLOW.md](GIT_WORKFLOW.md)** - Git 工作流程完整指南
  - 仓库位置和项目信息
  - PowerShell UTF-8 编码设置
  - 常用 Git 命令参考
  - 标准工作流程
  - 提交信息规范

### 版本更新
- **[UPDATE_SUMMARY_v1.1-SIGI.md](UPDATE_SUMMARY_v1.1-SIGI.md)** - v1.1 版本更新摘要
  - SIGI 品牌升级详情
  - LOGO 更换说明
  - UI 主题改版
  - 修改文件清单

---

## 🏗️ 架构与设计

- **[../ARCHITECTURE.md](../ARCHITECTURE.md)** - 项目架构设计文档
- **[../DELIVERY_SUMMARY.md](../DELIVERY_SUMMARY.md)** - 交付摘要

---

## 📱 Android 应用文档

### 构建与部署
- **[../android-app/docs/BUILD_INSTRUCTIONS.md](../android-app/docs/BUILD_INSTRUCTIONS.md)** - 构建说明
- **[../GITHUB_BUILD_GUIDE.md](../GITHUB_BUILD_GUIDE.md)** - GitHub Actions 构建指南

### 功能说明
- **[../android-app/docs/STOP_MECHANISM.md](../android-app/docs/STOP_MECHANISM.md)** - 停止机制详解
  - 双重保险停止机制
  - 视觉停止信号原理
  - 软着陆机制说明
  - 使用方法和最佳实践

### 资源更新
- **[../android-app/docs/ICON_UPDATE_LOG.md](../android-app/docs/ICON_UPDATE_LOG.md)** - 图标更新历史
  - 图标更换记录
  - 重新生成方法

---

## 🛠️ 开发指南

- **[../GIT_GUIDE.md](../GIT_GUIDE.md)** - Git 基础指南（如果存在）

---

## 📂 文档目录结构

```
Open-AutoGLM-Hybrid-main/
├── README.md                    # 项目主说明
├── ARCHITECTURE.md              # 架构设计
├── QUICK_START.md               # 快速开始
├── DELIVERY_SUMMARY.md          # 交付摘要
├── GITHUB_BUILD_GUIDE.md        # GitHub 构建指南
│
├── docs/                        # 📚 主文档目录
│   ├── INDEX.md                 # 本文件 - 文档索引
│   ├── AI_README.md             # AI 助手快速指引
│   ├── GIT_WORKFLOW.md          # Git 工作流程指南
│   └── UPDATE_SUMMARY_v1.1-SIGI.md  # v1.1 更新摘要
│
└── android-app/
    ├── docs/                    # 📱 Android 应用文档
    │   ├── BUILD_INSTRUCTIONS.md    # 构建说明
    │   ├── ICON_UPDATE_LOG.md       # 图标更新历史
    │   └── STOP_MECHANISM.md        # 停止机制说明
    │
    ├── app/                     # 应用源代码
    └── build-apk.bat            # 构建脚本
```

---

## 🎯 按需求查找文档

### 我想了解项目
→ 阅读 [../README.md](../README.md)

### 我是 AI 助手，需要操作仓库
→ 阅读 [AI_README.md](AI_README.md) 和 [GIT_WORKFLOW.md](GIT_WORKFLOW.md)

### 我想构建 APK
→ 阅读 [../android-app/docs/BUILD_INSTRUCTIONS.md](../android-app/docs/BUILD_INSTRUCTIONS.md)

### 我想了解停止按钮为什么有延迟
→ 阅读 [../android-app/docs/STOP_MECHANISM.md](../android-app/docs/STOP_MECHANISM.md)

### 我想更换应用图标
→ 阅读 [../android-app/docs/ICON_UPDATE_LOG.md](../android-app/docs/ICON_UPDATE_LOG.md)

### 我想提交代码到 Git
→ 阅读 [GIT_WORKFLOW.md](GIT_WORKFLOW.md)

### 我想了解最新版本的改动
→ 阅读 [UPDATE_SUMMARY_v1.1-SIGI.md](UPDATE_SUMMARY_v1.1-SIGI.md)

---

## 📝 文档维护

### 添加新文档
1. 根据类型放入对应目录：
   - 项目级文档 → `docs/`
   - Android 应用文档 → `android-app/docs/`
2. 更新本索引文件

### 文档命名规范
- 使用大写字母和下划线：`DOCUMENT_NAME.md`
- 版本文档包含版本号：`UPDATE_SUMMARY_v1.1.md`
- 特定功能文档使用描述性名称：`STOP_MECHANISM.md`

---

**最后更新**: 2025-12-19  
**维护者**: YANQIAO  
**项目**: SIGI (思想钢印)
