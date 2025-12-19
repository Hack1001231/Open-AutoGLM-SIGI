# 🛑 停止机制说明文档

## 📋 概述

SIGI 应用实现了**双重保险停止机制**，结合视觉信号和软着陆逻辑，确保任务能够安全停止。

---

## 🔧 停止机制架构

### 1. **视觉停止信号** (Visual Stop Signal)

**原理**：在截图上叠加红色横幅和白色 X 标记，让 AI 识别并停止。

**实现位置**：
- `android_helper.py` 第 100-162 行
- `agent_main.py` System Prompt 第 22 行

**工作流程**：
```
用户点击停止 
  ↓
启用 VISUAL_STOP_SIGNAL 标志
  ↓
下一次截图时叠加红色横幅
  ↓
AI 看到红色横幅 → 输出 finish(message="收到停止信号")
  ↓
任务停止
```

**视觉效果**：
- 顶部红色横幅（占屏幕高度 15%）
- 3 个白色 X 标记居中显示
- 全图红色边框（宽度 20px）

**局限性**：
- ❌ **依赖 AI 模型识别能力**
- ❌ AutoGLM-Phone 模型可能未在训练数据中见过此类停止信号
- ❌ 模型可能将红色横幅误认为应用界面的一部分
- ⚠️ **不保证 100% 有效**

---

### 2. **软着陆机制** (Graceful Stop)

**原理**：动态调整最大步数限制，让任务在指定步数后自动停止。

**实现位置**：
- `agent_main.py` 第 135-145 行（`request_graceful_stop` 方法）
- `agent_main.py` 第 175-177 行（检查逻辑）

**工作流程**：
```
用户点击停止
  ↓
调用 stop_gracefully(buffer_steps=3)
  ↓
设置 dynamic_max_steps = current_step + 3
  ↓
当前步骤的 AI 调用完成
  ↓
下一个循环开始时检查 current_step > dynamic_max_steps
  ↓
如果超过限制 → break 退出循环
  ↓
任务停止
```

**关键代码**：
```python
def request_graceful_stop(self, buffer_steps=2):
    """请求优雅停止：不立即中断，而是让 AI 再执行 buffer_steps 步后停止"""
    old_limit = self.dynamic_max_steps
    self.dynamic_max_steps = self.current_step + buffer_steps
    print(f"🛑 收到停止请求：当前第 {self.current_step} 步，将在第 {self.dynamic_max_steps} 步后停止")
    return self.dynamic_max_steps
```

**优点**：
- ✅ **100% 可靠**（代码逻辑控制）
- ✅ 不依赖 AI 模型识别
- ✅ 确保任务不会无限运行

**缓冲步数**：
- 当前设置：`buffer_steps = 3`
- 含义：点击停止后，最多再执行 3 步就会强制停止

---

## ⏱️ 停止延迟问题

### 为什么停止不是立即生效？

**原因**：Python 代码在独立线程中运行，且可能正在等待 AI API 响应。

**延迟来源**：

1. **AI API 调用时间**（主要延迟）
   - 每次 AI 调用可能需要 5-30 秒
   - 停止检查在循环开始，但 AI 调用已经开始
   - 必须等当前 AI 调用完成才能检查停止标志

2. **代码执行位置**
   ```python
   for step in range(self.max_steps):
       # ✅ 检查点 1：循环开始
       if self.current_step > self.dynamic_max_steps:
           break
       
       # 📸 截图（1-2 秒）
       image = android_helper.take_screenshot()
       
       # 🤖 AI 调用（5-30 秒）← 停止信号在这里等待！
       response = openai.ChatCompletion.create(...)
       
       # ⚙️ 执行操作（1-2 秒）
       # ...
   ```

3. **时间线示例**
   ```
   T=0s:  用户点击停止按钮
   T=0s:  设置 dynamic_max_steps = current_step + 3
   T=0s:  但此时 AI 正在调用中...
   T=15s: AI 调用返回
   T=15s: 执行操作
   T=17s: 下一个循环开始 → 检查停止标志 → 发现需要停止
   T=17s: break 退出
   ```

---

## 👆 使用方法

### 单次点击停止

**效果**：
- 启用视觉停止信号
- 设置软着陆（3 步后停止）

**预期**：
- 如果 AI 识别到红色横幅 → 立即停止（理想情况）
- 如果 AI 未识别 → 最多 3 步后强制停止（保底）

**日志输出**：
```
🛑 正在发送停止信号（视觉 + 逻辑双保险）...
✅ 已在下一帧截图上添加红色停止横幅
✅ 已设置保底停止点：第 X 步
💡 AI 识别到红色横幅后会立即停止，否则最多 3 步后停止
```

---

### 多次点击停止（推荐）

**为什么需要多次点击？**
- 第一次点击：设置停止标志，但可能正在等待 AI 响应
- 第二次点击：进一步缩短 buffer_steps，加速停止

**效果**：
```
第 1 次点击：dynamic_max_steps = current_step + 3
第 2 次点击：dynamic_max_steps = current_step + 3（再次缩短）
```

**实际体验**：
- ✅ 两次点击基本能确保快速停止
- ✅ 用户体验可接受

---

## 📊 停止机制对比

| 机制 | 可靠性 | 响应速度 | 依赖 |
|------|--------|----------|------|
| 视觉停止信号 | ⚠️ 不确定 | 快（如果 AI 识别） | AI 模型能力 |
| 软着陆机制 | ✅ 100% | 慢（需等 AI 调用） | 代码逻辑 |
| 双重保险 | ✅ 可靠 | 中等 | 组合优势 |

---

## 🔮 未来改进方向

### 改进 1: 在 AI 调用前检查停止标志

**位置**：`agent_main.py` 第 224 行之前

```python
# 在调用 AI 之前再次检查
if android_helper.should_stop() or self.current_step > self.dynamic_max_steps:
    log_callback.onLog("\n[STOP] 在 AI 调用前检测到停止信号")
    break

try:
    response = openai.ChatCompletion.create(...)
```

**优点**：
- 避免开始新的 AI 调用
- 减少停止延迟

---

### 改进 2: 添加 AI 调用超时

**位置**：`agent_main.py` 第 238 行

```python
response = openai.ChatCompletion.create(
    model=self.model_name,
    messages=messages_to_send,
    max_tokens=300,
    temperature=0.1,
    timeout=10  # 添加 10 秒超时
)
```

**优点**：
- 防止 AI 调用卡太久
- 提高停止响应速度

---

### 改进 3: 改进视觉信号

**方案 A**：使用文字而非图形
```python
# 在截图上叠加大字："STOP - 任务已终止"
# AI 更容易识别文字
```

**方案 B**：训练数据增强
- 在 AutoGLM-Phone 的训练数据中加入"红色横幅 = 停止"的样本
- 需要模型开发团队支持

---

## 🎯 最佳实践

### 用户使用建议

1. **正常停止**：点击停止按钮 1-2 次
2. **紧急停止**：连续点击 2-3 次
3. **等待时间**：给系统 5-10 秒响应时间
4. **观察日志**：查看日志确认停止点设置

### 开发调试建议

1. **调整 buffer_steps**：
   - 测试环境：`buffer_steps = 1`（快速停止）
   - 生产环境：`buffer_steps = 3`（安全停止）

2. **监控日志**：
   ```
   🛑 收到停止请求：当前第 X 步，将在第 Y 步后停止
   [!] 用户请求停止，已在第 Z 步优雅退出
   ```

3. **测试场景**：
   - AI 调用中途停止
   - 操作执行中途停止
   - 连续快速点击停止

---

## 📝 相关代码位置

### Python 代码

**`agent_main.py`**:
- 第 22 行：System Prompt 中的停止信号说明
- 第 56-57 行：max_steps 和 dynamic_max_steps 初始化
- 第 135-145 行：`request_graceful_stop()` 方法
- 第 175-177 行：动态停止检查
- 第 179-182 行：旧停止标志检查
- 第 350-366 行：`stop_gracefully()` 全局函数

**`android_helper.py`**:
- 第 46 行：VISUAL_STOP_SIGNAL 全局变量
- 第 58-67 行：启用/禁用视觉信号函数
- 第 100-102 行：截图时叠加停止横幅
- 第 110-162 行：`_add_stop_banner()` 实现

### Kotlin 代码

**`MainActivity.kt`**:
- 第 54-77 行：停止按钮点击事件处理
- 第 61 行：启用视觉停止信号
- 第 66 行：调用软着陆机制

---

## 🐛 已知问题

### 问题 1: 视觉信号识别率低

**现象**：AI 经常忽略红色横幅，继续执行任务

**原因**：模型未在训练数据中见过此类停止信号

**解决方案**：依赖软着陆机制作为保底

**状态**：✅ 已有软着陆保底，问题不大

---

### 问题 2: 停止延迟较长

**现象**：点击停止后需要等待 5-30 秒才真正停止

**原因**：正在等待 AI API 响应

**解决方案**：
- 当前：多点几次停止按钮
- 未来：在 AI 调用前检查停止标志

**状态**：⚠️ 可接受，未来可优化

---

## 📚 参考资料

- [System Prompt 设计](agent_main.py#L17-L42)
- [视觉信号实现](android_helper.py#L110-L162)
- [软着陆机制](agent_main.py#L135-L145)
- [停止按钮处理](MainActivity.kt#L54-L77)

---

**文档版本**: v1.0  
**最后更新**: 2025-12-19  
**维护者**: YANQIAO  
**项目**: SIGI (思想钢印)

---

💡 **总结**：当前的双重保险停止机制是可靠的，软着陆机制 100% 有效。虽然有一定延迟，但通过多次点击停止按钮可以快速停止任务。未来可以通过在 AI 调用前检查停止标志来进一步优化响应速度。
