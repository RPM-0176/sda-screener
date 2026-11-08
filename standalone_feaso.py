"""Radius SDA Feasibility – standalone Excel workbook (Jason's own Mac copy).

Type a suburb + state (or pick the SA4 / SA3), land, price and rent category on
'Start here'. Rates and demand are looked up from the NDIS tables inside the
workbook; all five Radius builds are worked out on their own itemised sheets,
all driven by one shared Cost library; the Overview compares them and picks the
best build that fits the site.
"""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as CL
import itemised_feaso as F

FI, FN, FB, FG, FT, FW, FH = F.FI, F.FN, F.FB, F.FG, F.FT, F.FW, F.FH
F_IN, F_HEAD, F_SEC, F_SUB, F_KEY = F.F_IN, F.F_HEAD, F.F_SEC, F.F_SUB, F.F_KEY
FL = Font(name='Arial', size=10, color='007A3D')      # green = linked to another sheet
M, P, P1 = F.M, F.P, F.P1
MODELS = F.MODELS
SHEET = {'2p': '2P House', '3p': '3P House', 'dp': '2P Duplex', 'd3': '3P Duplex', 'hv': 'House + Villa'}
SUFFIX = {'2p': '2', '3p': '3', 'dp': '2', 'd3': '3', 'hv': '2'}
PTS = {'2p': 2, '3p': 3, 'dp': 4, 'd3': 6, 'hv': 3}
ST = "'Start here'"


def _w(ws, ref, v, font=FN, fmt=None, fill=None, align=None, wrap=False):
    c = ws[ref]; c.value = v; c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if align or wrap: c.alignment = Alignment(horizontal=align, vertical='center', wrap_text=wrap)
    return c


# ---------------------------------------------------------------- data sheets ---
def _data_sheets(wb, D):
    # Rates (one row per SA4)
    ws = wb.create_sheet('Rates')
    hdr = ['key', 'state', 'sa4', 'd', 'il2', 'fa2', 'hps2', 'il3', 'fa3', 'hps3', 'il1v', 'fa1v', 'hps1v']
    nice = ['Key', 'State', 'SA4', 'Participants needing SDA (SA4)', 'IL 2-res house', 'FA 2-res house', 'HPS 2-res house',
            'IL 3-res house', 'FA 3-res house', 'HPS 3-res house', 'IL 1-res villa', 'FA 1-res villa', 'HPS 1-res villa']
    for i, h in enumerate(hdr, 1):
        _w(ws, f'{CL(i)}1', h, FH, fill=F_SUB)
        _w(ws, f'{CL(i)}2', nice[i-1], FB, fill=F_SUB, wrap=True)
    rows = sorted(D['SDA'], key=lambda r: (r['st'], r['sa4']))
    for r_i, r in enumerate(rows, 3):
        vals = [f"{r['st'].upper()} – {r['sa4']}", r['st'].upper(), r['sa4']] + [r.get(k, 0) for k in hdr[3:]]
        for i, v in enumerate(vals, 1):
            c = ws.cell(r_i, i, v); c.font = FN
            if i > 4: c.number_format = M
    ws.column_dimensions['A'].width = 44; ws.column_dimensions['C'].width = 36
    for i in range(4, 14): ws.column_dimensions[CL(i)].width = 13
    ws.row_dimensions[2].height = 30
    ws.freeze_panes = 'D3'
    n_rates = len(rows) + 2
    _w(ws, f'O1', 'NDIS SDA price limits 2026-27 (per participant p.a.), as used in the Radius SDA Screener. Demand: NDIS Quarterly Performance Report Q1 2026.', FG)

    # Demand by SA3
    ws = wb.create_sheet('Demand SA3')
    hdr = ['key', 'state', 'sa3', 'sa4', 'inUse', 'elig', 'total', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'cap13', 'gap']
    nice = ['Key', 'State', 'SA3', 'SA4', 'SDA in use', 'Eligible, not yet using', 'Total needing SDA', 'Enrolled 1-res',
            '2-res', '3-res', '4-res', '5-res', '6+-res', '1–3 resident places', 'Gap (total − 1–3 places)']
    for i, h in enumerate(hdr, 1):
        _w(ws, f'{CL(i)}1', h, FH, fill=F_SUB); _w(ws, f'{CL(i)}2', nice[i-1], FB, fill=F_SUB, wrap=True)
    rows = sorted(D['SA3D'], key=lambda r: (r['st'], r['sa3']))
    for r_i, r in enumerate(rows, 3):
        vals = [f"{r['st'].upper()} – {r['sa3']}", r['st'].upper(), r['sa3'], r['sa4']] + [r.get(k, 0) for k in hdr[4:14]]
        for i, v in enumerate(vals, 1):
            ws.cell(r_i, i, v).font = FN
        ws.cell(r_i, 15, f'=G{r_i}-N{r_i}').font = FN
    ws.column_dimensions['A'].width = 40; ws.column_dimensions['C'].width = 30; ws.column_dimensions['D'].width = 34
    ws.row_dimensions[2].height = 42
    ws.freeze_panes = 'E3'
    n_sa3 = len(rows) + 2
    _w(ws, 'Q1', 'Source: NDIS Quarterly Performance Report Q1 2026 (Tables P.15 and P.17), as at 31 March 2026.', FG)

    # Pipeline by SA4
    ws = wb.create_sheet('Pipeline')
    hdr = ['key', 'h_il', 'h_fa', 'h_hps', 'v_il', 'v_fa', 'v_hps', 'a_il', 'a_fa', 'a_hps', 'tot']
    nice = ['Key (State – SA4)', 'House IL', 'House FA', 'House HPS', 'Villa IL', 'Villa FA', 'Villa HPS', 'Apt IL', 'Apt FA', 'Apt HPS', 'Total']
    for i, h in enumerate(hdr, 1):
        _w(ws, f'{CL(i)}1', h, FH, fill=F_SUB); _w(ws, f'{CL(i)}2', nice[i-1], FB, fill=F_SUB)
    rows = sorted(D['PIPE'], key=lambda r: (r['st'], r['sa4']))
    for r_i, r in enumerate(rows, 3):
        ws.cell(r_i, 1, f"{r['st'].upper()} – {r['sa4']}").font = FN
        for i, k in enumerate(hdr[1:], 2):
            ws.cell(r_i, i, r.get(k, 0)).font = FN
    ws.column_dimensions['A'].width = 44
    _w(ws, 'M1', 'SDA dwellings under construction (not yet enrolled). NDIS Quarterly Performance Report Q1 2026, Table P.16.', FG)

    # Suburbs -> SA4 / SA3
    ws = wb.create_sheet('Suburbs')
    for i, h in enumerate(['Key (SUBURB|STATE)', 'SA4', 'SA3'], 1):
        _w(ws, f'{CL(i)}1', h, FB, fill=F_SUB)
    r_i = 2
    for st, subs in D['SUBURB_SA4'].items():
        for sub, v in sorted(subs.items()):
            ws.cell(r_i, 1, f'{sub}|{st.upper()}'); ws.cell(r_i, 2, v[0]); ws.cell(r_i, 3, v[1] if len(v) > 1 else '')
            r_i += 1
    ws.column_dimensions['A'].width = 40; ws.column_dimensions['B'].width = 36; ws.column_dimensions['C'].width = 30
    return n_rates, n_sa3


# ---------------------------------------------------------------- cost library ---
def _library(wb, rules, lib=None):
    lib = lib or {}
    ws = wb.create_sheet('Cost library')
    ws.sheet_view.showGridLines = False
    _w(ws, 'A1', 'Cost library – the Radius standard', FT)
    _w(ws, 'A2', 'Change a rate, quantity or on/off here and it flows to all five build sheets. To change one build only, type over the cell on that build sheet.', FG)
    # columns: A key, B section, C line, D GST, E-I rate per model, J-N qty per model, O-S on (1/0) per model, T note
    heads = ['Key', 'Section', 'Line', 'GST'] + [f'Rate {SHEET[m]}' for m in MODELS] + [f'Qty {SHEET[m]}' for m in MODELS] \
        + [f'On {SHEET[m]}' for m in MODELS] + ['Notes']
    for i, h in enumerate(heads, 1):
        _w(ws, f'{CL(i)}4', h, FH, fill=F_SUB, wrap=True, align='center')
    ws.row_dimensions[4].height = 40
    widths = [9, 22, 46, 6] + [11]*5 + [7]*5 + [6]*5 + [34]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[CL(i)].width = w
    ref = {}
    r = 5
    secs = [('Consultants & design', F.CONSULTANTS), ('Council, authority & site works', F.SITEWORKS),
            ('Site security & monitoring', F.SECURITY), ('Furniture & fit-out', F.FURNITURE)]
    for sec, items in secs:
        for key, label, rate, qty, on, gst, note in items:
            vals = [key, sec, label, gst]
            for i, v in enumerate(vals, 1):
                ws.cell(r, i, v).font = FG if i == 1 else FN
            for j, m in enumerate(MODELS):
                for col0, v, fmt in [(5, F._rate(rate, m), M), (10, qty[m], '0.##'), (15, 1 if on[m] else 0, '0')]:
                    c = ws.cell(r, col0 + j, v); c.font = FI; c.fill = F_IN; c.number_format = fmt; c.alignment = Alignment(horizontal='center') if col0 > 5 else Alignment()
            ws.cell(r, 20, note).font = FG
            ref[key] = r
            r += 1
    # other standard figures (single values)
    r += 1
    _w(ws, f'A{r}', 'Other standard figures', FB, fill=F_SEC)
    for c in range(2, 21): ws.cell(r, c).fill = F_SEC
    r += 1
    singles = [('leg', 'Legal & conveyancing', 1000, M), ('pexa', 'PEXA settlement fee', 495, M), ('val', 'Valuation', 3500, M),
               ('ba', "Radius buyer's advocacy (% of price, + GST)", 0.04, P1), ('pm', 'Radius PM fee (% of build contract, + GST)', 0.08, P1),
               ('cg', 'Construction contingency (% of contract)', 0.03, P1), ('villa', 'Builder contract – villa', 350000, M),
               ('mkt', 'SDA marketing fee per title', 1000, M), ('duty_nsw', 'Stamp duty NSW (flat %, VIC uses the scale)', 0.0575, P),
               ('duty_qld', 'Stamp duty QLD (flat %)', 0.0575, P)]
    for key, label, v, fmt in singles:
        if isinstance(lib.get(key), (int, float)): v = lib[key]
        ws.cell(r, 1, key).font = FG; ws.cell(r, 3, label).font = FN
        c = ws.cell(r, 5, v); c.font = FI; c.fill = F_IN; c.number_format = fmt
        ref[key] = r; r += 1
    # house build contract per model
    ws.cell(r, 1, 'house').font = FG; ws.cell(r, 3, 'Builder contract – per house').font = FN
    hb = lib.get('house') if isinstance(lib.get('house'), dict) else {}
    for j, m in enumerate(MODELS):
        v = hb.get(m) if isinstance(hb.get(m), (int, float)) else 900000
        c = ws.cell(r, 5 + j, v); c.font = FI; c.fill = F_IN; c.number_format = M
    ref['house'] = r; r += 2
    # site rules
    _w(ws, f'A{r}', 'Site rules (minimum to fit the build)', FB, fill=F_SEC)
    for c in range(2, 21): ws.cell(r, c).fill = F_SEC
    r += 1
    for key, label in [('minLand', 'Minimum land (m²)'), ('minFrontage', 'Minimum frontage (m)'), ('minDepth', 'Minimum depth (m, 0 = not tested)')]:
        ws.cell(r, 1, key).font = FG; ws.cell(r, 3, label).font = FN
        for j, m in enumerate(MODELS):
            c = ws.cell(r, 5 + j, rules[m][key]); c.font = FI; c.fill = F_IN; c.number_format = '0.##'
        ref[key] = r; r += 1
    ws.cell(r, 3, 'Note: Pat Ikonomidis (Feb 2026): side-by-side duplex on 20 m frontage needs at least 38 m depth.').font = FG
    ws.freeze_panes = 'D5'
    return ref


def _lib(col0, j, row):
    return f"'Cost library'!${CL(col0 + j)}${row}"


# ---------------------------------------------------------------- start sheet ---
def _start(wb, n_rates, n_sa3, A, start=None):
    st = start or {}
    ws = wb.create_sheet('Start here')
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 3; ws.column_dimensions['B'].width = 40; ws.column_dimensions['C'].width = 42; ws.column_dimensions['D'].width = 60
    _w(ws, 'B1', 'Radius SDA Feasibility', FT)
    _w(ws, 'B2', 'Fill in the yellow cells. Everything else – rates, demand, all five builds and the best build – works itself out.', FG)
    g = lambda k, d: st.get(k) if st.get(k) not in (None, '') else d
    rows = [
        (4, 'Street address', g('address', '1 Jones Street'), None, ''),
        (5, 'Suburb', g('suburb', 'WENTWORTHVILLE'), None, 'Finds the SA4 and SA3 for you'),
        (6, 'State', g('state', 'NSW'), None, 'VIC, NSW or QLD'),
        (7, 'SA4 – found from suburb', '=IFERROR(VLOOKUP(UPPER(TRIM(C5))&"|"&C6,Suburbs!$A:$C,2,FALSE),"not found – pick below")', None, ''),
        (8, 'SA4 – pick to override (optional)', g('sa4', ''), None, 'Dropdown; leave blank to use the one found'),
        (9, 'SA4 used', '=IF(C8<>"",C8,C7)', None, ''),
        (10, 'SA3 – found from suburb', '=IFERROR(VLOOKUP(UPPER(TRIM(C5))&"|"&C6,Suburbs!$A:$C,3,FALSE),"not found – pick below")', None, ''),
        (11, 'SA3 – pick to override (optional)', g('sa3', ''), None, 'Dropdown; leave blank to use the one found'),
        (12, 'SA3 used', '=IF(C11<>"",C11,C10)', None, ''),
        (14, 'Land area (m²)', g('land', 650), '#,##0', ''),
        (15, 'Frontage (m)', st.get('frontage', 16) if start is not None else 16, '0.0#', 'Leave blank if unknown'),
        (16, 'Depth (m)', st.get('depth', 40) if start is not None else 40, '0.0#', 'Leave blank if unknown'),
        (17, 'Purchase price', g('price', 1200000), M, 'For a client who already owns the land, enter its value'),
        (18, 'Rent category', g('cat', 'IL'), None, 'IL, FA or HPS – the rate every place is costed on'),
        (19, 'Client already owns the land?', g('owns', 'N'), None, 'Y switches off buyer\'s advocacy on every build'),
        (20, 'Valuation cap rate', g('cap', A['cap']), P, ''),
        (21, 'Status', g('status', 'Feasibility'), None, ''),
    ]
    for r, label, v, fmt, note in rows:
        _w(ws, f'B{r}', label, FB if r in (9, 12) else FN)
        is_in = not (isinstance(v, str) and v.startswith('='))
        c = _w(ws, f'C{r}', v, FI if is_in else FB, fmt, F_IN if is_in else None)
        if note: _w(ws, f'D{r}', note, FG)
    # helper keys
    _w(ws, 'B23', 'Lookup key – SA4', FG); _w(ws, 'C23', '=C6&" – "&C9', FG)
    _w(ws, 'B24', 'Lookup key – SA3', FG); _w(ws, 'C24', '=C6&" – "&C12', FG)
    _w(ws, 'B26', 'NDIS SDA rates for this SA4 (per participant p.a.)', FB)
    look = lambda code: (f'=IFERROR(INDEX(Rates!$A$1:$M${n_rates},MATCH($C$23,Rates!$A$1:$A${n_rates},0),'
                         f'MATCH(LOWER($C$18)&"{code}",Rates!$A$1:$M$1,0)),0)')
    for r, label, code in [(27, '2-resident house (2P house, 2P duplex, house of house + villa)', '2'),
                           (28, '3-resident house (3P house, 3P duplex)', '3'), (29, '1-resident villa (with OOA)', '1v')]:
        _w(ws, f'B{r}', label); _w(ws, f'C{r}', look(code), FB, M)
    _w(ws, 'D27', '=IF(C27=0,"Rate not found – check the SA4 and rent category","")', Font(name='Arial', size=10, bold=True, color='C00000'))
    for col, ref in [('C6', '"VIC,NSW,QLD"'), ('C18', '"IL,FA,HPS"'), ('C19', '"Y,N"')]:
        dv = DataValidation(type='list', formula1=ref, allow_blank=True); ws.add_data_validation(dv); dv.add(col)
    dv = DataValidation(type='list', formula1=f'=Rates!$C$3:$C${n_rates}', allow_blank=True); ws.add_data_validation(dv); dv.add('C8')
    dv = DataValidation(type='list', formula1=f"='Demand SA3'!$C$3:$C${n_sa3}", allow_blank=True); ws.add_data_validation(dv); dv.add('C11')
    return {'addr': f"{ST}!$C$4", 'sub': f"{ST}!$C$5", 'state': f"{ST}!$C$6", 'land': f"{ST}!$C$14", 'front': f"{ST}!$C$15",
            'depth': f"{ST}!$C$16", 'price': f"{ST}!$C$17", 'cat': f"{ST}!$C$18", 'owns': f"{ST}!$C$19", 'cap': f"{ST}!$C$20",
            'status': f"{ST}!$C$21", 'k4': f"{ST}!$C$23", 'k3': f"{ST}!$C$24", 'sa4': f"{ST}!$C$9", 'sa3': f"{ST}!$C$12",
            'r2': f"{ST}!$C$27", 'r3': f"{ST}!$C$28", 'r1v': f"{ST}!$C$29"}


# ---------------------------------------------------------------- build sheets ---
def _build_sheet(wb, m, AR, S, LR):
    j = MODELS.index(m)
    pts = PTS[m]
    pr = dict(short=SHEET[m], title=SHEET[m] + ' – itemised feasibility', address=f"={S['addr']}&\", \"&{S['sub']}",
              model=m, state='vic', land=0, status='', price=0, b_house=0, b_villa=0,
              places=[dict(label='', cat='IL', sda=0) for _ in range(pts)])
    R = F._project_sheet(wb, SHEET[m], pr, AR)
    ws = wb[SHEET[m]]

    def link(ref, v, fmt=None):
        c = ws[ref]; c.value = v; c.font = FL
        if fmt: c.number_format = fmt

    link(f"C{R['h_state']}", f"={S['state']}"); link(f"C{R['h_land']}", f"={S['land']}", '#,##0')
    link(f"C{R['h_status']}", f"={S['status']}"); link(f"C{R['h_addr']}", f"={S['addr']}&\", \"&{S['sub']}")
    pe = f"$E${R['price']}"
    link(f"E{R['price']}", f"={S['price']}", M)
    vic = (f'ROUND(IF({pe}<=25000,{pe}*0.014,IF({pe}<=130000,350+({pe}-25000)*0.024,IF({pe}<=960000,'
           f'2870+({pe}-130000)*0.06,IF({pe}<=2000000,{pe}*0.055,110000+({pe}-2000000)*0.065)))),0)')
    link(f"E{R['duty']}", f"=IF({S['state']}=\"VIC\",{vic},{pe}*IF({S['state']}=\"NSW\",{_lib(5,0,LR['duty_nsw'])},{_lib(5,0,LR['duty_qld'])}))", M)
    ws[f"L{R['duty']}"] = 'VIC scale; NSW / QLD flat rate from the Cost library'
    for k in ('leg', 'pexa', 'val'):
        link(f"E{R[k]}", f"={_lib(5,0,LR[k])}", M)
    link(f"C{R['ba']}", f"=IF({S['owns']}=\"Y\",\"N\",\"Y\")"); link(f"E{R['ba']}", f"={_lib(5,0,LR['ba'])}", P1)
    for sec in (F.CONSULTANTS, F.SITEWORKS, F.SECURITY, F.FURNITURE):
        for key, *_ in sec:
            r, lr = R[key], LR[key]
            link(f'C{r}', f"=IF({_lib(15,j,lr)}=1,\"Y\",\"N\")")
            link(f'D{r}', f"={_lib(10,j,lr)}", '0.##')
            link(f'E{r}', f"={_lib(5,j,lr)}", M)
    link(f"E{R['con_h']}", f"={_lib(5,j,LR['house'])}", M)
    link(f"E{R['con_v']}", f"={_lib(5,0,LR['villa'])}", M)
    link(f"E{R['conting']}", f"={_lib(5,0,LR['cg'])}", P1)
    link(f"E{R['pmfee']}", f"={_lib(5,0,LR['pm'])}", P1)
    link(f"E{R['mkt']}", f"={_lib(5,0,LR['mkt'])}", M)
    # income: each place on the chosen category's rate for this SA4
    for i in range(F.PLACES):
        r = R[f'pl{i}']
        if i < pts:
            villa = (m == 'hv' and i == 2)
            if m in ('dp', 'd3'):
                per = pts // 2; lab = f'Dwelling {i // per + 1} – resident {i % per + 1}'
            elif m == 'hv':
                lab = 'Villa – resident' if villa else f'House – resident {i + 1}'
            else:
                lab = f'Resident {i + 1}'
            ws[f'B{r}'] = lab; ws[f'B{r}'].font = FN
            link(f'D{r}', f"={S['cat']}")
            link(f'E{r}', f"={S['r1v'] if villa else (S['r3'] if SUFFIX[m] == '3' else S['r2'])}", M)
        else:
            ws[f'B{r}'] = '(not used)'; ws[f'B{r}'].font = FG
    link(f"E{R['cap']}", f"={S['cap']}", P)
    return R


# ---------------------------------------------------------------- overview ---
def _overview(wb, S, R, LR, n_rates, n_sa3):
    ws = wb.create_sheet('Overview')
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 3; ws.column_dimensions['B'].width = 46
    for c in 'CDEFG': ws.column_dimensions[c].width = 17
    _w(ws, 'B1', f"={S['addr']}&\", \"&{S['sub']}&\" \"&{S['state']}", FT)
    _w(ws, 'B2', 'SDA feasibility overview – demand, then all five Radius builds compared', FG)
    # demand
    r = 4
    _w(ws, f'B{r}', 'DEMAND', FW, fill=F_HEAD)
    for c in 'CDEFG': ws[f'{c}{r}'].fill = F_HEAD
    r += 1
    ix3 = lambda col: f"=IFERROR(INDEX('Demand SA3'!${col}$1:${col}${n_sa3},MATCH({S['k3']},'Demand SA3'!$A$1:$A${n_sa3},0)),\"–\")"
    pipe = lambda col: f"=IFERROR(INDEX(Pipeline!${col}:${col},MATCH({S['k4']},Pipeline!$A:$A,0)),0)"
    dem = [('SA4', f"={S['sa4']}", None), ('Participants needing SDA in this SA4', f"=IFERROR(INDEX(Rates!$D$1:$D${n_rates},MATCH({S['k4']},Rates!$A$1:$A${n_rates},0)),\"–\")", '#,##0'),
           ('SA3', f"={S['sa3']}", None),
           ('SA3 – participants with SDA in use', ix3('E'), '#,##0'), ('SA3 – eligible, not yet using SDA', ix3('F'), '#,##0'),
           ('SA3 – total participants needing SDA', ix3('G'), '#,##0'),
           ('SA3 – enrolled SDA dwellings', f"=IFERROR(SUM(INDEX('Demand SA3'!$H$1:$M${n_sa3},MATCH({S['k3']},'Demand SA3'!$A$1:$A${n_sa3},0),0)),\"–\")", '#,##0'),
           ('SA3 – places in 1–3 resident dwellings', ix3('N'), '#,##0'),
           ('SA3 – gap (participants − 1–3 resident places)', ix3('O'), '#,##0;[Red]-#,##0'),
           ('SA4 – SDA houses under construction', f"={pipe('B')[1:]}+{pipe('C')[1:]}+{pipe('D')[1:]}", '#,##0'),
           ('SA4 – SDA villas under construction', f"={pipe('E')[1:]}+{pipe('F')[1:]}+{pipe('G')[1:]}", '#,##0'),
           ('SA4 – SDA apartments under construction', f"={pipe('H')[1:]}+{pipe('I')[1:]}+{pipe('J')[1:]}", '#,##0')]
    for label, f, fmt in dem:
        _w(ws, f'B{r}', label); _w(ws, f'C{r}', f, FB, fmt, align='right'); r += 1
    _w(ws, f'B{r}', 'Gap positive = more participants than 1–3 resident SDA places (good for a new build). Source: NDIS Quarterly Performance Report Q1 2026.', FG)
    gap_row = r - 4
    r += 2
    _w(ws, f'B{r}', 'RENT RATES (per participant p.a.)', FW, fill=F_HEAD)
    for c in 'CDEFG': ws[f'{c}{r}'].fill = F_HEAD
    r += 1
    for label, ref in [('Category', S['cat']), ('2-resident house', S['r2']), ('3-resident house', S['r3']), ('1-resident villa', S['r1v'])]:
        _w(ws, f'B{r}', label); _w(ws, f'C{r}', f'={ref}', FB, None if label == 'Category' else M, align='right'); r += 1
    r += 1
    # comparison
    _w(ws, f'B{r}', 'BUILD OPTIONS', FW, fill=F_HEAD)
    for c in 'CDEFG': ws[f'{c}{r}'].fill = F_HEAD
    r += 1
    cols = dict(zip(MODELS, 'CDEFG'))
    _w(ws, f'B{r}', 'Build', FB)
    for m in MODELS: _w(ws, f'{cols[m]}{r}', SHEET[m], FB, align='center', wrap=True)
    top = r; r += 1
    fits_row = r
    _w(ws, f'B{r}', 'Fits the site?')
    for j, m in enumerate(MODELS):
        ml, mf, md = (_lib(5, j, LR[k]) for k in ('minLand', 'minFrontage', 'minDepth'))
        f = (f"=IF({S['land']}<{ml},\"No – land\",IF(AND({S['front']}<>\"\",{S['front']}<{mf}),\"No – frontage\","
             f"IF(AND({md}>0,{S['depth']}<>\"\",{S['depth']}<{md}),\"No – depth\",\"Yes\")))")
        _w(ws, f'{cols[m]}{r}', f, FB, align='center')
    r += 1
    sheet_rows = [('SDA places', 'n_places', '0'), ('Gross income – fully let', 'gross', M), ('Net income – fully let', 'net', M),
                  ('Total development cost', 'tdc', M), ('Net yield on TDC', 'yld', P), ('Completed, leased value', 'value', M),
                  ('Profit on completion', 'profit', M), ('Profit on cost', 'poc', P),
                  ('Equity left in after CBA refinance', 'eq_left', M), ('Levered return', 'lev', P),
                  ('CBA loan', 'cba', M), ('Cash left after CBA interest only', 'cash_io', M),
                  ('Cash left after CBA principal & interest', 'cash_pi', M), ('Rent covers P&I (times)', 'dscr', '0.00"x"'),
                  ('Total profit – sell after 5 yrs (interest only)', 'x5io', M), ('Total profit – sell after 5 yrs (P&I)', 'x5pi', M),
                  ('Total profit – sell after 10 yrs (interest only)', 'x10io', M), ('Total profit – sell after 10 yrs (P&I)', 'x10pi', M),
                  ('IRR on equity – 5 yrs (interest only)', 'irr5io', P), ('IRR on equity – 10 yrs (interest only)', 'irr10io', P)]
    res = {}
    for label, key, fmt in sheet_rows:
        _w(ws, f'B{r}', label, FB if key in ('yld', 'tdc') else FN)
        for m in MODELS:
            _w(ws, f'{cols[m]}{r}', f"='{SHEET[m]}'!I{R[key]}", FB if key in ('yld', 'tdc') else FN, fmt, align='right')
        res[key] = r; r += 1
    score = r
    _w(ws, f'B{r}', 'Score (yield if it fits)', FG)
    for m in MODELS:
        c = cols[m]; _w(ws, f'{c}{r}', f'=IF({c}{fits_row}="Yes",{c}{res["yld"]},-1)', FG, P, align='right')
    r += 2
    _w(ws, f'B{r}', 'BEST BUILD', FB, fill=F_KEY)
    _w(ws, f'C{r}', f'=IF(MAX(C{score}:G{score})<0,"Nothing fits this site",INDEX(C{top}:G{top},MATCH(MAX(C{score}:G{score}),C{score}:G{score},0)))', FB, fill=F_KEY)
    ws.merge_cells(f'C{r}:D{r}')
    _w(ws, f'E{r}', f'=IF(MAX(C{score}:G{score})<0,"",TEXT(MAX(C{score}:G{score}),"0.00%")&" net yield")', FB, fill=F_KEY)
    best = r
    r += 1
    _w(ws, f'C{r}', f'=IF(MAX(C{score}:G{score})<0,"",TEXT(INDEX(C{res["net"]}:G{res["net"]},MATCH(MAX(C{score}:G{score}),C{score}:G{score},0)),"$#,##0")&" net income a year")', FN)
    # highlight best column, grey out builds that don't fit
    ws.conditional_formatting.add(f'C{top}:G{score}', FormulaRule(formula=[f'AND(C${fits_row}="Yes",C${score}=MAX($C${score}:$G${score}))'], fill=PatternFill('solid', fgColor='C6EFCE'), font=Font(bold=True, color='006100')))
    ws.conditional_formatting.add(f'C{top}:G{score}', FormulaRule(formula=[f'C${fits_row}<>"Yes"'], font=Font(color='A6A6A6')))
    ws.conditional_formatting.add(f'C{fits_row-0}:G{fits_row}', FormulaRule(formula=[f'C${fits_row}<>"Yes"'], font=Font(color='C00000', bold=True)))
    r += 2
    _w(ws, f'B{r}', 'Every build uses the same Start here inputs and Cost library. Open a build sheet to see or change every line.', FG)
    ws.freeze_panes = 'C4'
    ws.page_setup.orientation = 'portrait'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return {'best': best, 'fits': fits_row, 'gap': gap_row}


# ---------------------------------------------------------------- internal ---
def _internal(wb, S, n_sa3):
    ws = wb.create_sheet('INTERNAL')
    ws.sheet_properties.tabColor = 'C00000'
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 3; ws.column_dimensions['B'].width = 60; ws.column_dimensions['C'].width = 16; ws.column_dimensions['D'].width = 60
    _w(ws, 'B1', 'INTERNAL – delete this tab before sending the workbook to anyone', Font(name='Arial', size=13, bold=True, color='C00000'))
    _w(ws, 'B2', "Jason's demand method. Supply figures come from the screener's provider register (internal data – not for clients). Enter them from the screener's Supply panel for this SA3.", FG)
    rows = [
        (4, 'Participants needing SDA in this SA3 (NDIS)', f"=IFERROR(INDEX('Demand SA3'!$G$1:$G${n_sa3},MATCH({S['k3']},'Demand SA3'!$A$1:$A${n_sa3},0)),0)", False),
        (5, 'Residents in group homes in this SA3 (moving to SDA)', 0, True),
        (6, 'Residents in legacy stock in this SA3 (closing)', 0, True),
        (7, 'Residents in homes above 3 bedrooms', 0, True),
        (8, 'TOTAL DEMAND', '=SUM(C4:C7)', False),
        (10, 'Competing SDA places – apartments', 0, True),
        (11, 'Competing SDA places – houses', 0, True),
        (12, 'Competing SDA places – villas / townhouses', 0, True),
        (13, 'Pipeline places (exclude anything stalled 3+ years)', 0, True),
        (14, 'TOTAL COMPETING SUPPLY', '=SUM(C10:C13)', False),
        (16, 'NET GAP (demand − competing supply)', '=C8-C14', False),
    ]
    for r, label, v, inp in rows:
        _w(ws, f'B{r}', label, FB if label.isupper() or label.startswith(('TOTAL', 'NET')) else FN)
        _w(ws, f'C{r}', v, FI if inp else FB, '#,##0;[Red]-#,##0', F_IN if inp else (F_KEY if r == 16 else None))
    _w(ws, 'D5', 'Group homes and legacy stock are deducted from supply in full (closing)', FG)
    _w(ws, 'D13', 'Treat pipeline stalled 3+ years as not being built', FG)


# ---------------------------------------------------------------- build ---
def build_standalone(D, A, start=None, lib=None):
    wb = Workbook()
    wb.remove(wb.active)
    n_rates, n_sa3 = _data_sheets(wb, D)
    rules = D['SITE_RULES']
    LR = _library(wb, rules, lib)
    S = _start(wb, n_rates, n_sa3, A, start)
    AR = F._assumptions(wb, A)
    R = None
    for m in MODELS:
        R = _build_sheet(wb, m, AR, S, LR)
    _overview(wb, S, R, LR, n_rates, n_sa3)
    _internal(wb, S, n_sa3)
    order = ['Start here', 'Overview'] + [SHEET[m] for m in MODELS] + ['Cost library', 'Assumptions', 'Rates', 'Demand SA3', 'Pipeline', 'Suburbs', 'INTERNAL']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for n in ('Start here', 'Cost library', 'INTERNAL') + tuple(('Rates', 'Demand SA3', 'Pipeline')):
        ws = wb[n]; ws.page_setup.orientation = 'landscape' if n != 'Start here' else 'portrait'
        ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb['Overview'].column_dimensions['C'].width = 22
    for n in ('Rates', 'Demand SA3', 'Pipeline', 'Suburbs'):
        wb[n].sheet_properties.tabColor = '808080'
    wb['Start here'].sheet_properties.tabColor = 'FFC000'; wb['Overview'].sheet_properties.tabColor = '00B050'
    return wb, R

