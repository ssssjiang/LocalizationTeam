# PCD 点云可视化操作流程（Potree Web）

> **状态**：✅ 2026-04-28 实测跑通（Ubuntu 22.04 + NVIDIA 580 + Node 20）
> **作者**：宋姝
> **关联**：展会模式 2026-06 Kaffa 展会，3D 地图渲染素材

---

## 0. 选型先看这里（30 秒决定走哪条路）


| 你的需求               | 推荐方案                              | 部署时间        |
| ------------------ | --------------------------------- | ----------- |
| **自己看一眼 PCD**      | `pcl_viewer`（30 秒）                | 30 秒        |
| **给销售/老板 demo**    | `pcl_viewer` 全屏 + 按 j 截图          | 1 分钟        |
| **生成市场宣传素材（图/视频）** | Blender + Photogrammetry Importer | 半天          |
| **展会现场浏览器全屏展示**    | **Potree（本文档）**                   | 30 分钟（按本流程） |
| **几亿点级超大场景**       | Potree 不二之选                       | -           |


### 最快路径（90% 自用场景）

```bash
sudo apt install -y pcl-tools
pcl_viewer /path/to/your.pcd
# 默认就是 RGB 着色，按 j 截图
```

**只有"展会浏览器展示"才需要继续往下看 Potree。**

---

## 1. 一句话总结 Potree 部署

```
PCD → (convert_pcd_to_las.py) → LAS → (PotreeConverter) → 八叉树 → (Potree Web + npm start) → 浏览器
```

**关键点**：

1. PCD → LAS 必须用本仓库的 `convert_pcd_to_las.py`（PDAL 直接转有 RGB bug，已知问题）
2. PotreeConverter 必须**本地编译**（PotreeDesktop 自带的是 Windows .exe）
3. Potree Web 必须用 `**npm start`** 启动（不能用 `python -m http.server`）⭐ 最大的坑

---

## 2. 一次性环境准备

> 已经做过的可跳过。这一节只需要**装一次**。

```bash
# 系统依赖
sudo apt update
sudo apt install -y git build-essential cmake libtbb-dev pcl-tools python3 python3-pip pdal
pip install numpy laspy

# Node.js 20（如果系统 node < 16）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 20 && nvm use 20

# 编译 PotreeConverter（约 2-3 分钟）
cd ~
git clone https://github.com/potree/PotreeConverter.git
cd PotreeConverter && mkdir build && cd build
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5    # ⚠️ CMake 4.0+ 必须加这个参数
make -j$(nproc)
ls ~/PotreeConverter/build/PotreeConverter      # 验证：应该是个可执行文件

# 部署 Potree Web
cd ~
git clone https://github.com/potree/potree.git
cd potree
npm install                                     # 会自动 build
ls ~/potree/build/potree/potree.js              # 验证：应该存在
```

---

## 3. 核心工作流：可视化一份 PCD

> 假设要可视化 `/home/songshu/下载/my.pcd`

### Step 1：PCD → LAS（保留 RGB）

```bash
python3 ~/repo/LocalizationTeam/projects/exhibition-mode-2026-06/howto/convert_pcd_to_las.py \
  /home/songshu/下载/my.pcd \
  /home/songshu/my.las
```

**期望输出**关键行：

```
backend: builtin  points: XXX,XXX  has_color: True
RGB sample (uint8): R=XX G=XX B=XX     ← 不应全是 0
```

**验证 RGB 是否正确进入 LAS**：

```bash
pdal info /home/songshu/my.las --stats 2>&1 | python3 -c "
import sys,json
d=json.loads(sys.stdin.read())
for s in d['stats']['statistic']:
    if s['name'] in ('Red','Green','Blue'):
        print(f\"{s['name']:6}: max={s['maximum']:.0f} avg={s['average']:.0f}\")
"
```

期望：`max=65535 avg=约2-3万`（max 是 0 就是出问题了）。

---

### Step 2：LAS → Potree 八叉树

```bash
mkdir -p ~/potree_data
~/PotreeConverter/build/PotreeConverter \
  /home/songshu/my.las \
  -o ~/potree_data/my
```

**期望输出**：最后一行类似 `total file size: XXX MB`，**不能有 `#points: 0` 或 `nlohmann json` 报错**。

**验证**：

```bash
ls ~/potree_data/my/
# 期望文件: metadata.json  octree.bin  hierarchy.bin
```

---

### Step 3：链接到 Potree Web

```bash
ln -sf ~/potree_data/my ~/potree/pointclouds/my
```

---

### Step 4：写专属 viewer 页面

```bash
# 复制模板，改名
cp ~/potree/examples/test_rgb_v2.html ~/potree/examples/my.html

# 把里面所有 test_rgb_v2 替换成 my（点云名 + 路径）
sed -i 's|test_rgb_v2|my|g' ~/potree/examples/my.html
```

> **不要直接用 `viewer.html?pointcloud=...`** —— Potree 的 `viewer.html` 不解析 URL 参数，会 fallback 到默认 demo。**必须自己写一个 HTML**。

---

### Step 5：⭐ 启动 Potree Web（必须 `npm start`）

```bash
cd ~/potree
npm start
```

**期望输出**关键行：

```
Server started http://localhost:1234
created build/potree/workers/2.0/DecoderWorker.js
created build/potree/workers/2.0/DecoderWorker_brotli.js
```

**保持这个终端开着**。

---

### Step 6：浏览器打开

```
http://localhost:1234/examples/my.html
```

加载后：

- 鼠标左键拖动旋转
- 滚轮缩放
- 右键拖动平移
- 按 **R** 键重置视角，**F** 键 fit to screen

---

## 4. 美化参数配方（按场景选）

打开侧边栏（左上角 ☰）→ Scene → 选中点云 → Properties 面板。

### 配方 A：真实质感（SLAM 建图、室外街景，**推荐默认**）


| 参数           | 值                      |
| ------------ | ---------------------- |
| Attribute    | **rgba**（不是 elevation） |
| Point sizing | **FIXED** ⭐            |
| Point size   | 1                      |
| Minimum size | 0                      |
| Shape        | **SQUARE** 或 CIRCLE    |
| Background   | Black                  |
| Point Budget | 10M+                   |


### 配方 B：电影级 wow（展会 demo 想炫）


| 参数           | 值                         |
| ------------ | ------------------------- |
| Point sizing | **FIXED** ⭐               |
| Shape        | **PARABOLOID**（小球感）       |
| Point size   | 1                         |
| EDL Enable   | ✅，Radius 1.4，Strength 0.4 |
| Point Budget | 50M（要点密）                  |


### ⚠️ 千万不要的组合

`**PARABOLOID + ADAPTIVE`** —— 会让外围稀疏区域的点变成**带轮廓的大圆球**，颗粒感极强。
ADAPTIVE 只在「点云非常稠密均匀」时好看，**SLAM 类数据基本都不适合**。

---

## 5. 模板文件参考

### 5.1 `convert_pcd_to_las.py`（同目录）

PCD → LAS 转换脚本，关键特性：

- 内置纯 numpy PCD 解析器，**不依赖 Open3D**
- 正确解包 PCD 的 packed RGB（PDAL 不会自动做）
- 输出 LAS PointFormat 3，含 16bit RGB

调用：

```bash
python3 convert_pcd_to_las.py input.pcd output.las
```

### 5.2 Viewer HTML 模板（`~/potree/examples/test_rgb_v2.html`）

最小可用模板，复制改名 + 改两处即可：

```javascript
Potree.loadPointCloud(
  "../pointclouds/【你的点云名】/metadata.json",   // 改这里
  "【你的点云名】",                                // 改这里
  function(e){
    let m = e.pointcloud.material;
    m.activeAttributeName = "rgba";
    m.pointSizeType = Potree.PointSizeType.ADAPTIVE;
    m.shape = Potree.PointShape.PARABOLOID;
    viewer.scene.addPointCloud(e.pointcloud);
    viewer.fitToScreen();
  }
);
```

---

## 6. 重要的坑（按踩坑严重程度排序）

### 🔥 坑 0：用 `python -m http.server` 启动 Potree

**症状**：浏览器加载 Potree v2 格式（`metadata.json`）的点云时：

- 显示残缺（"只有一小片"、"被裁掉一块"）
- 颜色全黑或异常
- 静默 fallback 到默认 demo（如 `sigeom.sa` 绿农田）
- F12 console 报 worker 加载失败

**根因**：Potree v2 的 worker（`build/potree/workers/2.0/DecoderWorker.js` 等）需要 gulp 实时构建。`python -m http.server` 只是静态文件服务，构不出来。

**解决**：永远用 `cd ~/potree && npm start`，端口 **1234**。

---

### 坑 1：CMake ≥ 4.0 编译 PotreeConverter 报错

**症状**：

```
CMake Error at Converter/libs/brotli/CMakeLists.txt:5:
Compatibility with CMake < 3.5 has been removed
```

**解决**：cmake 加参数

```bash
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5
```

---

### 坑 2：PotreeDesktop 在 Linux 上无法转换

**症状**：拖入 .las 后窗口黑屏，无报错。

**根因**：PotreeDesktop 自带的 `~/PotreeDesktop/libs/PotreeConverter2/PotreeConverter.exe` 是 Windows 可执行文件，Linux 跑不了。

**解决**：用本地编译的 PotreeConverter，或者干脆用 Potree Web 路线（本文档）。

---

### 坑 3：PotreeConverter 不支持 PLY

**症状**：

```bash
~/PotreeConverter/build/PotreeConverter input.ply -o ...
# 输出: #points: 0, cubicAABB: inf, nlohmann json type_error 崩溃
```

**根因**：源码 `main.cpp` 里只有 `iEndsWith(str, "las") || iEndsWith(str, "laz")`，**只吃 LAS/LAZ**。

**解决**：必须先转成 LAS，不能用 PLY。

---

### 坑 4：PDAL 直接 `pdal translate pcd las` 不保留 RGB

**症状**：

```bash
pdal translate input.pcd output.las
# RGB 全是 0
```

**根因**：PDAL 已知 bug（[issue 4456](https://github.com/PDAL/PDAL/issues/4456)），**到 2025 年仍未修复**。
PDAL 也尝试过用 `filters.assign` pipeline 拆 RGB，但 PDAL 2.3 的 assign 表达式语法不完整，照样不行。

**解决**：用本仓库的 `convert_pcd_to_las.py`（30 行 numpy + laspy，避开所有 PDAL bug）。

---

### 坑 5：Open3D 在 Python 3.13+ 装不上

**症状**：

```
$ pip install open3d
ERROR: Could not find a version that satisfies the requirement open3d
```

**根因**：Open3D wheel 只到 Python 3.12。

**解决**：用 `convert_pcd_to_las.py`（不需要 Open3D），或者建 conda Python 3.11 环境。

---

### 坑 6：`viewer.html?pointcloud=...` URL 参数被忽略

**症状**：传 URL 参数后，左侧 Scene 列表里点云名是 `sigeom.sa`（默认 demo），不是自己的。

**根因**：Potree 的 `viewer.html` 不解析 URL 参数，是个空模板。

**解决**：自己写一个 HTML（见 §3 Step 4），里面写 `Potree.loadPointCloud(...)` 显式加载。

---

### 坑 7：MESA-LOADER + X11 报错（Electron 双显卡）

**症状**：PotreeDesktop 启动报：

```
MESA-LOADER: failed to open nvidia-drm: Permission denied
```

**解决**：加 `--no-sandbox`：

```bash
./node_modules/.bin/electron . --no-sandbox
```

---

### 坑 8：放大点云时点云从下方出画面（相机焦点偏离）

**症状**：滚轮放大时，点云不是"在视图中放大"，而是被推出画面下方。

**根因**：PotreeConverter 把扁平点云的 `boundingBox` 强制撑成立方体（cubicAABB）。
你的点云 Z 范围 -3.95 ~ 32.73（高 36m），但 bbox 撑成 184m × 184m × 184m。
默认相机焦点在 bbox 中心 → **被推到点云上空 ~80m 的虚空中** → 滚轮缩放时镜头绕虚空旋转。

**解决**（按推荐度排序）：

1. **最简单**：在 3D 视图区**鼠标双击点云上一个清晰的点** → Potree 立即把焦点重设到那里
2. **viewer HTML 里强制设焦点**（参考 `test_rgb_v2.html` 的修改版）：
  ```javascript
   let bbox = pointcloud.pcoGeometry.tightBoundingBox || pointcloud.boundingBox;
   let center = bbox.getCenter(new THREE.Vector3());
   viewer.scene.view.lookAt(center);
   viewer.orbitControls.pivot = center;
  ```
3. **根本修复**：转换前给 LAS 加 8 个"立方体角点"虚拟点，让真实数据本身就是立方体 bbox

---

### 坑 9（误入歧途）：以为是离群点 / cubicAABB / 颜色编码 bug

**血泪教训**：4 小时调试中我反复怀疑是这些"数据问题"，写了 `clip_pcd_outliers.py`、`convert_pcd_to_ply.py`、加 anchor points 等等。**全是无用功**。

真相：所有显示异常的根因都是**坑 0**（用了 python http server）。一旦切到 `npm start`，所有"问题"瞬间消失。

**教训**：Potree 显示异常时，**第一件事是检查启动方式，不是怀疑数据**。

---

## 7. 完整命令快速参考（TL;DR）

```bash
# === 一次性环境（已装过跳过）===
sudo apt install -y git build-essential cmake libtbb-dev pcl-tools python3 python3-pip pdal
pip install numpy laspy
nvm install 20 && nvm use 20

# === 编译 PotreeConverter（一次性）===
cd ~ && git clone https://github.com/potree/PotreeConverter.git
cd PotreeConverter && mkdir build && cd build
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make -j$(nproc)

# === 部署 Potree Web（一次性）===
cd ~ && git clone https://github.com/potree/potree.git
cd potree && npm install

# === 每次有新 PCD 跑这个（4 步）===
PCD=/home/songshu/下载/new.pcd
NAME=new

# 1. 转 LAS
python3 ~/repo/LocalizationTeam/projects/exhibition-mode-2026-06/howto/convert_pcd_to_las.py \
  "$PCD" /tmp/$NAME.las

# 2. 转 Potree
rm -rf ~/potree_data/$NAME
~/PotreeConverter/build/PotreeConverter /tmp/$NAME.las -o ~/potree_data/$NAME

# 3. 链接 + 复制 viewer 模板
ln -sf ~/potree_data/$NAME ~/potree/pointclouds/$NAME
cp ~/potree/examples/test_rgb_v2.html ~/potree/examples/$NAME.html
sed -i "s|test_rgb_v2|$NAME|g" ~/potree/examples/$NAME.html

# 4. 启动（保持开着）
cd ~/potree && npm start

# 5. 浏览器打开（新终端）
xdg-open "http://localhost:1234/examples/$NAME.html"
```

---

## 8. 性能参考（实测）


| 阶段                       | 输入                  | 输出                 | 耗时   |
| ------------------------ | ------------------- | ------------------ | ---- |
| `convert_pcd_to_las.py`  | PCD 1196 万点 / 180MB | LAS 388MB          | 5 秒  |
| `PotreeConverter`        | LAS 388MB           | 八叉树 400MB（depth=9） | 30 秒 |
| Potree Web 启动（npm start） | -                   | -                  | 5 秒  |
| 浏览器加载 + 渲染               | -                   | 60fps 流畅           | 即时   |


---

## 9. 文件清单

本文档配套的脚本和模板（都在同目录）：


| 文件                                   | 用途                                          |
| ------------------------------------ | ------------------------------------------- |
| `convert_pcd_to_las.py`              | ⭐ PCD → LAS（核心）                             |
| `convert_pcd_to_ply.py`              | PCD → PLY（备用，Potree 不支持但 Blender/MeshLab 用） |
| `peek_pcd_color.py`                  | 快速生成俯视 4K 截图（市场素材）                          |
| `~/potree/examples/test_rgb_v2.html` | Potree viewer 模板                            |


---

## 9.5. Three.js 后处理特效（Bloom / SSAO / DOF）

Potree 基于 Three.js r124，可以挂 EffectComposer 实现：

- **Bloom** 辉光（亮处发光）
- **SSAO** 环境光遮蔽（凹陷处变暗）
- **DOF** 景深虚化

### 安装一次性依赖

```bash
mkdir -p ~/potree/libs/three.js/postprocessing
cd ~/potree/libs/three.js/postprocessing
BASE="https://raw.githubusercontent.com/mrdoob/three.js/r124/examples/js"
for f in postprocessing/EffectComposer.js postprocessing/RenderPass.js \
         postprocessing/ShaderPass.js postprocessing/UnrealBloomPass.js \
         shaders/CopyShader.js shaders/LuminosityHighPassShader.js; do
    curl -sL -o "$(basename $f)" "$BASE/$f"
done
```

### 完整模板

见 `~/potree/examples/test_rgb_v2_bloom.html`，已实现 Bloom，并通过 hook 替换 `viewer.renderer.render` 接管渲染管线。

### 控制台调参

```javascript
bloomPass.strength = 1.5    // 辉光强度 0~3
bloomPass.threshold = 0.3   // 亮度阈值，越低越多区域发光
bloomPass.radius = 0.6      // 光晕半径
```

### 关键坑

1. **必须用 r124 版本的 postprocessing 脚本**（Potree 的 Three.js 是 r124）
2. **Bloom 和 EDL 二选一**（EDL 也是后处理，会被取代）
3. **必须 hook `viewer.renderer.render`**，否则 composer 不会被调用

---

## 10. 后续 TODO

- 写一个 `serve.sh` 脚本：自动检查 Potree 是否在跑、没跑就 `npm start`
- 写一个 `add_pcd.sh` 一键脚本：传一个 PCD 路径，自动跑完 §3 的 4 步 + 打开浏览器
- 展会 kiosk 模式：浏览器全屏 + 隐藏菜单 + 自动相机环绕动画
- 准备展位 PC 装机一键脚本（含本文档所有依赖）

---

## 11. 参考资料

- Potree 官方：[https://potree.org/](https://potree.org/)
- PotreeConverter：[https://github.com/potree/PotreeConverter](https://github.com/potree/PotreeConverter)
- Potree Web：[https://github.com/potree/potree](https://github.com/potree/potree)
- 经典效果 demo：[https://potree.org/potree/examples/ca13.html](https://potree.org/potree/examples/ca13.html)
- PDAL PCD RGB bug：[https://github.com/PDAL/PDAL/issues/4456](https://github.com/PDAL/PDAL/issues/4456)

---

**首次完整跑通**：2026-04-28 22:45
**关联会议**：[展会模式研发内部讨论 2026-04-28](../../../inbox/) (3D 地图渲染素材工作项)