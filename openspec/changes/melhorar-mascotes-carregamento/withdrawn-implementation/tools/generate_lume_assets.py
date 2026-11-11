"""Original Lume artwork, matching the user-approved style board.

Regenerate: python tools/generate_lume_assets.py
Optimize afterwards: npx --yes --package=svgo@4.0.0 svgo --folder assets/illustrations/lume --config tools/svgo-lume.config.mjs
"""
from pathlib import Path
import xml.etree.ElementTree as ET

def head(expression='calmo'):
    mouth = {'calmo': 'M71 52h14', 'alegre': 'M69 49q10 11 20 0', 'curioso': 'M76 51q4-3 8 0'}[expression]
    return f'<g id="rosto-{expression}" class="line"><rect x="48" y="18" width="60" height="48" rx="17" class="brand" stroke="var(--illu-black)"/><rect x="55" y="25" width="46" height="34" rx="11" class="black" stroke="none"/><circle class="paper" stroke="none" cx="68" cy="39" r="2.5"/><circle class="paper" stroke="none" cx="88" cy="39" r="2.5"/><path stroke="var(--illu-paper)" d="{mouth}"/><circle cx="111" cy="41" r="10" class="accent" stroke="var(--illu-black)"/><circle cx="111" cy="37" r="2" class="black" stroke="none"/><circle cx="107" cy="44" r="2" class="black" stroke="none"/><circle cx="115" cy="44" r="2" class="black" stroke="none"/></g>'

def book():
    return '<g class="line"><path class="brand" d="M18 28q24-9 46 3 22-12 46-3v58q-24-9-46 3-22-12-46-3Z"/><path stroke="var(--illu-black)" d="M64 31v58m-32-44 20 3m-20 12 20 3m24-15 20-3m-20 18 20-3"/></g>'

def character(pose):
    arms = {'pausa': 'M53 84Q34 95 39 115M102 84q17 12 13 31', 'ola': 'M53 84Q34 95 39 115M102 84q20-9 19-35', 'leitura': 'M53 84 38 99l21 11m43-26 14 15-21 11'}[pose]
    legs = {'pausa': 'M64 133v25H49m42-25v25h15', 'ola': 'M64 133v25H49m42-25 9 25h15', 'leitura': 'M64 133v25H49m42-25v25h15'}[pose]
    hands = '<circle cx="39" cy="115" r="5" class="paper"/><circle cx="115" cy="115" r="5" class="paper"/>' if pose == 'pausa' else '<circle cx="39" cy="115" r="5" class="paper"/><circle cx="121" cy="49" r="5" class="paper"/>' if pose == 'ola' else ''
    prop = '<g transform="translate(32 77) scale(.7)">' + book() + '</g>' if pose == 'leitura' else ''
    return f'''<g class="line"><ellipse cx="79" cy="164" rx="45" ry="5" class="neutral" stroke="none" opacity=".12"/><path d="{legs}"/><path d="{arms}"/>{hands}<rect x="52" y="73" width="51" height="61" rx="18" class="brand" stroke="var(--illu-black)"/><path d="m71 88 17 10-17 10Z" class="black" stroke="none"/>{head('alegre' if pose == 'ola' else 'calmo')}{prop}</g>'''

objects = {'Livro': book(), 'Claquete': '<g class="line"><rect x="22" y="31" width="84" height="58" rx="7" class="brand"/><path d="M22 47h84m-74 0 15-16m6 16 15-16m6 16 15-16" stroke="var(--illu-black)"/><path d="m57 61 20 10-20 10Z" class="black" stroke="none"/></g>', 'Marcador': '<g class="line"><path d="M47 18h34v80L64 87 47 98Z" class="brand"/><path d="M57 35h14m-14 11h14" stroke="var(--illu-black)"/></g>', 'Lupa': '<g class="line"><circle cx="58" cy="49" r="27" class="accent"/><circle cx="58" cy="49" r="17" class="black"/><path d="m77 69 23 25" stroke="var(--illu-brand)"/><path d="m48 45 5-5" stroke="var(--illu-paper)"/></g>', 'Estante': '<g class="line"><path d="M21 91h86M25 32h20v59H25Zm24-9h20v68H49Z" class="brand"/><path d="m77 31 18-5 14 60-18 5Z" class="accent"/><path d="M30 76h10m14-38h10" stroke="var(--illu-black)"/></g>', 'Conversa': '<g class="line"><path d="M30 25h68q10 0 10 10v36q0 10-10 10H58L36 97V81h-6q-10 0-10-10V35q0-10 10-10Z" class="brand"/><circle cx="45" cy="53" r="3" class="black" stroke="none"/><circle cx="64" cy="53" r="3" class="black" stroke="none"/><circle cx="83" cy="53" r="3" class="black" stroke="none"/></g>'}

PALETTE = {
    "brand": "var(--illu-brand, #f5aa32)",
    "paper": "var(--illu-paper, #fff0d5)",
    "black": "var(--illu-black, #171411)",
    "neutral": "var(--illu-neutral, #8f897c)",
    "accent": "var(--illu-accent, #d9c86a)",
}
NAMES = ("onboarding", "empty", "not-found", "error", "success", "loading", "offline", "no-results")


def scene(name):
    pose = "ola" if name in {"onboarding", "success"} else "leitura" if name == "loading" else "pausa"
    person = character(pose)
    if name in {"not-found", "error", "offline", "no-results"}:
        person = person.replace(head("calmo"), head("curioso"))
    props = {
        "onboarding": '<g transform="translate(178 99) scale(.85)">' + objects["Claquete"] + '</g>',
        "empty": '<g class="line"><path d="m194 130 20-19h58l20 19v45h-98Z" class="neutral"/><path d="M194 130h28l9 12h24l9-12h28"/><path d="M228 94h30" stroke="var(--illu-brand)"/></g>',
        "not-found": '<g class="line"><path d="M200 100h68l18 18v69h-86Z" class="paper" stroke="var(--illu-black)"/><path d="M268 100v18h18m-66 45 14-19 15 10 15-22" stroke="var(--illu-black)" stroke-dasharray="4 6"/></g>',
        "error": '<g transform="translate(178 93) scale(.85)">' + objects["Claquete"] + '</g><g class="line" stroke="var(--illu-accent)"><path d="m244 144 19 19m0-19-19 19"/></g>',
        "success": '<g class="line"><circle cx="242" cy="144" r="34" class="accent" stroke="var(--illu-black)"/><path d="m225 144 12 12 24-27" stroke="var(--illu-black)"/></g>',
        "loading": '<g class="line"><circle cx="240" cy="140" r="31" class="accent" stroke="var(--illu-black)"/><circle cx="240" cy="140" r="6" class="black" stroke="none"/><circle cx="240" cy="120" r="5" class="black" stroke="none"/><circle cx="222" cy="150" r="5" class="black" stroke="none"/><circle cx="258" cy="150" r="5" class="black" stroke="none"/></g>',
        "offline": '<g class="line"><path d="M190 139h23v29h-23m23-24h11m-11 16h11m61-21h-23v29h23m-23-24h-11m11 16h-11" stroke="var(--illu-brand)"/><path d="m235 134-5 15 10 6-5 15" stroke="var(--illu-accent)"/></g>',
        "no-results": '<g transform="translate(177 91) scale(.85)">' + objects["Lupa"] + '</g>',
    }[name]
    xml = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 240" fill="none"><g id="fundo"><path d="M48 109C40 48 127 22 173 58s119 18 116 86-123 60-184 59-54-49-57-94Z" fill="var(--illu-brand)" opacity=".08"/></g><g id="personagem" transform="translate(25 30)">' + person + '</g><g id="objetos">' + props + '</g></svg>'
    root = ET.fromstring(xml)
    for node in root.iter():
        classes = node.attrib.pop("class", "").split()
        if "line" in classes:
            node.attrib.setdefault("fill", "none")
            node.attrib.setdefault("stroke", "var(--illu-line, #fff0d5)")
            node.attrib.setdefault("stroke-width", "2")
            node.attrib.setdefault("stroke-linecap", "round")
            node.attrib.setdefault("stroke-linejoin", "round")
        for color in PALETTE:
            if color in classes: node.attrib["fill"] = PALETTE[color]
        for key,value in list(node.attrib.items()):
            for color,fallback in PALETTE.items():
                value=value.replace("var(--illu-"+color+")",fallback)
            node.attrib[key]=value
        if node.tag.rsplit("}",1)[-1] not in {"svg","g"}:
            node.attrib["vector-effect"] = "non-scaling-stroke"
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    return ET.tostring(root, encoding="unicode")


def main():
    output = Path(__file__).resolve().parents[1] / "assets/illustrations/lume"
    output.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        text=scene(name)
        (output/(name+".svg")).write_text(text,encoding="utf-8")
        print(name, len(text.encode("utf-8")))


if __name__ == "__main__":
    main()
