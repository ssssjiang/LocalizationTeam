#!/usr/bin/env bash
# End-to-end pipeline for ds5 + standalone glomap mapper
# 1) Sample images by slam_to_colmap.py (downsample=5 by default)
# 2) COLMAP feature extraction + sequential matching (SIFT)
# 3) GLOMAP mapper
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLAM_SCRIPT="$ROOT/slam_to_colmap.py"
COLMAP_BIN="${COLMAP_BIN:-$HOME/local/bin/colmap}"
GLOMAP_BIN="${GLOMAP_BIN:-$HOME/local/bin/glomap}"

INPUT_RAW="${INPUT_RAW:-/mnt/data/roborock/60采集--长序列/}"
OUTPUT_DATA="${OUTPUT_DATA:-/mnt/data/roborock/60采集--长序列_colmap_ds5/}"

DOWNSAMPLE="${DOWNSAMPLE:-5}"
TOL_MS="${TOL_MS:-20}"
MAX_PCD_POINTS="${MAX_PCD_POINTS:-100000}"

DB="${DB:-$OUTPUT_DATA/colmap_glomap.db}"
OUT="${OUT:-$OUTPUT_DATA/sparse_glomap_legacy}"
IMAGES_DIR="$OUTPUT_DATA/images"
VOCAB="${VOCAB:-$HOME/.cache/colmap/vocab_tree_faiss_flickr100K_words32K.bin}"

CAM_MODEL="${CAM_MODEL:-PINHOLE}"
CAM_PARAMS="${CAM_PARAMS:-241.984,241.984,339.823,275.645}"

MAX_FEATURES="${MAX_FEATURES:-8192}"
PEAK_THRESHOLD="${PEAK_THRESHOLD:-0.0067}"
OVERLAP="${OVERLAP:-20}"
QUADRATIC_OVERLAP="${QUADRATIC_OVERLAP:-1}"
GUIDED_MATCHING="${GUIDED_MATCHING:-1}"
SIFT_MAX_RATIO="${SIFT_MAX_RATIO:-0.8}"
LOOP_DETECTION="${LOOP_DETECTION:-1}"
LOOP_PERIOD="${LOOP_PERIOD:-10}"
LOOP_NUM_IMAGES="${LOOP_NUM_IMAGES:-50}"
TVG_MIN_INLIERS="${TVG_MIN_INLIERS:-15}"
TVG_MIN_INLIER_RATIO="${TVG_MIN_INLIER_RATIO:-0.25}"

# GLOMAP knobs
BA_ITERS="${BA_ITERS:-6}"
RETRI_ITERS="${RETRI_ITERS:-2}"
MIN_VIEW_PER_TRACK="${MIN_VIEW_PER_TRACK:-4}"
OPTIMIZE_INTRINSICS="${OPTIMIZE_INTRINSICS:-0}"

SKIP_SAMPLING="${SKIP_SAMPLING:-0}"
SKIP_FEATURES="${SKIP_FEATURES:-0}"
SKIP_MATCHING="${SKIP_MATCHING:-0}"
CLEAN_DB="${CLEAN_DB:-0}"
CLEAN_OUT="${CLEAN_OUT:-0}"

log(){ printf '\n=== %s ===\n' "$*"; }
die(){ echo "ERROR: $*" >&2; exit 1; }

[ -x "$COLMAP_BIN" ] || die "COLMAP binary not found: $COLMAP_BIN"
[ -x "$GLOMAP_BIN" ] || die "GLOMAP binary not found: $GLOMAP_BIN"
[ -f "$SLAM_SCRIPT" ] || die "slam_to_colmap.py not found: $SLAM_SCRIPT"
[ -d "$INPUT_RAW" ] || die "input raw dir not found: $INPUT_RAW"

mkdir -p "$OUTPUT_DATA" "$OUT"

if [ "$CLEAN_DB" = "1" ]; then
  log "Cleaning DB: $DB"
  rm -f "$DB"
fi
if [ "$CLEAN_OUT" = "1" ]; then
  log "Cleaning output: $OUT"
  rm -rf "$OUT"
  mkdir -p "$OUT"
fi

if [ "$SKIP_SAMPLING" != "1" ]; then
  log "1/4 Sampling + COLMAP text export (downsample=$DOWNSAMPLE)"
  python3 "$SLAM_SCRIPT" \
    --input "$INPUT_RAW" \
    --output "$OUTPUT_DATA" \
    --downsample "$DOWNSAMPLE" \
    --max-pcd-points "$MAX_PCD_POINTS" \
    --tolerance-ms "$TOL_MS"
else
  log "1/4 Sampling skipped (SKIP_SAMPLING=1)"
fi

[ -d "$IMAGES_DIR" ] || die "images dir not found: $IMAGES_DIR"

if [ "$SKIP_FEATURES" != "1" ]; then
  log "2/4 COLMAP feature_extractor (SIFT)"
  "$COLMAP_BIN" feature_extractor \
    --database_path "$DB" \
    --image_path "$IMAGES_DIR" \
    --FeatureExtraction.type SIFT \
    --FeatureExtraction.use_gpu 1 \
    --ImageReader.camera_model "$CAM_MODEL" \
    --ImageReader.single_camera 1 \
    --ImageReader.camera_params "$CAM_PARAMS" \
    --SiftExtraction.max_num_features "$MAX_FEATURES" \
    --SiftExtraction.peak_threshold "$PEAK_THRESHOLD"
else
  log "2/4 feature_extractor skipped (SKIP_FEATURES=1)"
fi

if [ "$SKIP_MATCHING" != "1" ]; then
  log "3/4 COLMAP sequential_matcher"
  MATCH_ARGS=(
    --database_path "$DB"
    --FeatureMatching.type SIFT_BRUTEFORCE
    --FeatureMatching.use_gpu 1
    --FeatureMatching.guided_matching "$GUIDED_MATCHING"
    --SiftMatching.max_ratio "$SIFT_MAX_RATIO"
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
      echo "WARN: vocab tree not found: $VOCAB; disabling loop detection for this run" >&2
      MATCH_ARGS+=(--SequentialMatching.loop_detection 0)
    fi
  fi

  "$COLMAP_BIN" sequential_matcher "${MATCH_ARGS[@]}"
else
  log "3/4 sequential_matcher skipped (SKIP_MATCHING=1)"
fi

log "4/4 GLOMAP mapper"
set +e
"$GLOMAP_BIN" mapper \
  --database_path "$DB" \
  --image_path "$IMAGES_DIR" \
  --output_path "$OUT" \
  --output_format bin \
  --ba_iteration_num "$BA_ITERS" \
  --retriangulation_iteration_num "$RETRI_ITERS" \
  --TrackEstablishment.min_num_view_per_track "$MIN_VIEW_PER_TRACK" \
  --BundleAdjustment.optimize_intrinsics "$OPTIMIZE_INTRINSICS" \
  --BundleAdjustment.optimize_principal_point 0 \
  --BundleAdjustment.use_gpu 1 \
  --GlobalPositioning.use_gpu 1
rc=$?
set -e

if [ $rc -ne 0 ]; then
  cat <<'MSG' >&2
GLOMAP mapper failed.
If error contains `SQLite error: SQL logic error`, this is usually a COLMAP/GLOMAP schema mismatch.
Use COLMAP global_mapper pipeline instead:
  scripts/pipeline_ds5_colmap_mapper.sh
MSG
  exit $rc
fi

echo
ls -lh "$OUT"/0/ 2>/dev/null || true
echo
echo "Analyze: $COLMAP_BIN model_analyzer --path \"$OUT/0\""
echo "View   : $COLMAP_BIN gui --database_path \"$DB\" --import_path \"$OUT/0\" --image_path \"$IMAGES_DIR\""
