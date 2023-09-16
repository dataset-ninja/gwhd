# Path to the original dataset

import supervisely as sly
import gdown
import csv
import os
from dataset_tools.convert import unpack_if_archive
import settings as s
import tqdm

# def download_dataset():
#     archive_path = os.path.join(sly.app.get_data_dir(), 'archive.zip')

#     if not os.path.exists(archive_path):
#         if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
#             gdown.download(s.DOWNLOAD_ORIGINAL_URL, archive_path, quiet=False)
#         if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
#             for name, url in s.DOWNLOAD_ORIGINAL_URL:
#                 gdown.download(url, os.path.join(archive_path, name), quiet=False)
#     else:
#         sly.logger.info(f"Path '{archive_path}' already exists.")
#     return unpack_if_archive(archive_path)


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # create project and initialize meta
    dataset_path = "/mnt/c/users/german/Documents/gwhd_2021/images"
    project = api.project.create(workspace_id, project_name)
    meta = sly.ProjectMeta()

    # create object class
    obj_class = sly.ObjClass("wheat head", sly.Rectangle, color=[0, 0, 255])
    meta = meta.add_obj_class(obj_class)
    api.project.update_meta(project.id, meta)

    # create tag metas
    tag_value_type = sly.TagValueType.ANY_STRING

    tag_meta_name = sly.TagMeta("domain name", tag_value_type)
    tag_meta_location = sly.TagMeta("location", tag_value_type)
    tag_meta_dev = sly.TagMeta("development stage", tag_value_type)

    tag_meta_list = [tag_meta_name, tag_meta_location, tag_meta_dev]
    for tag_meta in tag_meta_list:
        meta = meta.add_tag_meta(tag_meta)
    api.project.update_meta(project.id, meta)

    # create a dict with domain's meta
    meta_dict = {}
    meta_path = "/mnt/c/users/german/documents/gwhd_2021/metadata_dataset.csv"
    with open(meta_path, "r") as file:
        meta_file = csv.reader(file)
        next(meta_file)
        for row in meta_file:
            if len(row) == 1:
                row_split = row[0].split(";")
                meta_dict[row_split[0]] = [(row_split[1] + ", " + row_split[2]), row_split[3]]
            else:
                row = row[0] + row[1]
                row_split = row.split(";")
                meta_dict[row_split[0]] = [
                    (row_split[1] + ", " + row_split[2].strip()),
                    row_split[3],
                ]

    # iterate over dataset
    ann_paths = sly.fs.list_files(os.path.dirname(dataset_path), valid_extensions=[".csv"])[:-1]
    for ann_path in ann_paths:
        dataset_name = sly.fs.get_file_name(ann_path)
        dataset = api.dataset.get_or_create(project.id, dataset_name.split("_")[1])
        with open(ann_path, "r") as file:
            ann_file = csv.reader(file)
            next(ann_file)
            pbar = tqdm.tqdm(desc="total images...", total=len(sly.fs.list_files(dataset_path)))
            # iterate over images within annotation file
            try:
                for row in ann_file:
                    image_name = row[0]
                    bboxes_list = row[1].split(";")
                    domain = row[2]

                    image_path = os.path.join(dataset_path, image_name)
                    if api.image.exists(dataset.id, image_name):
                        continue
                    image_info = api.image.upload_path(dataset.id, image_name, image_path)
                    # iterate over bboxes
                    labels = []
                    for bbox in bboxes_list:
                        if bbox == "no_box":
                            continue
                        x_min, y_min, x_max, y_max = bbox.split()
                        bbox = sly.Rectangle(
                            top=int(y_min), left=int(x_min), bottom=int(y_max), right=int(x_max)
                        )
                        label = sly.Label(bbox, obj_class)
                        labels.append(label)
                    # upload annotation and add tags
                    ann = sly.Annotation(
                        img_size=[image_info.height, image_info.width], labels=labels
                    )
                    for i, tagmeta in enumerate(tag_meta_list):
                        if i == 0:
                            tag = sly.Tag(tagmeta, domain)
                        else:
                            tag = sly.Tag(tagmeta, meta_dict.get(domain)[(i - 1)])
                        ann = ann.add_tag(tag)
                    api.annotation.upload_ann(image_info.id, ann)
                    pbar.update(1)
            except Exception as e:
                sly.logger.warning(e)
                pbar.update(1)
                continue
    pbar.close()

    return project
