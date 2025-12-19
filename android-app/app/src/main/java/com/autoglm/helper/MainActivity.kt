package com.autoglm.helper

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import com.chaquo.python.Python

class MainActivity : Activity(), LogCallback {

    private lateinit var statusText: TextView
    private lateinit var logText: TextView
    private lateinit var logScroll: ScrollView
    private lateinit var logToggle: TextView
    private lateinit var taskInput: EditText
    private lateinit var executeButton: Button
    private lateinit var stopButton: Button
    private lateinit var openSettingsButton: Button
    private lateinit var copyLogButton: Button
    
    private val handler = Handler(Looper.getMainLooper())
    private var isTaskRunning = false
    private var isLogExpanded = true  // 日志默认展开

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        statusText = findViewById(R.id.statusText)
        logText = findViewById(R.id.logText)
        logScroll = findViewById(R.id.logScroll)
        logToggle = findViewById(R.id.logToggle)
        taskInput = findViewById(R.id.taskInput)
        executeButton = findViewById(R.id.executeButton)
        stopButton = findViewById(R.id.stopButton)
        openSettingsButton = findViewById(R.id.openSettingsButton)
        copyLogButton = findViewById(R.id.copyLogButton)
        
        // 日志折叠/展开功能
        logToggle.setOnClickListener {
            toggleLogVisibility()
        }
        
        executeButton.setOnClickListener {
            startTask()
        }
        
        stopButton.setOnClickListener {
            onLog("🛑 正在发送停止信号（视觉 + 逻辑双保险）...")
            try {
                val py = Python.getInstance()
                
                // 1. 启用视觉停止信号（快速响应）
                val helperModule = py.getModule("android_helper")
                helperModule.callAttr("enable_visual_stop_signal")
                onLog("✅ 已在下一帧截图上添加红色停止横幅")
                
                // 2. 设置软着陆（保底机制，3步后强制停止）
                val agentModule = py.getModule("agent_main")
                val result = agentModule.callAttr("stop_gracefully", 3).toInt()
                
                if (result > 0) {
                    onLog("✅ 已设置保底停止点：第 $result 步")
                    onLog("💡 AI 识别到红色横幅后会立即停止，否则最多 3 步后停止")
                } else {
                    onLog("⚠️ 当前没有正在运行的任务")
                }
            } catch (e: Exception) {
                onLog("❌ 停止失败: ${e.message}")
            }
        }
        
        openSettingsButton.setOnClickListener {
            val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
            startActivity(intent)
        }
        
        copyLogButton.setOnClickListener {
            copyLogToClipboard()
        }
        
        updateStatus()
    }

    private fun copyLogToClipboard() {
        val clipboard = getSystemService(CLIPBOARD_SERVICE) as android.content.ClipboardManager
        val clip = android.content.ClipData.newPlainText("AutoGLM Log", logText.text.toString())
        clipboard.setPrimaryClip(clip)
        Toast.makeText(this, "日志已复制到剪贴板", Toast.LENGTH_SHORT).show()
    }
    
    private fun toggleLogVisibility() {
        isLogExpanded = !isLogExpanded
        if (isLogExpanded) {
            // 展开日志
            logScroll.visibility = View.VISIBLE
            logToggle.text = "▼"
        } else {
            // 折叠日志
            logScroll.visibility = View.GONE
            logToggle.text = "▶"
        }
    }

    override fun onResume() {
        super.onResume()
        updateStatus()
    }

    private fun updateStatus() {
        val service = AutoGLMAccessibilityService.getInstance()
        if (service != null) {
            statusText.text = "系统状态 :: 就绪"
            statusText.setTextColor(android.graphics.Color.parseColor("#1976D2"))
            executeButton.isEnabled = !isTaskRunning
        } else {
            statusText.text = "系统状态 :: 离线 (需无障碍权限)"
            statusText.setTextColor(android.graphics.Color.parseColor("#FF5252"))
            executeButton.isEnabled = false
        }
        // 只有在任务运行时，停止按钮才可用
        stopButton.isEnabled = isTaskRunning
    }

    private fun startTask() {
        val task = taskInput.text.toString()
        if (task.isBlank()) {
            Toast.makeText(this, "请输入任务", Toast.LENGTH_SHORT).show()
            return
        }

        logText.text = ""
        isTaskRunning = true
        updateStatus() // 更新按钮状态
        
        Thread {
            try {
                val py = Python.getInstance()
                val module = py.getModule("agent_main")
                
                // 这里你可以硬编码 API Key 或者从设置中读取
                val apiKey = "562eac47fb0c43fa995ee58261d12a52.Y2HAB0eRQPyXKiHI"
                val baseUrl = "https://open.bigmodel.cn/api/paas/v4/"
                val modelName = "autoglm-phone"
                
                module.callAttr("run_task", apiKey, baseUrl, modelName, task, this)
                
                runOnUiThread {
                    isTaskRunning = false
                    updateStatus()
                    Toast.makeText(this, "任务结束", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                runOnUiThread {
                    onLog("❌ 运行出错: ${e.message}")
                    isTaskRunning = false
                    updateStatus()
                }
            }
        }.start()
    }

    override fun onLog(message: String) {
        runOnUiThread {
            logText.append("$message\n")
            logScroll.post {
                logScroll.fullScroll(View.FOCUS_DOWN)
            }
        }
    }
}
