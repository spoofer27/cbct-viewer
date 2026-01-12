import os
import pydicom
from pydicom.uid import generate_uid
import numpy as np

def export_as_multiple_dicoms(dicom_datasets, output_dir):
    """
    Exports the current scan as multiple DICOM files
    using original metadata (one file per slice)
    """

    os.makedirs(output_dir, exist_ok=True)

    for i, ds in enumerate(dicom_datasets, start=1):
        # make a safe copy
        out_ds = ds.copy()

        # update instance number to be clean
        out_ds.InstanceNumber = i

        filename = os.path.join(output_dir, f"slice_{i:04d}.dcm")
        out_ds.save_as(filename)

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
