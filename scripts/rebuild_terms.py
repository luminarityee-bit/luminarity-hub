# -*- coding: utf-8 -*-
"""
LUMINARITY HUB — rebuild_terms.py

Σαρώνει τον φάκελο αιτησεις/, ξανα-encode-άρει τα PDFs σε base64
και ενημερώνει τα blocks PDF_TERMS, FIBER_PDFS, PDF_AERIO_B64,
PDF_GREEN_PASS_B64 στο ΕΦΑΡΜΟΓΗ/fillContract.html.

Χρήση: double-click "Ενημέρωση Όρων.bat" στον LUMINARITY_HUB.
"""

import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AITISEIS = ROOT / 'αιτησεις'
FILL = ROOT / 'ΕΦΑΡΜΟΓΗ' / 'fillContract.html'

# termsVariant key → relative path μέσα στο αιτησεις/
PDF_TERMS_MAP = {
    'myHomeEnter':          'ρευμα/οικιακα/myHomeEnter.pdf',
    'g1':                   'ρευμα/οικιακα/Γ1.pdf',
    'myHomeplan':           'ρευμα/οικιακα/myHomePlan.pdf',
    'myHome4AllOneRate':    'ρευμα/οικιακα/myHome4AllOneRate.pdf',
    'myHome4All':           'ρευμα/οικιακα/myHome4All.pdf',
    'myHome4Students':      'ρευμα/οικιακα/myHome4Students.pdf',
    'myHomeMaxima':         'ρευμα/οικιακα/myHomeMaxima.pdf',
    'myHomeEnterTwo':       'ρευμα/οικιακα/myHomeEnterTwo.pdf',
    'myBusiness4All':       'ρευμα/επαγγελματικα/myBusiness4All.pdf',
    'myBusiness4AllPlus':   'ρευμα/επαγγελματικα/myBusiness4AllPlus.pdf',
    'myBusinessEnter':      'ρευμα/επαγγελματικα/myBusinessEnter.pdf',
    'agrotiko':             'ρευμα/επαγγελματικα/Αγροτικό.pdf',
    'g21':                  'ρευμα/επαγγελματικα/Γ21.pdf',
    'g22':                  'ρευμα/επαγγελματικα/Γ22.pdf',
    'g23':                  'ρευμα/επαγγελματικα/Γ23.pdf',
    'myHomeGasControl':     'αεριο/οικιακα/myHomeGasControl.pdf',
    'myHomeGasBenefit':     'αεριο/οικιακα/myHomeGasBenefit.pdf',
    'myBuildingGasControl': 'αεριο/οικιακα/myBuildingGasControl.pdf',
    'myBusinessGasBenefit': 'αεριο/επαγγελματικα/myBusinessGasBenefit.pdf',
}

FIBER_KEYS = [
    '500Mbps_noStatic_noRepeater', '500Mbps_noStatic_Repeater',
    '500Mbps_Static_noRepeater',   '500Mbps_Static_Repeater',
    '1Gbps_noStatic_noRepeater',   '1Gbps_noStatic_Repeater',
    '1Gbps_Static_noRepeater',     '1Gbps_Static_Repeater',
    '2.5Gbps_noStatic_noRepeater', '2.5Gbps_noStatic_Repeater',
    '2.5Gbps_Static_noRepeater',   '2.5Gbps_Static_Repeater',
]

SINGLES = {
    'PDF_AERIO_B64':      'αεριο/ΣΥΜΒΑΣΗ ΑΕΡΙΟΥ.pdf',
    'PDF_GREEN_PASS_B64': 'ρευμα/οικιακα/GreenPass.pdf',
}


def b64(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode('ascii')


def main() -> int:
    if not AITISEIS.is_dir():
        print(f'❌ Δεν βρέθηκε ο φάκελος: {AITISEIS}')
        return 1
    if not FILL.is_file():
        print(f'❌ Δεν βρέθηκε το αρχείο: {FILL}')
        return 1

    print('=' * 60)
    print('LUMINARITY HUB — Ενημέρωση Ειδικών Όρων')
    print('=' * 60)
    size_mb = FILL.stat().st_size / (1024 * 1024)
    print(f'\n[1/4] Διάβασμα fillContract.html ({size_mb:.1f} MB)...')
    html = FILL.read_text(encoding='utf-8')
    original_len = len(html)

    updated = {'singles': 0, 'fiber': 0, 'terms': 0}
    skipped = []

    # ──────────────────────────────────────────────────────────────
    # 1. SINGLES (PDF_AERIO_B64, PDF_GREEN_PASS_B64)
    # ──────────────────────────────────────────────────────────────
    print('\n[2/4] Generic templates (αέριο, green pass)...')
    for var, rel in SINGLES.items():
        pdf = AITISEIS / rel
        if not pdf.is_file():
            skipped.append(f'{var}  (αρχείο λείπει: {rel})')
            print(f'  ⚠ SKIP  {var}')
            continue
        new_b64 = b64(pdf)
        pat = re.compile(r'(const\s+' + re.escape(var) + r'\s*=\s*")[^"]*(")')
        m = pat.search(html)
        if not m:
            skipped.append(f'{var}  (pattern δεν βρέθηκε στο fillContract.html)')
            print(f'  ⚠ SKIP  {var}')
            continue
        html = pat.sub(
            lambda mm, nb=new_b64: mm.group(1) + nb + mm.group(2), html, count=1
        )
        updated['singles'] += 1
        print(f'  ✔ {var:22s} ← {rel}  ({pdf.stat().st_size//1024} KB)')

    # ──────────────────────────────────────────────────────────────
    # 2. FIBER_PDFS (single-line dict)
    # ──────────────────────────────────────────────────────────────
    print('\n[3/4] Fiber PDFs...')
    fiber_dict = {}
    for k in FIBER_KEYS:
        pdf = AITISEIS / 'fiber' / f'{k}.pdf'
        if not pdf.is_file():
            skipped.append(f'fiber/{k}  (αρχείο λείπει)')
            print(f'  ⚠ SKIP  {k}')
            continue
        fiber_dict[k] = b64(pdf)
        print(f'  ✔ {k}')

    if fiber_dict:
        body = ','.join(f'"{k}":"{v}"' for k, v in fiber_dict.items())
        new_fiber = 'const FIBER_PDFS = {' + body + '};'
        pat = re.compile(r'const\s+FIBER_PDFS\s*=\s*\{[^\n]*\};')
        if pat.search(html):
            html = pat.sub(new_fiber, html, count=1)
            updated['fiber'] = len(fiber_dict)
        else:
            skipped.append('FIBER_PDFS  (pattern δεν βρέθηκε)')

    # ──────────────────────────────────────────────────────────────
    # 3. PDF_TERMS (multi-line dict)
    # ──────────────────────────────────────────────────────────────
    print('\n[4/4] PDF_TERMS (όροι ανά πρόγραμμα)...')
    terms_lines = []
    for k, rel in PDF_TERMS_MAP.items():
        pdf = AITISEIS / rel
        if not pdf.is_file():
            skipped.append(f'PDF_TERMS[{k}]  (αρχείο λείπει: {rel})')
            terms_lines.append(f'  {k}: ""')
            print(f'  ⚠ SKIP  {k}')
            continue
        terms_lines.append(f'  {k}: "{b64(pdf)}"')
        updated['terms'] += 1
        print(f'  ✔ {k}')

    new_terms_block = 'const PDF_TERMS = {\n' + ',\n'.join(terms_lines) + '\n};'
    pat = re.compile(r'const\s+PDF_TERMS\s*=\s*\{.*?\n\};', re.DOTALL)
    if pat.search(html):
        html = pat.sub(new_terms_block, html, count=1)
    else:
        skipped.append('PDF_TERMS  (pattern δεν βρέθηκε)')

    # ──────────────────────────────────────────────────────────────
    # save
    # ──────────────────────────────────────────────────────────────
    FILL.write_text(html, encoding='utf-8')
    new_mb = FILL.stat().st_size / (1024 * 1024)

    print('\n' + '=' * 60)
    print('✅ ΟΛΟΚΛΗΡΩΘΗΚΕ')
    print('=' * 60)
    print(f'  • Generic templates : {updated["singles"]}/{len(SINGLES)}')
    print(f'  • Fiber PDFs        : {updated["fiber"]}/{len(FIBER_KEYS)}')
    print(f'  • PDF_TERMS όροι    : {updated["terms"]}/{len(PDF_TERMS_MAP)}')
    print(f'  • Μέγεθος αρχείου   : {size_mb:.1f} MB → {new_mb:.1f} MB')
    if skipped:
        print(f'\n⚠ Παραλείψεις ({len(skipped)}):')
        for s in skipped:
            print(f'   - {s}')
    print('\n→ Κάνε refresh (F5) στο hub.html για να φορτωθούν οι νέοι όροι.')
    return 0


if __name__ == '__main__':
    try:
        rc = main()
    except Exception as e:
        print(f'\n❌ ΣΦΑΛΜΑ: {type(e).__name__}: {e}')
        rc = 1
    input('\nΠάτα Enter για κλείσιμο...')
    sys.exit(rc)
