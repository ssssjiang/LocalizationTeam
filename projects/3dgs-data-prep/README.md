# 3DGS data prep — SLAM → COLMAP text

Convert Roborock long-sequence SLAM exports (NV12 images + TUM `pose.txt` in lidar body frame + RGB PCD) into **COLMAP text** layout for [3D Gaussian Splatting](https://github.com/graphdeco-inria/gaussian-splatting) training.

## 1. Input layout

```
<input>/
├── pose.txt                          # TUM: ts tx ty tz qx qy qz qw (lidar body → world)
├── 0.01_downsample_rgb_0.01.pcd      # colored point map (binary PCD)
└── camera/
    ├── camera0/                      # default camera (NV12, 640×544)
    │   ├── 990123.yuv                # filename = timestamp in ms (extension optional)
    │   └── ...
    └── camera1/                      # optional (not exported by default)
```

CLI flags can override defaults if your tree differs.

## 2. Requirements

- Python ≥ 3.9
- `numpy`, `Pillow` (`pip install numpy pillow`)
- (Optional, for downstream SfM) COLMAP / GLOMAP — see §5.

## 3. Quick start: data conversion

### 3.1 Command

Default 7× downsample (recommended for typical sequences):

```bash
cd /path/to/LocalizationTeam/projects/3dgs-data-prep

python3 slam_to_colmap.py \
  --input /mnt/data/roborock/60采集--长序列/ \
  --output /mnt/data/roborock/60采集--长序列_colmap_ds7/ \
  --downsample 7 \
  --max-pcd-points 100000 \
  --tolerance-ms 20
```

### 3.2 CLI options

| Flag                   | Default                        | Description                                  |
| ---------------------- | ------------------------------ | -------------------------------------------- |
| `--input`              | (required)                     | Dataset root                                 |
| `--output`             | (required)                     | COLMAP-style output root                     |
| `--downsample`         | `20`                           | Keep every N-th matched frame (recommend 7)  |
| `--max-pcd-points`     | `100000`                       | Random subsample cap for `points3D.txt`      |
| `--tolerance-ms`       | `20`                           | Max \|t_pose − t_image\| when matching pose  |
| `--cam-subdir`         | `camera/camera0`               | Relative path to NV12 frames                 |
| `--pose-file`          | `pose.txt`                     | Relative path to TUM poses                   |
| `--pcd-file`           | `0.01_downsample_rgb_0.01.pcd` | Relative path to PCD                         |
| `--width` / `--height` | `640` / `544`                  | NV12 resolution                              |
| `--jobs`               | CPU count                      | Decoder worker processes                     |

### 3.3 Output layout

```
<output>/
├── images/
│   └── <ms>.png                      # decoded from NV12 (filename = timestamp ms)
└── sparse/0/
    ├── cameras.txt                   # PINHOLE intrinsics
    ├── images.txt                    # world → camera pose (qw qx qy qz tx ty tz)
    └── points3D.txt                  # XYZ + RGB sampled from PCD (no TRACK)
```

### 3.4 Coordinate conventions

- `pose.txt` (input): TUM order **`qx qy qz qw`**; pose is **lidar body → world** (`p_world = R · p_lidar + t`).
- `images.txt` (output): COLMAP order **`qw qx qy qz`**; pose is **world → camera** (`p_cam = R · p_world + t`).
- Script applies: `T_w2c = T_cam_lidar · inv(T_world_lidar)`.

### 3.5 Verification (data conversion)

```bash
DATA=/mnt/data/roborock/60采集--长序列_colmap_ds7

# image count vs sparse/0/images.txt frame count (should match)
ls "$DATA/images" | wc -l
awk 'NR>4 && NR%2==1 {n++} END {print n}' "$DATA/sparse/0/images.txt"

# spot-check a frame is decodable + non-empty pose row
file "$DATA/images/$(ls "$DATA/images" | head -1)"
sed -n '4,6p' "$DATA/sparse/0/images.txt"

# points3D.txt non-empty
wc -l "$DATA/sparse/0/points3D.txt"
```

## 4. Notes

- **Single camera (cam0) only**, single PINHOLE entry in `cameras.txt`.
- **Intrinsics + extrinsics are hardcoded in `slam_to_colmap.py`** — `DEFAULT_INTRINSICS`, `_RCL_FLAT` (rotation, lidar→camera), `_PCL` (translation), and the convenience builder `default_T_cam_lidar()`. Edit those constants if you switch rigs/calibrations.
- **Extrinsics last updated 2026-05-06** (refined `_RCL_FLAT` from fast-livo bring-up). Old values are kept as a comment in the source for diff/rollback.
- `points3D.txt` carries XYZ + RGB only; `TRACK` is empty (3DGS init does not need it).
- Frames whose pose timestamp does not fall within `--tolerance-ms` of any image timestamp are dropped (count is logged).

## 5. Optional: Build COLMAP + GLOMAP (CUDA → `~/local`)

Source-build script: [scripts/install_colmap_glomap_cuda.sh](scripts/install_colmap_glomap_cuda.sh).

Two things must be right before invoking it:

1. `nvcc` must come from CUDA 12.x (not the apt `/usr/bin/nvcc` that ships an older toolchain — that mis-detects Ada `sm_89`):

   ```bash
   export CUDA_HOME=/usr/local/cuda-12.8
   export PATH="$HOME/local/bin:$CUDA_HOME/bin:$PATH"
   ```

2. apt deps installed (one-time, sudo):

   ```bash
   sudo apt-get install -y \
     git build-essential ninja-build gcc-11 g++-11 \
     libeigen3-dev libopenimageio-dev openimageio-tools libfreeimage-dev libflann-dev \
     libmetis-dev libcgal-dev libglew-dev liblz4-dev \
     libqt5opengl5-dev libqt5svg5-dev qtbase5-dev qt5-qmake \
     libgflags-dev libopenblas-dev libsqlite3-dev libsuitesparse-dev
   ```

   Notes on common traps: `libopenimageio-dev` requires `openimageio-tools` (provides `iconvert`) or CMake configure fails; GUI/ONNX paths require `libqt5svg5-dev`.

Then build (parallel jobs default to 8, override with `JOBS=`):

```bash
cd projects/3dgs-data-prep
SKIP_CERES=1 bash scripts/install_colmap_glomap_cuda.sh
# or one-shot with apt: RUN_APT=1 SKIP_CERES=1 bash scripts/install_colmap_glomap_cuda.sh
```

Verify:

```bash
which nvcc && nvcc --version
which colmap && colmap -h | head -3
which glomap && glomap -h | head -3   # standalone glomap is archived; prefer `colmap global_mapper`
```

## 6. Optional: Pure-vision SfM pipelines

> Standalone GLOMAP (the repo) was archived 2026-01-30; its algorithm is now upstream as `colmap global_mapper`. Don't run the legacy `glomap` binary against COLMAP-4.x DBs — schema and API have diverged.

Two end-to-end pipelines are kept (both call `slam_to_colmap.py` + COLMAP `mapper`, with safe init-pair selection to avoid degenerate-init SIGFPEs):

| Script | Extractor + Matcher | When to use |
|---|---|---|
| [scripts/pipeline_ds5_colmap_mapper.sh](scripts/pipeline_ds5_colmap_mapper.sh) | SIFT-GPU + sequential matcher (vocab-tree loop) | Default; fastest on RTX 4070 (~3-6 min for 400 frames). |
| [scripts/run_sfm_v3_aliked_mapper.sh](scripts/run_sfm_v3_aliked_mapper.sh) | ALIKED N32 + LightGlue + sequential matcher | Weak-texture / repetitive scenes. ~2× slower; loop_detection must stay off (vocab tree is SIFT-typed). |

Common usage (env vars override defaults; full knobs in each script header):

```bash
DATA=/mnt/data/roborock/60采集--长序列_colmap_ds7 \
SKIP_SAMPLING=1 CLEAN_DB=1 CLEAN_SPARSE=1 \
bash scripts/pipeline_ds5_colmap_mapper.sh
```

Known traps documented per-script in their headers:
- COLMAP ≥ 3.12 switched to **FAISS** vocab; legacy FLANN files (e.g. `vocab_tree_flickr100K_words32K.bin`) crash on load. Let COLMAP auto-download to `~/.cache/colmap/`, or pin a local `vocab_tree_faiss_*` file via `VOCAB=`.
- `--FeatureMatching.guided_matching` is **not supported by LightGlue**; the ALIKED pipeline keeps it off.

## 7. SfM-side verification

Once a sparse model exists at `<DATA>/sparse_*/0/`:

```bash
# Programmatic format check (segfaults on some COLMAP builds if output dir missing — pre-create it)
mkdir -p <DATA>/sparse_bin/0
~/local/bin/colmap model_converter \
  --input_path <DATA>/sparse_*/0 \
  --output_path <DATA>/sparse_bin/0 \
  --output_type BIN

# Visual sanity (trajectory + cameras + points)
~/local/bin/colmap gui \
  --import_path <DATA>/sparse_*/0 \
  --image_path  <DATA>/images
```
