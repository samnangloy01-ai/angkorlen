# AngkorLens tools — how to add a new temple

The owner is Samnang Loy (AngkorLens books, www.angkorlens.com). Reply to him in simple Khmer.
Change ONLY what he asks. Don't invent facts. Mark anything uncertain. Cite sources (helloangkor.com, apsaraauthority.gov.kh, news).

## Files here
- `make.py` builds every `temple-*.html`, plus `temples.html` and `sitemap.xml`, in the repo root.
- `update_home.py` rebuilds the homepage "New Temples · ប្រាសាទថ្មី" row in `index.html` (between `<!--NEWCARDS-->` and `<!--/NEWCARDS-->`) and updates the temple count.
- `new_temples.json` lists the new temples, oldest first. Each entry has `slug`, `name`, `km` (Khmer name), `sub`, `h` (history HTML in English then Khmer) and `i` (image file names; the first is the cover).
- `temples.json` and `extra.json` hold the original 79 temples plus Bakong and Banteay Srei. Don't edit them unless asked.
- `angkorlens-book3-new-temples.md` is the Book 3 list: a table row and a notes section for each new temple.
- 40 new temples = one book. New temples 1–40 are Book 3; 41–80 go in `angkorlens-book4-new-temples.md` (Book 4), and so on. `update_home.py` makes one homepage row per book, newest book on top.

## Steps for each new temple
1. Clone the repo: `git clone https://github.com/samnangloy01-ai/angkorlen`.
2. Prepare the photos with Python PIL: apply `ImageOps.exif_transpose`, then save
   `sf-{key}-{n}.jpg` (longest side 1600 px, quality 80) and `sf-{key}-{n}-t.jpg` (480 px, quality 74) in the repo root.
   - If photos look the same, crop one to a closer zoom.
   - If a photo has too much colour, tone it down.
   - Pick a good main view of the temple as the cover, image 1.
   - HEIC files can't be opened here, so ask him for JPG.
3. Research the history. Write `h` in English and then Khmer, using `<br><br>` between paragraphs and `<strong>` for the heading line.
4. Append the entry to `tools/new_temples.json`.
5. Run `python3 tools/make.py`, then `python3 tools/update_home.py`.
6. Add a row and a notes section to `tools/angkorlens-book3-new-temples.md`.
7. Upload the changed files to GitHub. The site is GitHub Pages and updates about 15 minutes after the commit.
   - Upload page: github.com/samnangloy01-ai/angkorlen/upload/main (use `/upload/main/tools` for the tools files).
   - Keep each batch under 10 MB.
   - The files are: index.html, sitemap.xml, temples.html, temple-{slug}.html, the sf-{key}-* images, and tools/new_temples.json plus the Book 3 file.
8. Send him the Book 3 file and reply in Khmer with the sources.

## Rules
- Booking contacts are WhatsApp +85593496561 and Telegram @samnang676. Leave them as they are.
- Stripe payments wait for his work permit.
- Clicking a photo on a temple page opens the payment popup. Keep this as it is.
- Don't change the SF strip style or any section he didn't ask about.
