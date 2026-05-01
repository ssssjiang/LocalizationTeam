#!/usr/bin/env bash
# One-shot: apt deps (requires sudo) + Ceres 2.2 + COLMAP + GLOMAP → ~/local
# See README "Build COLMAP + GLOMAP (CUDA)" for manual steps.
set -euo pipefail

PREFIX="${PREFIX:-$HOME/local}"
SOFTWARE_DIR="${SOFTWARE_DIR:-$HOME/software}"
CUDA_HOME="${CUDA_HOME:-/usr/local/cuda-12.8}"
# Use gcc-11 as nvcc host compiler (supported by CUDA 12.x; avoids needing gcc-13)
HOST_CC="${HOST_CC:-gcc-11}"
HOST_CXX="${HOST_CXX:-g++-11}"
# Parallel compile jobs (override: JOBS=16 bash ...)
JOBS="${JOBS:-8}"
NVCC="${NVCC:-$CUDA_HOME/bin/nvcc}"

APT_PACKAGES=(
  git build-essential ninja-build gcc-11 g++-11
  libeigen3-dev libopenimageio-dev openimageio-tools libfreeimage-dev libflann-dev
  libmetis-dev libcgal-dev libglew-dev liblz4-dev
  libqt5opengl5-dev libqt5svg5-dev qtbase5-dev qt5-qmake
  libgflags-dev libopenblas-dev libsqlite3-dev libsuitesparse-dev
)

log() { printf '%s\n' "$*"; }

check_host_compiler() {
  command -v "$HOST_CC" &>/dev/null || {
    log "ERROR: $HOST_CC not found. Install: sudo apt install gcc-11 g++-11"
    exit 1
  }
  command -v "$HOST_CXX" &>/dev/null || {
    log "ERROR: $HOST_CXX not found. Install: sudo apt install gcc-11 g++-11"
    exit 1
  }
}

need_apt=false
if [[ "${SKIP_APT_CHECK:-0}" != "1" ]]; then
  for p in "${APT_PACKAGES[@]}"; do
    if ! dpkg -s "$p" &>/dev/null; then
      need_apt=true
      break
    fi
  done
fi

if [[ "${RUN_APT:-0}" == "1" ]]; then
  check_host_compiler
  sudo apt-get update
  sudo apt-get install -y "${APT_PACKAGES[@]}"
elif [[ "$need_apt" == true ]]; then
  log "Missing one or more apt packages. Run one of:"
  log "  RUN_APT=1 $0"
  log "  sudo apt-get install -y ${APT_PACKAGES[*]}"
  exit 2
fi

check_host_compiler

if [[ ! -d "$CUDA_HOME" ]]; then
  log "ERROR: CUDA_HOME=$CUDA_HOME not found."
  exit 1
fi
if [[ ! -x "$NVCC" ]]; then
  log "ERROR: CUDA compiler not found: $NVCC"
  exit 1
fi

# Prefer toolkit nvcc over /usr/bin/nvcc (same as: PATH=$CUDA_HOME/bin:$PATH)
export PATH="$PREFIX/bin:$CUDA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$PREFIX/lib:$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}"
export CMAKE_PREFIX_PATH="$PREFIX${CMAKE_PREFIX_PATH:+:$CMAKE_PREFIX_PATH}"
export CC="$HOST_CC"
export CXX="$HOST_CXX"
export CUDAHOSTCXX="$HOST_CXX"

mkdir -p "$SOFTWARE_DIR" "$PREFIX"

# --- Ceres 2.2 ---
CERES_ROOT="$SOFTWARE_DIR/ceres-solver"
if [[ "${SKIP_CERES:-0}" != "1" ]]; then
  if [[ ! -d "$CERES_ROOT/.git" ]]; then
    git clone --branch 2.2.0 --depth 1 https://github.com/ceres-solver/ceres-solver.git "$CERES_ROOT"
  fi
  cmake -S "$CERES_ROOT" -B "$CERES_ROOT/build" -GNinja \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF \
    -DUSE_CUDA=ON \
    -DCMAKE_CUDA_COMPILER="$NVCC" \
    -DCMAKE_CUDA_ARCHITECTURES=89 \
    -DCMAKE_CUDA_HOST_COMPILER="$(command -v "$HOST_CXX")"
  cmake --build "$CERES_ROOT/build" -j"$JOBS"
  cmake --install "$CERES_ROOT/build"
else
  log "SKIP_CERES=1: reusing existing Ceres in $PREFIX"
fi

# --- COLMAP ---
COLMAP_ROOT="$SOFTWARE_DIR/colmap"
if [[ ! -d "$COLMAP_ROOT/.git" ]]; then
  git clone --recursive https://github.com/colmap/colmap.git "$COLMAP_ROOT"
else
  git -C "$COLMAP_ROOT" submodule update --init --recursive
fi
cmake -S "$COLMAP_ROOT" -B "$COLMAP_ROOT/build" -GNinja \
  -DCMAKE_INSTALL_PREFIX="$PREFIX" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCUDA_ENABLED=ON \
  -DCMAKE_CUDA_COMPILER="$NVCC" \
  -DCMAKE_CUDA_ARCHITECTURES=89 \
  -DCMAKE_CUDA_HOST_COMPILER="$(command -v "$HOST_CXX")" \
  -DGUI_ENABLED=ON \
  -DCeres_DIR="$PREFIX/lib/cmake/Ceres"
cmake --build "$COLMAP_ROOT/build" -j"$JOBS"
cmake --install "$COLMAP_ROOT/build"

# --- GLOMAP ---
GLOMAP_ROOT="$SOFTWARE_DIR/glomap"
if [[ ! -d "$GLOMAP_ROOT/.git" ]]; then
  git clone --recursive https://github.com/colmap/glomap.git "$GLOMAP_ROOT"
else
  git -C "$GLOMAP_ROOT" submodule update --init --recursive
fi
cmake -S "$GLOMAP_ROOT" -B "$GLOMAP_ROOT/build" -GNinja \
  -DCMAKE_INSTALL_PREFIX="$PREFIX" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCUDA_ENABLED=ON \
  -DCMAKE_CUDA_COMPILER="$NVCC" \
  -DCMAKE_CUDA_ARCHITECTURES=89 \
  -DCMAKE_CUDA_HOST_COMPILER="$(command -v "$HOST_CXX")" \
  -DFETCH_COLMAP=OFF \
  -DCOLMAP_DIR="$PREFIX/share/colmap"
cmake --build "$GLOMAP_ROOT/build" -j"$JOBS"
cmake --install "$GLOMAP_ROOT/build"

log "Installed to $PREFIX/bin — ensure PATH includes $PREFIX/bin and $CUDA_HOME/bin"
