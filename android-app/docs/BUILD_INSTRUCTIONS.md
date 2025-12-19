# Android APP 构建说明

## 方式 1: 使用 Android Studio (推荐)

### 步骤

1. **安装 Android Studio**
   - 下载: https://developer.android.com/studio
   - 安装 Android SDK

2. **打开项目**
   - 启动 Android Studio
   - File → Open → 选择 `android-app` 目录

3. **同步 Gradle**
   - 等待 Gradle 自动同步
   - 如果失败，点击 "Sync Project with Gradle Files"

4. **构建 APK**
   - Build → Build Bundle(s) / APK(s) → Build APK(s)
   - 等待构建完成
   - APK 位置: `app/build/outputs/apk/debug/app-debug.apk`

5. **安装到手机**
   - 连接手机 (USB 调试模式)
   - Run → Run 'app'
   - 或手动安装: `adb install app-debug.apk`

---

## 方式 2: 使用命令行

### 前提条件

- 安装 JDK 11+
- 安装 Android SDK
- 设置环境变量 `ANDROID_HOME`

### 步骤

```bash
# 1. 进入项目目录
cd android-app

# 2. 赋予 gradlew 执行权限 (Linux/Mac)
chmod +x gradlew

# 3. 构建 Debug APK
./gradlew assembleDebug

# 4. APK 输出位置
# app/build/outputs/apk/debug/app-debug.apk

# 5. 安装到手机
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Windows

```cmd
# 3. 构建 Debug APK
gradlew.bat assembleDebug

# 5. 安装到手机
adb install app\build\outputs\apk\debug\app-debug.apk
```

---

## 方式 3: 在线构建 (无需本地环境)

### 使用 GitHub Actions

1. Fork 项目到 GitHub
2. 启用 Actions
3. 推送代码触发自动构建
4. 下载构建好的 APK

### 使用 AppCenter

1. 注册 AppCenter 账号
2. 连接 GitHub 仓库
3. 配置构建
4. 自动构建并分发

---

## 签名 APK (发布版本)

### 生成签名密钥

```bash
keytool -genkey -v -keystore autoglm-release.keystore \
  -alias autoglm -keyalg RSA -keysize 2048 -validity 10000
```

### 配置签名

在 `app/build.gradle.kts` 中添加:

```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("../autoglm-release.keystore")
            storePassword = "your_password"
            keyAlias = "autoglm"
            keyPassword = "your_password"
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            // ...
        }
    }
}
```

### 构建 Release APK

```bash
./gradlew assembleRelease
```

---

## 故障排除

### Gradle 同步失败

**问题**: Could not resolve dependencies

**解决**:
```bash
# 清理缓存
./gradlew clean

# 重新下载依赖
./gradlew --refresh-dependencies
```

### SDK 版本问题

**问题**: SDK not found

**解决**:
1. 打开 Android Studio
2. Tools → SDK Manager
3. 安装 Android SDK 34

### 构建失败

**问题**: Build failed with errors

**解决**:
```bash
# 查看详细错误
./gradlew assembleDebug --stacktrace

# 清理后重新构建
./gradlew clean assembleDebug
```

---

## 输出文件

### Debug APK
- 位置: `app/build/outputs/apk/debug/app-debug.apk`
- 大小: 约 2-3 MB
- 用途: 测试和开发

### Release APK
- 位置: `app/build/outputs/apk/release/app-release.apk`
- 大小: 约 1-2 MB (优化后)
- 用途: 正式发布

---

## 快速构建脚本

创建 `build.sh`:

```bash
#!/bin/bash
set -e

echo "开始构建 AutoGLM Helper APK..."

cd android-app

# 清理
./gradlew clean

# 构建
./gradlew assembleDebug

# 复制到根目录
cp app/build/outputs/apk/debug/app-debug.apk ../AutoGLM-Helper.apk

echo "构建完成！APK: ../AutoGLM-Helper.apk"
```

使用:
```bash
chmod +x build.sh
./build.sh
```

---

## 注意事项

1. **首次构建较慢** - 需要下载依赖，约 5-10 分钟
2. **网络要求** - 需要访问 Google Maven 仓库
3. **磁盘空间** - 需要约 2-3 GB 空间
4. **内存要求** - 建议 8 GB+ RAM

---

## 已构建 APK

为了方便使用，我已经预先构建好了 APK，您可以直接使用:

**文件**: `AutoGLM-Helper.apk`
**版本**: 1.0.0
**大小**: 约 2 MB
**签名**: Debug 签名（仅用于测试）

**安装**:
```bash
adb install AutoGLM-Helper.apk
```

或直接在手机上打开 APK 文件安装。
