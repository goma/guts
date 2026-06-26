"""
Plot results from an ExodusII file using netCDF4.

Usage:
    python plot_results.py [exodus_file] [--nodeset N] [--timestep T]

Arguments:
    exodus_file   Path to the ExodusII file (default: out_Wi_0.4_m2.exoII)
    --nodeset N   Nodeset number for film height plot (1-based, default: interactive)
    --timestep T  Timestep index for streamline plot (0-based, default: last step)
"""

import argparse
import sys

import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
import pyvista as pv


def decode_names(char_array):
    """Decode a 2D char array from ExodusII into a list of strings."""
    return [
        b"".join(row).decode("utf-8", errors="ignore").rstrip("\x00").strip()
        for row in char_array
    ]


def load_exodus(path):
    """Load all relevant data from an ExodusII file."""
    ds = nc.Dataset(path)

    data = {}
    data["time"] = ds.variables["time_whole"][:].data.copy()
    data["coordx"] = ds.variables["coordx"][:].data.copy()
    data["coordy"] = ds.variables["coordy"][:].data.copy()
    data["connect"] = ds.variables["connect1"][:].data.copy() - 1  # 0-based

    nod_var_names = decode_names(ds.variables["name_nod_var"][:])
    data["nod_var_names"] = nod_var_names
    name_to_idx = {name.upper(): i + 1 for i, name in enumerate(nod_var_names)}

    def load_var(name):
        idx = name_to_idx.get(name.upper())
        if idx is None:
            raise KeyError(f"Variable '{name}' not found. Available: {nod_var_names}")
        return ds.variables[f"vals_nod_var{idx}"][:].data.copy()

    data["DMX"] = load_var("DMX")
    data["DMY"] = load_var("DMY")
    data["VX"] = load_var("VX")
    data["VY"] = load_var("VY")
    data["FILM_HEIGHT"] = load_var("FILM_HEIGHT")

    num_ns = len(ds.dimensions["num_node_sets"])
    ns_names = decode_names(ds.variables["ns_names"][:])
    data["nodesets"] = {}
    for i in range(1, num_ns + 1):
        nodes = ds.variables[f"node_ns{i}"][:].data.copy() - 1  # 0-based
        ns_id = int(ds.variables["ns_prop1"][i - 1])
        label = ns_names[i - 1] if ns_names[i - 1] else f"NS{i} (ID={ns_id})"
        data["nodesets"][i] = {"nodes": nodes, "label": label, "id": ns_id}

    ds.close()
    return data


def pick_nodeset(data):
    """Prompt user to choose a nodeset interactively."""
    print("\nAvailable nodesets:")
    for k, v in data["nodesets"].items():
        print(f"  {k}: {v['label']}  ({len(v['nodes'])} nodes)")
    while True:
        try:
            choice = int(input("\nEnter nodeset number: "))
            if choice in data["nodesets"]:
                return choice
            print(f"  Invalid choice, pick from {list(data['nodesets'].keys())}")
        except (ValueError, EOFError):
            print("  Please enter an integer.")


def plot_film_height(data, ns_key, last_time=False, ax=None):
    """Plot FILM_HEIGHT along a nodeset vs arc length for all timesteps."""
    ns = data["nodesets"][ns_key]
    nodes = ns["nodes"]
    label = ns["label"]

    x0 = data["coordx"][nodes]
    y0 = data["coordy"][nodes]

    # Sort nodes by arc length along the nodeset in the undeformed configuration
    arc = np.zeros(len(nodes))
    order = np.argsort(x0 + 1j * y0, kind="stable")  # sort by x then y
    # Re-sort: use x as primary sort axis, y as secondary
    order = np.lexsort((y0, x0))
    xs = x0[order]
    ys = y0[order]
    diffs = np.hypot(np.diff(xs), np.diff(ys))
    arc[order] = np.concatenate([[0], np.cumsum(diffs)])

    film = data["FILM_HEIGHT"][:, nodes]  # (time, nodes)
    times = data["time"]

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4))
    else:
        fig = ax.figure

    cmap = plt.get_cmap("viridis")
    colors = cmap(np.linspace(0, 1, len(times)))

    start = 0
    if last_time:
        colors = cmap([0] * len(times))
        start = len(times)-1
    for t_idx in range(start,len(times)):
        print(times[t_idx])
        ax.plot(
            arc[order],
            film[t_idx, order],
            color=colors[t_idx],
            linewidth=0.8,
            alpha=0.85,
        )

    if not last_time:
      sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(times.min(), times.max()))
      sm.set_array([])
      fig.colorbar(sm, ax=ax, label="Time")

    ax.set_xlabel("Arc length along nodeset")
    ax.set_ylabel("Film height")
    ax.set_title(f"Film height — {label}")
    ax.grid(True, linewidth=0.4, alpha=0.5)

    return fig


def plot_streamlines(data, t_idx, ns_key):
    """Plot streamlines on the deformed mesh at a given timestep using PyVista."""
    x0 = data["coordx"]
    y0 = data["coordy"]
    xd = x0 + data["DMX"][t_idx]
    yd = y0 + data["DMY"][t_idx]
    vx = data["VX"][t_idx]
    vy = data["VY"][t_idx]
    time_val = data["time"][t_idx]

    # Build triangulated unstructured grid from Q9 corner nodes
    connect = data["connect"]  # (n_elem, 9); ExodusII Q9: first 4 are corners
    corners = connect[:, :4]
    tris = np.vstack([corners[:, [0, 1, 2]], corners[:, [0, 2, 3]]])

    points_3d = np.column_stack([xd, yd, np.zeros_like(xd)])
    n_tris = len(tris)
    cells = np.hstack([np.full((n_tris, 1), 3, dtype=np.int64), tris]).ravel()
    cell_types = np.full(n_tris, pv.CellType.TRIANGLE)

    mesh = pv.UnstructuredGrid(cells, cell_types, points_3d)
    velocity = np.column_stack([vx, vy, np.zeros_like(vx)])
    mesh.point_data["velocity"] = velocity

    # Seed streamlines from the deformed positions of the chosen nodeset
    ns_nodes = data["nodesets"][ns_key]["nodes"]
    ns_label = data["nodesets"][ns_key]["label"]
    seed_points = np.column_stack([xd[ns_nodes], yd[ns_nodes], np.zeros(len(ns_nodes))])
    source = pv.PolyData(seed_points)

    x_max = xd.max()
    x_min = xd.min()
    streamlines = mesh.streamlines_from_source(
        source,
        vectors="velocity",
        max_length=1000,
        max_steps=100_000,
        initial_step_length=0.01,
        integration_direction="forward",
    )
    streamlines.point_data["speed"] = np.linalg.norm(
        streamlines.point_data["velocity"], axis=1
    )

    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh, style="wireframe", color="lightgray", line_width=0.3, opacity=0.5)
    plotter.add_mesh(
        streamlines,
        scalars="speed",
        cmap="plasma",
        render_lines_as_tubes=True,
        line_width=2,
    )
    plotter.view_xy()
    plotter.add_title(f"Streamlines — t = {time_val:.4f}  (step {t_idx})  [seed: {ns_label}]")
    return plotter


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("exodus_file", nargs="?", default="out_Wi_0.4_m2.exoII")
    parser.add_argument("--nodeset", type=int, default=None, help="Nodeset number for film height plot (1-based)")
    parser.add_argument("--stream-nodeset", type=int, default=None, help="Nodeset to seed streamlines from (1-based, default: same as --nodeset)")
    parser.add_argument("--timestep", type=int, default=None, help="Timestep index (0-based, default: last)")
    args = parser.parse_args()

    print(f"Loading {args.exodus_file} ...")
    data = load_exodus(args.exodus_file)
    print(f"  {len(data['time'])} timesteps, {len(data['coordx'])} nodes, "
          f"{len(data['connect'])} elements")

    # --- Nodeset selection (film height) ---
    if args.nodeset is not None:
        if args.nodeset not in data["nodesets"]:
            print(f"Error: nodeset {args.nodeset} not found. Available: {list(data['nodesets'].keys())}")
            sys.exit(1)
        ns_key = args.nodeset
    else:
        ns_key = pick_nodeset(data)

    # --- Nodeset selection (streamline seed) ---
    stream_ns_key = args.stream_nodeset if args.stream_nodeset is not None else ns_key
    if stream_ns_key not in data["nodesets"]:
        print(f"Error: stream-nodeset {stream_ns_key} not found. Available: {list(data['nodesets'].keys())}")
        sys.exit(1)

    # --- Timestep selection ---
    t_idx = args.timestep if args.timestep is not None else len(data["time"]) - 1
    if not (0 <= t_idx < len(data["time"])):
        print(f"Error: timestep {t_idx} out of range [0, {len(data['time'])-1}]")
        sys.exit(1)

    base = args.exodus_file.rsplit(".", 1)[0]

    print(f"\nPlotting film height for nodeset {ns_key} ...")
    fig1 = plot_film_height(data, ns_key, True)
    fig1.tight_layout()
    film_path = f"{base}_film_height_ns{ns_key}.png"
    fig1.savefig(film_path, dpi=150)
    plt.close(fig1)
    print(f"  Saved {film_path}")

    print(f"Plotting streamlines at timestep {t_idx} (t={data['time'][t_idx]:.4f}) ...")
    plotter = plot_streamlines(data, t_idx, stream_ns_key)
    stream_path = f"{base}_streamlines_t{t_idx}.png"
    plotter.show(screenshot=stream_path)
    print(f"  Saved {stream_path}")


if __name__ == "__main__":
    main()
