from dataclasses import dataclass
from pathlib import Path
import glob
import json

from src.helpers import name_to_path



@dataclass
class TranscriptSegment:
    id_: str
    src: str
    start: float
    end: float
    text: str
    next: str="" # id
    prev: str="" # id



def transcript_path_to_src(file: Path) -> str:
    parent_dir = name_to_path(file.parent.name)
    stem_safe = glob.escape(file.stem)
    files = list( Path(parent_dir).rglob(f"{stem_safe}.*") )
    if len(files) == 0:
        return ""
    return str(files[0])



def get_transcript_segments(dir: str) -> tuple[dict[str, TranscriptSegment], list]:
    segments = {}
    
    transcript_files = list(Path(dir).rglob("*.json"))
    for file in transcript_files:
        src = transcript_path_to_src(file)
        if src == "":
            raise Exception(f"unable to find src for transcript: {file}")
        with open(str(file), 'r') as f:
            data = json.load(f)
        prev_seg = None
        for segment in data['segments']:
            seg_id = f"{file}-{segment['id']}"
            seg = TranscriptSegment(
                id_ = seg_id,
                src = src,
                start = segment["start"],
                end =   segment["end"],
                text =  segment["text"],
            )
            if prev_seg:
                prev_seg.next = seg.id_
                seg.prev = prev_seg.id_
            prev_seg = seg
            segments[seg_id] = seg
    
    return segments, transcript_files

