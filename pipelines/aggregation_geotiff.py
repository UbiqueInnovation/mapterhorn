import os
import shutil
from glob import glob

import utils


def main(filepath: str) -> None:
    _, aggregation_id, filename = filepath.split('/')

    z, x, y, child_z = [int(a) for a in filename.replace('-aggregation.csv', '').split('-')]

    tmp_folder = f'aggregation-store/{aggregation_id}/{z}-{x}-{y}-{child_z}-tmp'

    geotiff_done_filepath = f'{tmp_folder}/geotiff-done'
    if os.path.isfile(geotiff_done_filepath):
        print(f'geotiff {filename} already done...')
        return

    merge_done = os.path.isfile(f'{tmp_folder}/merge-done')
    if not merge_done:
        raise AssertionError(f'merge not done yet for {filepath}...')

    num_tiff_files = len(glob(f'{tmp_folder}/*.tiff'))
    tiff_filepath = f'{tmp_folder}/{num_tiff_files - 1}-3857.tiff'

    out_folder = utils.get_geotiff_folder(x, y, z)
    utils.create_folder(out_folder)
    out_filepath = f'{out_folder}/{z}-{x}-{y}-{child_z}.tif'
    shutil.copyfile(src=tiff_filepath, dst=out_filepath)
    utils.run_command(f'touch {geotiff_done_filepath}')
