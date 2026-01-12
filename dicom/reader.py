import pydicom

def read_case_metadata(dicom_file):
    ds = pydicom.dcmread(dicom_file, stop_before_pixels=True)

    return {
        "id": getattr(ds, "PatientID", "Unknown"),
        "name": getattr(ds, "PatientName", "Unknown"),
        "age": getattr(ds, "PatientAge", ""),
        "gender": getattr(ds, "PatientSex", ""),
        "date": getattr(ds, "StudyDate", "")
    }
