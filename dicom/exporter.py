import os
import pydicom
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
import numpy as np
from copy import deepcopy

def export_as_multiple_dicoms(dicom_datasets, output_dir, progress_callback=None):
    """
    Exports the current scan as multiple DICOM files
    using original metadata (one file per slice)
    """

    os.makedirs(output_dir, exist_ok=True)

    total = len(dicom_datasets)

    for i, ds in enumerate(dicom_datasets, start=1):
        # make a safe copy
        out_ds = ds.copy()

        # update instance number to be clean
        out_ds.InstanceNumber = i

        filename = os.path.join(output_dir, f"slice_{i:04d}.dcm")
        out_ds.save_as(filename)
        
        if progress_callback:
            progress_callback.emit(int((i + 1) / total * 100))

def o_export_as_single_dicom(
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

def fix_orientation_for_dicom(volume):
    """
    Fix volume orientation for PACS-compatible multi-frame DICOM export.
    Assumes volume is (Z, Y, X) after orient_volume.
    Returns volume flipped along required axes.
    """
    # Axial: flip up-down
    volume = np.flip(volume, axis=0)   # Y-axis
    # Sagittal: flip up-down (optional)
    # volume = np.flip(volume, axis=2)   # X-axis
    # Coronal: no change in Z-axis; already oriented

    return volume

def export_as_single_dicom(datasets, volume, output_path):
    if not datasets:
        raise ValueError("No datasets to export")

    # Use first slice as template
    template = deepcopy(datasets[0])

    # Stack pixel data
    # frames = []
    # for ds in datasets:
    #     frames.append(ds.pixel_array)

    # volume = np.stack(frames, axis=0)

    # Update required multi-frame tags
    template.NumberOfFrames = volume.shape[0]
    template.Rows = volume.shape[1]
    template.Columns = volume.shape[2]

    template.SamplesPerPixel = 1
    template.PhotometricInterpretation = "MONOCHROME2"
    template.BitsAllocated = 16
    template.BitsStored = 16
    template.HighBit = 15
    template.PixelRepresentation = 1

    # template.PixelData = volume.tobytes()
    template.PixelData = volume.astype(np.int16).tobytes()

    # VERY important
    template.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    template.SOPInstanceUID = generate_uid()

    # Remove per-slice attributes (illegal in multiframe)
    for tag in [
        "ImagePositionPatient",
        "SliceLocation",
        "InstanceNumber"
    ]:
        if tag in template:
            delattr(template, tag)

    template.save_as(output_path)
