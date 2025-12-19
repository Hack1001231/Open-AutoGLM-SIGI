# Open-AutoGLM 混合方案 - 部署指南

## 📋 目录

1. [前期准备](#前期准备)
2. [步骤 1: 安装 Termux](#步骤-1-安装-termux)
3. [步骤 2: 安装 AutoGLM Helper](#步骤-2-安装-autoglm-helper)
4. [步骤 3: 开启无障碍权限](#步骤-3-开启无障碍权限)
5. [步骤 4: 运行部署脚本](#步骤-4-运行部署脚本)
6. [步骤 5: 配置 GRS AI](#步骤-5-配置-grs-ai)
7. [步骤 6: 测试连接](#步骤-6-测试连接)
8. [故障排除](#故障排除)

---

## 前期准备

### 检查手机要求

**最低要求**:
- ✅ Android 7.0+ (推荐 Android 11+)
- ✅ 2GB+ RAM (推荐 4GB+)
- ✅ 500MB 可用存储空间
- ✅ 网络连接 (WiFi 或移动数据)

**检查方法**:
1. 设置 → 关于手机 → Android 版本
2. 设置 → 存储 → 可用空间

### 准备材料

- [ ] GRS AI API Key (从 https://grsai.com 获取)
- [ ] 手机充电器 (部署需要 30-45 分钟)
- [ ] 稳定的网络连接

---

## 步骤 1: 安装 Termux

### 方式 A: 从 F-Droid 安装 (推荐)

1. **下载 F-Droid**
   - 访问: https://f-droid.org/
   - 点击 "Download F-Droid"
   - 下载并安装 F-Droid.apk

2. **安装 Termux**
   - 打开 F-Droid
   - 搜索 "Termux"
   - 点击 "Install"
   - 等待安装完成

### 方式 B: 从 GitHub 安装

1. **下载 Termux APK**
   - 访问: https://github.com/termux/termux-app/releases
   - 下载最新版本的 `termux-app_vX.X.X+github-debug_arm64-v8a.apk`
   - (根据您的手机架构选择对应版本)

2. **安装 APK**
   - 打开下载的 APK 文件
   - 允许安装未知来源应用
   - 点击 "安装"

### 验证安装

1. 打开 Termux
2. 应该看到命令行界面
3. 输入 `pwd` 并回车，应该显示当前目录

---

## 步骤 2: 安装 AutoGLM Helper

### 获取 APK

**方式 A: 从项目获取**
- 文件位置: `android-app/app/build/outputs/apk/debug/app-debug.apk`
- 或项目根目录: `AutoGLM-Helper.apk`

**方式 B: 自己构建**
- 参考: `android-app/BUILD_INSTRUCTIONS.md`

### 安装步骤

1. **传输 APK 到手机**
   - 通过 USB 传输
   - 或通过云盘下载
   - 或通过 ADB: `adb install AutoGLM-Helper.apk`

2. **安装 APK**
   - 找到 APK 文件
   - 点击打开
   - 允许安装未知来源应用
   - 点击 "安装"
   - 等待安装完成

3. **打开 APP**
   - 在应用列表中找到 "AutoGLM Helper"
   - 点击打开
   - 应该看到主界面

---

## 步骤 3: 开启无障碍权限

### 为什么需要无障碍权限？

无障碍权限允许 AutoGLM Helper 执行以下操作:
- 模拟点击和滑动
- 截取屏幕内容
- 输入文字

**所有操作仅在本地执行，不会上传任何数据。**

### 开启步骤

#### 方式 A: 通过 APP 打开设置

1. 打开 AutoGLM Helper
2. 点击 "打开设置" 按钮
3. 跳转到无障碍设置页面

#### 方式 B: 手动打开

1. **打开设置**
   - 设置 → 无障碍 (或辅助功能)

2. **找到 AutoGLM Helper**
   - 在已安装的服务列表中找到 "AutoGLM Helper"

3. **开启服务**
   - 点击 "AutoGLM Helper"
   - 打开开关
   - 在弹出的对话框中点击 "允许"

### 不同品牌的设置路径

| 品牌 | 设置路径 |
|------|---------|
| **原生 Android** | 设置 → 无障碍 |
| **小米 (MIUI)** | 设置 → 更多设置 → 无障碍 |
| **OPPO/一加** | 设置 → 其他设置 → 无障碍 |
| **华为** | 设置 → 辅助功能 → 无障碍 |
| **三星** | 设置 → 辅助功能 → 已安装的服务 |
| **vivo** | 设置 → 更多设置 → 辅助功能 |

### 验证权限

1. 回到 AutoGLM Helper
2. 状态应显示: "AutoGLM 服务运行中"
3. 服务器状态应显示: "运行中 (端口 8080)"

---

## 步骤 4: 运行部署脚本

### 在 Termux 中执行

1. **打开 Termux**

2. **下载部署脚本**
   ```bash
   curl -O https://raw.githubusercontent.com/your-repo/deploy.sh
   ```
   
   或者手动创建脚本 (如果无法下载):
   ```bash
   # 将部署脚本内容复制粘贴到 Termux
   nano deploy.sh
   # 粘贴内容后，按 Ctrl+X, Y, Enter 保存
   ```

3. **赋予执行权限**
   ```bash
   chmod +x deploy.sh
   ```

4. **运行脚本**
   ```bash
   ./deploy.sh
   ```

### 部署过程

脚本会自动执行以下步骤:

1. ✅ 检查网络连接
2. ✅ 更新软件包列表
3. ✅ 安装 Python 和 Git
4. ✅ 安装 Python 依赖包
5. ✅ 下载 Open-AutoGLM 项目
6. ✅ 安装 Open-AutoGLM
7. ✅ 下载混合方案脚本
8. ✅ 配置 GRS AI (需要输入 API Key)
9. ✅ 创建启动脚本
10. ✅ 测试连接

**预计时间**: 15-30 分钟 (取决于网络速度)

### 可能遇到的问题

**问题 1: 网络连接失败**
```
[ERROR] 网络连接失败，请检查网络设置
```

**解决**:
- 检查 WiFi 或移动数据是否开启
- 尝试切换网络
- 重新运行脚本

**问题 2: 软件包下载失败**
```
E: Failed to fetch ...
```

**解决**:
```bash
pkg update
pkg upgrade
```
然后重新运行部署脚本

**问题 3: Python 安装失败**

**解决**:
```bash
pkg install python -y
```
手动安装后重新运行脚本

---

## 步骤 5: 配置 GRS AI

### 在部署过程中配置

部署脚本会提示输入 API Key:

```
请输入您的 GRS AI API Key:
API Key: sk-xxxxxxxxxxxxx
```

输入您的 API Key 并回车。

### 手动配置 (如果跳过了)

1. **编辑配置文件**
   ```bash
   nano ~/.autoglm/config.sh
   ```

2. **修改 API Key**
   ```bash
   export PHONE_AGENT_API_KEY="sk-your-actual-api-key"
   ```

3. **保存并退出**
   - 按 Ctrl+X
   - 按 Y
   - 按 Enter

4. **重新加载配置**
   ```bash
   source ~/.autoglm/config.sh
   ```

### 验证配置

```bash
echo $PHONE_AGENT_API_KEY
```

应该显示您的 API Key。

---

## 步骤 6: 测试连接

### 测试 AutoGLM Helper

1. **在 Termux 中运行**
   ```bash
   curl http://localhost:8080/status
   ```

2. **应该看到**
   ```json
   {
     "status": "ok",
     "service": "AutoGLM Helper",
     "version": "1.0.0",
     "accessibility_enabled": true
   }
   ```

### 测试自动降级逻辑

1. **运行测试脚本**
   ```bash
   cd ~/.autoglm
   python phone_controller.py
   ```

2. **应该看到**
   ```
   检测可用的控制模式...
   ✅ 使用无障碍服务模式 (http://localhost:8080)
   当前模式: accessibility
   测试截图...
   截图成功: (1080, 2400)
   ```

### 首次启动 AutoGLM

1. **运行启动命令**
   ```bash
   autoglm
   ```

2. **应该看到**
   ```
   ============================================================
                Open-AutoGLM 命令行模式 (GRS AI)
   ============================================================
   使用说明:
   1. 确保手机已连接并开启 USB 调试
   2. 直接输入任务描述，如: 打开淘宝搜索无线耳机
   3. 输入 'exit' 退出程序

   请输入任务: _
   ```

3. **输入测试任务**
   ```
   请输入任务: 打开设置
   ```

4. **观察手机**
   - 手机应该自动打开设置应用
   - 如果成功，说明部署完成！

---

## 故障排除

### 问题 1: AutoGLM Helper 无法连接

**症状**:
```
[ERROR] 无法连接到 AutoGLM Helper
```

**检查清单**:
- [ ] AutoGLM Helper 是否已安装？
- [ ] AutoGLM Helper 是否正在运行？
- [ ] 无障碍权限是否已开启？
- [ ] 手机是否允许后台运行？

**解决步骤**:
1. 打开 AutoGLM Helper
2. 检查状态显示
3. 如果显示 "服务已停止"，重新开启无障碍权限
4. 在 Termux 中重新测试连接

### 问题 2: 自动降级到 LADB 模式

**症状**:
```
⚠️ 降级到 LADB 模式 (设备: localhost:5555)
```

**原因**:
- 无障碍服务未开启
- AutoGLM Helper 未运行

**解决**:
1. 检查并开启无障碍权限
2. 重启 AutoGLM Helper
3. 重新运行 `autoglm`

### 问题 3: 无可用控制方式

**症状**:
```
❌ 无可用控制方式
```

**解决**:
1. **检查 AutoGLM Helper**
   - 是否安装？
   - 是否运行？
   - 无障碍权限是否开启？

2. **或者安装 LADB 作为备用**
   - 从 Google Play 安装 LADB
   - 配对 LADB
   - 重新运行 `autoglm`

### 问题 4: GRS AI API 调用失败

**症状**:
```
Error: API key not found
```

**解决**:
1. 检查 API Key 是否正确
   ```bash
   echo $PHONE_AGENT_API_KEY
   ```

2. 重新配置
   ```bash
   nano ~/.autoglm/config.sh
   ```

3. 重新加载
   ```bash
   source ~/.autoglm/config.sh
   ```

### 问题 5: 截图失败

**症状**:
```
截图失败
```

**Android 11+ 解决**:
- 检查无障碍权限中的 "允许截图" 选项

**Android 7-10 解决**:
- 无障碍服务不支持截图
- 自动降级到 LADB 模式
- 安装并配对 LADB

---

## 下一步

部署完成后，请阅读:
- [使用手册](USER_MANUAL.md) - 学习如何使用
- [常见问题](FAQ.md) - 解决常见疑问
- [故障排除](TROUBLESHOOTING.md) - 深入的故障排除指南

---

## 需要帮助？

如果遇到问题:
1. 查看 [故障排除](TROUBLESHOOTING.md)
2. 查看 [常见问题](FAQ.md)
3. 提交 Issue 到 GitHub
