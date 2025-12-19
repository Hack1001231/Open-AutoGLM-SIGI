# 🔧 Git 工作流程指南

> **给 AI 助手的说明**: 这是一个完整的 Git 操作指南，包含仓库位置、编码设置、常用命令和工作流程。

---

## 📍 仓库信息

### 仓库位置
```
本地路径: C:\Users\YANQIAO\Documents\Augment\Open-AutoGLM-Hybrid-main
工作目录: Open-AutoGLM-Hybrid-main
分支: master
```

### 项目信息
```
项目名称: SIGI (思想钢印)
原名称: AutoGLM Helper
版本: v1.1-SIGI
类型: Android 自动化应用
技术栈: Kotlin + Python (Chaquopy) + AI
```

---

## ⚙️ 重要：PowerShell 编码设置

**在执行任何 Git 命令前，必须先设置 UTF-8 编码！**

### 方法 1: 每次命令前添加（推荐）
```powershell
$OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; git <command>
```

### 方法 2: 会话开始时设置一次
```powershell
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### 为什么需要这个？
- Windows PowerShell 默认使用 GBK 编码
- Git 提交信息使用 UTF-8 编码
- 不设置会导致中文显示为乱码

---

## 📋 常用 Git 命令（带编码设置）

### 1. 查看状态
```powershell
# 查看当前状态
$OutputEncoding = [System.Text.Encoding]::UTF8; git status

# 查看简短状态
$OutputEncoding = [System.Text.Encoding]::UTF8; git status -s
```

### 2. 查看提交历史
```powershell
# 查看最近一次提交
$OutputEncoding = [System.Text.Encoding]::UTF8; git log -1

# 查看最近 5 次提交（单行）
$OutputEncoding = [System.Text.Encoding]::UTF8; git log --oneline -5

# 查看完整提交信息
$OutputEncoding = [System.Text.Encoding]::UTF8; git log -1 --format=fuller

# 查看提交统计
$OutputEncoding = [System.Text.Encoding]::UTF8; git show --stat
```

### 3. 查看差异
```powershell
# 查看未暂存的修改
$OutputEncoding = [System.Text.Encoding]::UTF8; git diff

# 查看已暂存的修改
$OutputEncoding = [System.Text.Encoding]::UTF8; git diff --cached

# 查看修改统计
$OutputEncoding = [System.Text.Encoding]::UTF8; git diff --stat

# 查看特定文件的修改
$OutputEncoding = [System.Text.Encoding]::UTF8; git diff <文件路径>
```

### 4. 添加文件
```powershell
# 添加所有修改
git add .

# 添加特定文件
git add <文件路径>

# 添加多个文件
git add <文件1> <文件2> <文件3>

# 交互式添加
git add -i
```

### 5. 提交更改
```powershell
# 简单提交
git commit -m "提交信息"

# 多行提交信息
git commit -m "标题" -m "详细描述第一行" -m "详细描述第二行"

# 修改上一次提交
git commit --amend

# 跳过暂存区直接提交所有修改
git commit -am "提交信息"
```

### 6. 创建标签
```powershell
# 创建轻量标签
git tag v1.1-SIGI

# 创建附注标签
git tag -a v1.1-SIGI -m "版本 1.1 - 思想钢印主题"

# 查看所有标签
git tag

# 查看标签详情
$OutputEncoding = [System.Text.Encoding]::UTF8; git show v1.1-SIGI

# 推送标签到远程
git push origin v1.1-SIGI

# 推送所有标签
git push origin --tags
```

### 7. 分支操作
```powershell
# 查看所有分支
git branch -a

# 创建新分支
git branch <分支名>

# 切换分支
git checkout <分支名>

# 创建并切换到新分支
git checkout -b <分支名>

# 删除分支
git branch -d <分支名>

# 强制删除分支
git branch -D <分支名>
```

### 8. 远程仓库操作
```powershell
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin <仓库URL>

# 推送到远程
git push origin master

# 拉取远程更新
git pull origin master

# 克隆仓库
git clone <仓库URL>
```

---

## 🔄 标准工作流程

### 场景 1: 日常开发提交

```powershell
# 1. 进入仓库目录
cd C:\Users\YANQIAO\Documents\Augment\Open-AutoGLM-Hybrid-main

# 2. 查看当前状态
$OutputEncoding = [System.Text.Encoding]::UTF8; git status

# 3. 查看修改内容
$OutputEncoding = [System.Text.Encoding]::UTF8; git diff

# 4. 添加修改的文件
git add .

# 5. 提交更改
git commit -m "feat: 添加新功能描述"

# 6. 查看提交结果
$OutputEncoding = [System.Text.Encoding]::UTF8; git log -1
```

### 场景 2: 版本发布

```powershell
# 1. 确保所有更改已提交
$OutputEncoding = [System.Text.Encoding]::UTF8; git status

# 2. 创建版本标签
git tag -a v1.2 -m "版本 1.2 发布"

# 3. 查看标签
$OutputEncoding = [System.Text.Encoding]::UTF8; git tag

# 4. 推送代码和标签（如果有远程仓库）
git push origin master
git push origin --tags
```

### 场景 3: 撤销操作

```powershell
# 撤销工作区的修改（未 add）
git checkout -- <文件名>

# 撤销暂存区的修改（已 add，未 commit）
git reset HEAD <文件名>

# 撤销最近一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最近一次提交（丢弃修改）
git reset --hard HEAD~1

# 查看所有操作记录
git reflog
```

---

## 📝 提交信息规范

### 提交信息格式
```
<类型>: <简短描述>

<详细描述>（可选）

<相关信息>（可选）
```

### 类型说明
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构代码
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关
- `ui`: UI/样式更新
- `release`: 版本发布

### 示例
```powershell
# 简单提交
git commit -m "feat: 添加语音输入功能"

# 详细提交
git commit -m "fix: 修复截图功能在 Android 11 上的崩溃问题

- 更新截图 API 调用方式
- 添加权限检查
- 增加错误处理

Fixes #123"

# 重大更新
git commit -m "🎨 重大更新：科幻主题改版 - 思想钢印 (SIGI)

## 主要变更
- 应用改名：AutoGLM Helper → SIGI
- LOGO 更换：机械大脑图标
- UI 主题升级：科幻赛博朋克风格

版本: v1.1-SIGI"
```

---

## 🎯 当前仓库状态（最后更新：2025-12-19）

### 最新提交
```
提交哈希: 6a4693f535d4b694c3f858bd81d1f0a58f3e2808
提交标题: 🎨 重大更新：科幻主题改版 - 思想钢印 (SIGI)
提交时间: 2025-12-19 21:10:00
提交者: User <user@example.com>
```

### 主要修改
- 应用改名：AutoGLM Helper → SIGI
- LOGO 更换为机械大脑图标
- UI 主题升级为科幻风格
- 更新全套 Android 图标资源
- 新增文档：ICON_UPDATE_LOG.md

### 修改文件统计
```
14 个文件修改
106 行新增代码
新增图标源文件: brain_icon.jpg (235 KB)
```

---

## 🔍 快速检查清单

### 提交前检查
- [ ] 代码已测试
- [ ] 没有调试代码
- [ ] 提交信息清晰
- [ ] 文件编码正确（UTF-8）
- [ ] 没有敏感信息（API Key 等）

### 推送前检查（如果有远程仓库）
- [ ] 本地测试通过
- [ ] 提交历史整洁
- [ ] 版本号已更新
- [ ] 文档已更新
- [ ] CHANGELOG 已更新

---

## 📚 项目特定的 Git 操作

### 更新应用图标
```powershell
# 1. 替换源图标文件
# 将新图标放到: android-app/app/src/main/res/

# 2. 修改生成脚本
# 编辑: android-app/generate_icons.py
# 更新 source_image 路径

# 3. 生成新图标
cd android-app
python generate_icons.py

# 4. 提交更改
cd ..
git add android-app/app/src/main/res/mipmap-*/*.png
git add android-app/app/src/main/res/<新图标文件>
git add android-app/generate_icons.py
git commit -m "ui: 更新应用图标"
```

### 更新应用名称
```powershell
# 1. 修改 strings.xml
# 文件: android-app/app/src/main/res/values/strings.xml
# 修改 app_name

# 2. 提交更改
git add android-app/app/src/main/res/values/strings.xml
git commit -m "chore: 更新应用名称"
```

### 发布新版本
```powershell
# 1. 更新版本号
# 编辑: android-app/app/build.gradle.kts
# 更新 versionCode 和 versionName

# 2. 更新 README
# 编辑: README.md
# 更新版本信息

# 3. 提交版本更新
git add android-app/app/build.gradle.kts README.md
git commit -m "release: 发布版本 v1.2"

# 4. 创建标签
git tag -a v1.2 -m "版本 1.2 发布"

# 5. 推送（如果有远程仓库）
git push origin master
git push origin v1.2
```

---

## 🛠️ 故障排除

### 问题 1: 中文显示乱码
**解决方案**: 使用本文档开头的编码设置命令

### 问题 2: 提交被拒绝
```powershell
# 查看冲突文件
git status

# 解决冲突后
git add <冲突文件>
git commit -m "fix: 解决合并冲突"
```

### 问题 3: 误提交敏感信息
```powershell
# 修改最后一次提交
git commit --amend

# 如果已推送，需要强制推送（危险！）
git push -f origin master
```

### 问题 4: 需要回退到之前版本
```powershell
# 查看提交历史
$OutputEncoding = [System.Text.Encoding]::UTF8; git log --oneline

# 临时查看某个版本
git checkout <commit-hash>

# 永久回退（危险！）
git reset --hard <commit-hash>
```

---

## 📖 相关文档

- `README.md` - 项目说明
- `ARCHITECTURE.md` - 架构设计
- `QUICK_START.md` - 快速开始
- `ICON_UPDATE_LOG.md` - 图标更新历史
- `UPDATE_SUMMARY_v1.1-SIGI.md` - v1.1 更新摘要
- `GIT_GUIDE.md` - Git 基础指南（如果存在）

---

## 🤖 给 AI 助手的快速参考

### 执行 Git 命令的标准模板
```powershell
# 工作目录
cd C:\Users\YANQIAO\Documents\Augment\Open-AutoGLM-Hybrid-main

# 设置编码（必须！）
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 执行 Git 命令
git <command>
```

### 常用操作快捷方式
```powershell
# 查看状态
$OutputEncoding = [System.Text.Encoding]::UTF8; git status

# 查看最新提交
$OutputEncoding = [System.Text.Encoding]::UTF8; git log -1

# 添加并提交
git add . && git commit -m "提交信息"

# 查看修改统计
$OutputEncoding = [System.Text.Encoding]::UTF8; git diff --stat
```

### 项目关键路径
```
应用代码: android-app/app/src/main/
Kotlin 代码: android-app/app/src/main/java/com/autoglm/helper/
Python 代码: android-app/app/src/main/python/
资源文件: android-app/app/src/main/res/
图标文件: android-app/app/src/main/res/mipmap-*/
配置文件: android-app/app/build.gradle.kts
```

---

**最后更新**: 2025-12-19  
**维护者**: YANQIAO  
**项目**: SIGI (思想钢印)

---

💡 **提示**: 将此文件保存在项目根目录，任何 AI 助手都能快速了解如何操作这个仓库！
