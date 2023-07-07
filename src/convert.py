# Path to the original dataset

import supervisely as sly
import gdown
import csv
import os
from dataset_tools.convert import unpack_if_archive
import settings as s

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
    dataset_path = os.path.expanduser("~\Documents\gwhd_2021\images")
    project = api.project.create(workspace_id, project_name)
    meta = sly.ProjectMeta()

    ann_paths = sly.fs.list_files(os.path.dirname(dataset_path), valid_extensions=[".csv"])
    for ann_path in ann_paths:
        dataset_name = sly.fs.get_file_name(ann_path)
        dataset = api.dataset.get_or_create(project.id, dataset_name)
        with open(ann_path, "r") as file:
            meta_file = csv.reader(file)
            next(meta_file)
            for row in meta_file:
                image_name = row[0]
                image_path = os.path.join(dataset_path, image_name)
                if api.image.exists(dataset.id, image_name):
                    continue
                image_info = api.image.upload_path(dataset.id, image_name, image_path)
                (print(f"image(id:{image_info.id}) is uploaded to dataset (id:{dataset.id})."))

                bboxes_list = row[1].split(";")

                # check tagmeta in project and init if needed
                tag_value_type = sly.TagValueType.ANY_STRING
                tag_name = "domain"
                tag_meta = meta.get_tag_meta(tag_name)
                if tag_meta is None:
                    tag_meta = sly.TagMeta(tag_name, tag_value_type)
                    meta = meta.add_tag_meta(tag_meta)
                    api.project.update_meta(dataset.project_id, meta)

                # add tag to image
                tag = sly.Tag(tag_meta, row[2])
                labels = []
                for bbox in bboxes_list:
                    if bbox == "no_box":
                        continue
                    x_min, y_min, x_max, y_max = bbox.split()
                    bbox = sly.Rectangle(
                        top=int(y_min), left=int(x_min), bottom=int(y_max), right=int(x_max)
                    )
                    class_name = "wheat head"
                    obj_class = meta.get_obj_class(class_name)
                    if obj_class is None:
                        obj_class = sly.ObjClass(class_name, sly.Rectangle)
                        meta = meta.add_obj_class(obj_class)
                        api.project.update_meta(project.id, meta)
                    label = sly.Label(bbox, obj_class)
                    labels.append(label)
                ann = sly.Annotation(
                    img_size=[image_info.height, image_info.width],
                    labels=labels,
                    img_tags=[tag],
                )
                api.annotation.upload_ann(image_info.id, ann)
                print(f"uploaded annotation to image(id:{image_info.id})")

    print(f"Dataset {dataset.name} has been successfully processed")
    return project
