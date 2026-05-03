#!/usr/bin/env bash
# ALIKED + LightGlue + COLMAP incremental mapper (not global_mapper)
# Designed for ds5 dataset and robust init-pair selection to avoid SIGFPE.
set -euo pipefail

COLMAP_BIN="${COLMAP_BIN:-$HOME/local/bin/colmap}"
DATA="${DATA:-/mnt/data/roborock/60采集--长序列_colmap_ds5}"
IMAGES="${IMAGES:-$DATA/images}"
DB="${DB:-$DATA/colmap_aliked_mapper.db}"
SPARSE="${SPARSE:-$DATA/sparse_aliked_mapper}"
VOCAB="${VOCAB:-$HOME/.cache/colmap/vocab_tree_faiss_flickr100K_words32K.bin}"

CAM_MODEL="${CAM_MODEL:-PINHOLE}"
CAM_PARAMS="${CAM_PARAMS:-241.984,241.984,339.823,275.645}"

ALIKED_TYPE="${ALIKED_TYPE:-ALIKED_N32}"
MAX_FEATURES="${MAX_FEATURES:-4096}"
ALIKED_MIN_SCORE="${ALIKED_MIN_SCORE:-0.15}"
LG_MIN_SCORE="${LG_MIN_SCORE:-0.1}"

OVERLAP="${OVERLAP:-30}"
QUADRATIC_OVERLAP="${QUADRATIC_OVERLAP:-1}"
GUIDED_MATCHING="${GUIDED_MATCHING:-0}"
# NOTE: For ALIKED descriptors, the commonly available vocab trees are SIFT-based,
# which causes feature-type mismatch and crash in vocab retrieval. Keep loop off by default.
LOOP_DETECTION="${LOOP_DETECTION:-0}"
LOOP_PERIOD="${LOOP_PERIOD:-5}"
LOOP_NUM_IMAGES="${LOOP_NUM_IMAGES:-50}"
TVG_MIN_INLIERS="${TVG_MIN_INLIERS:-15}"
TVG_MIN_INLIER_RATIO="${TVG_MIN_INLIER_RATIO:-0.25}"

MAPPER_MIN_MODEL_SIZE="${MAPPER_MIN_MODEL_SIZE:-50}"
MAPPER_MULTIPLE_MODELS="${MAPPER_MULTIPLE_MODELS:-0}"
MAPPER_MAX_NUM_MODELS="${MAPPER_MAX_NUM_MODELS:-1}"

# Init relaxations for forward-motion robot capture
INIT_MIN_NUM_INLIERS="${INIT_MIN_NUM_INLIERS:-50}"
INIT_MAX_ERROR="${INIT_MAX_ERROR:-4}"
INIT_MAX_FORWARD_MOTION="${INIT_MAX_FORWARD_MOTION:-0.98}"
INIT_MIN_TRI_ANGLE="${INIT_MIN_TRI_ANGLE:-4}"
INIT_MAX_REG_TRIALS="${INIT_MAX_REG_TRIALS:-3}"
INIT_GAP_MIN_MS="${INIT_GAP_MIN_MS:-2000}"
INIT_GAP_MAX_MS="${INIT_GAP_MAX_MS:-12000}"

CLEAN_DB="${CLEAN_DB:-1}"
CLEAN_SPARSE="${CLEAN_SPARSE:-1}"
SKIP_FEATURES="${SKIP_FEATURES:-0}"
SKIP_MATCHING="${SKIP_MATCHING:-0}"

log() { printf '\n=== %s ===\n' "$*"; }
die() { echo "ERROR: $*" >&2; exit 1; }

[ -x "$COLMAP_BIN" ] || die "COLMAP not found: $COLMAP_BIN"
[ -d "$IMAGES" ] || die "images dir not found: $IMAGES"
mkdir -p "$SPARSE"

if [ "$CLEAN_DB" = "1" ]; then
  log "Reset DB: $DB"
  rm -f "$DB"
fi
if [ "$CLEAN_SPARSE" = "1" ]; then
  log "Reset sparse dir: $SPARSE"
  rm -rf "$SPARSE"
  mkdir -p "$SPARSE"
fi

if [ "$SKIP_FEATURES" != "1" ]; then
  log "1/3 feature_extractor (ALIKED)"
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
else
  log "1/3 feature_extractor skipped"
fi

if [ "$SKIP_MATCHING" != "1" ]; then
  log "2/3 sequential_matcher (ALIKED_LIGHTGLUE)"
  MATCH_ARGS=(
    --database_path "$DB"
    --FeatureMatching.type ALIKED_LIGHTGLUE
    --FeatureMatching.use_gpu 1
    --AlikedMatching.lightglue_min_score "$LG_MIN_SCORE"
    --TwoViewGeometry.compute_relative_pose 1
    --TwoViewGeometry.min_num_inliers "$TVG_MIN_INLIERS"
    --TwoViewGeometry.min_inlier_ratio "$TVG_MIN_INLIER_RATIO"
    --SequentialMatching.overlap "$OVERLAP"
    --SequentialMatching.quadratic_overlap "$QUADRATIC_OVERLAP"
    --SequentialMatching.loop_detection "$LOOP_DETECTION"
  )

  # LightGlue backend does not support guided matching.
  if [ "$GUIDED_MATCHING" = "1" ]; then
    echo "WARN: guided_matching is not supported for ALIKED_LIGHTGLUE; forcing 0." >&2
  fi
  MATCH_ARGS+=(--FeatureMatching.guided_matching 0)
  if [ "$LOOP_DETECTION" = "1" ]; then
    if [ -f "$VOCAB" ] && [[ "$ALIKED_TYPE" == SIFT* ]]; then
      MATCH_ARGS+=(
        --SequentialMatching.vocab_tree_path "$VOCAB"
        --SequentialMatching.loop_detection_period "$LOOP_PERIOD"
        --SequentialMatching.loop_detection_num_images "$LOOP_NUM_IMAGES"
      )
    else
      echo "WARN: loop_detection requires a feature-type-matched vocab tree." >&2
      echo "WARN: ALIKED with SIFT vocab will crash; disable loop for this run." >&2
      MATCH_ARGS+=(--SequentialMatching.loop_detection 0)
    fi
  fi
  "$COLMAP_BIN" sequential_matcher "${MATCH_ARGS[@]}"
else
  log "2/3 sequential_matcher skipped"
fi

log "3/3 mapper with safe init pair"
INIT_PAIR_FILE="$DATA/.mapper_init_pair_aliked.txt"
rm -f "$INIT_PAIR_FILE"
python3 - "$DB" "$INIT_PAIR_FILE" "$INIT_GAP_MIN_MS" "$INIT_GAP_MAX_MS" <<'PY'
import os, sqlite3, sys
M = 2147483647
def inv_pair(pid: int):
    i2 = pid % M
    i1 = (pid - i2) // M
    return int(i1), int(i2)
def ts(name: str):
    s = os.path.splitext(os.path.basename(name))[0]
    return int(s) if s.isdigit() else None
db = sqlite3.connect(sys.argv[1]); out = sys.argv[2]
gap_min = int(sys.argv[3]); gap_max = int(sys.argv[4])
cur = db.cursor()
name = {i: n for i, n in cur.execute("SELECT image_id,name FROM images")}
rows = cur.execute("""
  SELECT pair_id, rows
  FROM two_view_geometries
  WHERE config=2 AND rows>=80
  ORDER BY rows DESC
  LIMIT 2000
""").fetchall()
for pid, inl in rows:
    i1, i2 = inv_pair(pid)
    n1, n2 = name.get(i1), name.get(i2)
    if not n1 or not n2:
        continue
    t1, t2 = ts(n1), ts(n2)
    if t1 is None or t2 is None:
        continue
    gap = abs(t1 - t2)
    if gap_min <= gap <= gap_max:
        with open(out, "w", encoding="utf-8") as f:
            f.write(f"{i1} {i2}\n")
        print(f"INIT_PAIR ({i1},{i2}) inliers={inl} gap_ms={gap} {n1} {n2}")
        break
else:
    print("NO_INIT_PAIR")
PY

MAPPER_ARGS=(
  --database_path "$DB"
  --image_path "$IMAGES"
  --output_path "$SPARSE"
  --Mapper.multiple_models "$MAPPER_MULTIPLE_MODELS"
  --Mapper.max_num_models "$MAPPER_MAX_NUM_MODELS"
  --Mapper.min_model_size "$MAPPER_MIN_MODEL_SIZE"
  --Mapper.ba_refine_focal_length 0
  --Mapper.ba_refine_principal_point 0
  --Mapper.ba_refine_extra_params 0
  --Mapper.init_min_num_inliers "$INIT_MIN_NUM_INLIERS"
  --Mapper.init_max_error "$INIT_MAX_ERROR"
  --Mapper.init_max_forward_motion "$INIT_MAX_FORWARD_MOTION"
  --Mapper.init_min_tri_angle "$INIT_MIN_TRI_ANGLE"
  --Mapper.init_max_reg_trials "$INIT_MAX_REG_TRIALS"
)

if [ -f "$INIT_PAIR_FILE" ]; then
  INIT1="$(awk '{print $1}' "$INIT_PAIR_FILE")"
  INIT2="$(awk '{print $2}' "$INIT_PAIR_FILE")"
  MAPPER_ARGS+=(--Mapper.init_image_id1 "$INIT1" --Mapper.init_image_id2 "$INIT2" --Mapper.init_num_trials 1)
else
  echo "WARN: safe init pair not found; mapper auto init (may be unstable)." >&2
fi

"$COLMAP_BIN" mapper "${MAPPER_ARGS[@]}"

BEST_MODEL=""
BEST_COUNT=0
for d in "$SPARSE"/*; do
  [ -d "$d" ] || continue
  cnt="$("$COLMAP_BIN" model_analyzer --path "$d" 2>/dev/null | awk '/Registered images:/ {print $NF}')"
  cnt="${cnt:-0}"
  printf "model=%s registered_images=%s\n" "$d" "$cnt"
  if [ "$cnt" -gt "$BEST_COUNT" ]; then
    BEST_COUNT="$cnt"
    BEST_MODEL="$d"
  fi
done

echo
echo "BEST_MODEL=$BEST_MODEL"
echo "BEST_REGISTERED_IMAGES=$BEST_COUNT"
echo
echo "Analyze:"
echo "  $COLMAP_BIN model_analyzer --path \"$BEST_MODEL\""
echo
echo "View:"
echo "  $COLMAP_BIN gui --database_path \"$DB\" --import_path \"$BEST_MODEL\" --image_path \"$IMAGES\""
