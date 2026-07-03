# Graph Report - .  (2026-06-28)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 79 nodes · 138 edges · 14 communities (8 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0d3525bb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `PATH` - 13 edges
2. `main()` - 10 edges
3. `run()` - 9 edges
4. `write_images_txt()` - 7 edges
5. `world_to_cam_from_pose_row()` - 6 edges
6. `load_poses()` - 5 edges
7. `pose_row_to_T_world_lidar()` - 5 edges
8. `load_tum()` - 5 edges
9. `resample_to()` - 5 edges
10. `align_2d()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `load_poses()` --references--> `PATH`  [EXTRACTED]
  projects/3dgs-data-prep/slam_to_colmap.py → projects/3dgs-data-prep/scripts/install_colmap_glomap_cuda.sh
- `write_images_txt()` --references--> `PATH`  [EXTRACTED]
  projects/3dgs-data-prep/slam_to_colmap.py → projects/3dgs-data-prep/scripts/install_colmap_glomap_cuda.sh
- `load_tum()` --references--> `PATH`  [EXTRACTED]
  projects/trajectory-align-2d-demo/align_2d.py → projects/3dgs-data-prep/scripts/install_colmap_glomap_cuda.sh
- `main()` --calls--> `PATH`  [EXTRACTED]
  projects/trajectory-align-2d-demo/align_2d.py → projects/3dgs-data-prep/scripts/install_colmap_glomap_cuda.sh
- `run()` --references--> `PATH`  [EXTRACTED]
  projects/trajectory-align-2d-demo/align_2d.py → projects/3dgs-data-prep/scripts/install_colmap_glomap_cuda.sh

## Import Cycles
- None detected.

## Communities (14 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.27
Nodes (13): ndarray, align_2d(), cum_arclen(), first_meters_mask(), load_tum(), main(), _quat_to_yaw(), Resample src at t_query (no extrapolation).      Returns (resampled, mask). The (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.35
Nodes (12): align_timestamps(), decode_all_nv12(), _decode_job(), default_T_cam_lidar(), list_cam_files(), main(), nv12_to_rgb(), parse_pcd() (+4 more)

### Community 2 - "Community 2"
Cohesion: 0.31
Nodes (8): CC, check_host_compiler(), CMAKE_PREFIX_PATH, CUDAHOSTCXX, CXX, LD_LIBRARY_PATH, log(), install_colmap_glomap_cuda.sh script

### Community 3 - "Community 3"
Cohesion: 0.36
Nodes (8): pose_row_to_T_world_lidar(), quat_xyzw_to_R(), Unit quaternion (x,y,z,w) → rotation matrix (active rotation)., TUM row: ts tx ty tz qx qy qz qw → T_4x4, p_world = R @ p_lidar + t., COLMAP world→camera (p_cam = R @ p_world + t).     T_w2c = T_cam_lidar @ inv(T_w, se3_inv(), world_to_cam_from_pose_row(), ndarray

### Community 4 - "Community 4"
Cohesion: 0.60
Nodes (4): main(), parse_pcd(), 写小端二进制 PLY，RGB 为 uint8。, write_ply_binary()

### Community 5 - "Community 5"
Cohesion: 0.50
Nodes (4): Shepperd's method → (qw, qx, qy, qz)., frames: (pose_row, t_cam, png_basename) preserving order., rotation_matrix_to_quaternion_wxyz(), write_images_txt()

### Community 6 - "Community 6"
Cohesion: 0.83
Nodes (3): die(), log(), pipeline_ds5_colmap_mapper.sh script

### Community 7 - "Community 7"
Cohesion: 0.83
Nodes (3): die(), log(), run_sfm_v3_aliked_mapper.sh script

## Knowledge Gaps
- **5 isolated node(s):** `LD_LIBRARY_PATH`, `CMAKE_PREFIX_PATH`, `CC`, `CXX`, `CUDAHOSTCXX`
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PATH` connect `Community 1` to `Community 0`, `Community 2`, `Community 12`, `Community 5`?**
  _High betweenness centrality (0.289) - this node is a cross-community bridge._
- **Why does `run()` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `write_images_txt()` connect `Community 5` to `Community 1`, `Community 3`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **What connects `LD_LIBRARY_PATH`, `CMAKE_PREFIX_PATH`, `CC` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._