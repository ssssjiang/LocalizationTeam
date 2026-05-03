#!/usr/bin/env bash
# One-command pipeline:
# raw dataset -> downsample=5 export -> ALIKED+LightGlue matching -> COLMAP global_mapper
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLAM_SCRIPT="$ROOT/slam_to_colmap.py"
COLMAP_BIN="${COLMAP_BIN:-$HOME/local/bin/colmap}"

# Input/output
RAW_INPUT="${RAW_INPUT:-/mnt/data/roborock/60采集--长序列/}"
DATA="${DATA:-/mnt/data/roborock/60采集--长序列_colmap_ds5/}"

# Step-1 sampling/export
DOWNSAMPLE="${DOWNSAMPLE:-5}"
TOL_MS="${TOL_MS:-20}"
MAX_PCD_POINTS="${MAX_PCD_POINTS:-100000}"

# Paths inside DATA
IMAGES="${IMAGES:-$DATA/images}"
DB="${DB:-$DATA/colmap_aliked.db}"
OUT="${OUT:-$DATA/sparse_global_aliked}"
VOCAB="${VOCAB:-$HOME/.cache/colmap/vocab_tree_faiss_flickr100K_words32K.bin}"

# Camera model (fixed calibrated pinhole)
CAM_MODEL="${CAM_MODEL:-PINHOLE}"
CAM_PARAMS="${CAM_PARAMS:-241.984,241.984,339.823,275.645}"

# ALIKED + LightGlue
ALIKED_TYPE="${ALIKED_TYPE:-ALIKED_N32}"
MAX_FEATURES="${MAX_FEATURES:-4096}"
ALIKED_MIN_SCORE="${ALIKED_MIN_SCORE:-0.15}"
LG_MIN_SCORE="${LG_MIN_SCORE:-0.1}"

# Matching strategy
OVERLAP="${OVERLAP:-30}"
QUADRATIC_OVERLAP="${QUADRATIC_OVERLAP:-1}"
GUIDED_MATCHING="${GUIDED_MATCHING:-1}"
LOOP_DETECTION="${LOOP_DETECTION:-1}"
LOOP_PERIOD="${LOOP_PERIOD:-5}"
LOOP_NUM_IMAGES="${LOOP_NUM_IMAGES:-50}"

# Two-view geometry verification
TVG_MIN_INLIERS="${TVG_MIN_INLIERS:-15}"
TVG_MIN_INLIER_RATIO="${TVG_MIN_INLIER_RATIO:-0.25}"

# global_mapper knobs
BA_ITERS="${BA_ITERS:-8}"
MIN_VIEW_PER_TRACK="${MIN_VIEW_PER_TRACK:-4}"
REFINE_FOCAL="${REFINE_FOCAL:-0}"
REFINE_EXTRA="${REFINE_EXTRA:-0}"

# Controls
SKIP_EXPORT="${SKIP_EXPORT:-0}"
CLEAN_DB="${CLEAN_DB:-1}"
CLEAN_OUT="${CLEAN_OUT:-1}"

log() { printf '\n=== %s ===\n' "$*"; }
die() { echo "ERROR: $*" >&2; exit 1; }

[ -x "$COLMAP_BIN" ] || die "COLMAP binary not found: $COLMAP_BIN"
[ -f "$SLAM_SCRIPT" ] || die "slam_to_colmap.py not found: $SLAM_SCRIPT"
[ -d "$RAW_INPUT" ] || die "raw input not found: $RAW_INPUT"

mkdir -p "$DATA" "$OUT"

if [ "$SKIP_EXPORT" != "1" ]; then
  log "1/4 Export ds=$DOWNSAMPLE from raw"
  python3 "$SLAM_SCRIPT" \
    --input "$RAW_INPUT" \
    --output "$DATA" \
    --downsample "$DOWNSAMPLE" \
    --max-pcd-points "$MAX_PCD_POINTS" \
    --tolerance-ms "$TOL_MS"
else
  log "1/4 Export skipped (SKIP_EXPORT=1)"
fi

[ -d "$IMAGES" ] || die "images dir not found: $IMAGES"

if [ "$CLEAN_DB" = "1" ]; then
  log "Reset DB: $DB"
  rm -f "$DB"
fi
if [ "$CLEAN_OUT" = "1" ]; then
  log "Reset output: $OUT"
  rm -rf "$OUT"
  mkdir -p "$OUT"
fi

log "2/4 feature_extractor (ALIKED)"
"$COLMAP_BIN" feature_extractor \
  --database_path "$DB" \
  --image_path "$IMAGES" \
  --FeatureExtraction.type "$ALIKED_TYPE" \
  --FeatureExtraction.use_gpu 1 \
  --ImageReader.camera_model "$CAM_MODEL" \
  --ImageReader.single_camera 1 \
  --ImageReader.camera_params "$CAM_PARAMS" \
  --AlikedExtraction.max_num_features "$MAX_FEATURES" \
  --AlikedExtraction.min_score "$ALIKED_MIN_SCORE"

log "3/4 sequential_matcher (ALIKED_LIGHTGLUE)"
MATCH_ARGS=(
  --database_path "$DB"
  --FeatureMatching.type ALIKED_LIGHTGLUE
  --FeatureMatching.use_gpu 1
  --FeatureMatching.guided_matching "$GUIDED_MATCHING"
  --AlikedMatching.lightglue_min_score "$LG_MIN_SCORE"
  --TwoViewGeometry.compute_relative_pose 1
  --TwoViewGeometry.min_num_inliers "$TVG_MIN_INLIERS"
  --TwoViewGeometry.min_inlier_ratio "$TVG_MIN_INLIER_RATIO"
  --SequentialMatching.overlap "$OVERLAP"
  --SequentialMatching.quadratic_overlap "$QUADRATIC_OVERLAP"
  --SequentialMatching.loop_detection "$LOOP_DETECTION"
)

if [ "$LOOP_DETECTION" = "1" ]; then
  if [ -f "$VOCAB" ]; then
    MATCH_ARGS+=(
      --SequentialMatching.vocab_tree_path "$VOCAB"
      --SequentialMatching.loop_detection_period "$LOOP_PERIOD"
      --SequentialMatching.loop_detection_num_images "$LOOP_NUM_IMAGES"
    )
  else
    echo "WARN: vocab tree not found: $VOCAB ; disable loop detection for this run." >&2
    MATCH_ARGS+=(--SequentialMatching.loop_detection 0)
  fi
fi

"$COLMAP_BIN" sequential_matcher "${MATCH_ARGS[@]}"

log "4/4 global_mapper"
"$COLMAP_BIN" global_mapper \
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

echo
echo "DONE"
echo "  DATA: $DATA"
echo "  DB  : $DB"
echo "  OUT : $OUT/0"
echo
echo "Analyze:"
echo "  $COLMAP_BIN model_analyzer --path \"$OUT/0\""
echo
echo "View:"
echo "  $COLMAP_BIN gui --database_path \"$DB\" --import_path \"$OUT/0\" --image_path \"$IMAGES\""
