# 3DGS data prep — SLAM → COLMAP text

Convert Roborock long-sequence SLAM exports (NV12 images + TUM `pose.txt` in lidar body frame + RGB PCD) into **COLMAP text** layout for [3D Gaussian Splatting](https://github.com/graphdeco-inria/gaussian-splatting) training.

## Expected input layout

```
<input>/
├── pose.txt                          # TUM: ts tx ty tz qx qy qz qw (lidar body → world)
├── 0.01_downsample_rgb_0.01.pcd      # colored point map (binary PCD)
└── camera/
    ├── camera0/                      # default camera (NV12, 640×544)
    │   ├── 990123.yuv               # filename = timestamp in ms (optional extension)
    │   └── ...
    └── camera1/                      # optional (not exported by default)
```

Paths can be overridden with CLI flags if your tree differs.

## Requirements

- Python ≥ 3.9
- `numpy`, `Pillow` (`pip install numpy pillow`)

## Build COLMAP + GLOMAP (CUDA → `~/local`)

源码安装脚本：[scripts/install_colmap_glomap_cuda.sh](scripts/install_colmap_glomap_cuda.sh)。**先保证 `nvcc` 来自 CUDA 12.x**（避免 CMake 误用 apt 装在 `/usr/bin/nvcc` 的旧工具链，导致 Ada `sm_89` 等编译失败）。推荐与 `~/.zshrc` 里已有块一致：

```bash
export CUDA_HOME=/usr/local/cuda-12.8
export PATH="$HOME/local/bin:$CUDA_HOME/bin:$PATH"
```

并行编译默认 **8** 个 job（`cmake --build -j8`）；要改就运行前设环境变量，例如 `JOBS=16 ...`。

**1. 系统依赖（需本机 `sudo` 一次）：**

`libopenimageio-dev` 的 CMake 会检查 CLI 目标 `iconvert`，需同时安装 **`openimageio-tools`**（提供 `/usr/bin/iconvert`），否则配置阶段报错。**启用 GUI / ONNX 等路径时 CMake 会找 Qt5Svg → 需 `libqt5svg5-dev`**。

```bash
sudo apt-get update && sudo apt-get install -y \
  git build-essential ninja-build gcc-11 g++-11 \
  libeigen3-dev libopenimageio-dev openimageio-tools libfreeimage-dev libflann-dev \
  libmetis-dev libcgal-dev libglew-dev liblz4-dev \
  libqt5opengl5-dev libqt5svg5-dev qtbase5-dev qt5-qmake \
  libgflags-dev libopenblas-dev libsqlite3-dev libsuitesparse-dev
```

**2. 编译安装**（依赖装完后；若已装过 Ceres 可加 `SKIP_CERES=1`）：

```bash
cd projects/3dgs-data-prep
chmod +x scripts/install_colmap_glomap_cuda.sh
SKIP_CERES=1 bash scripts/install_colmap_glomap_cuda.sh
```

或一键 `sudo apt` + 编译（终端能接受密码时）：

```bash
RUN_APT=1 SKIP_CERES=1 bash scripts/install_colmap_glomap_cuda.sh
```

**3. 验证：**

```bash
which nvcc && nvcc --version
which colmap && colmap -h | head -3
which glomap && glomap -h | head -3
```

## Pure-vision SfM (COLMAP global_mapper)

> **Important**: standalone GLOMAP repo was archived 2026-01-30; the algorithm is now in COLMAP main as **`colmap global_mapper`**. Don't use the `glomap` binary against a COLMAP-4.x DB — schema and API have diverged (`SQL logic error`, `DatabaseCache::Create` arity, `ceres::FAILURE` enum, etc.).

Two ready-to-run pipelines under `scripts/`. Both default to:

- input  : `/mnt/data/roborock/60采集--长序列_colmap`
- camera : `PINHOLE 241.984 241.984 339.823 275.645` (matches `slam_to_colmap.py`)
- matcher: `sequential` + `quadratic_overlap` + vocab-tree loop detection
- mapper : `colmap global_mapper` (`ba_num_iterations=6`, `ba_refine_focal_length=0`)

| Script | Extractor | Matcher | When to use |
|---|---|---|---|
| [scripts/run_sfm_v1_sift.sh](scripts/run_sfm_v1_sift.sh) | SIFT-GPU | `SIFT_BRUTEFORCE` | Default. Fastest on RTX 4070 (~3-6 min for 400 frames). |
| [scripts/run_sfm_v2_aliked.sh](scripts/run_sfm_v2_aliked.sh) | `ALIKED_N32` | `ALIKED_LIGHTGLUE` | Weak-texture / repetitive scenes (grass, low light). ~2x slower. |

Run with defaults:

```bash
bash scripts/run_sfm_v1_sift.sh         # outputs <DATA>/sparse_global_sift/0/
bash scripts/run_sfm_v2_aliked.sh       # outputs <DATA>/sparse_global_aliked/0/
```

Override anything via env vars, e.g.:

```bash
DATA=/path/to/dataset \
CAM_PARAMS="241.984,241.984,339.823,275.645" \
OVERLAP=30 BA_ITERS=8 REFINE_FOCAL=1 \
bash scripts/run_sfm_v1_sift.sh
```

Verify result with `colmap gui --import_path <DATA>/sparse_global_*/0 --image_path <DATA>/images`.

Both scripts let COLMAP auto-download the **FAISS** vocab tree to `~/.cache/colmap/` on first run (COLMAP ≥ 3.12 switched FLANN→FAISS — legacy `vocab_tree_*words32K.bin` files crash with `Failed to read faiss index`). ALIKED / LightGlue ONNX weights are fetched by COLMAP itself the first time. To pin a local file: `VOCAB=/abs/path/vocab_tree_faiss_flickr100K_words32K.bin bash scripts/...`.

## Usage

```bash
cd /path/to/LocalizationTeam/projects/3dgs-data-prep

python3 slam_to_colmap.py \
  --input /mnt/data/roborock/60采集--长序列/ \
  --output /mnt/data/roborock/60采集--长序列_colmap/ \
  --downsample 20 \
  --max-pcd-points 100000 \
  --tolerance-ms 20
```

### Main options


| Flag                   | Default                        | Description                             |
| ---------------------- | ------------------------------ | --------------------------------------- |
| `--input`              | (required)                     | Dataset root                            |
| `--output`             | (required)                     | COLMAP-style output root                |
| `--downsample`         | `20`                           | Keep every N-th matched frame           |
| `--max-pcd-points`     | `100000`                       | Random subsample cap for `points3D.txt` |
| `--tolerance-ms`       | `20`                           | Max                                     |
| `--cam-subdir`         | `camera/camera0`               | Relative path to NV12 frames            |
| `--pose-file`          | `pose.txt`                     | Relative path to TUM poses              |
| `--pcd-file`           | `0.01_downsample_rgb_0.01.pcd` | Relative path to PCD                    |
| `--width` / `--height` | `640` / `544`                  | NV12 resolution                         |
| `--jobs`               | CPU count                      | Decoder worker processes                |


Intrinsics and `T_cam_lidar` are **hardcoded** in `slam_to_colmap.py` for the calibrated Roborock rig (PINHOLE after rectification). Edit `DEFAULT_INTRINSICS` and `DEFAULT_T_CAM_LIDAR` if you use another calibration.

## Output layout

```
<output>/
├── images/
│   └── <sec_with_6_decimals>.png    # decoded from NV12; name encodes pose-aligned time
└── sparse/0/
    ├── cameras.txt
    ├── images.txt
    └── points3D.txt
```

## Verification (manual)

1. **Counts**
  ```bash
   ls <output>/images | wc -l
   ls <output>/sparse/0
  ```
2. **COLMAP `model_converter`** (if COLMAP is installed)
  ```bash
   mkdir -p <output>/sparse_bin/0
   colmap model_converter \
     --input_path <output>/sparse/0 \
     --output_path <output>/sparse_bin/0 \
     --output_type BIN
  ```
   No error → text model parses. (Some COLMAP builds segfault if the output directory does not exist — create it first.)
3. **GUI sanity** (trajectory + cameras)
  ```bash
   colmap gui --import_path <output>/sparse/0 --image_path <output>/images
  ```

## Coordinate conventions

- `pose.txt`: TUM quaternion order **qx qy qz qw**; pose is **lidar body in world** (`p_world = R * p_lidar + t`).
- COLMAP `images.txt`: **world → camera** (`p_cam = R * p_world + t`), quaternion **qw qx qy qz**.
- Script applies: `T_w2c = T_cam_lidar @ inv(T_world_lidar)`.

## Notes

- Only **cam0** is exported by default (single PINHOLE camera entry).
- `points3D.txt` uses PCD RGB; `TRACK` is omitted (empty). 3DGS uses XYZ + color for initialization.
- Frames without a pose match within `--tolerance-ms` are skipped (logged at end).

