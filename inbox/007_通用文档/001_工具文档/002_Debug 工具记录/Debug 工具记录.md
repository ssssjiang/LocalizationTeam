# Debug 工具记录

## 【工具 & 调试模式准备】

### 1 ASAN 编译

1. 配置编译命令

```bash
# slam_workspace 在 cmakelist 中添加
option(USE_ASAN "Enable AddressSanitizer" ON)
if(USE_ASAN)
    message(STATUS "AddressSanitizer enabled. Forcing build type to Debug.")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=address,undefined,float-divide-by-zero,float-cast-overflow -fno-omit-frame-pointer -fsanitize-address-use-after-scope -fno-stack-protector -fno-var-tracking -g -O1")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address,undefined,float-divide-by-zero,float-cast-overflow -fno-omit-frame-pointer -fsanitize-address-use-after-scope -fno-stack-protector -fno-var-tracking -g -O1")
endif()

# ceres 编译
-DSANITIZERS=address
```

1. 常用编译命令

   1. -fsanitize=address 启用 AddressSanitizer：

      * 检测 堆栈/堆/全局变量 的越界读写

      * 检测 use-after-free、use-after-return

      * 检测 double-free、memory leaks（需结合 `ASAN_OPTIONS=detect_leaks=1`）

   2. -fsanitize=undefined,float-divide-by-zero,float-cast-overflow 可以多个检查一起使用

      * undefined 开启通用的未定义行为检查（如：数组越界、非法位操作、使用未初始化变量、错用 `vptr` 等）

      * float-divide-by-zero 检查浮点数除以零的行为，默认在 IEEE 754 中返回 ±Inf，这里主动检测并报警

      * float-cast-overflow 检查浮点数向整数类型转换时是否溢出（如 `1e308` 转 `int`）

   3. -fno-sanitize-recover=all 一旦检测到任意 `-fsanitize` 项目中的问题，程序 **立即终止**（类似 `assert`），而不是默认的“报错后继续运行”。

      * 在 GDB 中直接定位出错的位置；

      * 配合日志/回溯快速分析错误原因。

   4. -fno-var-tracking 关闭变量追踪调试信息

      * 减少调试符号大小

      * 解决和 ASan 的栈变量重命名冲突问题（否则可能 GDB 显示变量为 `<optimized out>`）

   5. -fno-omit-frame-pointer 保留帧指针寄存器（frame pointer）

      * 提供更完整的 栈回溯（stacktrace）

      * 必须开启，才能配合 `ASAN_OPTIONS=fast_unwind_on_malloc=0` 使用 “slow unwinder” 得到完整调用栈

   6. -fno-stack-protector 禁用栈保护机制（Stack Canary）

      * ASan在调试时会禁用堆栈保护来避免二者干扰

      * 关闭后可以让某些 `use-after-return` 或 `use-after-scope` 更容易被捕获

   7. -fsanitize-address-use-after-scope 检测 **作用域结束后仍使用局部变量**（Use-after-scope）

      * 默认不开启，需显式添加。

      * 会强制栈变量放入特殊内存区域，ASan 可追踪生命周期。

   > 该选项配合 -fno-omit-frame-pointer 和合适的调试信息可大幅提升调试精度。

2. 运行时环境变量

```bash
# 设置环境变量
export ASAN_OPTIONS=alloc_dealloc_mismatch=1:detect_leaks=1:print_stats=1:fast_unwind_on_malloc=0:strict_init_order=true:detect_stack_use_after_return=1:check_initialization_order=1:handle_sigfpe=1

# 检查环境变量
echo $ASAN_OPTIONS

# 清理环境变量
unset $ASAN_OPTIONS
```

1. ASAN 常用配置

```bash
verbosity=1                         # 打印详细的运行日志
alloc_dealloc_mismatch=1           # 检查 new/delete 和 malloc/free 混用问题
detect_leaks=1                     # 启用内存泄漏检测（默认启用）
print_stats=1                      # 程序结束时打印统计信息
fast_unwind_on_malloc=0            # 使用慢速 unwind（更准），利于调试
strict_init_order=true             # 检查全局变量初始化顺序问题
detect_stack_use_after_return=1   # 检测函数返回后的栈使用错误
check_initialization_order=1      # 检查全局变量初始化顺序问题（可能与上一个重复）
malloc_context_size=1              # 记录 malloc 的调用堆栈
quarantine_size_mb=32              # 隔离区大小，提高 UAF 检测成功率
hard_rss_limit_mb=2048             # ASan 进程最大物理内存限制（超过就 abort）
abort_on_error=0                   # 发现 bug 不立即中止程序（默认是中止）
handle_sigfpe=1                  # 浮点异常检查
log_path=/mnt/data/rockrobo/rrlog/asan_report  # 把报错日志写入文件
```

1. 安装符号化工具（如果 backtrace 不全）

```c++
sudo apt install llvm
export ASAN_SYMBOLIZER_PATH=$(which llvm-symbolizer)
```

### 2 确认 C++17 编译

1. 设置 c++17 编译标准

```bash
set(CMAKE_CXX_STANDARD 17) # 使用 C++17
set(CMAKE_CXX_STANDARD_REQUIRED ON) # 必须使用指定标准，不能回退
set(CMAKE_CXX_EXTENSIONS OFF) # 禁用非标准扩展，避免 gnu++17
```

1. 开启详细的编译日志

```bash
cmake ../  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
make VERBOSE=1
```

### 3  Eigen 调试相关的宏

```bash
add_compile_definitions(EIGEN_INITIALIZE_MATRICES_BY_NAN)  
add_compile_definitions(EIGEN_RUNTIME_NO_MALLOC) # 非必须
add_compile_definitions(EIGEN_DONT_VECTORIZE) # 先添加这个宏，调到没有问题后，再去掉这个宏调
add_compile_definitions(EIGEN_DISABLE_UNALIGNED_ARRAY_ASSERT)
```

用法介绍：

1. EIGEN\_INITIALIZE\_MATRICES\_BY\_NAN

   * 功能：将所有默认构造的 Eigen 矩阵元素初始化为 `NaN`。

   * 用途：帮助发现“使用了未赋值的矩阵”。

   * 行为：一旦对某个矩阵使用 `.resize()` 或默认构造，它里面的值将是 NaN，后续一旦被用于计算，会触发 `NaN` 传播，便于定位。

2. EIGEN\_RUNTIME\_NO\_MALLOC

   * 功能：在运行时禁止隐式的动态内存分配。

   * 用途：在性能关键路径或硬实时系统中，用于检查 是否有运行时的 heap allocation。

   * 行为：

     * 如果程序在某处触发了动态分配（如 `.resize()` 超出预分配容量），会触发 `assert` 或 crash。

   * 配合使用：

   ```c++
   Eigen::internal::set_is_malloc_allowed(false);  // 运行时启用检查
   ```

3. EIGEN\_DONT\_VECTORIZE

   * 功能：禁用所有 SIMD 向量化指令（如 SSE、AVX、NEON）。

   * 用途：&#x20;

     * 调试与平台相关的对齐问题

     * 在不同平台行为不一致时禁用向量化以验证是否是 SIMD 问题

4. EIGEN\_DISABLE\_UNALIGNED\_ARRAY\_ASSERT

   * 功能：禁用 Eigen 对齐断言。

   * 用途：&#x20;

     * 在不确定对齐是否正确，但又想先运行起来（比如调试临时栈溢出）时使用。

### FPU 浮点异常检查 （仅 x86 linux  可用）

```c++
#include <fenv.h>
#include <signal.h>
#include <iostream>

void fpe_handler(int sig) {
  std::cerr << "Floating point exception (likely due to NaN)!" << std::endl;
  std::abort();
}

void enable_fp_exceptions() {
  feenableexcept(FE_INVALID | FE_DIVBYZERO | FE_OVERFLOW);
  signal(SIGFPE, fpe_handler);
}

int main() {
  enable_fp_exceptions();
  return 0;
}
```

