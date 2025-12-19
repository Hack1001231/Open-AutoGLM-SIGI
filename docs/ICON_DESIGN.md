# Sigillum Mentis 图标设计方案

## 设计概念
融合中国印章美学与科幻元素的方形应用图标

## 配色方案
- 主色：深空蓝 `#0A1929`
- 强调色：科技蓝 `#1976D2`
- 高光：浅蓝 `#90CAF9`
- 纯白：`#FFFFFF`

## 设计元素

### 方案 A：简约几何印章
```
┌─────────────────┐
│                 │
│   ╔═══════╗     │  深蓝背景
│   ║       ║     │  
│   ║   S   ║     │  白色印章轮廓
│   ║   M   ║     │  中央字母 S M (Sigillum Mentis)
│   ╚═══════╝     │  
│                 │
└─────────────────┘
```

### 方案 B：电路印章
```
┌─────────────────┐
│  ╱╲    ╱╲       │  深蓝背景
│ ╱  ╲  ╱  ╲      │  
│ ╲  ╱  ╲  ╱      │  电路纹路
│  ╲╱════╲╱       │  
│   ║████║        │  中央印章
│   ╚════╝        │  蓝色发光效果
└─────────────────┘
```

### 方案 C：神经网络印章（推荐）
```
┌─────────────────┐
│    ●───●───●    │  深蓝背景
│    │╲ │ ╱│      │  
│    │ ╲│╱ │      │  神经网络节点
│    ●──◆──●      │  中央钻石形印章
│    │ ╱│╲ │      │  
│    │╱ │ ╲│      │  白色/浅蓝线条
│    ●───●───●    │  
└─────────────────┘
```

## 具体实现建议

### 使用 Android Vector Drawable
创建文件：`app/src/main/res/drawable/ic_launcher_foreground.xml`

```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    
    <!-- 背景 -->
    <path
        android:fillColor="#0A1929"
        android:pathData="M0,0h108v108h-108z"/>
    
    <!-- 印章外框 -->
    <path
        android:strokeColor="#FFFFFF"
        android:strokeWidth="3"
        android:fillColor="#00000000"
        android:pathData="M30,30 L78,30 L78,78 L30,78 Z"/>
    
    <!-- 中央字母 S -->
    <path
        android:fillColor="#90CAF9"
        android:pathData="M45,40 Q50,35 55,40 L55,48 Q50,53 45,48 Z"/>
    
    <!-- 中央字母 M -->
    <path
        android:fillColor="#1976D2"
        android:pathData="M45,55 L48,68 L51,55 L54,68 L57,55 L57,68 L45,68 Z"/>
    
    <!-- 装饰线条（电路风格）-->
    <path
        android:strokeColor="#1976D2"
        android:strokeWidth="1"
        android:pathData="M20,54 L30,54 M78,54 L88,54"/>
</vector>
```

### 或使用在线工具生成
1. 访问 [Figma](https://figma.com) 或 [Canva](https://canva.com)
2. 创建 1024x1024 画布
3. 背景填充 `#0A1929`
4. 添加方形印章轮廓（白色，圆角 8px）
5. 中央添加 "S M" 字母或抽象几何图案
6. 添加电路纹路或神经网络线条
7. 导出为 PNG

### 快速原型（使用 Emoji + 文字）
如果需要快速测试，可以暂时使用：
- 图标：🔷（蓝色菱形）
- 或者：⬛（方块）+ 文字叠加

## 文件位置
- `app/src/main/res/mipmap-xxxhdpi/ic_launcher.png` (192x192)
- `app/src/main/res/mipmap-xxhdpi/ic_launcher.png` (144x144)
- `app/src/main/res/mipmap-xhdpi/ic_launcher.png` (96x96)
- `app/src/main/res/mipmap-hdpi/ic_launcher.png` (72x72)
- `app/src/main/res/mipmap-mdpi/ic_launcher.png` (48x48)

## 印章元素参考
- 中国传统印章：方形、篆刻风格
- 科幻元素：电路板纹路、神经网络、发光效果
- 极简主义：几何图形、对称设计
- 颜色：深蓝 + 白色/浅蓝，体现"思想钢印"的冷峻科技感
