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
        name="Plantburgh Light Meter", updated="2026-11-11",
        short="Readings, spots, photos and projects stay on your phone. There is no account and no analytics. The free version shows ads from a small feed we run; Pro removes them. Location is optional and stays on the phone.",
        privacy=lambda: [
            ("Who we are", f"Plantburgh Light Meter is made by {CO}. Questions: {MAIL}."),
            ("What the app keeps", "Your light readings, spots, spot photos, plant checks, client projects, care reminders, home-screen widget pictures and settings. They are stored only on this phone, in the app's private storage. There is no account and we never receive them."),
            ("Sensors", "The light sensor gives the reading. The compass (the phone's motion and magnetic sensors) tells which way a window faces. Both are read on the phone only and nothing is sent anywhere."),
            ("Location (optional)", "The app asks once whether it may use your approximate location to put the real sun in the window picture. If you say no, it guesses from the phone's time zone instead. If you turn on Save spot location, new spots keep the address where they were taken; the phone's own Android address lookup turns the position into an address. Your location is kept only on this phone, never sent to us, and never tracked in the background."),
            ("Camera and photos", "Spot photos you take or pick are saved inside the app on this phone."),
            ("Internet", "The app downloads two small files: the list of ad cards (from app.giganize.work, run by us) and the Pro plan list (from plantburgh.github.io), plus the pictures for the cards. These requests carry only what any web request does, such as your IP address, and nothing about your readings. Links to our website, Play or these pages open in your browser."),
            ("Ads", "The free version shows one small card at a time: our own products, or a partner's product through an affiliate network (for example CJ). No ad network runs inside the app, there is no advertising ID, and nothing about you is used to pick the ads. Tapping a card opens it in your browser through our link counter, which counts taps per card per day and keeps no identifier. If you buy something, the partner's site and the affiliate network handle it under their own policies. Pro shows no ads."),
            ("Pro subscription and purchases", "Pro is a Google Play subscription. Google Play takes the payment and tells the app whether Pro is active; we never see your payment details. Google may collect diagnostics about purchases under Google's own privacy policy."),
            ("Notifications", "Watering and re-measure reminders are scheduled on the phone. Nothing is sent to us."),
            ("Home-screen widgets", "The widgets show copies of your spots and reminders that the app keeps on this phone. A Quick read tap reads the light sensor on the phone."),
            ("Phone assistant (optional)", "Android assistants can ask the app for a reading or a plant check through Android's app functions. What the assistant does with the answer is covered by that assistant's own privacy policy."),
            ("Sharing and backups", "Data leaves the phone only when you share a PDF report, export a file or save a backup, and you choose where it goes. If Android backup is on, Android may include the app's data in your own Google account backup."),
            ("Deleting", "Settings › Delete all my data erases everything the app saved on this phone. Uninstalling the app also removes it. We hold no copy."),
            ("Children", "The app is not directed at children under 13."),
            ("Changes", "If the app starts handling data differently, this page is updated before that version is released, with the date at the top."),
        ],
        terms=lambda: [
            ("Readings are estimates", "Phone light sensors vary by model and are not lab instruments. Readings, sun times, the compass and plant suggestions are guidance, not a guarantee of how a plant will do."),
            ("Plant safety", "Pet and toxicity notes are general guidance from published sources. If a person or pet eats a plant, call a doctor, a vet or poison control."),
            ("Free and Pro", "The app is free to use with ads and some limits (for example how many spots you can save). Pro removes ads and unlocks the extra tools and limits shown in the app before you buy. What is in Pro and the free limits can change over time; anything you already saved stays yours."),
            ("Subscription", "Pro is sold through Google Play, monthly or yearly, at the price Google Play shows before you confirm. It renews automatically at the end of each period until you cancel. Cancel any time in Google Play › Payments and subscriptions; Pro stays on until the end of the period you paid for. Refunds follow Google Play's refund policy."),
            ("Ads and partner offers", "Partner cards link to other companies' sites. Their products, prices and terms are theirs; we may earn a commission when you buy."),
            ("The app", "The app is provided as is by Plantburgh Products LLC. We work to keep it accurate but cannot promise it is error free. To the extent the law allows, we are not liable for indirect or consequential losses."),
            ("Contact", f"Questions: {MAIL}."),
        ],
        delete="Open the app, go to <b>Settings › Delete all my data</b>, and confirm. That erases every reading, spot, photo, project and reminder on this phone. Uninstalling the app also removes it. We hold no copy. Deleting data does not cancel a Pro subscription; cancel it in Google Play.",
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
            ("Keeping and deleting", "We keep your data until you delete your account. Delete it any time in the app (More › Delete account), which erases everything stored under it right away, or follow the account deletion page linked at the top."),
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
        delete="<b>In the app:</b> open <b>More › Delete account</b> (or <b>Settings › Delete account</b>) and confirm. That deletes your account and everything stored under it right away: garden, notes, reminders, scan history, scan photos, usage counts and advisor threads. A Google Play subscription is not cancelled by deleting the account; cancel it in Google Play first.</p><p><b>Without the app:</b> email <a href=\"mailto:contact@plantburgh.com?subject=Delete%20my%20Plant%20Id%20account\">contact@plantburgh.com</a> with the subject <i>Delete my Plant Id account</i> from the email address on the account. If you only use the app as a guest, include the account code shown in the app's More tab. We delete the account and everything stored under it within 30 days and reply to confirm. Scan counts kept for fraud and billing checks are deleted at the same time.",
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


# ---------------------------------------------------------------------------
# Replicost: published straight from the app's own Markdown (app/assets/legal).
RC_LEGAL = pathlib.Path("/Users/user11/Developer/Replicost-sourced/app/assets/legal")


def md_to_html(md):
    """Small Markdown subset: #/## headings, paragraphs, - and 1. lists, **bold**, `code`."""
    inline = lambda t: re.sub(r"`([^`]+)`", r"<code>\1</code>",
                              re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(t, quote=False)))
    out, para, lst = [], [], None

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst:
            tag, items = lst
            out.append(f"<{tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{tag}>"); lst = None

    for line in md.splitlines():
        s = line.strip()
        if not s:
            flush(); continue
        if s.startswith("# "):
            flush(); continue  # page title comes from the template
        if s.startswith("## "):
            flush(); out.append("<h2>" + inline(s[3:]) + "</h2>"); continue
        m = re.match(r"^(-|\d+\.)\s+(.*)", s)
        if m:
            if para:
                out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
            tag = "ul" if m.group(1) == "-" else "ol"
            if not lst or lst[0] != tag:
                if lst: flush()
                lst = (tag, [])
            lst[1].append(m.group(2)); continue
        if lst and line.startswith("   "):
            lst[1][-1] += " " + s; continue
        if lst: flush()
        para.append(s)
    flush()
    return "\n".join(out)


APPS["replicost"] = dict(name="Replicost", updated="2026-10-20",
                         short="", privacy=lambda: [], terms=lambda: [],
                         delete="Open Replicost and choose <b>You › Erase everything on this device</b>. That removes every saved estimate, project, ledger, report, note, your shop profile and your stored Gemini key. Nothing is kept on a server. Photos you identified were sent to Google under your own key; delete them from your Google account.")
for kind, fname in (("Privacy Policy", "privacy.md"), ("Terms of Use", "terms.md")):
    write("replicost", kind, raw=md_to_html((RC_LEGAL / fname).read_text()))
write("replicost", "Delete Your Data", raw=f"<p>{APPS['replicost']['delete']}</p>")

# ---------------------------------------------------------------------------
# Light Meter Spanish pages (the app links /light-meter/es/privacy.html and terms.html).
CO_ES = "Plantburgh Products LLC, una empresa de Pensilvania propiedad de Plantburgh LLC"
LM_ES_PRIV = [
    ("Quiénes somos", f"Plantburgh Light Meter es creado por {CO_ES}. Preguntas: {MAIL}."),
    ("Qué guarda la app", "Tus lecturas de luz, lugares, fotos de lugares, revisiones de plantas, proyectos de clientes, recordatorios de cuidado, imágenes de los widgets y ajustes. Se guardan solo en este teléfono, en el almacenamiento privado de la app. No hay cuenta y nunca los recibimos."),
    ("Sensores", "El sensor de luz da la lectura. La brújula (los sensores de movimiento y magnéticos del teléfono) indica hacia dónde mira una ventana. Ambos se leen solo en el teléfono y no se envía nada."),
    ("Ubicación (opcional)", "La app pregunta una vez si puede usar tu ubicación aproximada para poner el sol real en la ventana. Si dices que no, la calcula a partir de la zona horaria del teléfono. Si activas Guardar ubicación del lugar, los lugares nuevos guardan la dirección donde se tomaron; la búsqueda de direcciones de Android convierte la posición en una dirección. Tu ubicación se guarda solo en este teléfono, nunca se nos envía y nunca se rastrea en segundo plano."),
    ("Cámara y fotos", "Las fotos de lugares que tomas o eliges se guardan dentro de la app en este teléfono."),
    ("Internet", "La app descarga dos archivos pequeños: la lista de tarjetas de anuncios (de app.giganize.work, nuestro) y la lista de planes Pro (de plantburgh.github.io), además de las imágenes de las tarjetas. Esas solicitudes llevan solo lo que lleva cualquier solicitud web, como tu dirección IP, y nada sobre tus lecturas. Los enlaces a nuestro sitio, a Play o a estas páginas se abren en tu navegador."),
    ("Anuncios", "La versión gratuita muestra una tarjeta pequeña a la vez: nuestros productos o el producto de un socio a través de una red de afiliados (por ejemplo, CJ). No hay ninguna red publicitaria dentro de la app, no hay ID de publicidad y nada sobre ti se usa para elegir los anuncios. Al tocar una tarjeta se abre en tu navegador a través de nuestro contador de enlaces, que cuenta los toques por tarjeta y por día y no guarda ningún identificador. Si compras algo, el sitio del socio y la red de afiliados lo gestionan con sus propias políticas. Pro no muestra anuncios."),
    ("Suscripción Pro y compras", "Pro es una suscripción de Google Play. Google Play cobra el pago e informa a la app si Pro está activo; nunca vemos tus datos de pago. Google puede recopilar diagnósticos de las compras según su propia política de privacidad."),
    ("Notificaciones", "Los recordatorios de riego y de volver a medir se programan en el teléfono. No se nos envía nada."),
    ("Widgets de la pantalla de inicio", "Los widgets muestran copias de tus lugares y recordatorios que la app guarda en este teléfono. Un toque en Lectura rápida lee el sensor de luz en el teléfono."),
    ("Asistente del teléfono (opcional)", "Los asistentes de Android pueden pedirle a la app una lectura o una revisión de planta mediante las funciones de apps de Android. Lo que el asistente haga con la respuesta se rige por su propia política de privacidad."),
    ("Compartir y copias de seguridad", "Los datos salen del teléfono solo cuando compartes un informe PDF, exportas un archivo o guardas una copia de seguridad, y tú eliges a dónde van. Si la copia de seguridad de Android está activada, Android puede incluir los datos de la app en la copia de tu propia cuenta de Google."),
    ("Borrar", "Ajustes › Borrar todos mis datos elimina todo lo que la app guardó en este teléfono. Desinstalar la app también lo elimina. No guardamos ninguna copia."),
    ("Niños", "La app no está dirigida a menores de 13 años."),
    ("Cambios", "Si la app empieza a tratar los datos de otra forma, esta página se actualiza antes de publicar esa versión, con la fecha arriba."),
]
LM_ES_TERMS = [
    ("Las lecturas son estimaciones", "Los sensores de luz de los teléfonos varían según el modelo y no son instrumentos de laboratorio. Las lecturas, las horas de sol, la brújula y las sugerencias de plantas son una guía, no una garantía de cómo le irá a una planta."),
    ("Seguridad de las plantas", "Las notas sobre mascotas y toxicidad son una guía general basada en fuentes publicadas. Si una persona o una mascota come una planta, llama a un médico, a un veterinario o al centro de toxicología."),
    ("Gratis y Pro", "La app se puede usar gratis con anuncios y algunos límites (por ejemplo, cuántos lugares puedes guardar). Pro quita los anuncios y desbloquea las herramientas y límites extra que la app muestra antes de comprar. Lo que incluye Pro y los límites gratuitos pueden cambiar con el tiempo; lo que ya guardaste sigue siendo tuyo."),
    ("Suscripción", "Pro se vende a través de Google Play, mensual o anual, al precio que Google Play muestra antes de que confirmes. Se renueva automáticamente al final de cada periodo hasta que la canceles. Cancela cuando quieras en Google Play › Pagos y suscripciones; Pro sigue activo hasta el final del periodo pagado. Los reembolsos siguen la política de reembolsos de Google Play."),
    ("Anuncios y ofertas de socios", "Las tarjetas de socios enlazan a sitios de otras empresas. Sus productos, precios y términos son suyos; podemos ganar una comisión cuando compras."),
    ("La app", "La app se ofrece tal cual por Plantburgh Products LLC. Trabajamos para que sea precisa, pero no podemos prometer que no tenga errores. En la medida que la ley lo permita, no somos responsables de pérdidas indirectas o consecuentes."),
    ("Contacto", f"Preguntas: {MAIL}."),
]
PAGE_ES = (PAGE.replace('lang="en"', 'lang="es"').replace("../docs.css", "../../docs.css")
           .replace(">Privacy<", ">Privacidad<").replace(">Terms<", ">Términos<")
           .replace('<a href="delete.html">Delete your data</a>', '<a href="../delete.html">Borrar tus datos</a> <a href="../privacy.html">English</a>')
           .replace("Last updated:", "Última actualización:").replace("<h2>Contact</h2>", "<h2>Contacto</h2>")
           .replace("<p>Questions:", "<p>Preguntas:"))
for kind, secs, fname in (("Política de privacidad", LM_ES_PRIV, "privacy.html"), ("Términos de uso", LM_ES_TERMS, "terms.html")):
    body = "\n".join(f"<h2>{esc(t)}</h2>\n<p>{esc(b)}</p>" for t, b in secs)
    short = ('<div class="short"><p><b>En resumen:</b> Las lecturas, lugares, fotos y proyectos se quedan en tu teléfono. '
             'No hay cuenta ni analíticas. La versión gratuita muestra anuncios de un pequeño listado que gestionamos nosotros; Pro los quita. '
             'La ubicación es opcional y se queda en el teléfono.</p></div>') if fname == "privacy.html" else ""
    out = PAGE_ES.format(name="Plantburgh Light Meter", kind=kind, updated="2026-11-11", co=CO_ES, mail=MAIL, short=short, body=body)
    p = ROOT / "light-meter" / "es" / fname
    p.parent.mkdir(exist_ok=True); p.write_text(out); print("wrote", p.relative_to(ROOT))
