import curses

from src.segment import TranscriptSegment
from src.helpers import open_vlc_to_segment


# ==============================================================================
# transcript explore tui
# ==============================================================================

def enter_transcript_explore_tui(
    stdscr,
    segments: dict[str, TranscriptSegment],
    # index2id: dict[int, str],
    target_seg: TranscriptSegment,
):
    """  """

    stdscr.clear()
    stdscr.refresh()
    

    header = "q/Esc: quit   ↑/↓ or j/k: move   o: open media at position    "
    
    curses.curs_set(0)
    stdscr.keypad(True)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(0, 0, header[:w-1], curses.A_DIM)

        # print segments below
        curr = target_seg
        for i in range(10):
            if curr is None:
                break
            y = h//2 + i
            if y >= h:
                break
            if i == 0: stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, 0, curr.text[:w-1])
            if i == 0: stdscr.attroff(curses.A_REVERSE)
            curr = segments.get(curr.next)

        # print segments above
        curr = segments.get(target_seg.prev)
        for i in range(10):
            if curr is None:
                break
            y = h//2 - 1 - i
            if y <= 2:
                break
            stdscr.addstr(y, 0, curr.text[:w-1])
            curr = segments.get(curr.prev)

        # KEYBOARD INTERACTIONS
        key = stdscr.getch()

        if key in (ord('q'), ord('Q'), 27):  # q or Esc
            return None
        elif key in (curses.KEY_UP, ord('k'), ord('K')):
            if target_seg.prev:
                target_seg = segments[target_seg.prev]
        elif key in (curses.KEY_DOWN, ord('j'), ord('J')):
            if target_seg.next:
                target_seg = segments[target_seg.next]
        elif key in (ord('o'), ord('O')): # Open position in media
            open_vlc_to_segment(target_seg)



# ==============================================================================
# results list tui
# ==============================================================================

def enter_results_list_tui(
    segments: dict[str, TranscriptSegment],
    index2id: dict[int, str],
    top_results_pairs,
):
    """  """
    limit = 20
    top_segments = [ segments[index2id[idx]] for idx, _ in top_results_pairs[:limit] ]
    sims = [ sim for _, sim in top_results_pairs[:limit] ]

    header = "q/Esc: quit   ↑/↓ or j/k: move   Enter: jump to transcript    o: open media    "

    def _tui(stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)

        idx = 0

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            # header line
            stdscr.addstr(0, 0, header[:w-1], curses.A_DIM)

            # items start at line 1
            for i, (seg, sim) in enumerate(zip(top_segments, sims)):
                y = i + 2
                if y >= h:
                    break
                if i == idx:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, 0, seg.text[:w-1])
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 0, seg.text[:w-1])

            key = stdscr.getch()

            if key in (ord('q'), ord('Q'), 27):  # q or Esc
                return
            elif key in (curses.KEY_UP, ord('k'), ord('K')):
                idx = max(0, idx - 1)
            elif key in (curses.KEY_DOWN, ord('j'), ord('J')):
                idx = min(limit - 1, idx + 1)
            elif key in (curses.KEY_ENTER, 10, 13): # Jump to transcript
                enter_transcript_explore_tui(
                    stdscr,
                    segments,
                    top_segments[idx],
                )
            elif key in (ord('o'), ord('O')): # Open position in media
                open_vlc_to_segment(top_segments[idx])
                

    return curses.wrapper(_tui)
