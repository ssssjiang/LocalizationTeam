#!/usr/bin/env bash
# Pure-vision SfM v1 — SIFT-GPU + sequential matcher (+ vocab-tree loop) → COLMAP global_mapper
# Optimized for: PINHOLE-rectified single camera, ~hundreds of sequential frames, RTX 4070.
# Note: standalone `glomap` is archived (2026-01); upstream merged into `colmap global_mapper`.
# Output: <DATA>/sparse_global_sift/0/{cameras,images,points3D}.bin
set -euo pipefail

DATA="${DATA:-/mnt/data/roborock/60采集--长序列_colmap}"
IMAGES="${IMAGES:-$DATA/images}"
DB="${DB:-$DATA/colmap_sift.db}"
OUT="${OUT:-$DATA/sparse_global_sift}"

# Camera intrinsics (must match images/). Override via env if needed.
CAM_MODEL="${CAM_MODEL:-PINHOLE}"
CAM_PARAMS="${CAM_PARAMS:-241.984,241.984,339.823,275.645}"

# SIFT-GPU knobs (defaults are good for 640x544 rectified frames)
MAX_FEATURES="${MAX_FEATURES:-8192}"
PEAK_THRESHOLD="${PEAK_THRESHOLD:-0.0067}"

# Sequential matcher knobs
OVERLAP="${OVERLAP:-20}"
QUADRATIC_OVERLAP="${QUADRATIC_OVERLAP:-1}"
LOOP_PERIOD="${LOOP_PERIOD:-10}"
LOOP_NUM_IMAGES="${LOOP_NUM_IMAGES:-50}"
# Two-view geometric verification thresholds (tighten to drop bad pairs)
TVG_MIN_INLIERS="${TVG_MIN_INLIERS:-15}"
TVG_MIN_INLIER_RATIO="${TVG_MIN_INLIER_RATIO:-0.25}"
# SIFT matching knobs (loose ratio + guided second pass help recall)
SIFT_MAX_RATIO="${SIFT_MAX_RATIO:-0.8}"
GUIDED_MATCHING="${GUIDED_MATCHING:-0}"
# Two-view geometry: with known intrinsics, prefer Essential-matrix path (5-pt) over Fundamental (7-pt).
# 7-pt cubic root finder can hit SIGFPE on degenerate samples when matches are noisy.
COMPUTE_RELATIVE_POSE="${COMPUTE_RELATIVE_POSE:-1}"

# Vocab tree: COLMAP 3.12+ uses FAISS format (legacy FLANN files crash). Empty = let COLMAP
# auto-download to ~/.cache/colmap/ on first run. Override VOCAB to pin a local FAISS file.
VOCAB="${VOCAB:-}"

# global_mapper knobs (post-merge GLOMAP)
BA_ITERS="${BA_ITERS:-6}"
MIN_VIEW_PER_TRACK="${MIN_VIEW_PER_TRACK:-4}"
# Refine intrinsics? 0 = keep your given fx,fy,cx,cy (recommended when calibration is trusted)
REFINE_FOCAL="${REFINE_FOCAL:-0}"
REFINE_EXTRA="${REFINE_EXTRA:-0}"

COLMAP="${COLMAP:-$HOME/local/bin/colmap}"

log() { printf '\n=== %s ===\n' "$*"; }

[ -d "$IMAGES" ] || { echo "ERROR: IMAGES not found: $IMAGES"; exit 1; }
[ -x "$COLMAP" ] || { echo "ERROR: colmap not found: $COLMAP"; exit 1; }

mkdir -p "$OUT"

if [ -f "$DB" ]; then
  echo "WARN: $DB exists; reusing. Delete it for a clean rebuild."
fi

log "1/3 feature_extractor (SIFT-GPU, single PINHOLE camera)"
"$COLMAP" feature_extractor \
  --database_path "$DB" \
  --image_path "$IMAGES" \
  --FeatureExtraction.type SIFT \
  --FeatureExtraction.use_gpu 1 \
  --ImageReader.camera_model "$CAM_MODEL" \
  --ImageReader.single_camera 1 \
  --ImageReader.camera_params "$CAM_PARAMS" \
  --SiftExtraction.max_num_features "$MAX_FEATURES" \
  --SiftExtraction.peak_threshold "$PEAK_THRESHOLD" \
  --SiftExtraction.estimate_affine_shape 0 \
  --SiftExtraction.domain_size_pooling 0

log "2/3 sequential_matcher (overlap=$OVERLAP + quadratic + vocab-tree loop)"
SEQ_VOCAB_FLAG=()
[ -n "$VOCAB" ] && SEQ_VOCAB_FLAG=(--SequentialMatching.vocab_tree_path "$VOCAB")
"$COLMAP" sequential_matcher \
  --database_path "$DB" \
  --FeatureMatching.type SIFT_BRUTEFORCE \
  --FeatureMatching.use_gpu 1 \
  --FeatureMatching.guided_matching "$GUIDED_MATCHING" \
  --SiftMatching.max_ratio "$SIFT_MAX_RATIO" \
  --TwoViewGeometry.compute_relative_pose "$COMPUTE_RELATIVE_POSE" \
  --TwoViewGeometry.min_num_inliers "$TVG_MIN_INLIERS" \
  --TwoViewGeometry.min_inlier_ratio "$TVG_MIN_INLIER_RATIO" \
  --SequentialMatching.overlap "$OVERLAP" \
  --SequentialMatching.quadratic_overlap "$QUADRATIC_OVERLAP" \
  --SequentialMatching.loop_detection 1 \
  "${SEQ_VOCAB_FLAG[@]}" \
  --SequentialMatching.loop_detection_period "$LOOP_PERIOD" \
  --SequentialMatching.loop_detection_num_images "$LOOP_NUM_IMAGES"

log "3/3 colmap global_mapper (BA=$BA_ITERS, refine_focal=$REFINE_FOCAL, refine_extra=$REFINE_EXTRA)"
"$COLMAP" global_mapper \
  --database_path "$DB" \
  --image_path "$IMAGES" \
  --output_path "$OUT" \
  --GlobalMapper.ba_num_iterations "$BA_ITERS" \
  --GlobalMapper.track_min_num_views_per_track "$MIN_VIEW_PER_TRACK" \
  --GlobalMapper.ba_refine_focal_length "$REFINE_FOCAL" \
  --GlobalMapper.ba_refine_principal_point 0 \
  --GlobalMapper.ba_refine_extra_params "$REFINE_EXTRA" \
  --GlobalMapper.ba_ceres_use_gpu 1 \
  --GlobalMapper.gp_use_gpu 1

log "done. result: $OUT/0/{cameras,images,points3D}.bin"
ls -lh "$OUT"/0/ 2>/dev/null || echo "(no model output — check log above)"
