from typing import Union

from pose_format import Pose

from .concatenate import concatenate_poses
from .lookup import PoseLookup, CSVPoseLookup
from ..text_to_gloss.types import Gloss
from ..facial_expressions import add_facial_expressions


def gloss_to_pose(glosses: Gloss,
                  pose_lookup: PoseLookup,
                  spoken_language: str,
                  signed_language: str,
                  source: str = None,
                  anonymize: Union[bool, Pose] = False,
                  enable_expressions: bool = True) -> Pose:
    # Transform the list of glosses into a list of poses
    poses = pose_lookup.lookup_sequence(glosses, spoken_language, signed_language, source)

    # Add facial expressions to each pose
    if enable_expressions:
        poses = [add_facial_expressions(pose, str(gloss), enable_expressions) for pose, gloss in zip(poses, glosses)]

    # Anonymize poses
    if anonymize:
        try:
            from pose_anonymization.appearance import remove_appearance, transfer_appearance
        except ImportError as e:
            raise ImportError("Please install pose_anonymization. "
                              "pip install git+https://github.com/sign-language-processing/pose-anonymization") from e

        if isinstance(anonymize, Pose):
            print("Transferring appearance...")
            poses = [transfer_appearance(pose, anonymize) for pose in poses]
        else:
            print("Removing appearance...")
            poses = [remove_appearance(pose) for pose in poses]

    # Concatenate the poses to create a single pose
    return concatenate_poses(poses)
