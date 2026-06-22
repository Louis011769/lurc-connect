# Loughborough URC — website

A clean, fast, **owned** website. Plain HTML + CSS + a little JavaScript — **no build step, no framework, no lock-in.** It will run by double-clicking `index.html`, and hosts for free on Netlify, GitHub Pages or Cloudflare Pages.

## Files
| File | What it is |
|---|---|
| `index.html` | Home — one page with sections: Welcome, This Week, Video, Worship, Community, Rooms for Hire, About, Contact |
| `blog.html` | Minister's Blog (its own page, as Craig asked) |
| `safeguarding.html` | Safeguarding + Policies (available on request) |
| `styles.css` | All styling — colours and fonts are set once at the top (`:root`) |
| `script.js` | Mobile menu only |
| `assets/` | Drop images here (logo, photo of the building) |

## Preview it locally
Either double-click `index.html`, or for the calendar/map to behave run a tiny server:
```
cd "Loughborough URC/website"
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy it free (recommended: Netlify drop)
1. Go to **app.netlify.com/drop**
2. Drag the whole `website` folder onto the page.
3. It's live in seconds on a free URL. Then point `loughboroughurc.co.uk` at it in Netlify's domain settings.

(GitHub Pages or Cloudflare Pages work just as well — it's only static files.)

## Editing content
All text lives in the HTML and reads like plain English between the tags. To change a service time, edit the line in `index.html`. To add a blog post, copy one `<article class="post">` block in `blog.html`, change the date/title/text, and put it at the top.

## Done — pulled from the old site and wired in
- ✅ **Real logo** (`assets/logo.png`) in the header — it's already transparent, so Craig's "white background" snag is solved.
- ✅ **Favicon** (`assets/favicon.png`).
- ✅ **Welcome video** embedded on the homepage (YouTube `rBKv3TVX4O4`).
- ✅ **Full safeguarding page** — real contacts (Coordinator Bob Cornes, Deputy Daphne Beale, Synod/national/statutory contacts) and the complete **policy PDF** (`assets/LURC-Safeguarding-GP6.pdf`, self-hosted so it survives the old site being retired).
- ✅ **History** — matches the old site's current text.
- ✅ **Minister's Blog** — all 50 posts imported with full text; images downloaded into `assets/blog/` so the blog is fully self-contained. To refresh later (while the old site still exists): `python3 tools/build-blog.py`.

## Still to fill (search the code for `TODO`)
1. **Live calendar** — your friend's Google Calendar. In `index.html` ("This Week" section) there's a commented `<iframe>`; paste the calendar's embed. To get it: in Google Calendar → *Settings → [the calendar] → Integrate calendar*, make it public, then copy the **Embed code** (or just the **Calendar ID**) into the iframe.
2. **History** — Craig said he'd like to write a fuller version; drop it into the About section of `index.html` when ready.
3. **Photos** (optional, high impact) — a photo of the building can become the hero background (see `.hero` in `styles.css`), and group photos lift the Community section.

## One thing to confirm
- **Daphne's email:** the Contact section uses `churchsecretary@loughboroughurc.co.uk` (her secretary role); the Safeguarding page uses `safeguarding@loughboroughurc.co.uk` (the real safeguarding inbox from the live policy). Both are intentional — just confirm `churchsecretary@` is the address Daphne wants shown for general contact.

## Everything from Craig's snagging list is applied
Minister email + "no Rev." title, single-@ YouTube, "Gather Together" replacing Open Thursday / T@2, no Tuesday Bible Study, Friday Bible Study 1st/3rd/5th 10:30 in the Blue Room, WWW in the Upper Hall, Grub Club via grub-club@outlook.com (no personal number), social events removed, Open Prayers removed, Bhavnagar removed, "Equality Action and Town of Sanctuary" replacing Human Rights & Equalities, Eco Church Silver, Fairtrade wording verbatim, Minister's Blog on its own page, treasurer email, secretary email + safeguarding, Health & Safety/Discipleship/Lone Working "available on request", no "Last Updated Jan 2020", calendar + welcome video placeholders ready.
