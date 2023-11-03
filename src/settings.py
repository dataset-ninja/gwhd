from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "GWHD 2021"
PROJECT_NAME_FULL: str = "GWHD: Global Wheat Head Dataset 2021"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Agricultural(is_used=True)]
CATEGORY: Category = Category.Agriculture()

CV_TASKS: List[CVTask] = [CVTask.ObjectDetection()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.ObjectDetection()]

RELEASE_DATE: Optional[str] = "2021-07-12"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://www.global-wheat.com/gwhd.html"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 4234685
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/gwhd"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[
    Union[str, dict]
] = "https://zenodo.org/record/5092309/files/gwhd_2021.zip?download=1"
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = [
    "https://spj.science.org/doi/full/10.34133/2020/3521852?adobe_mc=MCMID%3D13000678418609464879081490540568399952%7CMCORGID%3D242B6472541199F70A4C98A6%2540AdobeOrg%7CTS%3D1670889600",
    "https://arxiv.org/abs/2105.07660",
    "https://spj.science.org/doi/full/10.34133/2021/9846158",
]
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = {"GitHub":"https://zenodo.org/record/5092309#.ZGJAAHbMIuV"}

CITATION_URL: Optional[str] = "https://zenodo.org/record/5092309/export/hx"
AUTHORS: Optional[List[str]] = [
    "Etienne David",
    "Mario Serouart",
    "Daniel Smith",
    "Simon Madec",
    "Kaaviya Velumani",
    "Shouyang Liu",
    "Xu Wang",
    "Francisco Pinto Espinosa",
    "Shahameh Shafiee",
    "Izzat S. A. Tahir",
    "Hisashi Tsujimoto",
    "Shuhei Nasuda",
    "Bangyou Zheng",
    "Norbert Kichgessner",
    "Helge Aasen",
    "Andreas Hund",
    "Pouria Sadhegi-Tehran",
    "Koichi Nagasawa",
    "Goro Ishikawa",
    "Sébastien Dandrifosse",
    "Alexis Carlier",
    "Benoit Mercatoris",
    "Ken Kuroki",
    "Haozhou Wang",
    "Masanori Ishii",
    "Minhajul A. Badhon",
    "Curtis Pozniak",
    "David Shaner LeBauer",
    "Morten Lilimo",
    "Jesse Poland",
    "Scott Chapman",
    "Benoit de Solan",
    "Frédéric Baret",
    "Ian Stavness",
    "Wei Guo",
]
AUTHORS_CONTACTS: Optional[List[str]] = ["n.stavness@usask.ca", "owei@isas.a.u-tokyo.ac.jp"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "FR-AUS-CN-USA-MEX-NW-SUD-JAP-CH-UK-BEL-CND joint research group"
]
ORGANIZATION_URL: Optional[
    Union[str, List[str]]
] = "https://arxiv.org/ftp/arxiv/papers/2105/2105.07660.pdf"

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = None
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
