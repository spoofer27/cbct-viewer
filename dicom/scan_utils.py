import os
import pydicom
import numpy as np

def analyze_scan(scan_path):
    dicoms = [
        os.path.join(scan_path, f)
        for f in os.listdir(scan_path)
        if f.lower().endswith(".dcm")
    ]

    if not dicoms:
        return None

    if len(dicoms) == 1:
        return {
            "type": "scout",
            "files": dicoms
        }

    # CBCT volume
    # slices = []
    datasets = []
    for f in dicoms:
        try:
            ds = pydicom.dcmread(f, stop_before_pixels=True)
            # slices.append((ds, f))
            datasets.append(ds)
        except:
            continue

    # Sort slices by Z (ImagePositionPatient)
    # slices.sort(
    #     key=lambda x: float(x[0].ImagePositionPatient[2])
    #     if hasattr(x[0], "ImagePositionPatient") else 0
    # )
    datasets = sort_slices_by_position(datasets)

    return {
        "type": "cbct",
         "datasets": datasets
        # "files": [f for _, f in slices]
    }

def sort_slices_by_position(datasets):
    iop = np.array(datasets[0].ImageOrientationPatient, dtype=float)
    row = iop[:3]
    col = iop[3:]
    normal = np.cross(row, col)

    positions = [
        np.dot(np.array(ds.ImagePositionPatient, dtype=float), normal)
        for ds in datasets
    ]

    return [ds for _, ds in sorted(zip(positions, datasets))]