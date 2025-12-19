# 设置 Java 环境（使用正确的路径）
$env:JAVA_HOME = "D:\android-studio\jbr"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

Write-Host "Using Java: $env:JAVA_HOME" -ForegroundColor Green
java -version

Write-Host "`nStarting build..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes. Please wait..." -ForegroundColor Yellow

# 使用 Git 的 sh 运行 gradlew
if (Get-Command sh -ErrorAction SilentlyContinue) {
    sh gradlew clean assembleDebug --no-daemon
} else {
    Write-Host "Error: sh command not found!" -ForegroundColor Red
    Write-Host "Please use Android Studio menu: Build -> Generate APKs" -ForegroundColor Yellow
}

Write-Host "`nPress any key to exit..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
