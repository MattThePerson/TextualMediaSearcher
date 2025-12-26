import curses
from pathlib import Path

from src.segment import TranscriptSegment
from src.helpers import open_vlc_to_segment


def print_to_line(stdscr, y: int, start_x: int, end_x: int, msg: str, attr=None):
    wid = int(end_x - start_x)
    if attr: stdscr.attron(attr)
    stdscr.addstr(y, int(start_x), str(msg)[:wid-1])
    if attr: stdscr.attroff(attr)



# ==============================================================================
# region READ TRANSCRIPT
# ==============================================================================

def enter_transcript_explore_tui(
    stdscr,
    segments: dict[str, TranscriptSegment],
    target_seg: TranscriptSegment,
):
    """  """
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)
    stdscr.keypad(True)

    header = "q/Esc: quit   ↑/↓ or j/k: move   o: open media at position    "
    target_seg_orig = target_seg
    
    # LOOP
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(0, 0, header[:w-1], curses.A_DIM)
        stdscr.addstr(2, 2, f"source: \"{target_seg.src}\""[:w-1], curses.A_BOLD)

        # print segments below
        curr = target_seg
        for i in range(30):
            if curr is None:
                break
            y = int(h*0.3) + i
            if y >= h:
                break
            if i == 0: stdscr.attron(curses.A_REVERSE)
            print_to_line(stdscr, y, w*0.1,  w*0.2,  f"{curr.start:>.1f} - {curr.end:>.1f}")
            print_to_line(stdscr, y, w*0.2+4,  w-1,    curr.text)
            if curr.id_ == target_seg_orig.id_:
                print_to_line(stdscr, y, w*0.2+1,  w*0.2+3,  f"*")
            if i == 0: stdscr.attroff(curses.A_REVERSE)
            curr = segments.get(curr.next)

        # print segments above
        curr = segments.get(target_seg.prev)
        for i in range(20):
            if curr is None:
                break
            y = int(h*0.3) - 1 - i
            if y <= 3:
                break
            print_to_line(stdscr, y, w*0.1,  w*0.2,  f"{curr.start:>.1f} - {curr.end:>.1f}")
            print_to_line(stdscr, y, w*0.2+4,  w-1,    curr.text)
            if curr.id_ == target_seg_orig.id_:
                print_to_line(stdscr, y, w*0.2+1,  w*0.2+3,  f"*")
            curr = segments.get(curr.prev)


        # KEYBOARD INTERACTIONS
        key = stdscr.getch()

        if key in (ord('q'), ord('Q'), ord('b'), ord('B')):  # q or b
            # BACK
            return

        elif key in (curses.KEY_UP, ord('k'), ord('K'), ord('w'), ord('W')):
            # UP
            if target_seg.prev:
                target_seg = segments[target_seg.prev]
            
        elif key in (curses.KEY_DOWN, ord('j'), ord('J'), ord('s'), ord('S')):
            # DOWN
            if target_seg.next:
                target_seg = segments[target_seg.next]
            
        elif key in (ord('o'), ord('O'), ord('g'), ord('G')):
            # OPEN MEDIA
            open_vlc_to_segment(target_seg)



# ==============================================================================
# region RESULTS LIST
# ==============================================================================


def display_segment(seg: TranscriptSegment, sim: float, i: int, stdscr, y, w, attr=None):
    print_to_line(stdscr, y, 1,       5,         f"{i:>}", attr)
    print_to_line(stdscr, y, 5,       w*0.1,     f"{sim:.3f}", attr)
    print_to_line(stdscr, y, w*0.1,   w*0.35-1,  Path(seg.src).name, attr)
    print_to_line(stdscr, y, w*0.35,  w*0.4,     f"{seg.start:>.1f}", attr)
    print_to_line(stdscr, y, w*0.4,   w-1,       seg.text, attr)
    return 1

def display_table_header(stdscr, y, w):
    print_to_line(stdscr, y, 1,       5,         "#",       curses.A_DIM)
    print_to_line(stdscr, y, 5,       w*0.1,     "SIM",     curses.A_DIM)
    print_to_line(stdscr, y, w*0.1,   w*0.35,    "SRC",     curses.A_DIM)
    print_to_line(stdscr, y, w*0.35,  w*0.4,     "START",   curses.A_DIM)
    print_to_line(stdscr, y, w*0.4,   w-1,       "TEXT",    curses.A_DIM)


def enter_results_list_tui(
    stdscr,
    query: str,
    segments: dict[str, TranscriptSegment],
    index2id: dict[int, str],
    top_results_pairs,
):
    """  """
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(0)
    stdscr.keypad(True)

    header = "q/Esc: quit   ↑/↓ or j/k: move   Enter: jump to transcript    o: open media    "

    limit = 35
    top_segments = [ segments[index2id[idx]] for idx, _ in top_results_pairs[:limit] ]
    sims = [ sim for _, sim in top_results_pairs[:limit] ]

    idx = 0

    # LOOP
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # header line
        stdscr.addstr(0, 0, header[:w-1], curses.A_DIM)
        stdscr.addstr(2, 2, f"query: \"{query[:w-1]}\"", curses.A_BOLD)

        # items start at line 1
        display_table_header(stdscr, 4, w)
        i = 0
        for number, (seg, sim) in enumerate(zip(top_segments, sims)):
            y = i + 5
            if y >= h:
                break
            attr = None
            if i == idx:
                attr = curses.A_REVERSE
            lines_printed = display_segment(seg, sim, number+1, stdscr=stdscr, y=y, w=w, attr=attr)
            i += lines_printed


        # KEYBOARD INTERACTIONS
        key = stdscr.getch()

        if key in (ord('q'), ord('Q'), ord('b'), ord('B')):  # q or b
            # BACK
            return
        
        elif key in (curses.KEY_UP, ord('k'), ord('K'), ord('w'), ord('W')):
            # UP
            idx = max(0, idx - 1)
            
        elif key in (curses.KEY_DOWN, ord('j'), ord('J'), ord('s'), ord('S')):
            # DOWN
            idx = min(limit - 1, idx + 1)
            
        elif key in (curses.KEY_ENTER, ord('e'), ord('E'), 10, 13):
            # JUMP TO
            enter_transcript_explore_tui(
                stdscr,
                segments,
                top_segments[idx],
            )
            
        elif key in (ord('o'), ord('O'), ord('g'), ord('G')):
            # OPEN MEDIA
            print(top_segments[idx].id_)
            open_vlc_to_segment(top_segments[idx])




# ==============================================================================
# region TUI
# ==============================================================================


def enter_TUI(
    query: str,
    segments: dict[str, TranscriptSegment],
    index2id: dict[int, str],
    top_results_pairs,
):
    """  """
    def _tui(stdscr):
        enter_results_list_tui(
            stdscr,
            query,
            segments,
            index2id,
            top_results_pairs,
        )
    return curses.wrapper(_tui)
