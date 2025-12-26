# v1.4 版本发布说明 - 弹窗点击修复

**发布日期**: 2024-12-26  
**版本号**: v1.4

---

## 🎯 核心问题

### 问题现象
在美团 App 中点击"加入购物车"弹窗按钮时，点击会**穿透弹窗**，点到了弹窗后面的商品图片，导致任务失败并进入死循环。

### 问题根因
1. **AccessibilityService 的 `dispatchGesture` 在弹窗上失效** - 手势模拟无法正确作用在弹窗 Window 上
2. **多节点重叠问题** - 目标坐标被多个节点的 bounds 包含，之前的代码会选择错误的（面积大的）节点

---

## ✅ 解决方案

### 核心修改：选择最小面积的 clickable 节点

**修改文件**: `AutoGLMAccessibilityService.kt`

当有多个 clickable 节点的 bounds 都包含目标坐标时，**选择 bounds 面积最小的那个**（最精确匹配）。

```kotlin
// 收集所有包含目标坐标的 clickable 节点
val candidates = mutableListOf<Pair<AccessibilityNodeInfo, Int>>() // node to area
collectClickableNodes(node, x, y, candidates)

// 选择面积最小的节点
val best = candidates.minByOrNull { it.second }!!
```

### 效果对比

**修复前**:
```
Found: android.view.ViewGroup, bounds=(0, 122 - 1228, 2700), area=3165784  ← 选了这个错误的大容器
```

**修复后**:
```
Found 6 clickable candidates, selected smallest (area=31108)
Found: android.view.ViewGroup, bounds=(812, 2091 - 1120, 2192)  ← 正确的"加入购物车"按钮
```

---

## 📁 修改文件清单

### 1. AutoGLMAccessibilityService.kt
**路径**: `android-app/app/src/main/java/com/autoglm/helper/AutoGLMAccessibilityService.kt`

**主要修改**:

1. **performTap 函数增强**
   - 添加版本标识日志 `performTap V2.0`
   - 添加详细的窗口遍历日志
   - 添加操作结果日志

2. **findClickableNodeAt 函数重写**
   - 改为收集所有候选节点，选最小面积
   - 新增 `collectClickableNodes` 递归收集函数

3. **日志增强**
   - 🎯 Target 标记目标坐标
   - 📱 显示找到的窗口数量
   - 🪟 显示每个窗口的层级和标题
   - ✅ 显示找到的节点信息
   - 🎉 成功点击时的详细信息

### 2. agent_main.py
**路径**: `android-app/app/src/main/python/agent_main.py`

**修改内容**:

1. **死循环检测增强**
   - 检测到重复动作时自动执行返回操作
   - 清空动作历史，给 AI 一个"新开始"

2. **修复函数调用错误**
   - `android_helper.back()` → `android_helper.go_back()`

### 3. android_helper.py
**路径**: `android-app/app/src/main/python/android_helper.py`

**修改内容**:
- 移除之前添加的 shell tap 备选方案（因为 Android App 没有权限执行）
- 简化 tap 函数逻辑

---

## 🔧 技术细节

### 为什么选择最小面积？

在 Android 的 View 层级中：
- 父容器（如整个页面的 ViewGroup）bounds 很大
- 子元素（如按钮）bounds 很小

当目标坐标位于按钮上时，父容器和按钮的 bounds 都包含这个坐标。
选择**面积最小**的节点（即按钮本身或其直接父节点），可以确保点击到正确的元素。

### 为什么遍历所有 Window？

美团的弹窗（BottomSheet）虽然不是独立的 Window（在 `windows` 列表中只有 5 个系统窗口），
但弹窗内的元素仍然在主 Window 的节点树中。
通过遍历所有 Window 并按 Z-order 排序，可以确保优先检查最上层的窗口。

---

## 🧪 测试验证

**测试场景**: 打开美团 → 搜索瑞幸咖啡 → 买一杯香草拿铁

**关键步骤验证**:
1. ✅ 打开美团
2. ✅ 点击外卖
3. ✅ 点击搜索框
4. ✅ 输入"瑞幸咖啡"
5. ✅ 点击搜索按钮
6. ✅ 点击店铺
7. ✅ 搜索"香草拿铁"
8. ✅ 点击"选规格"按钮
9. ✅ **点击"加入购物车"按钮** ← 之前失败，现在成功
10. ✅ 点击"去结算"

---

## 📝 经验总结

1. **AccessibilityService 的 dispatchGesture 不可靠** - 在弹窗等特殊 Window 上可能失效
2. **优先使用 performAction(ACTION_CLICK)** - 比手势模拟更可靠
3. **选择最小面积节点** - 当多个节点重叠时，最小的通常是目标
4. **详细日志很重要** - 可以快速定位问题

---

## 🔮 后续优化方向

1. 考虑添加基于文本/描述的节点查找（如查找包含"加入购物车"文本的节点）
2. 优化等待弹窗展开的时机
3. 添加更多的容错和重试机制
