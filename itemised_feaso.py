"""Itemised portfolio feasibility workbook + admin-only earnings workbook.

build_feaso_workbook(title, projects, A)    -> Workbook  (client / funder safe)
build_earnings_workbook(title, projects, A) -> Workbook  (ADMIN ONLY - separate function,
                                                          shares no code path with the feaso)

Every project sheet uses the SAME row layout (all lines exist for every build type; lines
that don't apply have Qty 0 or Include = N). That is what lets the Overview link
cell-for-cell. Inputs are blue on yellow; everything else is a formula.

Line amounts:  base = IF(Include="Y", Qty x Rate, 0)
  GST "+GST"  quote is ex GST       -> inc = base x 1.1
  GST "Inc"   quote includes GST    -> inc = base
  GST "None"  no GST (duty, bonds, government fees, interest)
Totals, TDC and returns use the Inc GST column (GST is a real cost on hold-and-lease SDA).
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.worksheet.datavalidation import DataValidation

MODELS = ['2p', '3p', 'dp', 'd3', 'hv']
MODEL_NAMES = {'2p': '2P House', '3p': '3P House', 'dp': '2P Duplex (2 × 2P)',
               'd3': '3P Duplex (2 × 3P)', 'hv': '2P House + 1P Villa'}
DWELL = {'2p': 1, '3p': 1, 'dp': 2, 'd3': 2, 'hv': 2}
HOUSES = {'2p': 1, '3p': 1, 'dp': 2, 'd3': 2, 'hv': 1}
VILLAS = {'2p': 0, '3p': 0, 'dp': 0, 'd3': 0, 'hv': 1}
TITLES = {'2p': 1, '3p': 1, 'dp': 2, 'd3': 2, 'hv': 1}
PLACES = 6


def per(a, b, c, d, e):
    return dict(zip(MODELS, (a, b, c, d, e)))


ALL1 = per(1, 1, 1, 1, 1)
X2 = per(1, 1, 2, 2, 2)
X15 = per(1, 1, 1.5, 1.5, 1.5)
ON = per(True, True, True, True, True)
OFF = per(False, False, False, False, False)

# (key, label, rate (number or per-model dict), qty per model, default include, gst, note)
CONSULTANTS = [
    ('arch', 'Architect – design & documentation', 17600, X15, ON, 'Inc', ''),
    ('arb', 'Arborist (if required)', 500, ALL1, ON, 'Inc', ''),
    ('photo', 'Advertising photography – marketing & progress', 5500, X2, ON, 'Inc', ''),
    ('bs', 'Building surveyor – building permit (per dwelling)', 3575, X2, ON, 'Inc', ''),
    ('bsps', 'Building surveyor – performance solutions', 800, per(4, 4, 4, 4, 4), ON, 'Inc', 'Qty = number of performance solutions'),
    ('boe', 'Build over easement fee', 600, X2, OFF, 'Inc', 'Turn on if building over an easement'),
    ('sda', 'SDA assessor – certification before, during & after', per(8000, 8800, 8800, 8800, 8800), ALL1, ON, 'Inc', 'Covers both dwellings on a duplex'),
    ('sdaps', 'SDA assessor – performance solutions (NCC)', 800, per(4, 4, 4, 4, 4), ON, 'Inc', 'Qty = number of performance solutions'),
    ('capp', 'Council application fee (if required)', 2200, ALL1, ON, 'None', ''),
    ('drain', 'Drainage engineering design & certification', 1320, X2, ON, 'Inc', ''),
    ('energy', 'Energy ratings', 990, X2, ON, 'Inc', ''),
    ('fsvc', 'Fire services design – sprinklers, electrical, hydraulics', 6270, X15, ON, 'Inc', ''),
    ('feng', 'Fire engineering brief & report', 7480, X15, ON, 'Inc', ''),
    ('ase', 'ASE fire installation – Romteck', 1800, X2, ON, 'Inc', ''),
    ('lscape', 'Landscape plan design', 990, X2, ON, 'Inc', ''),
    ('svcloc', 'Service locator / service protection report', 1100, ALL1, ON, 'Inc', ''),
    ('soil', 'Soil report – geotechnical', 495, per(1, 1, 2, 2, 1), ON, 'Inc', ''),
    ('struct', 'Structural engineering', 1650, X2, ON, 'Inc', ''),
    ('survey', 'Feature level & re-establishment survey', 4620, X2, ON, 'Inc', ''),
    ('subdiv', 'Subdivision surveyor application', 8000, X15, per(False, False, True, True, False), 'Inc', 'On when subdividing'),
    ('sect_j', 'Sustainable design assessment – Section J', per(990, 1100, 1100, 1100, 1100), ALL1, ON, 'Inc', ''),
    ('wsud', 'Stormwater & WSUD plan', 1100, X2, ON, 'Inc', ''),
    ('traffic', 'Traffic management', 5000, ALL1, ON, 'Inc', ''),
    ('tp', 'Town planning report (clause 55)', 0, ALL1, OFF, 'Inc', 'Enter a quote if a permit is needed'),
]
SITEWORKS = [
    ('demo', 'Demolition of existing house', 30000, ALL1, ON, 'Inc', 'One house, even for a duplex'),
    ('elec', 'Electrical pit underground', 10000, per(1, 1, 2, 2, 1), ON, 'Inc', ''),
    ('ftank', 'Fire tank & pump', 30000, ALL1, ON, 'Inc', 'Off if the water main is on our side of the street'),
    ('nbn', 'NBN connection', 2000, X2, ON, 'Inc', ''),
    ('xover', 'New crossover – driveway', 10000, per(1, 1, 2, 2, 1), ON, 'Inc', 'House + villa share one crossover'),
    ('retain', 'Retaining walls (per lineal metre)', 800, per(0, 0, 0, 0, 0), ON, 'Inc', 'Qty = metres; site specific'),
    ('rock', 'Rock excavation allowance', 30000, ALL1, ON, 'Inc', ''),
    ('sewer', 'Sewer & drainage connection (new dwelling)', 15000, ALL1, per(False, False, True, True, True), 'Inc', 'Usually duplex / villa only'),
    ('stip', 'STIP – sewer tie-in point relocation', 5000, ALL1, OFF, 'Inc', 'On if the sewer point must move'),
    ('storm', 'Stormwater tank & pump to LPOD', 25000, per(1, 1, 2, 2, 1), ON, 'Inc', ''),
    ('water', 'Water tapping & 50mm meter upgrade (sprinklers)', 10000, X2, ON, 'Inc', ''),
    ('bond_d', 'Asset protection bond – demolition', 5000, ALL1, ON, 'None', 'Refundable'),
    ('bond_c', 'Asset protection bond – construction', 10000, ALL1, ON, 'None', 'Refundable'),
]
SECURITY = [
    ('cam_i', 'Security camera installation', 750, ALL1, ON, 'Inc', ''),
    ('cam_m', 'Security cameras & guard monitoring (build period)', 9820.80, ALL1, ON, 'Inc', ''),
]
FURNITURE = [
    ('furn_h', 'Furniture package with white goods – house', 20000, per(1, 1, 2, 2, 1), ON, 'Inc', '$20k per house, 2P or 3P'),
    ('furn_v', 'Furniture package – villa', 10000, per(0, 0, 0, 0, 1), ON, 'Inc', ''),
]
STAGES = [('Deposit', 0.05), ('Base', 0.15), ('Frame', 0.20), ('Lock-up', 0.30), ('Fixing', 0.20), ('Completion', 0.10)]

NAVY = '1F3A5F'
F_IN = PatternFill('solid', fgColor='FFF2CC')
F_HEAD = PatternFill('solid', fgColor=NAVY)
F_SEC = PatternFill('solid', fgColor='DCE6F1')
F_SUB = PatternFill('solid', fgColor='F2F2F2')
F_KEY = PatternFill('solid', fgColor='E2EFDA')
NOFILL = PatternFill()
FN = Font(name='Arial', size=10)
FB = Font(name='Arial', size=10, bold=True)
FI = Font(name='Arial', size=10, color='0000FF')
FW = Font(name='Arial', size=10, bold=True, color='FFFFFF')
FT = Font(name='Arial', size=14, bold=True, color=NAVY)
FG = Font(name='Arial', size=8.5, italic=True, color='808080')
FH = Font(name='Arial', size=8.5, bold=True, color='595959')
M = '$#,##0;[Red]-$#,##0;"–"'
P = '0.00%'
P1 = '0.0%'
Q = '0.##'
COLS = 'ABCDEFGHIJKL'   # Ref Item Incl Qty Rate GST Ex GST Inc Status Supplier Notes
INC = 'I'               # the column the Overview and totals use


def _rate(v, m):
    return v[m] if isinstance(v, dict) else v


# ============================================================ FEASO WORKBOOK ===
def _assumptions(wb, A):
    ws = wb.create_sheet('Assumptions')
    ws.sheet_view.showGridLines = False
    for c, w in zip('ABC', [50, 14, 58]):
        ws.column_dimensions[c].width = w
    ws['A1'] = 'Shared assumptions'; ws['A1'].font = FT
    ws['A2'] = 'Every project sheet links here. Change a rate once and it flows to every project and the Overview.'; ws['A2'].font = FG
    rows = [
        ('h', 'Construction finance: ' + str(A.get('lender') or 'Private funder (Austar terms)')),
        ('cIr', 'Interest rate (p.a.)', A['cIr'], P, ''),
        ('cLine', 'Line fee (p.a.)', A['cLine'], P, 'On the full facility for the construction period'),
        ('cEst', 'Establishment fee', A['cEst'], P, 'Once, on the facility'),
        ('cEstGst', 'GST on the establishment fee (1 = yes, 0 = no)', 0 if A.get('cEstGst', 1) == 0 else 1, '0', 'Private funder 1; bank fees carry no GST, so 0'),
        ('cLvr', 'Loan to cost (of TDC)', A['cLvr'], P1, 'Equity goes in first'),
        ('cMonths', 'Construction period (months)', A['cMonths'], '0', ''),
        ('h', 'Completion refinance (CBA / tier 1 bank)'),
        ('lvr', 'Refinance LVR (of completed value)', A['lvr'], P1, ''),
        ('ir', 'Interest rate (p.a.)', A['ir'], P, ''),
        ('term', 'Loan term for principal & interest (years)', A.get('cbaTerm', 30), '0', 'Monthly repayments'),
        ('h', 'Hold & sell'),
        ('rg', 'Rent and cost growth each year (CPI)', A.get('rg', 0.03), P1, ''),
        ('salecap', 'Sale cap rate – institutional exit (0 = valuation cap)', A.get('saleCap', 0) or 0, P, 'Cap rate an institution pays at the sale'),
        ('exitcost', 'Sale costs (per project)', A.get('exitCost', 100000), M, ''),
        ('cap', 'Valuation cap rate', A['cap'], P, 'Each project can override its own'),
        ('h', 'Income and ongoing costs'),
        ('rrc', 'Reasonable rent contribution (per resident p.a.)', A['rrc'], M, ''),
        ('mgr', 'SDA management (% of gross rent, inc GST)', A['sdaMgr'], P1, ''),
        ('clean', 'Cleaning & grounds (per title p.a.)', A['cleanPa'], M, '$100 a week'),
        ('fire', 'Fire safety audit (per dwelling p.a.)', A['fire'], M, ''),
        ('ins', 'Insurance (per dwelling p.a.)', A['ins'], M, ''),
        ('rates', 'Council rates (per title p.a.)', A['rates'], M, ''),
        ('maint', 'Repairs & maintenance (per dwelling p.a.)', A['maint'], M, ''),
        ('h', 'Other'),
        ('bondref', 'Share of bonds refunded', 0.8, '0%', 'Bonds count as a cost net of the refund'),
        ('letwk', 'Letting fee (weeks of SDA rent per resident)', 2, '0', 'Inc GST'),
        ('gst', 'GST rate', 0.10, '0%', ''),
    ]
    refs, r = {}, 4
    for row in rows:
        if row[0] == 'h':
            r += 1
            for c in 'ABC':
                ws[f'{c}{r}'].fill = F_SEC
            ws[f'A{r}'] = row[1]; ws[f'A{r}'].font = FB
            r += 1
            continue
        key, label, val, fmt, note = row
        ws[f'A{r}'] = label; ws[f'A{r}'].font = FN
        c = ws[f'B{r}']; c.value = val; c.font = FI; c.fill = F_IN; c.number_format = fmt
        ws[f'C{r}'] = note; ws[f'C{r}'].font = FG
        refs[key] = f'Assumptions!$B${r}'
        r += 1
    return refs


class _W:
    """Small writer that tracks the current row."""
    def __init__(self, ws):
        self.ws, self.r = ws, 1

    def c(self, col, v, font=FN, fmt=None, fill=None, align=None):
        cell = self.ws[f'{col}{self.r}']
        cell.value = v
        cell.font = font
        if fmt: cell.number_format = fmt
        if fill: cell.fill = fill
        if align: cell.alignment = Alignment(horizontal=align, vertical='center')
        return cell


def _project_sheet(wb, name, pr, AR):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    for col, w in zip(COLS + 'MNOPQ', [6, 46, 6, 12, 13, 11, 13, 13, 14, 13, 18, 30, 3, 13, 13, 13, 13]):
        ws.column_dimensions[col].width = w
    W, R, m = _W(ws), {}, pr['model']
    G = AR['gst']

    def amounts(row, base):
        """Writes Ex / GST / Inc for a line whose GST type sits in F."""
        ws[f'G{row}'] = f'=IF(F{row}="+GST",{base},IF(F{row}="Inc",{base}/(1+{G}),{base}))'
        ws[f'I{row}'] = f'=IF(F{row}="+GST",{base}*(1+{G}),{base})'
        ws[f'H{row}'] = f'=I{row}-G{row}'
        for col in 'GHI':
            ws[f'{col}{row}'].number_format = M; ws[f'{col}{row}'].font = FN

    LV = pr.get('lines') or {}

    def cost(key, ref, label, qty, rate, incl=True, gst='Inc', note='', qty_fmt=Q, rate_fmt=M,
             qty_input=True, rate_input=True, status='Estimate'):
        r = W.r
        o = LV.get(key)
        if isinstance(o, dict):
            if 'on' in o: incl = bool(o['on'])
            if o.get('gst') in ('+GST', 'Inc', 'None'): gst = o['gst']
            if o.get('qty') is not None and not str(qty).startswith('='): qty = o['qty']
            if o.get('rate') is not None and (not str(rate).startswith('=') or o.get('force')):
                rate = o['rate']
            if o.get('note'): note = o['note']
            if o.get('status'): status = o['status']
        W.c('A', ref, FG); W.c('B', label)
        W.c('C', 'Y' if incl else 'N', FI, fill=F_IN, align='center')
        q_in = qty_input and not str(qty).startswith('=')
        W.c('D', qty, FI if q_in else FN, qty_fmt, F_IN if q_in else None, align='center')
        r_in = rate_input and not str(rate).startswith('=')
        W.c('E', rate, FI if r_in else FN, rate_fmt, F_IN if r_in else None)
        W.c('F', gst, FI, fill=F_IN, align='center')
        amounts(r, f'IF($C{r}="Y",$D{r}*$E{r},0)')
        W.c('J', status, FI, fill=F_IN, align='center'); W.c('K', '', FI, fill=F_IN)
        if note: W.c('L', note, FG)
        R[key] = r; W.r += 1
        return r

    def calc_row(key, label, formula, fmt=M, bold=False, fill=None, note='', col=INC):
        W.c('B', label, FB if bold else FN)
        W.c(col, formula, FB if bold else FN, fmt)
        if fill:
            for cc in COLS: ws[f'{cc}{W.r}'].fill = fill
        if note: W.c('L', note, FG)
        R[key] = W.r; W.r += 1

    def subtotal(key, label, rows):
        r = W.r
        for col in 'GHI':
            ws[f'{col}{r}'] = '=' + '+'.join(f'{col}{x}' for x in rows) if rows else 0
            ws[f'{col}{r}'].number_format = M; ws[f'{col}{r}'].font = FB
        W.c('B', label, FB)
        for cc in COLS: ws[f'{cc}{r}'].fill = F_SEC
        R[key] = r; W.r += 1

    def section(title, head=True):
        W.r += 1
        for cc in COLS: ws[f'{cc}{W.r}'].fill = F_HEAD
        W.c('A', title, FW); W.r += 1
        if head:
            for col, h in zip(COLS, ['Ref', 'Item', 'Incl.', 'Qty', 'Rate', 'GST', 'Ex GST', 'GST', 'Inc GST', 'Status', 'Supplier', 'Notes']):
                W.c(col, h, FH, fill=F_SUB, align='center' if col not in 'BL' else None)
            W.r += 1

    # ------------------------------------------------------------ header
    W.c('A', pr['title'], FT); W.r += 1
    W.c('A', 'Itemised development feasibility – all amounts in AUD', FG); W.r += 2
    for key, label, val, fmt in [('h_addr', 'Address', pr['address'], None), ('h_model', 'Build model', MODEL_NAMES[m], None),
                                 ('h_state', 'State', pr['state'].upper(), None), ('h_land', 'Land area (m²)', pr['land'], '#,##0'),
                                 ('h_houses', 'Houses', HOUSES[m], '0'), ('h_villas', 'Villas', VILLAS[m], '0'),
                                 ('h_dw', 'Dwellings', '=__DW__', '0'),
                                 ('h_titles', 'Titles (for rates & cleaning)', TITLES[m], '0'),
                                 ('h_status', 'Portfolio status', pr.get('status', 'Target'), None)]:
        W.c('B', label)
        is_in = not str(val).startswith('=')
        W.c('C', val, FI if is_in else FN, fmt, F_IN if is_in else None, align='left')
        ws.merge_cells(f'C{W.r}:F{W.r}')
        R[key] = W.r; W.r += 1
    ws[f"C{R['h_dw']}"] = f"=C{R['h_houses']}+C{R['h_villas']}"
    dw, titles = f"$C${R['h_dw']}", f"$C${R['h_titles']}"
    W.r += 1
    W.c('B', 'Yellow cells are inputs. Incl. Y/N switches a line on or off. GST: +GST = quote is ex GST, Inc = quote includes GST, None = no GST.', FG)
    W.r += 1
    W.c('B', 'Status: Estimate → Quote → Contract → Paid. Totals and returns use the Inc GST column.', FG)

    # ------------------------------------------------------------ 1 land
    section('1. LAND ACQUISITION')
    price = cost('price', '1.01', 'Purchase price', 1, pr['price'], gst='None', qty_input=False)
    pc = f'$E${price}'
    duty = (f'=ROUND(IF({pc}<=25000,{pc}*0.014,IF({pc}<=130000,350+({pc}-25000)*0.024,IF({pc}<=960000,'
            f'2870+({pc}-130000)*0.06,IF({pc}<=2000000,{pc}*0.055,110000+({pc}-2000000)*0.065)))),0)')
    cost('duty', '1.02', 'Stamp duty (VIC scale)', 1, duty, gst='None', qty_input=False, note='Type over for other states')
    cost('leg', '1.03', 'Legal & conveyancing', 1, pr.get('leg', 1000))
    cost('pexa', '1.04', 'PEXA settlement fee', 1, pr.get('pexa', 495))
    cost('val', '1.05', 'Valuation', 1, pr.get('val', 3500))
    cost('ltax', '1.06', 'Land tax', 1, 0, gst='None')
    cost('ba', '1.07', "Radius buyer's advocacy (% of price)", f'={pc}', pr.get('ba', 0.04), gst='+GST', qty_fmt=M,
         rate_fmt=P, note='Qty = purchase price')
    cost('dd', '1.08', 'Due diligence report', 1, 0)
    land_rows = [R[k] for k in ('price', 'duty', 'leg', 'pexa', 'val', 'ltax', 'ba', 'dd')]
    subtotal('t_land', 'Total land acquisition', land_rows)

    # ------------------------------------------------------------ 2 consultants
    LIB = pr.get('lib')

    def library(sec_no, items, sec_key=None):
        rows = []
        if LIB and sec_key:
            defs = [d for d in LIB if d['sec'] == sec_key]
            for i, d in enumerate(defs, 1):
                o = LV.get(d['key']) or {}
                rows.append(cost(d['key'], f'{sec_no}.{i:02d}', d['label'], o.get('qty', 0), o.get('rate', 0),
                                 o.get('on', False), o.get('gst', d.get('gst', 'Inc')), d.get('note', '')))
            return rows
        for i, (key, label, rate, qty, inc, gst, note) in enumerate(items, 1):
            rows.append(cost(key, f'{sec_no}.{i:02d}', label, qty[m], _rate(rate, m), inc[m], gst, note))
        return rows

    section('2. CONSULTANTS & DESIGN')
    subtotal('t_cons', 'Total consultants & design', library(2, CONSULTANTS, 'cons'))

    # ------------------------------------------------------------ 3 site works
    section('3. COUNCIL, AUTHORITY & SITE WORKS')
    rows = library(3, SITEWORKS, 'site')
    bonds = f"(I{R['bond_d']}+I{R['bond_c']})"
    r = W.r
    W.c('A', f'3.{len(SITEWORKS)+1:02d}', FG); W.c('B', 'Less bonds refunded')
    W.c('E', f"=-{AR['bondref']}", FN, '0%'); W.c('F', 'None', FN, align='center')
    for col in 'GI':
        ws[f'{col}{r}'] = f"=E{r}*({col}{R['bond_d']}+{col}{R['bond_c']})"; ws[f'{col}{r}'].number_format = M
    ws[f'H{r}'] = 0; ws[f'H{r}'].number_format = M
    W.c('L', 'Share refunded is on the Assumptions sheet', FG)
    R['bond_ref'] = r; W.r += 1
    subtotal('t_site', 'Total council, authority & site works', rows + [r])

    # ------------------------------------------------------------ 4 security
    section('4. SITE SECURITY & MONITORING')
    subtotal('t_sec', 'Total site security & monitoring', library(4, SECURITY, 'sec'))

    # ------------------------------------------------------------ 5 furniture
    section('5. FURNITURE & FIT-OUT')
    subtotal('t_furn', 'Total furniture & fit-out', library(5, FURNITURE, 'furn'))

    # ------------------------------------------------------------ 6 construction
    section('6. CONSTRUCTION')
    ch = cost('con_h', '6.01', 'Builder contract – house (per house)', f"=$C${R['h_houses']}", pr['b_house'],
              note='Contract price, inc GST')
    cv = cost('con_v', '6.02', 'Builder contract – villa (per villa)', f"=$C${R['h_villas']}", pr['b_villa'],
              note='Contract price, inc GST')
    calc_row('contract', 'Total builder contract', f'=I{ch}+I{cv}', bold=True)
    W.c('B', 'Paid to the builder by stage (memo – already in the contract):', FG); W.r += 1
    first = W.r
    for i, (lab, pct) in enumerate(STAGES, 1):
        W.c('A', f'6.{i+2:02d}', FG); W.c('B', f'      {lab}', FN)
        W.c('D', pct, FI, '0%', F_IN, align='center')
        W.c('E', f"=$I${R['contract']}*D{W.r}", FN, M)
        W.c('L', '% of contract', FG)
        R[f'stage{i}'] = W.r; W.r += 1
    W.c('B', '      Stages total (must be 100%)', FG); W.c('D', f'=SUM(D{first}:D{W.r-1})', FN, '0%', align='center')
    W.c('E', f'=SUM(E{first}:E{W.r-1})', FN, M); R['stage_chk'] = W.r; W.r += 1
    cg = cost('conting', '6.09', 'Construction contingency (% of contract)', f"=$I${R['contract']}", pr.get('cg', 0.03),
              qty_fmt=M, rate_fmt=P1, note='Qty = contract')
    pm = cost('pmfee', '6.10', 'Radius project management fee (% of contract)', f"=$I${R['contract']}", pr.get('pm', 0.08),
              gst='+GST', qty_fmt=M, rate_fmt=P1, note='Struck on contract, not contingency')
    subtotal('t_build', 'Total construction', [ch, cv, cg, pm])

    # ------------------------------------------------------------ 7 SDA leasing (once-off)
    section('7. SDA LEASING (ONCE-OFF)')
    let = cost('letting', '7.01', 'SDA letting fee – 2 weeks SDA rent per resident', 1, '=__LET__', gst='Inc',
               rate_input=False, note='From the income table below')
    if isinstance(LV.get('letting'), dict) and LV['letting'].get('changed'):
        ws[f'E{let}'] = LV['letting'].get('rate', 0); ws[f'E{let}'].font = FI; ws[f'E{let}'].fill = F_IN
        ws[f'L{let}'] = 'Changed for this project'
    mkt = cost('mkt', '7.02', 'SDA marketing fee (per title)', f'={titles}', 1000)
    subtotal('t_lease', 'Total SDA leasing', [let, mkt])

    # ------------------------------------------------------------ 8 finance
    section('8. CONSTRUCTION FINANCE', head=False)
    base_keys = ['t_land', 't_cons', 't_site', 't_sec', 't_furn', 't_build', 't_lease']
    calc_row('base', 'Development cost before finance (inc GST)', '=' + '+'.join(f'I{R[k]}' for k in base_keys), bold=True)
    w0 = W.r
    r_, lf, e_, lv, T = AR['cIr'], AR['cLine'], AR['cEst'], AR['cLvr'], f"({AR['cMonths']}/12)"
    B_, L_ = f"$I${R['base']}", f"$I${R['t_land']}"
    eg = f"{e_}*(1+{G}*{AR['cEstGst']})"
    work = [('kA', f'={lv}*(0.5*{r_}*{T}+{lf}*{T}+{eg})'), ('XA', f'={B_}/(1-O{w0})'),
            ('kB', f'={r_}*{T}*({lv}-0.5)+{lv}*({lf}*{T}+{eg})'), ('XB', f'=({B_}+0.5*{r_}*{T}*{L_})/(1-O{w0+2})'),
            ('kC', f'={lv}*({r_}*{T}+{lf}*{T}+{eg})'), ('XC', f'={B_}/(1-O{w0+4})'),
            ('land debt (B)', f'={L_}-(1-{lv})*O{w0+3}'),
            ('TDC solved', f'=IF(O{w0+6}<=0,O{w0+1},IF(O{w0+6}>={lv}*O{w0+3},O{w0+5},O{w0+3}))')]
    ws[f'N{w0-1}'] = 'Finance workings'; ws[f'N{w0-1}'].font = FG
    for i, (lab, f) in enumerate(work):
        ws[f'N{w0+i}'] = lab; ws[f'N{w0+i}'].font = FG
        ws[f'O{w0+i}'] = f; ws[f'O{w0+i}'].font = Font(name='Arial', size=8.5, color='808080')
        ws[f'O{w0+i}'].number_format = '0.0000' if lab.startswith('k') else M
    X = f'$O${w0+7}'
    W.c('E', f'={lv}', FN, P1); calc_row('fac', 'Facility (loan to cost × TDC)', f'={X}*E{W.r}')
    F_ = f"$I${R['fac']}"
    calc_row('eqin', 'Equity in (goes in first)', f'={X}-{F_}')
    calc_row('ldebt', 'Loan drawn at settlement (land not covered by equity)', f"=MAX(0,MIN({F_},{L_}-I{R['eqin']}))")
    calc_row('pdebt', 'Loan drawn progressively (about half out on average)', f"={F_}-I{R['ldebt']}")
    W.c('E', f'={r_}', FN, P); calc_row('f_int', 'Interest', f"=E{W.r}*{T}*(I{R['ldebt']}+0.5*I{R['pdebt']})")
    W.c('E', f'={lf}', FN, P); calc_row('f_line', 'Line fee', f'=E{W.r}*{T}*{F_}')
    W.c('E', f'={e_}', FN, P); calc_row('f_est', 'Establishment fee (+ GST if charged)', f"=E{W.r}*(1+{G}*{AR['cEstGst']})*{F_}")
    calc_row('t_fin', 'Total finance costs (capitalised)', f"=I{R['f_int']}+I{R['f_line']}+I{R['f_est']}", bold=True, fill=F_SEC)
    W.r += 1
    calc_row('tdc', 'TOTAL DEVELOPMENT COST (TDC)', f"=I{R['base']}+I{R['t_fin']}", bold=True, fill=F_KEY)
    calc_row('tdc_pp', 'TDC per SDA place', '=IFERROR(I{}/I__NP__,0)'.format(R['tdc']))

    # ------------------------------------------------------------ 9 income
    section('9. INCOME (SDA + RRC, per resident p.a.)', head=False)
    for col, h in zip('BCDEFGHI', ['Resident place', 'Now?', 'Cat.', 'SDA p.a.', '', '', '', 'SDA + RRC']):
        W.c(col, h, FH, fill=F_SUB)
    W.r += 1
    first = W.r
    for i in range(PLACES):
        pl = pr['places'][i] if i < len(pr['places']) else None
        W.c('A', f'9.{i+1:02d}', FG)
        W.c('B', pl['label'] if pl else '(not used)', FN if pl else FG)
        W.c('C', 'Y' if (pl and pl.get('now', True)) else 'N', FI, fill=F_IN, align='center')
        W.c('D', pl['cat'] if pl else '', FI, fill=F_IN, align='center')
        W.c('E', pl['sda'] if pl else 0, FI, M, F_IN)
        W.c('I', f'=IF(E{W.r}>0,E{W.r}+{AR["rrc"]},0)', FN, M)
        R[f'pl{i}'] = W.r; W.r += 1
    last = W.r - 1
    calc_row('n_places', 'SDA places', f'=COUNTIF(E{first}:E{last},">0")', fmt='0')
    calc_row('n_now', 'Residents living there now', f'=COUNTIFS(E{first}:E{last},">0",C{first}:C{last},"Y")', fmt='0')
    calc_row('gross', 'Gross income – fully let', f'=SUM(I{first}:I{last})', bold=True)
    calc_row('gross_now', 'Gross income – residents now', f'=SUMIF(C{first}:C{last},"Y",I{first}:I{last})')
    calc_row('sda_sum', 'SDA amount only (for the letting fee)', f'=SUM(E{first}:E{last})')

    # ------------------------------------------------------------ 10 ongoing
    section('10. ONGOING COSTS (p.a., inc GST)', head=False)
    W.c('E', f"={AR['mgr']}", FN, P1); calc_row('o_mgr', 'SDA management (% of gross income)', f"=I{R['gross']}*E{W.r}")
    for key, label, qty, ref in [('o_clean', 'Cleaning & grounds', titles, 'clean'), ('o_fire', 'Fire safety audit', dw, 'fire'),
                                 ('o_ins', 'Insurance', dw, 'ins'), ('o_rates', 'Council rates', titles, 'rates'),
                                 ('o_maint', 'Repairs & maintenance', dw, 'maint')]:
        W.c('D', f'={qty}', FN, '0', align='center'); W.c('E', f'={AR[ref]}', FN, M)
        calc_row(key, label, f'=D{W.r}*E{W.r}')
    calc_row('t_ong', 'Total ongoing costs – fully let', '=SUM(I{}:I{})'.format(R['o_mgr'], R['o_maint']), bold=True, fill=F_SEC)
    calc_row('ong_now', 'Total ongoing costs – residents now', f"=I{R['t_ong']}-I{R['o_mgr']}+I{R['gross_now']}*E{R['o_mgr']}")

    # ------------------------------------------------------------ 11 returns
    section('11. RETURNS', head=False)
    calc_row('net', 'Net income – fully let', f"=I{R['gross']}-I{R['t_ong']}", bold=True)
    calc_row('net_now', 'Net income – residents now', f"=I{R['gross_now']}-I{R['ong_now']}")
    calc_row('yld', 'Net yield on TDC – fully let', f"=IFERROR(I{R['net']}/I{R['tdc']},0)", fmt=P)
    calc_row('yld_now', 'Net yield on TDC – residents now', f"=IFERROR(I{R['net_now']}/I{R['tdc']},0)", fmt=P)
    W.c('E', f"={AR['cap']}", FI, P, F_IN); calc_row('cap', 'Valuation cap rate', '', note='Type over to override for this project')
    calc_row('value', 'Completed, leased value (net ÷ cap rate)', f"=IFERROR(I{R['net']}/E{R['cap']},0)", bold=True)
    calc_row('profit', 'Profit on completion', f"=I{R['value']}-I{R['tdc']}")
    calc_row('poc', 'Profit on cost', f"=IFERROR(I{R['profit']}/I{R['tdc']},0)", fmt=P)
    W.r += 1
    W.c('E', f"={AR['lvr']}", FN, P1); calc_row('cba', 'CBA refinance loan (LVR × value, capped at TDC)', f"=MAX(0,MIN(E{W.r}*I{R['value']},I{R['tdc']}))")
    W.c('E', f"={AR['ir']}", FN, P); calc_row('cba_int', 'CBA interest p.a.', f"=I{R['cba']}*E{W.r}")
    calc_row('eq_left', 'Equity left in after refinance', f"=I{R['tdc']}-I{R['cba']}")
    calc_row('eq_back', 'Equity returned at refinance (− = top-up needed)', f"=I{R['cba']}-I{R['fac']}")
    calc_row('lev', 'Levered return: (net income − interest) ÷ equity left in',
             f"=IF(I{R['eq_left']}>I{R['tdc']}*0.005,(I{R['net']}-I{R['cba_int']})/I{R['eq_left']},\"n/a – all equity out\")", fmt=P)
    W.r += 1
    W.c('B', 'Holding with the CBA loan (per year)', FB); W.r += 1
    calc_row('cash_io', 'Cash left after interest only', f"=I{R['net']}-I{R['cba_int']}", bold=True)
    W.c('E', f"={AR['term']}", FN, '0" yrs"')
    calc_row('cba_pi', 'CBA principal & interest repayments', f"=IF(I{R['cba']}>0,PMT(E{R['cba_int']}/12,E{W.r}*12,-I{R['cba']})*12,0)")
    calc_row('cash_pi', 'Cash left after principal & interest', f"=I{R['net']}-I{R['cba_pi']}", bold=True)
    calc_row('icr', 'Rent covers the interest (times)', f"=IF(I{R['cba_int']}>0,I{R['net']}/I{R['cba_int']},0)", fmt='0.00"x"')
    calc_row('dscr', 'Rent covers principal & interest (times)', f"=IF(I{R['cba_pi']}>0,I{R['net']}/I{R['cba_pi']},0)", fmt='0.00"x"')

    # ------------------------------------------------------------ 12 hold & sell
    section('12. HOLD & SELL TO AN INSTITUTION', head=False)
    W.c('B', 'Rent and costs rise with CPI each year (Assumptions). Sold at the sale cap rate on that year\'s net income, less sale costs and the loan payout.', FG); W.r += 1
    y0 = W.r
    for col, h in zip('BDEFGHIJ', ['Year', 'Gross rent', 'Net income', 'Interest only', 'Cash after IO', 'P&I', 'Cash after P&I', 'Loan left (P&I)']):
        W.c(col, h, FH, fill=F_SUB, align='center')
    for col, h in zip('NOPQ', ['IRR 5y IO', 'IRR 5y P&I', 'IRR 10y IO', 'IRR 10y P&I']):
        W.c(col, h, FG)
    eqc = f"$I${R['eq_left']}"
    for col in 'NOPQ':
        ws[f'{col}{y0}'] = f'=-{eqc}'; ws[f'{col}{y0}'].font = FG; ws[f'{col}{y0}'].number_format = M
    W.r += 1
    g = AR['rg']
    yr = {}
    for y in range(1, 11):
        r = W.r; yr[y] = r
        W.c('B', y, FN, '0', align='center')
        W.c('D', f"=I{R['gross']}*(1+{g})^({y}-1)", FN, M)
        W.c('E', f"=I{R['net']}*(1+{g})^({y}-1)", FN, M)
        W.c('F', f"=I{R['cba_int']}", FN, M)
        W.c('G', f'=E{r}-F{r}', FB, M)
        W.c('H', f"=I{R['cba_pi']}", FN, M)
        W.c('I', f'=E{r}-H{r}', FB, M)
        W.c('J', f"=IF(I{R['cba']}>0,MAX(0,FV(E{R['cba_int']}/12,12*{y},I{R['cba_pi']}/12,-I{R['cba']})),0)", FN, M)
        if y in (5, 10):
            for cc in 'BDEFGHIJ': ws[f'{cc}{r}'].fill = PatternFill('solid', fgColor='FFF9E6')
        W.r += 1
    W.r += 1
    hx = W.r
    for col, h in zip('BFGHI', ['Sell to an institution', '5 yrs – IO', '5 yrs – P&I', '10 yrs – IO', '10 yrs – P&I']):
        W.c(col, h, FW, fill=F_HEAD, align=None if col == 'B' else 'center')
    for cc in 'CDE': ws[f'{cc}{hx}'].fill = F_HEAD
    W.r += 1
    sc = {'F': (5, 'io'), 'G': (5, 'pi'), 'H': (10, 'io'), 'I': (10, 'pi')}
    salecap = f"IF({AR['salecap']}>0,{AR['salecap']},E{R['cap']})"
    xr = {}
    labels = [('cash', 'Cash from rent over the hold (after loan)'), ('val', 'Sale value'), ('cost', 'Less sale costs'),
              ('pay', 'Less CBA loan paid out'), ('proc', 'Net sale proceeds'), ('eq', 'Less equity left in'),
              ('prof', 'TOTAL PROFIT'), ('mult', 'Equity multiple (cash back ÷ equity)'), ('irr', 'IRR on equity')]
    for k, lab in labels:
        xr[k] = W.r; W.c('B', lab, FB if k in ('proc', 'prof', 'irr') else FN); W.r += 1
    helper = {'F': 'N', 'G': 'O', 'H': 'P', 'I': 'Q'}
    for col, (N, mode) in sc.items():
        cashcol = 'G' if mode == 'io' else 'I'
        ws[f'{col}{xr["cash"]}'] = f'=SUM({cashcol}{yr[1]}:{cashcol}{yr[N]})'
        ws[f'{col}{xr["val"]}'] = f'=E{yr[N]}/{salecap}'
        ws[f'{col}{xr["cost"]}'] = f"=-{AR['exitcost']}"
        ws[f'{col}{xr["pay"]}'] = f"=-I{R['cba']}" if mode == 'io' else f'=-J{yr[N]}'
        ws[f'{col}{xr["proc"]}'] = f'={col}{xr["val"]}+{col}{xr["cost"]}+{col}{xr["pay"]}'
        ws[f'{col}{xr["eq"]}'] = f'=-{eqc}'
        ws[f'{col}{xr["prof"]}'] = f'={col}{xr["cash"]}+{col}{xr["proc"]}+{col}{xr["eq"]}'
        ok = f"{eqc}>I{R['tdc']}*0.005"
        ws[f'{col}{xr["mult"]}'] = f'=IF({ok},({col}{xr["cash"]}+{col}{xr["proc"]})/{eqc},"n/a")'
        hc = helper[col]
        for y in range(1, N + 1):
            ws[f'{hc}{yr[y]}'] = f'={cashcol}{yr[y]}' + (f'+{col}{xr["proc"]}' if y == N else '')
            ws[f'{hc}{yr[y]}'].font = FG; ws[f'{hc}{yr[y]}'].number_format = M
        ws[f'{col}{xr["irr"]}'] = f'=IF({ok},IFERROR(IRR({hc}{y0}:{hc}{yr[N]}),"n/a"),"n/a")'
        for k in xr:
            c = ws[f'{col}{xr[k]}']
            c.number_format = P if k == 'irr' else ('0.00"x"' if k == 'mult' else M)
            c.font = FB if k in ('proc', 'prof', 'irr') else FN
            if k == 'prof': c.fill = F_KEY
    ws[f'B{xr["prof"]}'].fill = F_KEY
    W.r += 1
    W.c('B', 'For the portfolio overview', FG); W.r += 1
    for key, lab, col, k, fmt in [('x5io', 'Total profit – sell after 5 yrs, interest only', 'F', 'prof', M),
                                  ('x5pi', 'Total profit – sell after 5 yrs, P&I', 'G', 'prof', M),
                                  ('x10io', 'Total profit – sell after 10 yrs, interest only', 'H', 'prof', M),
                                  ('x10pi', 'Total profit – sell after 10 yrs, P&I', 'I', 'prof', M),
                                  ('irr5io', 'IRR on equity – 5 yrs, interest only', 'F', 'irr', P),
                                  ('irr10io', 'IRR on equity – 10 yrs, interest only', 'H', 'irr', P)]:
        calc_row(key, lab, f'={col}{xr[k]}', fmt=fmt)

    # forward references
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                if '__LET__' in c.value:
                    c.value = c.value.replace('__LET__', f"I{R['sda_sum']}/52*{AR['letwk']}")
                if '__NP__' in c.value:
                    c.value = c.value.replace('__NP__', str(R['n_places']))
    # validations
    for formula, rng in [('"Y,N"', f'C1:C{R["mkt"]}'), ('"+GST,Inc,None"', f'F1:F{R["mkt"]}'),
                         ('"Estimate,Quote,Contract,Paid"', f'J1:J{R["mkt"]}'), ('"Y,N"', f'C{R["pl0"]}:C{R["pl5"]}')]:
        dv = DataValidation(type='list', formula1=formula, allow_blank=True); ws.add_data_validation(dv); dv.add(rng)
    ws.freeze_panes = 'C4'
    ws.print_area = f'A1:L{W.r}'
    ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return R


def _overview(wb, title, names, R):
    ws = wb['Overview']
    ws.sheet_view.showGridLines = False
    n = len(names)
    pc = [CL(3 + i) for i in range(n)]          # project columns
    tot, tex, tg = CL(3 + n), CL(4 + n), CL(5 + n)
    ws.column_dimensions['A'].width = 6; ws.column_dimensions['B'].width = 48
    for col in pc + [tot, tex, tg]:
        ws.column_dimensions[col].width = 14
    ws['A1'] = title; ws['A1'].font = FT
    ws['A2'] = 'Portfolio feasibility – every figure links to the project sheets. Change a project and this sheet updates.'; ws['A2'].font = FG
    r = 4
    ws.cell(r, 2, 'Project').font = FB
    for i, nm in enumerate(names):
        c = ws.cell(r, 3 + i, f"='{nm}'!A1"); c.font = FB
        c.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
    for col, h in [(tot, 'PORTFOLIO\nInc GST'), (tex, 'Portfolio\nEx GST'), (tg, 'Portfolio\nGST')]:
        ws[f'{col}{r}'] = h; ws[f'{col}{r}'].font = FB
        ws[f'{col}{r}'].alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
    ws.row_dimensions[r].height = 44
    for lab, key in [('Build model', 'h_model'), ('Status', 'h_status'), ('Dwellings', 'h_dw')]:
        r += 1
        ws.cell(r, 2, lab).font = FN
        for i, nm in enumerate(names):
            c = ws.cell(r, 3 + i, f"='{nm}'!C{R[key]}"); c.font = FN
            c.alignment = Alignment(horizontal='center', wrap_text=True)
        if key == 'h_dw':
            ws[f'{tot}{r}'] = f'=SUM({pc[0]}{r}:{pc[-1]}{r})'; ws[f'{tot}{r}'].font = FB
            ws[f'{tot}{r}'].alignment = Alignment(horizontal='center')
    r += 1
    tmpl = wb[names[0]]
    by_row = {v: k for k, v in R.items()}
    ratio = {'yld': ('net', 'tdc'), 'yld_now': ('net_now', 'tdc'), 'poc': ('profit', 'tdc'), 'tdc_pp': ('tdc', 'n_places'),
             'icr': ('net', 'cba_int'), 'dscr': ('net', 'cba_pi')}
    skip = {'cap', 'contract', 'stage_chk', 'sda_sum'} | {f'stage{i}' for i in range(1, 7)} | {f'pl{i}' for i in range(PLACES)}
    has_gst = set()
    ov = {}
    for tr in range(R['price'] - 2, tmpl.max_row + 1):
        key = by_row.get(tr)
        a, b = tmpl[f'A{tr}'].value, tmpl[f'B{tr}'].value
        if tmpl[f'A{tr}'].font.color is not None and tmpl[f'A{tr}'].font.color.rgb == 'FFFFFFFF' and a:
            r += 1
            for cc in range(1, 6 + n): ws.cell(r, cc).fill = F_HEAD
            ws.cell(r, 1, a).font = FW
            r += 1
            continue
        if not key or key in skip or key.startswith('h_'):
            continue
        bold = bool(tmpl[f'B{tr}'].font.bold)
        fill = tmpl[f'B{tr}'].fill if tmpl[f'B{tr}'].fill.fill_type else None
        fill = PatternFill('solid', fgColor=fill.fgColor.rgb[-6:]) if fill else None
        fmt = tmpl[f'I{tr}'].number_format
        ws.cell(r, 1, a).font = FG
        ws.cell(r, 2, b.strip() if isinstance(b, str) else b).font = FB if bold else FN
        for i, nm in enumerate(names):
            c = ws.cell(r, 3 + i, f"='{nm}'!I{tr}"); c.number_format = fmt; c.font = FB if bold else FN
        if key in ratio:
            na, nb = ratio[key]
            f = f'=IFERROR({tot}@@{na}@@/{tot}@@{nb}@@,0)'
        elif key.startswith('irr'):
            f = None
        elif key == 'lev':
            f = (f'=IF({tot}{ov["eq_left"]}>{tot}{ov["tdc"]}*0.005,({tot}{ov["net"]}-{tot}{ov["cba_int"]})'
                 f'/{tot}{ov["eq_left"]},"n/a")')
        else:
            f = f'=SUM({pc[0]}{r}:{pc[-1]}{r})'
        c = ws[f'{tot}{r}']; c.value = f if f is not None else '–'; c.number_format = fmt; c.font = FB; c.fill = F_SUB
        if f is None: c.alignment = Alignment(horizontal='right')
        # Ex GST / GST only for cost lines and subtotals (they have G/H on the project sheet)
        if tmpl[f'G{tr}'].value is not None and key not in ratio:
            for col, src in [(tex, 'G'), (tg, 'H')]:
                ws[f'{col}{r}'] = '=' + '+'.join(f"'{nm}'!{src}{tr}" for nm in names)
                ws[f'{col}{r}'].number_format = M; ws[f'{col}{r}'].font = FB if bold else FN
        if fill:
            for cc in range(1, 3 + n): ws.cell(r, cc).fill = fill
        ov[key] = r; r += 1
    import re
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and '@@' in c.value:
                c.value = re.sub(r'@@(\w+)@@', lambda mm: str(ov[mm.group(1)]), c.value)
    ws.freeze_panes = 'C5'
    ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return ov


def _fund_sheet(wb, ov, n_proj, A, AR, cap_f=None, net_f=None, rate_f=None, net_label=None):
    ws = wb.create_sheet('Investor fund')
    ws.sheet_view.showGridLines = False
    Fd = A['fund']
    for c, w in zip('ABCDEFGHIJ', [3, 44, 15, 15, 15, 15, 15, 3, 14, 14]):
        ws.column_dimensions[c].width = w
    ws['B1'] = 'Investor fund – no debt'; ws['B1'].font = FT
    ws['B2'] = 'Investors fund 100% of the cost. No construction loan or CBA loan. Change the yellow cells to test other terms.'; ws['B2'].font = FG
    tot = CL(3 + n_proj)
    inputs = [('cap', 'Funds raised (total development cost)', cap_f or f"=Overview!{tot}{ov['tdc']}", M, False),
              ('net', net_label or 'Net rent a year once leased (residents now)', net_f or f"=Overview!{tot}{ov['net_now']}", M, False),
              ('rate', 'Fixed return to investors (p.a., on funds invested)', rate_f if rate_f else Fd['rate'], P, not rate_f),
              ('fee', 'Radius fund management fee (p.a., on funds invested)', Fd['fee'], P, True),
              ('start', 'Fixed return starts after (months)', Fd['startMonths'], '0', True),
              ('build', 'Build period before rent starts (months)', f"={AR['cMonths'].split('!')[0]}!{AR['cMonths'].split('!')[1]}", '0', False),
              ('split', "Investors' share of the upside at the sale", Fd['split'], '0%', True),
              ('g', 'Rent and cost growth a year (CPI)', f"={AR['rg']}", P1, False),
              ('salecap', 'Sale cap rate', f"=IF({AR['salecap']}>0,{AR['salecap']},{AR['cap']})", P, False),
              ('exit', 'Sale costs (all projects)', f"={AR['exitcost']}*{n_proj}", M, False)]
    ref, r = {}, 4
    for key, lab, v, fmt, inp in inputs:
        ws[f'B{r}'] = lab; ws[f'B{r}'].font = FN
        c = ws[f'C{r}']; c.value = v; c.number_format = fmt
        c.font = FI if inp else FB
        if inp: c.fill = F_IN
        ref[key] = f'$C${r}'; r += 1
    r += 1
    hdr = r
    for col, h in zip('BCDEFG', ['Year (from investment)', 'Net rent', 'Manager fee', 'Fixed return', 'Surplus', 'Fund cash']):
        ws[f'{col}{r}'] = h; ws[f'{col}{r}'].font = FW; ws[f'{col}{r}'].fill = F_HEAD
    ws[f'I{r}'] = 'IRR 5 yrs'; ws[f'J{r}'] = 'IRR 10 yrs'
    for col in 'IJ':
        ws[f'{col}{r}'].font = FG
        ws[f'{col}{r}'] = ws[f'{col}{r}'].value
    ws[f'I{r+0}'].value = 'IRR 5 yrs'
    r += 1
    y0 = r
    ws[f'I{y0}'] = f"=-{ref['cap']}"; ws[f'J{y0}'] = f"=-{ref['cap']}"
    for c in 'IJ': ws[f'{c}{y0}'].font = FG; ws[f'{c}{y0}'].number_format = M
    ws[f'B{y0}'] = 'Investment'; ws[f'B{y0}'].font = FG
    r += 1
    yr = {}
    for y in range(1, 11):
        yr[y] = r
        ws[f'B{r}'] = y; ws[f'B{r}'].alignment = Alignment(horizontal='left')
        k = f"({y}-ROUNDUP({ref['build']}/12,0))"
        ws[f'C{r}'] = f"=IF({k}>=1,{ref['net']}*(1+{ref['g']})^({k}-1),0)"
        ws[f'D{r}'] = f"=-{ref['cap']}*{ref['fee']}"
        ws[f'E{r}'] = f"=IF({y}>=INT({ref['start']}/12)+1,-{ref['cap']}*{ref['rate']},0)"
        ws[f'F{r}'] = f'=C{r}+D{r}+E{r}'
        ws[f'G{r}'] = f'=F{r}' if y == 1 else f'=G{r-1}+F{r}'
        for c in 'CDEFG': ws[f'{c}{r}'].number_format = M; ws[f'{c}{r}'].font = FB if c in 'FG' else FN
        if y in (5, 10):
            for c in 'BCDEFG': ws[f'{c}{r}'].fill = PatternFill('solid', fgColor='FFF9E6')
        r += 1
    r += 1
    hx = r
    for col, h in zip('BCD', ['Sell to an institution', 'After 5 yrs', 'After 10 yrs']):
        ws[f'{col}{r}'] = h; ws[f'{col}{r}'].font = FW; ws[f'{col}{r}'].fill = F_HEAD
    r += 1
    labs = [('val', 'Sale value'), ('cost', 'Less sale costs'), ('cash', 'Plus cash in the fund'), ('pool', 'Available to distribute'),
            ('capb', "Investors' capital back"), ('up', 'Upside to split'), ('invup', "Investors' share of the upside"),
            ('radup', "Radius' share of the upside"), ('fixed', 'Fixed returns paid to investors'),
            ('tot', 'Investors receive in total'), ('prof', "Investors' profit"), ('mult', "Investors' multiple"), ('irr', "Investors' IRR")]
    X = {}
    for k, lab in labs:
        X[k] = r; ws[f'B{r}'] = lab; ws[f'B{r}'].font = FB if k in ('pool', 'tot', 'prof', 'irr') else FN; r += 1
    for col, N, hc in [('C', 5, 'I'), ('D', 10, 'J')]:
        last = yr[N]
        ws[f'{col}{X["val"]}'] = f"=IF(C{last}>0,C{last},{ref['net']})/{ref['salecap']}"
        ws[f'{col}{X["cost"]}'] = f"=-{ref['exit']}"
        ws[f'{col}{X["cash"]}'] = f'=G{last}'
        ws[f'{col}{X["pool"]}'] = f'={col}{X["val"]}+{col}{X["cost"]}+{col}{X["cash"]}'
        ws[f'{col}{X["capb"]}'] = f"=MAX(0,MIN({ref['cap']},{col}{X['pool']}))"
        ws[f'{col}{X["up"]}'] = f"=MAX(0,{col}{X['pool']}-{ref['cap']})"
        ws[f'{col}{X["invup"]}'] = f"={col}{X['up']}*{ref['split']}"
        ws[f'{col}{X["radup"]}'] = f"={col}{X['up']}-{col}{X['invup']}"
        ws[f'{col}{X["fixed"]}'] = f'=-SUM(E{yr[1]}:E{last})'
        ws[f'{col}{X["tot"]}'] = f'={col}{X["fixed"]}+{col}{X["capb"]}+{col}{X["invup"]}'
        ws[f'{col}{X["prof"]}'] = f"={col}{X['tot']}-{ref['cap']}"
        ws[f'{col}{X["mult"]}'] = f"=IFERROR({col}{X['tot']}/{ref['cap']},0)"
        for y in range(1, N + 1):
            ws[f'{hc}{yr[y]}'] = f'=-E{yr[y]}' + (f'+{col}{X["capb"]}+{col}{X["invup"]}' if y == N else '')
            ws[f'{hc}{yr[y]}'].font = FG; ws[f'{hc}{yr[y]}'].number_format = M
        ws[f'{col}{X["irr"]}'] = f'=IFERROR(IRR({hc}{y0}:{hc}{last}),"n/a")'
        for k in X:
            c = ws[f'{col}{X[k]}']
            c.number_format = P if k == 'irr' else ('0.00"x"' if k == 'mult' else M)
            c.font = FB if k in ('pool', 'tot', 'prof', 'irr') else FN
            if k == 'prof': c.fill = F_KEY
    ws[f'B{X["prof"]}'].fill = F_KEY
    r += 1
    ws[f'B{r}'] = 'Surplus stays in the fund. Fund cash below zero in the early years (fee before rent starts) has to come from the money raised.'
    ws[f'B{r}'].font = FG


def build_feaso_workbook(title, projects, A):
    wb = Workbook()
    wb.active.title = 'Overview'
    AR = _assumptions(wb, A)
    names, R = [], None
    for i, pr in enumerate(projects, 1):
        nm = f"P{i:02d} {pr['short']}"[:31].replace("'", '')
        names.append(nm)
        R = _project_sheet(wb, nm, pr, AR)
    ov = _overview(wb, title, names, R)
    if isinstance(A.get('fund'), dict):
        _fund_sheet(wb, ov, len(names), A, AR)
        wb.move_sheet('Investor fund', offset=-(len(names) + 1))
    wb.move_sheet('Assumptions', offset=len(names))
    return wb, R, ov, names


# ======================================================== EARNINGS (ADMIN ONLY) ===
# Kept deliberately separate: takes already-calculated per-project figures and never
# touches the feaso workbook. Only ever served to admins.
def build_earnings_workbook(title, rows, A, fund=None):
    """rows: list of dicts with name, model, price, contract, titles, dw, gross, sda_sum, value."""
    wb = Workbook()
    ws = wb.active; ws.title = 'Earnings'
    ws.sheet_view.showGridLines = False
    n = len(rows)
    pc = [CL(4 + i) for i in range(n)]
    tot, tex = CL(4 + n), CL(5 + n)
    ws.column_dimensions['A'].width = 4; ws.column_dimensions['B'].width = 46; ws.column_dimensions['C'].width = 30
    for col in pc + [tot, tex]:
        ws.column_dimensions[col].width = 15
    ws['A1'] = f'{title} – Group earnings'; ws['A1'].font = FT
    ws['A2'] = 'ADMIN ONLY – Jason & Tanya. Not for clients, funders or partners. Gross, before tax and wages.'
    ws['A2'].font = Font(name='Arial', size=10, bold=True, color='C00000')
    # inputs block
    r = 4
    ws.cell(r, 2, 'Inputs').font = FB
    for i, row in enumerate(rows):
        c = ws.cell(r, 4 + i, row['name']); c.font = FB; c.alignment = Alignment(wrap_text=True, horizontal='center')
    ws.row_dimensions[r].height = 40
    inputs = [('price', 'Purchase price'), ('ba', "Buyer's advocacy charged (inc GST)"), ('pm', 'PM fee charged (inc GST)'),
              ('cam', 'Security cameras charged (inc GST)'), ('letting', 'Letting fee charged (inc GST)'),
              ('mkt', 'Marketing fee charged (inc GST)'), ('houses', 'Houses'), ('villas', 'Villas'),
              ('margin', 'Radius margin per house in the build price (inc GST)'), ('fundfee', 'Fund management fee p.a. (fund mode)'), ('titles', 'Titles'),
              ('dw', 'Dwellings'), ('gross', 'Gross rent p.a. (SDA + RRC, fully let)'),
              ('value', 'Completed value (sale price if sold)')]
    IR = {}
    for key, lab in inputs:
        r += 1
        ws.cell(r, 2, lab).font = FN
        for i, row in enumerate(rows):
            c = ws.cell(r, 4 + i, row[key]); c.font = FI; c.fill = F_IN
            c.number_format = '0' if key in ('titles', 'dw', 'houses', 'villas') else M
        IR[key] = r
    r += 2
    ws.cell(r, 2, 'Rates').font = FB
    rates = [('bm_v', 'Radius margin in the build price – per villa (inc GST)', 0, M),
             ('clean', 'Cleaning & grounds per title p.a. (inc GST)', A['cleanPa'], M),
             ('maint', 'Maintenance per dwelling p.a. (inc GST)', A['maint'], M),
             ('mgr', 'SDA management (% of gross, inc GST)', A['sdaMgr'], P1),
             ('comm', 'Sales commission (% of sale, + GST)', 0.02, P1),
             ('sold', 'Model a sale through Radius Real Estate? (Y/N)', 'N', None),
             ('hold', 'Hold period (years)', 5, '0'), ('gst', 'GST', 0.10, '0%')]
    RR = {}
    for key, lab, v, fmt in rates:
        r += 1
        ws.cell(r, 2, lab).font = FN
        c = ws.cell(r, 4, v); c.font = FI; c.fill = F_IN
        if fmt: c.number_format = fmt
        RR[key] = f'$D${r}'
    g, hold = RR['gst'], RR['hold']
    r += 2
    hdr = ['', 'Fee', 'Timing'] + [row['name'] for row in rows] + ['TOTAL\ninc GST', 'TOTAL\nex GST']
    for ci, h in enumerate(hdr, 1):
        c = ws.cell(r, ci, h); c.font = FW; c.fill = F_HEAD; c.alignment = Alignment(wrap_text=True, horizontal='center')
    ws.row_dimensions[r].height = 40
    # (entity, label, timing, formula(col) -> inc GST, gst_included?)
    def col_ref(key, col): return f'{col}${IR[key]}'
    lines = [
        ('Radius', "Buyer's advocacy", 'At purchase', lambda c: f"={col_ref('ba', c)}"),
        ('Radius', 'Project management fee', 'During build', lambda c: f"={col_ref('pm', c)}"),
        ('Radius', 'Cleaning & grounds', 'Per year', lambda c: f"={col_ref('titles', c)}*{RR['clean']}"),
        ('Radius – Build margin', 'Margin built into the build price', 'During build', lambda c: f"={col_ref('houses', c)}*{col_ref('margin', c)}+{col_ref('villas', c)}*{RR['bm_v']}"),
        ('Radius – Maintenance', 'Repairs & maintenance', 'Per year', lambda c: f"={col_ref('dw', c)}*{RR['maint']}"),
        ('Radius – Fund manager', 'Fund management fee on funds invested', 'Per year', lambda c: f"={col_ref('fundfee', c)}"),
        ('Away Site Vision', 'Security cameras – install & monitoring', 'During build', lambda c: f"={col_ref('cam', c)}"),
        ('Haven SDA', 'Letting fee (2 weeks SDA rent per resident)', 'At leasing', lambda c: f"={col_ref('letting', c)}"),
        ('Haven SDA', 'Marketing fee', 'At leasing', lambda c: f"={col_ref('mkt', c)}"),
        ('Haven SDA', 'SDA management', 'Per year', lambda c: f"={col_ref('gross', c)}*{RR['mgr']}"),
        ('Radius Real Estate', 'Sales commission', 'On sale', lambda c: f"=IF({RR['sold']}=\"Y\",{col_ref('value', c)}*{RR['comm']}*(1+{g}),0)"),
    ]
    entity_rows, cur = {}, None
    LR = []
    for ent, lab, timing, fn in lines:
        if ent != cur:
            r += 1; cur = ent
            ws.cell(r, 2, ent).font = FB
            for ci in range(1, 6 + n): ws.cell(r, ci).fill = F_SEC
        r += 1
        ws.cell(r, 2, '   ' + lab).font = FN; ws.cell(r, 3, timing).font = FG
        for col in pc:
            c = ws[f'{col}{r}']; c.value = fn(col); c.number_format = M; c.font = FN
        ws[f'{tot}{r}'] = f'=SUM({pc[0]}{r}:{pc[-1]}{r})'; ws[f'{tot}{r}'].number_format = M; ws[f'{tot}{r}'].font = FB
        ws[f'{tex}{r}'] = f'={tot}{r}/(1+{g})'; ws[f'{tex}{r}'].number_format = M
        entity_rows.setdefault(ent, []).append((r, timing)); LR.append((r, timing))
    # summary
    r += 2
    hdr2 = ['', 'Summary by business', ''] + [row['name'] for row in rows] + ['TOTAL\ninc GST', 'TOTAL\nex GST']
    for ci, h in enumerate(hdr2, 1):
        c = ws.cell(r, ci, h); c.font = FW; c.fill = F_HEAD; c.alignment = Alignment(wrap_text=True, horizontal='center')
    ws.row_dimensions[r].height = 40
    sumrows = []
    for ent, lst in entity_rows.items():
        once = [x for x, t in lst if t != 'Per year']; yearly = [x for x, t in lst if t == 'Per year']
        for lab, fml in [('once-off', once), ('per year', yearly)]:
            if not fml: continue
            r += 1
            ws.cell(r, 2, f'{ent} – {lab}').font = FN
            for col in pc + [tot]:
                ws[f'{col}{r}'] = '=' + '+'.join(f'{col}{x}' for x in fml); ws[f'{col}{r}'].number_format = M
            ws[f'{tex}{r}'] = f'={tot}{r}/(1+{g})'; ws[f'{tex}{r}'].number_format = M
        r += 1
        ws.cell(r, 2, f'{ent} – total over the hold').font = FB
        for col in pc + [tot]:
            parts = [f'{col}{x}' for x in once] + [f'{col}{x}*{hold}' for x in yearly]
            ws[f'{col}{r}'] = '=' + '+'.join(parts); ws[f'{col}{r}'].number_format = M; ws[f'{col}{r}'].font = FB
        ws[f'{tex}{r}'] = f'={tot}{r}/(1+{g})'; ws[f'{tex}{r}'].number_format = M; ws[f'{tex}{r}'].font = FB
        for ci in range(2, 6 + n): ws.cell(r, ci).border = Border(bottom=Side(style='thin', color='BFBFBF'))
        sumrows.append(r)
    r += 1
    ws.cell(r, 2, 'ALL BUSINESSES – total over the hold').font = FB
    for col in pc + [tot, tex]:
        ws[f'{col}{r}'] = '=' + '+'.join(f'{col}{x}' for x in sumrows); ws[f'{col}{r}'].number_format = M
        ws[f'{col}{r}'].font = FB; ws[f'{col}{r}'].fill = F_KEY
    ws.cell(r, 2).fill = F_KEY; ws.cell(r, 3).fill = F_KEY
    if fund:
        r += 2
        ws.cell(r, 2, 'Investor fund – Radius share of the upside at the sale (whole portfolio)').font = FB
        for ci in range(2, 6 + n): ws.cell(r, ci).fill = F_SEC
        for lab, key in [('Funds raised', 'capital'), ('Fixed return to investors', 'rate'),
                         ('Radius share of the upside – sell after 5 years', 'up5'), ('Radius share of the upside – sell after 10 years', 'up10'),
                         ('Fund management fees over 5 years (all projects)', 'fees5'), ('Fund management fees over 10 years (all projects)', 'fees10')]:
            r += 1
            ws.cell(r, 2, '   ' + lab).font = FN
            c = ws.cell(r, 4, fund.get(key) or 0); c.font = FB; c.number_format = P if key == 'rate' else M
        r += 1
        ws.cell(r, 2, 'The fund management fee per project per year is in the Radius – Fund manager line above (its hold total uses the hold period). The upside is split once, on the sale of the whole portfolio.').font = FG
    ws.freeze_panes = 'D5'
    ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return wb


