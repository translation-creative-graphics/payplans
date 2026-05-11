#!/usr/bin/env python3
"""Build CRE8 Members (PayPlans) language pack ZIPs — one per locale, with Joomla XML manifest."""

import re
import zipfile
from datetime import date
from pathlib import Path

DIST = Path('dist')
DIST.mkdir(exist_ok=True)

LANG_NAMES = {
    "af-ZA": "Afrikaans",               "am-ET": "Amharic",
    "ar-SA": "Arabic",                  "az-AZ": "Azerbaijani",
    "be-BY": "Belarusian",              "bg-BG": "Bulgarian",
    "bn-BD": "Bengali",                 "bs-BA": "Bosnian",
    "ca-ES": "Catalan",                 "cs-CZ": "Czech",
    "da-DK": "Danish",                  "de-AT": "German (Austria)",
    "de-CH": "German (Switzerland)",    "de-DE": "German",
    "el-GR": "Greek",                   "es-AR": "Spanish (Argentina)",
    "es-BO": "Spanish (Bolivia)",       "es-CL": "Spanish (Chile)",
    "es-CO": "Spanish (Colombia)",      "es-CR": "Spanish (Costa Rica)",
    "es-EC": "Spanish (Ecuador)",       "es-ES": "Spanish",
    "es-MX": "Spanish (Mexico)",        "es-NI": "Spanish (Nicaragua)",
    "es-PE": "Spanish (Peru)",          "es-SV": "Spanish (El Salvador)",
    "es-US": "Spanish (US)",            "es-VE": "Spanish (Venezuela)",
    "et-EE": "Estonian",                "eu-ES": "Basque",
    "fa-IR": "Persian",                 "fi-FI": "Finnish",
    "fr-BE": "French (Belgium)",        "fr-CA": "French (Canada)",
    "fr-CH": "French (Switzerland)",    "fr-FR": "French",
    "gl-ES": "Galician",                "gu-IN": "Gujarati",
    "he-IL": "Hebrew",                  "hi-IN": "Hindi",
    "hr-HR": "Croatian",                "hu-HU": "Hungarian",
    "hy-AM": "Armenian",                "id-ID": "Indonesian",
    "is-IS": "Icelandic",               "it-IT": "Italian",
    "ja-JP": "Japanese",                "ka-GE": "Georgian",
    "kk-KZ": "Kazakh",                  "km-KH": "Khmer",
    "ko-KR": "Korean",                  "lt-LT": "Lithuanian",
    "lv-LV": "Latvian",                 "mk-MK": "Macedonian",
    "mn-MN": "Mongolian",               "mr-IN": "Marathi",
    "ms-MY": "Malay",                   "nb-NO": "Norwegian",
    "nl-BE": "Dutch (Belgium)",         "nl-NL": "Dutch",
    "pl-PL": "Polish",                  "pt-BR": "Portuguese (Brazil)",
    "pt-PT": "Portuguese",              "ro-RO": "Romanian",
    "ru-RU": "Russian",                 "sk-SK": "Slovak",
    "sl-SI": "Slovenian",               "sq-AL": "Albanian",
    "sr-RS": "Serbian",                 "sv-SE": "Swedish",
    "sw-KE": "Swahili",                 "ta-IN": "Tamil",
    "te-IN": "Telugu",                  "th-TH": "Thai",
    "tr-TR": "Turkish",                 "uk-UA": "Ukrainian",
    "ur-PK": "Urdu",                    "vi-VN": "Vietnamese",
    "zh-CN": "Chinese (Simplified)",    "zh-HK": "Chinese (Hong Kong)",
    "zh-TW": "Chinese (Traditional)",
}

VERSION      = "6.0"
CREATED      = date.today().strftime("%-d %B %Y")
AUTHOR       = "CRE8"
AUTHOR_URL   = "https://cre8.social"
AUTHOR_EMAIL = "support@birdgraphics.ch"


def make_manifest(locale: str, name: str, admin_files: list, site_files: list) -> str:
    def file_tags(files):
        return "\n".join(f"            <filename>{f}</filename>" for f in files)

    return f"""<?xml version="1.0" encoding="utf-8"?>
<extension type="file" version="3.0.0" method="upgrade">
\t<name>CRE8 Members - Language Pack {name} ({locale})</name>
\t<version>{VERSION}</version>
\t<creationDate>{CREATED}</creationDate>
\t<author>{AUTHOR}</author>
\t<authorEmail>{AUTHOR_EMAIL}</authorEmail>
\t<authorUrl>{AUTHOR_URL}</authorUrl>
\t<copyright>Copyright {date.today().year} {AUTHOR}. All rights reserved.</copyright>
\t<license>GPL License</license>
\t<description>{name} Language Pack for CRE8 Members {VERSION}</description>
\t<fileset>
\t\t<files folder="administrator/language/{locale}" target="administrator/language/{locale}">
{file_tags(admin_files)}
\t\t</files>
\t\t<files folder="language/{locale}" target="language/{locale}">
{file_tags(site_files)}
\t\t</files>
\t</fileset>
</extension>
"""


locales = sorted([
    d.name for d in Path('language').iterdir()
    if d.is_dir()
    and d.name != 'en-GB'
    and re.match(r'^[a-z]{2}-[A-Z]{2}$', d.name)
])

for locale in locales:
    name = LANG_NAMES.get(locale, locale)

    site_dir  = Path('language') / locale
    admin_dir = Path('administrator') / 'language' / locale

    site_files  = sorted(f.name for f in site_dir.iterdir())  if site_dir.exists()  else []
    admin_files = sorted(f.name for f in admin_dir.iterdir()) if admin_dir.exists() else []

    manifest = make_manifest(locale, name, admin_files, site_files)
    manifest_name = f'payplans_{locale}.xml'

    zip_path = DIST / f'com_payplans_{locale}.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(manifest_name, manifest)

        for f in sorted(site_dir.iterdir()) if site_dir.exists() else []:
            zf.write(f, f'language/{locale}/{f.name}')

        for f in sorted(admin_dir.iterdir()) if admin_dir.exists() else []:
            zf.write(f, f'administrator/language/{locale}/{f.name}')

    print(f'Built {zip_path.name}  ({zip_path.stat().st_size:,} bytes)')

print(f'\nTotal: {len(locales)} language packs')
