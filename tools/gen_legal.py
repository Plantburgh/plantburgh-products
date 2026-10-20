#!/usr/bin/env python3
"""Generate privacy / terms / delete pages for apps in the docs.css style.

Usage: python3 tools/gen_legal.py   (writes <slug>/privacy.html, terms.html, delete.html)
Edit the APPS table below, rerun, review the diff, commit.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CO = "Plantburgh Products LLC, a Pennsylvania company owned by Plantburgh LLC"
MAIL = "contact@plantburgh.com"


def ts_sections(path, name):
    """Read a [title, body] array (single-quoted or double-quoted strings) from a .ts file."""
    src = pathlib.Path(path).read_text()
    block = re.search(r"export const %s[^=]*=\s*\[(.*?)\n\];" % name, src, re.S).group(1)
    lit = r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\""
    out = []
    for m in re.finditer(r"\[\s*(?:%s)\s*,\s*(?:%s)\s*\]" % (lit, lit), block, re.S):
        t = m.group(1) if m.group(1) is not None else m.group(2)
        b = m.group(3) if m.group(3) is not None else m.group(4)
        unesc = lambda s: s.replace("\\'", "'").replace('\\"', '"')
        out.append((unesc(t), unesc(b)))
    return out


SWIM = "/Users/user11/Developer/swimpro/src/constants/legal.ts"

APPS = {
    "swimtime-pal": dict(
        name="Swimtime Pal", updated="2026-10-20",
        short="Your swims, plans and settings stay on your phone. There is no account and we run no server that stores them. The Free plan shows ads; Standard and Pro make no internet requests of their own.",
        privacy=lambda: ts_sections(SWIM, "PRIVACY"),
        terms=lambda: ts_sections(SWIM, "TERMS"),
        delete="Open Swimtime Pal, go to <b>Settings › Privacy and data › Delete all my data</b>, and confirm. That erases every workout, plan, personal best and setting on this phone. Uninstalling the app also removes it. Swims you saved to Health Connect stay there until you delete them in Health Connect. A Google Play subscription is not cancelled by deleting data; cancel it in Google Play.",
    ),
    "light-meter": dict(
        name="Plantburgh Light Meter", updated="2026-10-20",
        short="Readings, spots, photos and projects stay on your phone. There is no account, the app makes no internet requests of its own, and it shows no third-party ads.",
        privacy=lambda: [
            ("Who we are", f"Plantburgh Light Meter is made by {CO}. Questions: {MAIL}."),
            ("What the app keeps", "Your light readings, spots, spot photos, plant checks, client projects, care reminders and settings. They are stored only on this phone, in the app's private storage. There is no account and we never receive them."),
            ("Location (optional)", "If you allow location, the app uses it only when you add a spot or a project, to fill in the address on the phone. Your location is not sent to us or tracked in the background."),
            ("Camera and photos", "Spot photos you take or pick are saved inside the app on this phone."),
            ("Internet", "The app does not connect to the internet on its own. Links to our website, Play or the terms open in your browser."),
            ("Ads and purchases", "This version shows only our own offline cards and no third-party ads. If a future version adds ads or a paid upgrade, this page will be updated before that version is released. Any purchase is handled by Google Play; we never see your payment details."),
            ("Notifications", "Watering and care reminders are scheduled on the phone. Nothing is sent to us."),
            ("Phone assistant (optional)", "If you turn on the assistant feature, an assistant on your phone can read readings you ask it about. What it does with them is covered by that assistant's own privacy policy."),
            ("Sharing and backups", "Data leaves the phone only when you share a PDF report, export a file or save a backup, and you choose where it goes. If Android backup is on, Android may include the app's data in your own Google account backup."),
            ("Deleting", "Settings › Delete all my data erases everything the app saved on this phone. Uninstalling the app also removes it."),
            ("Children", "The app is not directed at children under 13."),
        ],
        terms=lambda: [
            ("Readings are estimates", "Phone light sensors vary by model and are not lab instruments. Readings and plant suggestions are guidance, not a guarantee of how a plant will do."),
            ("Plant safety", "Pet and toxicity notes are general guidance from published sources. If a person or pet eats a plant, call a doctor, a vet or poison control."),
            ("The app", "The app is provided as is by Plantburgh Products LLC. We work to keep it accurate but cannot promise it is error free. To the extent the law allows, we are not liable for indirect or consequential losses."),
            ("Contact", f"Questions: {MAIL}."),
        ],
        delete="Open the app, go to <b>Settings › Delete all my data</b>, and confirm. That erases every reading, spot, photo, project and reminder on this phone. Uninstalling the app also removes it. We hold no copy.",
    ),
    "tourlog": dict(
        name="TourLog", updated="2026-10-20",
        short="Recordings, photos and transcripts stay on your phone. Transcription runs on the phone. There is no account, no ads and no server of ours.",
        privacy=lambda: [
            ("Who we are", f"TourLog is made by {CO}. Questions: {MAIL}."),
            ("What the app keeps", "Your recordings, photos, bookmarks, notes, speaker names and transcripts, stored only on this phone in the app's private storage. There is no account and we never receive them."),
            ("Microphone", "The microphone is used only while you are recording a tour. A notification shows the whole time it is on."),
            ("Camera", "Photos you take during a tour are saved inside the app on this phone."),
            ("Transcription", "Speech-to-text and speaker labels run on the phone. Audio is never uploaded for transcription."),
            ("Internet", "The app connects to the internet only to download the speech models once (from the open-source sherpa-onnx releases on GitHub). That download carries what any web request does (your IP address) and nothing about your recordings."),
            ("Phone assistant (optional)", "If you turn on the assistant feature, an assistant on your phone can read the transcripts you ask it about. It cannot record, change or delete anything. What it does with what it reads is covered by that assistant's own privacy policy."),
            ("Sharing", "Data leaves the phone only when you share a transcript or save a file to Downloads, and you choose where it goes."),
            ("Recording other people", "Many places, including Pennsylvania, require everyone in a conversation to agree before it is recorded. You are responsible for getting that consent. The app can show a consent notice before you start."),
            ("Deleting", "Delete a tour, its recording or its photos inside the app. Speech models can be deleted in Settings. Uninstalling the app removes everything."),
            ("Children", "TourLog is not directed at children under 13."),
        ],
        terms=lambda: [
            ("Consent", "Only record people who have agreed to it, as the law where you are requires."),
            ("Transcripts are automatic", "Transcripts and speaker labels are made by software and can be wrong. Check anything important against the recording."),
            ("The app", "TourLog is provided as is by Plantburgh Products LLC. To the extent the law allows, we are not liable for indirect or consequential losses."),
            ("Contact", f"Questions: {MAIL}."),
        ],
        delete="Delete a tour inside TourLog to erase its recording, photos and transcript. Uninstalling the app removes everything. We hold no copy.",
    ),
    "drift": dict(
        name="Drift", updated="2026-10-20",
        short="Drift saves your progress on your phone. It has no account, no ads and no internet connection of its own.",
        privacy=lambda: [
            ("Who we are", f"Drift is made by {CO}. Questions: {MAIL}."),
            ("What the game keeps", "Your level progress, coins, upgrades and settings, stored only on this phone. We never receive them."),
            ("Internet, ads and tracking", "Drift does not connect to the internet, shows no ads and has no analytics."),
            ("Backups", "If Android backup is on, Android may include Drift's save in your own Google account backup."),
            ("Deleting", "Clear Drift's storage in Android Settings or uninstall the game to erase your progress."),
            ("Children", "Drift is not directed at children under 13 and collects no personal information from anyone."),
        ],
        terms=lambda: [
            ("The game", "Drift is provided as is by Plantburgh Products LLC. In-game coins have no cash value."),
            ("Contact", f"Questions: {MAIL}."),
        ],
        delete="Clear Drift's storage in Android Settings › Apps › Drift › Storage, or uninstall the game. We hold no copy.",
    ),
    "plant-id": dict(
        name="Plantburgh Plant Id", updated="2026-10-20",
        short="To identify or diagnose a plant, the photo you scan is sent to our server and our AI provider. Your garden, reminders and scan history are stored on our servers under a guest account tied to your phone. The free tier shows ads.",
        privacy=lambda: [
            ("Who we are", f"Plantburgh Plant Id is made by {CO}. Questions: {MAIL}."),
            ("Your account", "The app signs you in as a guest tied to this phone, using Google Firebase. You can add an email address to keep your garden on a new phone. If you uninstall or clear the app's data without adding an email, a new guest starts and the old data can no longer be reached from the phone."),
            ("Photos you scan", "Each photo you scan is sent to our server (Google Cloud, United States) and to our AI provider, Anthropic, to produce the identification, diagnosis or care answer. Anthropic processes it under its commercial API terms, which do not allow using it to train models. We keep your recent scans in your history so you can look back at them."),
            ("What we store", "Your garden (plants, notes, care settings), reminders, scan history and photos, your plan and daily scan counts, stored in Google Firebase under your account."),
            ("Ads on the free tier", "The free tier shows a Google AdMob banner and, when AdMob has nothing, one of our own products or a partner offer. Google may use your phone's advertising ID, IP address and device details to show and measure ads under Google's policies. Your photos and garden are never sent to advertisers. Premium shows no ads."),
            ("Purchases", "Premium is billed by Google Play. Google tells our server which plan your account has. We never see your payment details."),
            ("Notifications", "Care reminders are scheduled on the phone."),
            ("Sharing", "We do not sell your data. We share it only with the services above that run the app (Google Firebase and Cloud, Anthropic, Google AdMob and Google Play) or when the law requires it."),
            ("Keeping and deleting", "We keep your data until you delete your account. See the account deletion page linked at the bottom for how to delete your account and everything stored under it."),
            ("Children", "Plantburgh Plant Id is not directed at children under 13."),
        ],
        terms=lambda: [
            ("AI results", "Names, diagnoses, repot checks, watering amounts and care notes come from an AI and can be wrong. Look twice before you eat, touch or treat anything based on a result."),
            ("Toxicity", "Toxicity notes are general guidance from published sources. If a person or a pet has eaten a plant, call a doctor, a vet or poison control right away."),
            ("Fair use", "A photo scan is one identify, diagnose or repot check. Free accounts get 5 scans a day and Premium gets 100, counted by the UTC day. Premium is for one person and their plants; an account that keeps hitting the cap may be slowed for a few days."),
            ("Premium", "Premium is a monthly or yearly Google Play subscription that renews until you cancel in Google Play. Refunds follow Google Play's policies."),
            ("Rules", "Do not upload photos you have no right to share, automate scans, resell results, or get around the daily limits. We can suspend accounts that do. If we retire Premium, we will not charge for time you did not get."),
            ("The app", "The app is provided as is by Plantburgh Products LLC. To the extent the law allows, we are not liable for indirect or consequential losses."),
            ("Contact", f"Questions: {MAIL}."),
        ],
        delete="<b>To delete your account and all its data</b> (garden, reminders, scan history, photos and plan), email <a href=\"mailto:contact@plantburgh.com?subject=Delete%20my%20Plant%20Id%20account\">contact@plantburgh.com</a> with the subject <i>Delete my Plant Id account</i> from the email address on the account. If you only use the app as a guest, include the account code shown in the app's More tab. We delete the account and everything stored under it within 30 days and reply to confirm. Scan counts kept for fraud and billing checks are deleted at the same time. A Google Play subscription is not cancelled by deleting the account; cancel it in Google Play first.",
    ),
}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name}: {kind}</title>
<link rel="stylesheet" href="../docs.css">
</head>
<body>
<div class="wrap">
<div class="top"><span class="tag">Plantburgh Products</span><a href="privacy.html">Privacy</a> <a href="terms.html">Terms</a> <a href="delete.html">Delete your data</a></div>
<h1>{name}: {kind}</h1>
<p class="muted">Last updated: {updated} · {co}</p>
{short}
{body}
<h2>Contact</h2>
<p>Questions: <a href="mailto:{mail}">{mail}</a>.</p>
<footer>{co} · <a href="mailto:{mail}">{mail}</a></footer>
</div>
</body>
</html>
"""


def esc(s):
    return html.escape(s, quote=False)


def write(slug, kind, sections=None, raw=None, short=""):
    a = APPS[slug]
    body = raw if raw is not None else "\n".join(
        f"<h2>{esc(t)}</h2>\n<p>{esc(b)}</p>" for t, b in sections)
    out = PAGE.format(name=esc(a["name"]), kind=kind, updated=a["updated"], co=CO, mail=MAIL,
                      short=short, body=body)
    p = ROOT / slug / {"Privacy Policy": "privacy.html", "Terms of Use": "terms.html",
                       "Delete Your Data": "delete.html"}[kind]
    p.parent.mkdir(exist_ok=True)
    p.write_text(out)
    print("wrote", p.relative_to(ROOT))


for slug, a in APPS.items():
    short = f'<div class="short"><p><b>The short version:</b> {esc(a["short"])}</p></div>'
    write(slug, "Privacy Policy", a["privacy"](), short=short)
    write(slug, "Terms of Use", a["terms"]())
    write(slug, "Delete Your Data", raw=f"<p>{a['delete']}</p>")
