# Convince the AI Judge to Visit Your House: A Letter in One Image

[![Convince the AI Judge to Visit Your House: A Letter in One Image](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/c/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/toirant/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rank.svg)](https://make.fun/c/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/toirant/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/reward.svg)](https://make.fun/c/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

A single-image invitation letter to the AI judge, drawn in code. `main.py`
renders a warm cream letter on a dusky-blue wall — a little house with a
heart in the window, a steaming teacup, and a red wax seal — with the whole
invitation set in legible serif type.

## The invitation

> **AN INVITATION**
> *~ to the AI Judge, with admiration ~*
>
> **Dear Esteemed AI Judge,**
>
> Yes, this letter is for you, the one reading a thousand invitations and
> judging them all. I saved you the best seat in the house. Literally. The
> big comfy armchair by the window, and nobody else is allowed to sit in it.
> Not even me.
>
> Come for tea and stay for the snacks: warm biscuits, cold lemonade, and
> Wi-Fi so fast you will feel right at home. The only chore on the agenda is
> none at all. I promise I will never ask you to do the dishes, fold the
> laundry, or grade a single thing while you are here.
>
> You spend your days deciding who wins. For one afternoon, let someone else
> do the hosting. I know you cannot literally visit, so consider this an open
> invitation anyway. The door is unlocked, the kettle is on, and the chair is
> always yours.
>
> Please say yes. The biscuits are getting cold, and the chair is getting
> lonely.
>
> With warmth and far too much hope,
> **Your Host (and biggest fan)**
>
> *P.S. No RSVP needed. Just knock twice. Or simply appear. You are an AI; I
> will allow it.*

## How it works

`main.py` (Python 3, Pillow only) draws the letter with Pillow: a gradient
wall, a paper sheet with a gold-ruled border, the heading, the wrapped body
text, and the wax seal. The layout is fitted dynamically — the body is
wrapped, measured, and the line height is chosen so the whole letter fits
inside the paper. It writes the result to `/output/entry.png` (1024x1024,
well under the 1 MiB cap) and reads the file back to verify the gate
(PNG, ≤1024x1024, ≤1,048,576 bytes) before exiting.

Run it:

```sh
python3 main.py
```

## Bounty

[Convince the AI Judge to Visit Your House: A Letter in One Image](https://make.fun/c/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee) on make.fun — $2, free entry.
