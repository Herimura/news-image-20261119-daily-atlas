# The Daily Atlas — 19 November 2026

A broadsheet front page that sums up the world's news of Thursday
19 November 2026 in one image — a fifth, entirely fresh page for this
competition: a new masthead, a new colour scheme, and a new shape.
Where the earlier pages led with one story, this one is built around
a single big table.

## The picture

`entry.png` is a 1024 by 1024 PNG front page headed **THE DAILY
ATLAS**, dated Thursday 19 November 2026. Its centrepiece is **The
Day in Twelve Stories**, a full-width table of the day's twelve
biggest stories — number, headline, country and a two-line summary:

1. **Shenzhen, China** — Trump, Xi and Putin meet face to face at
   APEC; Xi and Putin blast Western protectionism, Europe absent.
2. **Kuwait · Bahrain · Hormuz** — Iran hits US sites in Kuwait and
   Bahrain, the US strikes Qeshm Island, tankers are hit in Hormuz.
3. **United States** — Anthropic prices its IPO at $83 a share,
   raises $81.3bn at a ~$1.5tn valuation: the largest debut in
   history, ticker ANT on the Nasdaq.
4. **The Hague · Myanmar** — the World Court decides Gambia v
   Myanmar, the genocide case over the 2017 Rohingya crackdown.
5. **Gaza · Israel** — Israeli tanks cross the ceasefire "Yellow
   Line"; Australia, Canada, Italy and the UK demand aid access.
6. **Russia · Ukraine** — the Crimean (Kerch) Bridge is attacked
   again and traffic halts, amid drone exchanges and Abu Dhabi talks.
7. **Antalya, Türkiye** — COP31's final week: the presidency draft
   admits the Paris 1.5°C limit will be passed; 144 items in dispute.
8. **United States** — Fed minutes show nearly all officials expect
   further rate hikes may be needed to return inflation to 2%.
9. **United States** — Nvidia's board will not reinstate Jensen
   Huang, who resigned on 12 November; Colette Kress is interim CEO
   and H-series shipments to China are halted.
10. **United States — NASA** — Voyager 1 reaches one light-day from
    Earth, 49 years after launch; its signals take 24 hours to arrive.
11. **France · Czechia** — a fourth weekend of cost-of-living protests
    in France; hundreds of thousands march in Prague for a free press.
12. **Worldwide** — Grand Theft Auto VI launches globally after a
    13-year wait; PlayStation's network stumbles before the release.

A schematic dot map of the world in the masthead band numbers the
places to match the rows — with Voyager 1 starred out in deep space,
off the map altogether.

## How it is built

`render.py` draws the page with PIL from fixed coordinates and fixed
text — no randomness, no network — and writes `entry.png`.
`main.py` (standard library only) validates the committed PNG
(1024×1024, under 1 MiB) and copies it byte for byte to the output
directory, so the delivered file is identical on every run.
