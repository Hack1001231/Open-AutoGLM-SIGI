@echo off
set JAVA_HOME=C:\Program Files\Android\Android Studio\jbr
set PATH=%JAVA_HOME%\bin;%PATH%
echo Using Java: %JAVA_HOME%
java -version
echo.
echo Starting build...
bash gradlew clean assembleDebug --no-daemon
