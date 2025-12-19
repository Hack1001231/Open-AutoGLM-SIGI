# Open-AutoGLM 混合方案 - 用户手册

## 📱 日常使用

### 快速开始

1. **打开 Termux**
2. **输入启动命令**
   ```bash
   autoglm
   ```
3. **输入任务**
   ```
   请输入任务: 打开淘宝搜索蓝牙耳机
   ```
4. **观察手机自动执行**

就这么简单！

---

## 🎯 任务示例

### 购物类

```
打开淘宝搜索无线耳机
打开京东查看购物车
打开拼多多搜索手机壳
打开美团外卖搜索附近的火锅店
```

### 社交类

```
打开微信，找到张三的聊天，发送"今晚聚餐"
打开抖音刷5个视频
打开微博查看热搜
打开小红书搜索护肤品推荐
```

### 工具类

```
打开支付宝查看余额
打开支付宝扫一扫
打开高德地图导航到北京天安门
打开日历查看今天的日程
```

### 娱乐类

```
打开网易云音乐播放周杰伦的歌
打开B站搜索科技视频
打开爱奇艺播放电视剧
```

---

## ⚙️ 配置管理

### 查看当前配置

```bash
cat ~/.autoglm/config.sh
```

### 修改 API Key

```bash
nano ~/.autoglm/config.sh
```

修改这一行:
```bash
export PHONE_AGENT_API_KEY="your-new-api-key"
```

保存后重新加载:
```bash
source ~/.autoglm/config.sh
```

### 修改模型

默认使用 `gpt-4-vision-preview`，可以修改为其他模型:

```bash
export PHONE_AGENT_MODEL="gpt-4-turbo"
```

### 修改 API 地址

如果使用其他兼容 OpenAI 的 API:

```bash
export PHONE_AGENT_BASE_URL="https://your-api-url.com/v1"
```

---

## 🔧 高级功能

### 查看当前控制模式

```bash
cd ~/.autoglm
python -c "from phone_controller import PhoneController; c = PhoneController(); print(c.get_mode())"
```

输出:
- `accessibility` - 无障碍服务模式
- `ladb` - LADB 模式

### 手动测试截图

```bash
cd ~/.autoglm
python << EOF
from phone_controller import PhoneController
c = PhoneController()
img = c.screenshot()
if img:
    img.save('/sdcard/test_screenshot.png')
    print("截图已保存到 /sdcard/test_screenshot.png")
else:
    print("截图失败")
EOF
```

### 手动测试点击

```bash
cd ~/.autoglm
python << EOF
from phone_controller import PhoneController
c = PhoneController()
success = c.tap(500, 1000)
print(f"点击结果: {success}")
EOF
```

### 查看日志

```bash
# 查看最近的日志
tail -f ~/.autoglm/autoglm.log
```

---

## 📊 性能优化

### 减少 API 调用成本

**方法 1: 降低图片质量**

修改 `phone_controller.py`:
```python
# 在 _screenshot_accessibility 方法中
bitmap.compress(Bitmap.CompressFormat.JPEG, 60, outputStream)  # 从 80 降到 60
```

**方法 2: 使用更便宜的模型**

```bash
export PHONE_AGENT_MODEL="gpt-4-mini"
```

### 提高响应速度

**方法 1: 使用更快的网络**
- 优先使用 WiFi
- 避免使用移动数据

**方法 2: 减少超时时间**

修改 `phone_controller.py`:
```python
timeout=3  # 从 5 秒降到 3 秒
```

---

## 🛡️ 安全建议

### 保护 API Key

1. **不要分享配置文件**
   ```bash
   # 配置文件包含 API Key
   ~/.autoglm/config.sh
   ```

2. **定期更换 API Key**
   - 每月更换一次
   - 或者设置使用限额

### 权限管理

1. **仅在需要时开启无障碍权限**
   - 不使用时可以关闭
   - 下次使用时再开启

2. **监控 API 使用量**
   - 定期检查 GRS AI 控制台
   - 设置使用警报

---

## 🔄 更新和维护

### 更新 Open-AutoGLM

```bash
cd ~/Open-AutoGLM
git pull
pip install -e .
```

### 更新混合方案脚本

```bash
cd ~/.autoglm
# 下载最新的 phone_controller.py
wget -O phone_controller.py https://your-link/phone_controller.py
```

### 重新部署

如果遇到问题，可以重新部署:

```bash
# 备份配置
cp ~/.autoglm/config.sh ~/config_backup.sh

# 删除旧文件
rm -rf ~/Open-AutoGLM ~/.autoglm

# 重新运行部署脚本
./deploy.sh

# 恢复配置
cp ~/config_backup.sh ~/.autoglm/config.sh
```

---

## 📱 多设备使用

### 在多台手机上使用

1. **在每台手机上分别部署**
   - 安装 Termux
   - 安装 AutoGLM Helper
   - 运行部署脚本

2. **使用相同的 API Key**
   - 所有设备共享配额

### 切换设备

如果使用 LADB 模式，切换设备时:

```bash
# 查看已连接设备
adb devices

# 指定设备
export ANDROID_SERIAL=device_id

# 运行 autoglm
autoglm
```

---

## 💡 使用技巧

### 技巧 1: 组合任务

```
打开淘宝搜索蓝牙耳机，点进第一个商品，查看详情，加入购物车
```

### 技巧 2: 使用具体描述

❌ 不好的描述:
```
打开APP
```

✅ 好的描述:
```
打开淘宝
```

### 技巧 3: 分步执行复杂任务

复杂任务可以分成多步:

```
步骤 1: 打开微信
步骤 2: 找到张三的聊天
步骤 3: 发送"今晚聚餐"
```

### 技巧 4: 使用快捷命令

创建别名:

```bash
echo 'alias taobao="echo \"打开淘宝\" | autoglm"' >> ~/.bashrc
source ~/.bashrc
```

使用:
```bash
taobao
```

---

## 📈 监控和统计

### 查看使用统计

```bash
# 查看 API 调用次数
grep "API call" ~/.autoglm/autoglm.log | wc -l

# 查看成功率
grep "success" ~/.autoglm/autoglm.log | wc -l
```

### 成本估算

**GRS AI 定价** (示例):
- gpt-4-vision-preview: $0.01 / 1K tokens
- 平均每次任务: 2K tokens
- 每次成本: $0.02

**月度估算**:
- 每天使用 10 次
- 每月 300 次
- 月度成本: $6

---

## 🎓 最佳实践

### 1. 保持简洁

任务描述应该简洁明了:
- ✅ "打开淘宝搜索耳机"
- ❌ "请帮我打开淘宝这个APP然后搜索一下蓝牙耳机"

### 2. 一次一个任务

避免在一个命令中执行太多操作:
- ✅ 分成 2-3 步
- ❌ 一次执行 10 个操作

### 3. 验证结果

执行完任务后，检查手机确认:
- 是否达到预期效果
- 是否需要调整描述

### 4. 定期维护

- 每月更新一次 Open-AutoGLM
- 每周检查一次 API 使用量
- 定期清理日志文件

---

## ❓ 常见问题

### Q: 如何退出 autoglm？

**A**: 输入 `exit` 或按 `Ctrl+C`

### Q: 可以在后台运行吗？

**A**: 可以，使用 `nohup`:
```bash
nohup autoglm &
```

### Q: 如何查看历史任务？

**A**: 查看日志:
```bash
cat ~/.autoglm/autoglm.log
```

### Q: 支持语音输入吗？

**A**: 目前不支持，但可以使用手机的语音输入法在 Termux 中输入

### Q: 可以定时执行任务吗？

**A**: 可以使用 cron:
```bash
# 每天早上 8 点打开微信
crontab -e
# 添加: 0 8 * * * echo "打开微信" | autoglm
```

---

## 📚 进阶阅读

- [架构设计](../ARCHITECTURE.md) - 了解技术细节
- [故障排除](TROUBLESHOOTING.md) - 解决常见问题
- [常见问题](FAQ.md) - 更多问答

---

## 💬 反馈和建议

如果您有任何建议或发现问题:
1. 提交 Issue 到 GitHub
2. 发送邮件到 support@example.com
3. 加入用户社区讨论
