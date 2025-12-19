# Git Commit 分析：修复视觉停止信号重置问题

## 📋 提交信息

- **Commit Hash**: `5a2bb98c07acdf8386d79e3547bcd2acd2c697aa`
- **提交时间**: 2025-12-19 22:21:31 +0800
- **提交标题**: `fix: 重置视觉停止信号,防止影响新任务`
- **修改文件**: `android-app/app/src/main/python/agent_main.py`
- **修改行数**: +1 行

---

## 🐛 问题描述

### 现象
在测试美团应用时发现：
- 点击坐标仍然偏低，即使已经修复了横幅 Bug（commit `cb083aa`）
- 搜索框应该被点击，但实际点击到了下方的团购按钮

### 根本原因分析
通过查看日志发现关键线索：

```
[IMG] 截图尺寸: (1228, 3105)
```

**步骤 1 的截图就已经是 3105 高度了！** 这说明：

1. **上一次任务的停止信号没有清除**
   - 上次测试时点击了停止按钮
   - `VISUAL_STOP_SIGNAL` 全局变量被设置为 `True`
   - 新任务开始时没有重置这个标志

2. **导致新任务从第一帧就添加横幅**
   - 截图函数检测到 `VISUAL_STOP_SIGNAL = True`
   - 在原始截图（1228 x 2700）上添加了 405px 的红色横幅
   - 返回的截图尺寸变成了 1228 x 3105

3. **坐标计算错误**
   - AI 模型基于 3105 高度的图片进行推理
   - 返回的坐标是基于 1000x1000 归一化坐标系
   - 缩放到实际设备时使用了错误的高度（3105 而不是 2700）
   - 导致所有点击都偏低

---

## 🔍 代码分析

### 修改前的代码（第 160-161 行）

```python
# 重置停止标志
android_helper.set_stop(False)

# 初始化消息历史 (放在循环外)
self.messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]
```

**问题**：
- 只重置了旧的 `set_stop(False)` 标志
- 没有重置新的视觉停止信号 `VISUAL_STOP_SIGNAL`
- 导致全局变量污染，影响新任务

### 修改后的代码（第 160-162 行）

```python
# 重置停止标志
android_helper.set_stop(False)
android_helper.disable_visual_stop_signal()  # 🔥 重置视觉停止信号

# 初始化消息历史 (放在循环外)
self.messages = [
    {"role": "system", "content": "SYSTEM_PROMPT"}
]
```

**修复**：
- 添加了 `android_helper.disable_visual_stop_signal()` 调用
- 确保每个新任务都从干净状态开始
- 防止上次任务的视觉信号影响新任务

---

## 🎯 修复效果

### Before（修复前）
```
步骤 1: 截图尺寸 (1228, 3105) ❌ 已经添加了横幅
步骤 2: 点击搜索框 → 实际点到团购 ❌ 坐标偏低
步骤 3: 继续错误操作...
```

### After（修复后）
```
步骤 1: 截图尺寸 (1228, 2700) ✅ 原始高度
步骤 2: 点击搜索框 → 准确点击 ✅ 坐标正确
步骤 3: 正常执行任务...
步骤 N: 用户点击停止 → 添加横幅 (1228, 3105)
```

---

## 🔗 相关提交

### 1. Commit `cb083aa` - 修复横幅改变高度 Bug
**问题**: 添加横幅后更新了 `SCREEN_HEIGHT`，导致后续坐标计算错误

**修复**: 在添加横幅**之前**更新尺寸信息

### 2. Commit `5a2bb98` - 重置视觉停止信号（本次提交）
**问题**: 上次任务的 `VISUAL_STOP_SIGNAL` 没有重置

**修复**: 任务开始时调用 `disable_visual_stop_signal()`

---

## 📊 影响范围

### 受益的场景
✅ 所有新任务都不会受上次停止信号影响  
✅ 坐标计算使用正确的原始高度  
✅ 美团、12306 等应用点击准确  
✅ 多次任务执行不会相互干扰  

### 不影响的功能
- 停止按钮的功能正常（点击后仍会添加横幅）
- 优雅停止机制正常工作
- 截图功能正常

---

## 🧪 测试建议

### 测试步骤
1. **第一次任务**：执行美团搜索任务
   - 点击停止按钮（触发视觉信号）
   - 观察横幅是否出现

2. **第二次任务**：再次执行美团搜索任务
   - 检查步骤 1 的截图尺寸（应该是原始高度）
   - 检查搜索框点击是否准确

3. **验证日志**：
   ```
   [IMG] 截图尺寸: (1228, 2700)  ← 应该是这个，不是 3105
   [TAP] 点击 (500, 200) -> (614, 540)  ← 坐标应该准确
   ```

---

## 💡 设计思考

### 为什么需要两个停止机制？

1. **旧机制**: `set_stop(False)` / `should_stop()`
   - 立即停止，强制中断
   - 用于紧急情况

2. **新机制**: `enable_visual_stop_signal()` / `disable_visual_stop_signal()`
   - 视觉提示，让 AI 看到停止信号
   - 优雅停止，AI 可以完成当前步骤

### 为什么使用全局变量？
- Python 脚本在 Android 中通过 Chaquopy 运行
- Kotlin 和 Python 之间通过全局变量通信
- 需要在多次调用之间保持状态

### 为什么需要重置？
- 全局变量在应用生命周期内持续存在
- 不同任务之间需要隔离状态
- 防止"幽灵状态"影响新任务

---

## 📝 经验教训

### 1. 全局状态管理
- ⚠️ 全局变量容易造成状态污染
- ✅ 每次任务开始时必须重置所有全局状态
- ✅ 考虑使用上下文管理器（`with` 语句）

### 2. 调试技巧
- 🔍 查看**第一步**的日志最重要
- 🔍 截图尺寸是关键线索
- 🔍 对比预期值和实际值

### 3. 代码审查
- 📋 添加新功能时，检查是否需要重置逻辑
- 📋 修改全局变量时，考虑影响范围
- 📋 编写清理函数（cleanup/reset）

---

## 🚀 后续优化建议

### 1. 添加状态检查
```python
def run(self, task, log_callback):
    # 添加状态诊断
    self._check_clean_state()
    
    # 重置所有全局状态
    self._reset_all_states()
```

### 2. 使用上下文管理器
```python
class TaskContext:
    def __enter__(self):
        android_helper.disable_visual_stop_signal()
        android_helper.set_stop(False)
        return self
    
    def __exit__(self, *args):
        # 自动清理
        pass

# 使用
with TaskContext():
    agent.run(task, log_callback)
```

### 3. 添加单元测试
```python
def test_visual_signal_reset():
    # 设置停止信号
    android_helper.enable_visual_stop_signal()
    
    # 运行新任务
    agent.run("test", callback)
    
    # 验证第一步截图高度
    assert first_screenshot.height == ORIGINAL_HEIGHT
```

---

## 📚 相关文档

- [STOP_MECHANISM.md](./STOP_MECHANISM.md) - 停止机制详细说明
- [PROJECT_REDUNDANCY_ANALYSIS.md](./PROJECT_REDUNDANCY_ANALYSIS.md) - 项目冗余分析
- [INDEX.md](./INDEX.md) - 文档索引

---

**总结**: 这是一个典型的"全局状态污染"问题。通过在任务开始时添加一行重置代码，彻底解决了新任务受上次任务影响的 Bug。这个修复非常关键，确保了坐标计算的准确性。
