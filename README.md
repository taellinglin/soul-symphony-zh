# 灵魂交响曲

**灵魂交响曲** 是一款互动和沉浸式应用，结合了引人入胜的视觉效果和音乐，创造出一种超凡的体验。它具有动态粒子效果、动画传送门和引人入胜的音乐系统，将“灵魂交响曲”的概念带入生活。

---

## 🚀 特性

- **动态粒子系统：** 实时动画效果，支持颜色循环和随机化。
- **互动传送门：** 通过精美设计的传送门传送到不同的世界。
- **音乐集成：** 将粒子效果和动画与音乐的节奏同步。
- **高度可定制：** 可以轻松调整颜色、速度和动画的参数。

---

## 🛠️ 设置

请按照以下步骤在本地设置并运行项目：

### 前提条件

- Python 3.9+
- [Panda3D](https://www.panda3d.org/download.php)
- Git
- 可选： [Git LFS](https://git-lfs.com/)（用于处理大型文件，如 `.wav` 音频文件）

### 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/taellinglin/soul-symphony-zh.git
   cd soul-symphony-zh

2. 安装依赖：

    ```pip install -r requirements.txt```

3. 设置 Git LFS（如果处理 .wav 或其他大型文件）：

    ```git lfs install```
    ```git lfs pull```

4. 运行应用：

    ```python main.py```

    或

    ```./start_soul_symphony.bat```

## 🎨 工作原理

    粒子系统： soulparticles.py 脚本控制视觉效果。它动态更新颜色并管理粒子随机化。
    传送门： 通过动画资产处理传送门，负责场景或关卡之间的过渡。
    音乐同步： 系统将视觉效果与背景音乐的节奏和速度同步。

## 🖋️ 使用方法

    修改粒子效果： 编辑 soulparticles.py 中的参数，以自定义颜色、间隔和效果。
    添加传送门： 将资产放入相应目录，并在 main.py 中更新以包含新的传送门。
    集成新音乐： 将 .wav 文件放入指定目录，并在项目配置中链接它们。

### 项目结构

```soul-symphony/ │ 
               ├── assets/ # 视觉和音频资产 
               │ ├── models/ # 3D 模型和传送门资产 
               │ ├── music/ # 背景音乐（.wav 文件） 
               │ └── textures/ # 粒子和传送门纹理 
               │ ├── soulparticles.py # 粒子系统脚本 
               ├── portals.py # 传送门逻辑 
               ├── main.py # 主应用入口点 
               ├── requirements.txt # Python 依赖 
               └── README.md # 项目文档```
## 🤝 贡献

欢迎贡献！如果你想改进该项目，请按照以下步骤：

    Fork 仓库。

    创建一个新分支：

    ```git checkout -b feature-name```

提交你的更改：

    ```git commit -m "功能描述"```

推送到你的分支：

    ```git push origin feature-name```

    创建一个拉取请求（Pull Request）。

## 📝 许可证

本项目遵循 MIT 许可证。请参阅 LICENSE 文件以了解更多信息。

## 🌟 致谢

    感谢 Panda3D 社区提供了这个令人惊叹的引擎和支持。
    特别感谢所有贡献者，使这个项目每天都变得更好！
# Soul Symphony

**Soul Symphony** is an interactive and immersive application that combines captivating visuals and music to create an otherworldly experience. It features dynamic particle effects, animated portals, and an engaging music system to bring the concept of a **symphony of the soul** to life.

---

## 🚀 Features

- **Dynamic Particle System:** Real-time animated effects with color-cycling and randomization.
- **Interactive Portals:** Transport to different worlds with beautifully designed animated portals.
- **Music Integration:** Sync particle effects and animations to the rhythm of the music.
- **High Customizability:** Easily adjust parameters for colors, speeds, and animations.

---

## 🛠️ Setup

Follow these steps to set up and run the project locally:

### Prerequisites

- Python 3.9+
- [Panda3D](https://www.panda3d.org/download.php)
- Git
- Optional: [Git LFS](https://git-lfs.com/) (for handling large files like `.wav` audio files)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/taellinglin/soul-symphony-zh.git
   cd soul-symphony-zh```

2. Install Dependencies
   ```pip install -r requirements.txt```

3. Set up Git LFS (if handling .wav or other large files):
   ```git lfs install
      git lfs pull```

4. Run the application
   ```python main.py```
   or
   ```./start_soul_symphony.bat```

## 🎨 How It Works

    Particle System: The soulparticles.py script controls the visual effects. It updates colors dynamically and manages particle randomization.
    Portals: Portals are handled through animated assets, tied to transitions between levels or scenes.
    Music Synchronization: The system syncs visual effects to the rhythm and tempo of background audio.
## 🖋️ Usage

    Modify Particle Effects:
        Edit parameters in soulparticles.py to customize colors, intervals, and effects.
    Add Portals:
        Place assets in the appropriate directories and update main.py to include new portals.
    Integrate New Music:
        Drop .wav files into the designated directory and link them in the project configuration.


## 📂 Project Structure
   soul-symphony/
   │
   ├── assets/                 # Visual and audio assets
   │   ├── models/             # 3D models and portal assets
   │   ├── music/              # Background music (.wav files)
   │   └── textures/           # Particle and portal textures
   │
   ├── soulparticles.py        # Particle system script
   ├── portals.py              # Portal logic
   ├── main.py                 # Main application entry point
   ├── requirements.txt        # Python dependencies
   └── README.md               # Project documentation
## 🤝 Contributing

Contributions are welcome! If you'd like to improve the project, please follow these steps:

    Fork the repository.
    Create a new branch:

git checkout -b feature-name

Commit your changes:

git commit -m "Description of your feature"

Push to your branch:

    git push origin feature-name

    Create a pull request.

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for more information.

🌟 Acknowledgments

    Thanks to the Panda3D community for their awesome engine and support.
    Special thanks to all contributors for making this project better every day!