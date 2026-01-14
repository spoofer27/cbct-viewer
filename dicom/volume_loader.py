import pydicom
import numpy as np

def load_volume(datasets, folder_path, progress_callback=None):
    if len(datasets) == 1:
        ds = datasets[0]
        full_ds = pydicom.dcmread(ds.filename, force=True)
        if hasattr(full_ds, 'NumberOfFrames') and full_ds.NumberOfFrames > 1:
            volume = full_ds.pixel_array
            volume = volume.astype(np.int16)
            if progress_callback:
                progress_callback.emit(100)
            return volume, [full_ds]

    slices = []
    image_datasets = []
    total = len(datasets)

    for i, ds in enumerate(datasets):

        full_ds = pydicom.dcmread(ds.filename, force=True)

        if "PixelData" not in full_ds:
            continue
        arr = full_ds.pixel_array
        slices.append(arr)
        image_datasets.append(full_ds)

        if progress_callback:
            progress_callback.emit(int((i + 1) / total * 100))

    if not slices:
        raise ValueError("No image slices found in this scan")
    
    image_datasets.sort(
        key=lambda ds: float(ds.ImagePositionPatient[2])
    )

    slices = [ds.pixel_array for ds in image_datasets]

    volume = np.stack(slices, axis=0)
    volume = volume.astype(np.int16)


    return volume, image_datasets  # return reference slice for orientation
