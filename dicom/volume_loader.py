import pydicom
import numpy as np

# def load_volume(dicom_files):
def load_volume(datasets, folder_path):
    # volume = np.stack([ds.pixel_array for ds in datasets], axis=0)

    # volume = volume.astype(np.int16)

    # return volume, datasets[0]

    # slices = []
    # for f in dicom_files:
    #     ds = pydicom.dcmread(f)
    #     slices.append(ds.pixel_array)

    # volume = np.stack(slices, axis=0)  # Z, Y, X
    # return volume
    print("Datasets count:", len(datasets))
    slices = []
    image_datasets = []

    for i, ds in enumerate(datasets):

        full_ds = pydicom.dcmread(ds.filename, force=True)

        if "PixelData" not in full_ds:
            continue
        arr = full_ds.pixel_array
        slices.append(arr)
        image_datasets.append(full_ds)

    # for ds in datasets:
    #     # f = ds.filename  # full path to DICOM file
    #     # ds_full = pydicom.dcmread(f)  # load with pixel data
    #     full_ds = pydicom.dcmread(ds.filename)
    #     print("Has PixelData:", "PixelData" in ds)
    #     if "PixelData" not in ds:
    #         continue   # skip non-image DICOMs
    #     slices.append(full_ds.pixel_array)
    #     image_datasets.append(full_ds)

    # print("TransferSyntaxUID:", full_ds.file_meta.TransferSyntaxUID)
    # print("Has PixelData:", "PixelData" in full_ds)

    if not slices:
        raise ValueError("No image slices found in this scan")
    

    # ---- sort slices by ImagePositionPatient (Z) ----
    image_datasets.sort(
        key=lambda ds: float(ds.ImagePositionPatient[2])
    )

    # ---- build volume AFTER sorting ----
    slices = [ds.pixel_array for ds in image_datasets]

    volume = np.stack(slices, axis=0)
    volume = volume.astype(np.int16)
    # print("Datasets received:", len(datasets))
    # print("First dataset tags:", datasets[0].dir())
    print(
        image_datasets[0].ImagePositionPatient[2],
        image_datasets[-1].ImagePositionPatient[2]
    )

    return volume, image_datasets  # return reference slice for orientation
