#!/usr/bin/env bash
# End-to-end pipeline:
# 1) Sample frames with slam_to_colmap.py (default downsample=5)
# 2) Build COLMAP incremental SfM with SIFT + sequential matcher
# 3) Analyze models and print GUI command for the best model
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLAM_SCRIPT="$ROOT/slam_to_colmap.py"
COLMAP_BIN="${COLMAP_BIN:-$HOME/local/bin/colmap}"

INPUT_RAW="${INPUT_RAW:-/mnt/data/roborock/60采集--长序列/}"
OUTPUT_DATA="${OUTPUT_DATA:-/mnt/data/roborock/60采集--长序列_colmap_ds5/}"

DOWNSAMPLE="${DOWNSAMPLE:-5}"
TOL_MS="${TOL_MS:-20}"
MAX_PCD_POINTS="${MAX_PCD_POINTS:-100000}"

DB="${DB:-$OUTPUT_DATA/colmap_inc.db}"
SPARSE_DIR="${SPARSE_DIR:-$OUTPUT_DATA/sparse_colmap_inc}"
VOCAB="${VOCAB:-$HOME/.cache/colmap/vocab_tree_faiss_flickr100K_words32K.bin}"

# Known calibrated intrinsics (rectified pinhole)
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

MAPPER_MIN_MODEL_SIZE="${MAPPER_MIN_MODEL_SIZE:-50}"
MAPPER_MULTIPLE_MODELS="${MAPPER_MULTIPLE_MODELS:-0}"
MAPPER_MAX_NUM_MODELS="${MAPPER_MAX_NUM_MODELS:-1}"

SKIP_SAMPLING="${SKIP_SAMPLING:-0}"
SKIP_FEATURES="${SKIP_FEATURES:-0}"
SKIP_MATCHING="${SKIP_MATCHING:-0}"
SKIP_MAPPER="${SKIP_MAPPER:-0}"
CLEAN_DB="${CLEAN_DB:-0}"
CLEAN_SPARSE="${CLEAN_SPARSE:-0}"

log() { printf '\n=== %s ===\n' "$*"; }

die() { echo "ERROR: $*" >&2; exit 1; }

[ -x "$COLMAP_BIN" ] || die "COLMAP binary not found: $COLMAP_BIN"
[ -f "$SLAM_SCRIPT" ] || die "slam_to_colmap.py not found: $SLAM_SCRIPT"
[ -d "$INPUT_RAW" ] || die "input raw dir not found: $INPUT_RAW"

mkdir -p "$OUTPUT_DATA" "$SPARSE_DIR"

if [ "$CLEAN_DB" = "1" ]; then
  log "Cleaning DB: $DB"
  rm -f "$DB"
fi
if [ "$CLEAN_SPARSE" = "1" ]; then
  log "Cleaning sparse dir: $SPARSE_DIR"
  rm -rf "$SPARSE_DIR"
  mkdir -p "$SPARSE_DIR"
fi

if [ "$SKIP_SAMPLING" != "1" ]; then
  log "1/6 Sampling + COLMAP text export (downsample=$DOWNSAMPLE)"
  python3 "$SLAM_SCRIPT" \
    --input "$INPUT_RAW" \
    --output "$OUTPUT_DATA" \
    --downsample "$DOWNSAMPLE" \
    --max-pcd-points "$MAX_PCD_POINTS" \
    --tolerance-ms "$TOL_MS"
else
  log "1/6 Sampling skipped (SKIP_SAMPLING=1)"
fi

IMAGES_DIR="$OUTPUT_DATA/images"
[ -d "$IMAGES_DIR" ] || die "images dir not found: $IMAGES_DIR"

if [ "$SKIP_FEATURES" != "1" ]; then
  log "2/6 COLMAP feature_extractor (SIFT)"
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
  log "2/6 feature_extractor skipped (SKIP_FEATURES=1)"
fi

if [ "$SKIP_MATCHING" != "1" ]; then
  log "3/6 COLMAP sequential_matcher"
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
  log "3/6 sequential_matcher skipped (SKIP_MATCHING=1)"
fi

INIT_PAIR_FILE="$OUTPUT_DATA/.mapper_init_pair.txt"
rm -f "$INIT_PAIR_FILE"

log "4/6 Selecting safe initial image pair from DB"
python3 - "$DB" "$INIT_PAIR_FILE" <<'PY'
import os
import sqlite3
import sys

M = 2147483647

def inv_pair(pid: int):
    i2 = pid % M
    i1 = (pid - i2) // M
    return int(i1), int(i2)

def ts_from_name(name: str):
    base = os.path.basename(name)
    stem = os.path.splitext(base)[0]
    return int(stem) if stem.isdigit() else None

db_path, out_path = sys.argv[1], sys.argv[2]
con = sqlite3.connect(db_path)
cur = con.cursor()
name_by_id = {i: n for i, n in cur.execute("SELECT image_id, name FROM images")}

# Prefer calibrated two-view geometries with enough inliers and moderate temporal gap.
rows = cur.execute(
    """
    SELECT pair_id, rows
    FROM two_view_geometries
    WHERE config = 2 AND rows >= 120
    ORDER BY rows DESC
    LIMIT 2000
    """
).fetchall()

best = None
for pair_id, inliers in rows:
    i1, i2 = inv_pair(pair_id)
    n1, n2 = name_by_id.get(i1), name_by_id.get(i2)
    if not n1 or not n2:
        continue
    t1, t2 = ts_from_name(n1), ts_from_name(n2)
    if t1 is None or t2 is None:
        continue
    gap = abs(t1 - t2)  # ms
    # Avoid too-near (pure rotation risk) and too-far (overlap too small) pairs.
    if 200 <= gap <= 5000:
        best = (i1, i2, inliers, gap, n1, n2)
        break

if best is None:
    print("NO_INIT_PAIR")
else:
    i1, i2, inliers, gap, n1, n2 = best
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"{i1} {i2}\n")
    print(f"INIT_PAIR image_id=({i1},{i2}) inliers={inliers} gap_ms={gap} names=({n1},{n2})")
PY

MAPPER_ARGS=(
  --database_path "$DB"
  --image_path "$IMAGES_DIR"
  --output_path "$SPARSE_DIR"
  --Mapper.multiple_models "$MAPPER_MULTIPLE_MODELS"
  --Mapper.max_num_models "$MAPPER_MAX_NUM_MODELS"
  --Mapper.min_model_size "$MAPPER_MIN_MODEL_SIZE"
  --Mapper.ba_refine_focal_length 0
  --Mapper.ba_refine_principal_point 0
  --Mapper.ba_refine_extra_params 0
)

if [ -f "$INIT_PAIR_FILE" ]; then
  INIT1="$(awk '{print $1}' "$INIT_PAIR_FILE")"
  INIT2="$(awk '{print $2}' "$INIT_PAIR_FILE")"
  MAPPER_ARGS+=(
    --Mapper.init_image_id1 "$INIT1"
    --Mapper.init_image_id2 "$INIT2"
    --Mapper.init_num_trials 1
  )
else
  echo "WARN: No safe init pair found; mapper will auto-select initial pair" >&2
fi

if [ "$SKIP_MAPPER" != "1" ]; then
  log "5/6 COLMAP mapper"
  "$COLMAP_BIN" mapper "${MAPPER_ARGS[@]}"
else
  log "5/6 mapper skipped (SKIP_MAPPER=1)"
fi

log "6/6 Analyze models and pick best"
BEST_MODEL=""
BEST_COUNT=0
for d in "$SPARSE_DIR"/*; do
  [ -d "$d" ] || continue
  cnt="$($COLMAP_BIN model_analyzer --path "$d" 2>/dev/null | awk '/Registered images:/ {print $NF}')"
  cnt="${cnt:-0}"
  printf "model=%s registered_images=%s\n" "$d" "$cnt"
  if [ "$cnt" -gt "$BEST_COUNT" ]; then
    BEST_COUNT="$cnt"
    BEST_MODEL="$d"
  fi
done

if [ -n "$BEST_MODEL" ]; then
  echo
  echo "BEST_MODEL=$BEST_MODEL"
  echo "BEST_REGISTERED_IMAGES=$BEST_COUNT"
  echo
  echo "View command:"
  echo "$COLMAP_BIN gui --database_path \"$DB\" --import_path \"$BEST_MODEL\" --image_path \"$IMAGES_DIR\""
else
  echo "WARN: no model folders under $SPARSE_DIR" >&2
fi
