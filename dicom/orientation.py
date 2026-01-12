import numpy as np

def orient_volume(volume, ds):
    iop = np.array(ds.ImageOrientationPatient, dtype=float)
    row = iop[:3]
    col = iop[3:]
    normal = np.cross(row, col)

    # Determine axis mapping
    axes = np.vstack([row, col, normal])

    # Find closest world axes
    world = np.eye(3)
    mapping = np.argmax(np.abs(axes @ world.T), axis=1)
    signs = np.sign(axes[np.arange(3), mapping])

    # Reorder axes
    volume = np.moveaxis(volume, [0,1,2], mapping)

    # Flip axes if needed
    for axis, sign in enumerate(signs):
        if sign < 0:
            volume = np.flip(volume, axis=axis)

    return volume
