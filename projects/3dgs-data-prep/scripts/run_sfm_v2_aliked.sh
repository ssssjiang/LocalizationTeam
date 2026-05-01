#!/usr/bin/env bash
# Pure-vision SfM v2 — ALIKED + LightGlue + sequential matcher → COLMAP global_mapper
# Higher recall on weak-texture / repetitive scenes, ~2x slower than SIFT-GPU.
# Note: standalone `glomap` is archived (2026-01); upstream merged into `colmap global_mapper`.
# Output: <DATA>/sparse_global_aliked/0/{cameras,images,points3D}.bin
set -euo pipefail

DATA="${DATA:-/mnt/data/roborock/60采集--长序列_colmap}"
IMAGES="${IMAGES:-$DATA/images}"
DB="${DB:-$DATA/colmap_aliked.db}"
OUT="${OUT:-$DATA/sparse_global_aliked}"

CAM_MODEL="${CAM_MODEL:-PINHOLE}"
CAM_PARAMS="${CAM_PARAMS:-241.984,241.984,339.823,275.645}"

# ALIKED knobs (N32 = larger ONNX model, better; N16ROT adds rotation invariance)
ALIKED_TYPE="${ALIKED_TYPE:-ALIKED_N32}"
MAX_FEATURES="${MAX_FEATURES:-4096}"
ALIKED_MIN_SCORE="${ALIKED_MIN_SCORE:-0.2}"

# Matcher (LightGlue is the headline pairing for ALIKED)
LG_MIN_SCORE="${LG_MIN_SCORE:-0.1}"

# Sequential matcher knobs
OVERLAP="${OVERLAP:-20}"
LOOP_PERIOD="${LOOP_PERIOD:-10}"
LOOP_NUM_IMAGES="${LOOP_NUM_IMAGES:-50}"

# Vocab tree: COLMAP 3.12+ uses FAISS format (legacy FLANN files crash). Empty = let COLMAP
# auto-download to ~/.cache/colmap/ on first run. Override VOCAB to pin a local FAISS file.
VOCAB="${VOCAB:-}"

# global_mapper knobs (post-merge GLOMAP)
BA_ITERS="${BA_ITERS:-6}"
MIN_VIEW_PER_TRACK="${MIN_VIEW_PER_TRACK:-4}"
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

log "1/3 feature_extractor ($ALIKED_TYPE, max_num_features=$MAX_FEATURES)"
"$COLMAP" feature_extractor \
  --database_path "$DB" \
  --image_path "$IMAGES" \
  --FeatureExtraction.type "$ALIKED_TYPE" \
  --FeatureExtraction.use_gpu 1 \
  --ImageReader.camera_model "$CAM_MODEL" \
  --ImageReader.single_camera 1 \
  --ImageReader.camera_params "$CAM_PARAMS" \
  --AlikedExtraction.max_num_features "$MAX_FEATURES" \
  --AlikedExtraction.min_score "$ALIKED_MIN_SCORE"

log "2/3 sequential_matcher (ALIKED_LIGHTGLUE, lg_min_score=$LG_MIN_SCORE, overlap=$OVERLAP + loop)"
SEQ_VOCAB_FLAG=()
[ -n "$VOCAB" ] && SEQ_VOCAB_FLAG=(--SequentialMatching.vocab_tree_path "$VOCAB")
COMPUTE_RELATIVE_POSE="${COMPUTE_RELATIVE_POSE:-1}"
"$COLMAP" sequential_matcher \
  --database_path "$DB" \
  --FeatureMatching.type ALIKED_LIGHTGLUE \
  --FeatureMatching.use_gpu 1 \
  --AlikedMatching.lightglue_min_score "$LG_MIN_SCORE" \
  --TwoViewGeometry.compute_relative_pose "$COMPUTE_RELATIVE_POSE" \
  --SequentialMatching.overlap "$OVERLAP" \
  --SequentialMatching.quadratic_overlap 1 \
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
