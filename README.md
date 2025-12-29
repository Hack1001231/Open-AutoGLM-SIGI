<p align="center">
  <img src="android-app/app/src/main/res/drawable/title_sigillum_pixel.png" alt="SIGI Logo" width="100%" />
</p>

# AutoGLM-SIGI: The Last Cyberphone
> **An Immersive Cyberpunk Interface for the Last AI Assistant**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Android-green.svg)](https://developer.android.com)
[![Philosophy](https://img.shields.io/badge/philosophy-Accelerationism-red.svg)](#philosophy)

---

## 🛑 Manifesto: Driving the Singularity

**SIGI** (Short for *Sigillum Mentis*, Latin for "Mental Seal") is not just an automation tool. It is a philosophy, an art installation, and a glimpse into the future of Human-AI interaction.

Inspired by the "Mental Seal" (思想钢印) from *The Three-Body Problem*, SIGI simplifies the complex relationship between humans and AI into a **driving metaphor**:

*   🔴 **EXECUTE (The Accelerator)**: Represents **e/acc (Effective Accelerationism)**. Pressing this surrenders control to the AI Agent (AutoGLM), allowing it to drive your device at full speed towards the objective. It is the Ye Wenjie button—sending a signal that cannot be unsent.
*   🟢 **ABORT (The Brake)**: Represents **Salvation / AI Safety**. A hard stop. The human reclaiming control from the machine.
*   ⌨️ **PROMPT (The Steering Wheel)**: Your text input, guiding the ghost in the machine.

## 🌟 Features: More Than A Tool

SIGI is built upon the powerful **AutoGLM** engine but wrapped in a narrative-driven experience.

### 1. Immersive Cyberpunk Aesthetics
*   **Cosmic Ripples**: Ambient space electronic music loops in the settings, providing a shelter from the digital noise.
*   **The Last Cyberphone Skin**: A UI designed to look like a terminal from a post-apocalyptic future. 
*   **Visual Storytelling**: A breathing star signals AI inference; a desolate base background hints at the consequences of acceleration.

### 2. The Doomsday List
Not just a "Favorites" menu. The **Doomsday List** is a collection of protocols you would execute if the world were ending tomorrow.
*   *"Order a bucket of fried chicken."*
*   *"Buy a train ticket to nowhere."*
*   *"Play Jay Chou's 'Common Jasmine Orange'."*

### 3. Permissionless Power (Hybrid Architecture)
Leveraging **ADB (Android Debug Bridge)** permissions, SIGI bypasses the limitations of standard accessibility services.
*   **Zero-Cost AI Phone**: Transforms any Android device into a $0 AI Agent.
*   **No PC Required (After Setup)**: Once granted permission via our one-click script, the phone runs independently.

---

## 🛠️ Installation

### For Non-Tech Users (The "One-Click" Method)
We believe AI should be accessible to everyone.
1.  Download the **SIGI Deployment Pack**.
2.  Enable **USB Debugging** on your phone.
3.  Connect to PC and double-click `一键安装(双击我).bat`.
4.  Disconnect and drive.

*See [User Manual (CN)](docs/SIGI_用户手册.md) for a step-by-step visual guide.*

### For Developers (Build from Source)
```bash
git clone https://github.com/ToTheMoon/Open-AutoGLM-SIGI.git
cd Open-AutoGLM-SIGI/android-app
./gradlew assembleDebug
```
**Requirements**:
*   Android SDK Platform-Tools (ADB)
*   JDK 17+
*   ZhipuAI API Key (or ModelScope)

---

## 🧠 Philosophy & Creator

> *"Software is a living organism. It is the best carrier for an artist's philosophical view of the world."*

**SIGI** is created by **Yanqiao** — a Hybrid Creator (Novelist / Artist / CS Engineer).

In an era where "AI Phones" are becoming consumer commodities, SIGI asks a different question: **Where are we going?**
The app is a thought experiment. It places you in the driver's seat of a vehicle moving at breakneck speed. The destination is unknown—survival or destruction?

To be, or not to be?
**To Accelerate, or to Abort?**

The choice is yours.

---

## 📂 Project Structure
*   `android-app/`: The Native Android Container (Kotlin).
*   `android-app/src/main/python/`: The Brain. AutoGLM agent logic running via Chaquopy.
*   `deploy_pack/`: Tools for mass distribution.
*   `docs/`: The Manuals and Manifestos.

---

*“We are all insects in the gutter, but some of us are looking at the stars.”*
