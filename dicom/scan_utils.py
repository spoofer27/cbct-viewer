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

    # if len(dicoms) == 1:
    #     return {
    #         "type": "scout",
    #         "files": dicoms
    #     }

    # CBCT volume
    datasets = []
    for f in dicoms:
        try:
            ds = pydicom.dcmread(f, stop_before_pixels=True)
            datasets.append(ds)
        except:
            continue

    if not datasets:
        return None

    if len(datasets) == 1:
        print("Only one valid DICOM file found")
        ds = datasets[0]
        # print(ds)
        if hasattr(ds, 'NumberOfFrames') and ds.NumberOfFrames > 1:
            print("Single-file CBCT detected")
            return {
                "type": "cbct-singlefile",
                "datasets": datasets
            }
        else:
            print(" scout detected")
            return {
                "type": "scout",
                "datasets": datasets
            }
    else:
        # Assume CBCT: multiple single-slice DICOM files
        datasets = sort_slices_by_position(datasets)
        print("Multi-file CBCT detected")
        return {
            "type": "cbct",
            "datasets": datasets
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