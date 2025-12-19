"""
Open-AutoGLM 混合方案 - 手机控制器（自动降级逻辑）
版本: 1.0.0

支持两种控制模式:
1. 无障碍服务模式 (优先) - 通过 AutoGLM Helper APP
2. LADB 模式 (备用) - 通过 ADB 连接

自动检测可用模式并降级
"""

import os
import subprocess
import requests
import base64
import time
import logging
from typing import Optional, Tuple
from PIL import Image
from io import BytesIO

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PhoneController')


class PhoneController:
    """手机控制器 - 支持自动降级"""
    
    # 控制模式
    MODE_ACCESSIBILITY = "accessibility"  # 无障碍服务模式
    MODE_LADB = "ladb"  # LADB 模式
    MODE_NONE = "none"  # 无可用模式
    
    def __init__(self, helper_url: str = "http://localhost:8080"):
        """
        初始化手机控制器
        
        Args:
            helper_url: AutoGLM Helper 的 URL
        """
        self.helper_url = helper_url
        self.mode = self.MODE_NONE
        self.adb_device = None
        
        # 自动检测可用模式
        self._detect_mode()
    
    def _detect_mode(self):
        """检测可用的控制模式"""
        logger.info("检测可用的控制模式...")
        
        # 1. 尝试无障碍服务模式
        if self._try_accessibility_service():
            self.mode = self.MODE_ACCESSIBILITY
            logger.info(f"✅ 使用无障碍服务模式 ({self.helper_url})")
            return
        
        # 2. 降级到 LADB 模式
        if self._try_ladb():
            self.mode = self.MODE_LADB
            logger.warning(f"⚠️ 降级到 LADB 模式 (设备: {self.adb_device})")
            return
        
        # 3. 都不可用
        self.mode = self.MODE_NONE
        logger.error("❌ 无可用控制方式")
        raise Exception(
            "无法连接到手机控制服务！\n"
            "请确保:\n"
            "1. AutoGLM Helper 已运行并开启无障碍权限\n"
            "2. 或者 LADB 已配对并运行\n"
        )
    
    def _try_accessibility_service(self) -> bool:
        """尝试连接无障碍服务"""
        try:
            response = requests.get(
                f"{self.helper_url}/status",
                timeout=3
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('accessibility_enabled'):
                    return True
                else:
                    logger.warning("AutoGLM Helper 运行中，但无障碍服务未开启")
                    return False
            
            return False
        except Exception as e:
            logger.debug(f"无障碍服务连接失败: {e}")
            return False
    
    def _try_ladb(self) -> bool:
        """尝试连接 LADB"""
        try:
            # 检查 adb 是否可用
            result = subprocess.run(
                ['adb', 'devices'],
                capture_output=True,
                text=True,
                timeout=3
            )
            
            if result.returncode != 0:
                logger.debug("ADB 命令不可用")
                return False
            
            # 解析设备列表
            lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
            devices = [line.split('\t')[0] for line in lines if '\tdevice' in line]
            
            if not devices:
                logger.debug("未找到已连接的 ADB 设备")
                return False
            
            # 使用第一个设备
            self.adb_device = devices[0]
            logger.info(f"找到 ADB 设备: {self.adb_device}")
            
            # 测试连接
            test_result = subprocess.run(
                ['adb', '-s', self.adb_device, 'shell', 'echo', 'test'],
                capture_output=True,
                timeout=3
            )
            
            return test_result.returncode == 0
            
        except Exception as e:
            logger.debug(f"LADB 连接失败: {e}")
            return False
    
    def get_mode(self) -> str:
        """获取当前控制模式"""
        return self.mode
    
    def screenshot(self) -> Optional[Image.Image]:
        """
        截取屏幕
        
        Returns:
            PIL.Image 对象，失败返回 None
        """
        if self.mode == self.MODE_ACCESSIBILITY:
            return self._screenshot_accessibility()
        elif self.mode == self.MODE_LADB:
            return self._screenshot_ladb()
        else:
            logger.error("无可用的截图方式")
            return None
    
    def _screenshot_accessibility(self) -> Optional[Image.Image]:
        """通过无障碍服务截图"""
        try:
            response = requests.get(
                f"{self.helper_url}/screenshot",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    # 解码 Base64 图片
                    image_data = base64.b64decode(data['image'])
                    image = Image.open(BytesIO(image_data))
                    logger.debug(f"截图成功 (无障碍): {image.size}")
                    return image
            
            logger.error(f"截图失败: HTTP {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"截图失败 (无障碍): {e}")
            return None
    
    def _screenshot_ladb(self) -> Optional[Image.Image]:
        """通过 LADB 截图"""
        try:
            # 截图到设备
            subprocess.run(
                ['adb', '-s', self.adb_device, 'shell', 'screencap', '-p', '/sdcard/autoglm_screenshot.png'],
                check=True,
                timeout=5
            )
            
            # 拉取到本地
            local_path = '/tmp/autoglm_screenshot.png'
            subprocess.run(
                ['adb', '-s', self.adb_device, 'pull', '/sdcard/autoglm_screenshot.png', local_path],
                check=True,
                timeout=5
            )
            
            # 打开图片
            image = Image.open(local_path)
            logger.debug(f"截图成功 (LADB): {image.size}")
            
            # 清理临时文件
            subprocess.run(
                ['adb', '-s', self.adb_device, 'shell', 'rm', '/sdcard/autoglm_screenshot.png'],
                timeout=3
            )
            
            return image
            
        except Exception as e:
            logger.error(f"截图失败 (LADB): {e}")
            return None
    
    def tap(self, x: int, y: int) -> bool:
        """
        执行点击操作
        
        Args:
            x: X 坐标
            y: Y 坐标
        
        Returns:
            是否成功
        """
        if self.mode == self.MODE_ACCESSIBILITY:
            return self._tap_accessibility(x, y)
        elif self.mode == self.MODE_LADB:
            return self._tap_ladb(x, y)
        else:
            logger.error("无可用的点击方式")
            return False
    
    def _tap_accessibility(self, x: int, y: int) -> bool:
        """通过无障碍服务点击"""
        try:
            response = requests.post(
                f"{self.helper_url}/tap",
                json={'x': x, 'y': y},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                logger.debug(f"点击 ({x}, {y}): {success}")
                return success
            
            return False
            
        except Exception as e:
            logger.error(f"点击失败 (无障碍): {e}")
            return False
    
    def _tap_ladb(self, x: int, y: int) -> bool:
        """通过 LADB 点击"""
        try:
            result = subprocess.run(
                ['adb', '-s', self.adb_device, 'shell', 'input', 'tap', str(x), str(y)],
                check=True,
                timeout=3
            )
            
            logger.debug(f"点击 ({x}, {y}): True")
            return True
            
        except Exception as e:
            logger.error(f"点击失败 (LADB): {e}")
            return False
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> bool:
        """
        执行滑动操作
        
        Args:
            x1: 起点 X 坐标
            y1: 起点 Y 坐标
            x2: 终点 X 坐标
            y2: 终点 Y 坐标
            duration: 持续时间 (毫秒)
        
        Returns:
            是否成功
        """
        if self.mode == self.MODE_ACCESSIBILITY:
            return self._swipe_accessibility(x1, y1, x2, y2, duration)
        elif self.mode == self.MODE_LADB:
            return self._swipe_ladb(x1, y1, x2, y2, duration)
        else:
            logger.error("无可用的滑动方式")
            return False
    
    def _swipe_accessibility(self, x1: int, y1: int, x2: int, y2: int, duration: int) -> bool:
        """通过无障碍服务滑动"""
        try:
            response = requests.post(
                f"{self.helper_url}/swipe",
                json={'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'duration': duration},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                logger.debug(f"滑动 ({x1},{y1}) -> ({x2},{y2}): {success}")
                return success
            
            return False
            
        except Exception as e:
            logger.error(f"滑动失败 (无障碍): {e}")
            return False
    
    def _swipe_ladb(self, x1: int, y1: int, x2: int, y2: int, duration: int) -> bool:
        """通过 LADB 滑动"""
        try:
            result = subprocess.run(
                ['adb', '-s', self.adb_device, 'shell', 'input', 'swipe', 
                 str(x1), str(y1), str(x2), str(y2), str(duration)],
                check=True,
                timeout=5
            )
            
            logger.debug(f"滑动 ({x1},{y1}) -> ({x2},{y2}): True")
            return True
            
        except Exception as e:
            logger.error(f"滑动失败 (LADB): {e}")
            return False
    
    def input_text(self, text: str) -> bool:
        """
        输入文字
        
        Args:
            text: 要输入的文字
        
        Returns:
            是否成功
        """
        if self.mode == self.MODE_ACCESSIBILITY:
            return self._input_accessibility(text)
        elif self.mode == self.MODE_LADB:
            return self._input_ladb(text)
        else:
            logger.error("无可用的输入方式")
            return False
    
    def _input_accessibility(self, text: str) -> bool:
        """通过无障碍服务输入"""
        try:
            response = requests.post(
                f"{self.helper_url}/input",
                json={'text': text},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                logger.debug(f"输入文字: {success}")
                return success
            
            return False
            
        except Exception as e:
            logger.error(f"输入失败 (无障碍): {e}")
            return False
    
    def _input_ladb(self, text: str) -> bool:
        """通过 LADB 输入"""
        try:
            # ADB input text 不支持中文，需要使用其他方法
            # 这里简化处理，仅支持英文
            escaped_text = text.replace(' ', '%s')
            result = subprocess.run(
                ['adb', '-s', self.adb_device, 'shell', 'input', 'text', escaped_text],
                check=True,
                timeout=5
            )
            
            logger.debug(f"输入文字: True")
            return True
            
        except Exception as e:
            logger.error(f"输入失败 (LADB): {e}")
            return False


# 测试代码
if __name__ == '__main__':
    print("测试 PhoneController...")
    
    try:
        controller = PhoneController()
        print(f"当前模式: {controller.get_mode()}")
        
        # 测试截图
        print("测试截图...")
        img = controller.screenshot()
        if img:
            print(f"截图成功: {img.size}")
        else:
            print("截图失败")
        
        # 测试点击
        print("测试点击...")
        success = controller.tap(500, 500)
        print(f"点击结果: {success}")
        
    except Exception as e:
        print(f"错误: {e}")
