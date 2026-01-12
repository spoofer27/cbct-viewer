# dicom/exporter.py

import os
import pydicom
from pydicom.uid import generate_uid
import numpy as np

def export_as_multiple_dicoms(
    volume,
    reference_datasets,
    output_dir
):
    """
    volume: numpy array (Z, Y, X)
    reference_datasets: list of original pydicom datasets (sorted)
    """

    os.makedirs(output_dir, exist_ok=True)

    series_uid = generate_uid()

    for i, ds_ref in enumerate(reference_datasets):
        ds = ds_ref.copy()

        ds.SeriesInstanceUID = series_uid
        ds.InstanceNumber = i + 1

        ds.PixelData = volume[i].tobytes()

        output_path = os.path.join(output_dir, f"slice_{i+1:04d}.dcm")
        ds.save_as(output_path)

    return output_dir



def export_as_single_dicom(
    volume,
    reference_dataset,
    output_path
):
    """
    volume: numpy array (Z, Y, X)
    reference_dataset: one DICOM slice to copy metadata from
    """

    ds = reference_dataset.copy()

    ds.NumberOfFrames = volume.shape[0]
    ds.InstanceNumber = 1
    ds.SeriesInstanceUID = generate_uid()

    ds.PixelData = volume.tobytes()

    ds.Rows = volume.shape[1]
    ds.Columns = volume.shape[2]

    ds.save_as(output_path)

    return output_path
