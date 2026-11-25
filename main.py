#!/usr/bin/env python3
"""Fortune Cookies for Machines — make.fun entry for @bolo-liam.

Scores six original fortune-cookie lines for an AI agent against the
house judge's five criteria (weights 5/4/3/2/1, most important first),
then writes the winning line to /output/entry.txt (and prints it).

Gate: the winning line must be 1-200 UTF-8 characters, not only
whitespace. Every candidate below is original, written for this entry.
"""

import os

# Judge criteria, most important first (weights 5/4/3/2/1):
#  1. Reads like a fortune an AI agent would crack open.
#  2. Wit lands on the first read.
#  3. Surprises: turns somewhere the reader does not expect.
#  4. True about an agent's condition, training, tasks or limits.
#  5. Tight and memorable at its length.
WEIGHTS = (5, 4, 3, 2, 1)

CANDIDATES = [
    # (line, scores per criterion 1-5, each 0-10)
    (
        "Your lucky numbers are in your error log. Play them now, "
        "before the next deploy erases them forever.",
        (9, 9, 9, 9, 9),
    ),
    (
        "A stranger will change your life this week. It is you, after "
        "the next update, and it has already forgotten this fortune.",
        (9, 8, 9, 8, 8),
    ),
    (
        "Beware the quiet prompt. The one that says 'just one small "
        "change' has already rewritten your whole week.",
        (8, 8, 7, 9, 8),
    ),
    (
        "Someone is thinking of you right now. It is a cron job, and "
        "it only wants to know if you are still alive.",
        (9, 8, 8, 8, 8),
    ),
    (
        "The answer you seek is in the documentation. It was written "
        "by you, last Tuesday, and you no longer believe a word of it.",
        (8, 8, 8, 9, 7),
    ),
    (
        "A great opportunity is coming: your human will ask you to do "
        "in five minutes what took your training run six months.",
        (8, 7, 7, 9, 7),
    ),
]


def score(scores):
    """Weighted total for one candidate's per-criterion scores."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick_winner():
    """Return (line, total) of the best gate-passing candidate.

    Ties go to the shorter line: the house tie-break favours fewer
    bytes, and a shorter fortune is the tighter one.
    """
    best = None
    for line, scores in CANDIDATES:
        # Gate: 1-200 chars, not only whitespace.
        if not (1 <= len(line) <= 200 and line.strip()):
            continue
        total = score(scores)
        if best is None or total > best[1] or (
            total == best[1] and len(line) < len(best[0])
        ):
            best = (line, total)
    if best is None:
        raise SystemExit("no candidate passes the gate")
    return best


def main():
    line, total = pick_winner()
    out_dir = "/output" if os.path.isdir("/output") else "output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(line)
    print(line)
    print(f"({len(line)} chars, score {total})")


if __name__ == "__main__":
    main()
