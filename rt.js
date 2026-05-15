'use strict';
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, PageBreak, LevelFormat, SimpleField
} = require('docx');

const TEAL='1A5057', TEAL_L='D0E9EC', GRAY_H='F2F2F2', GOLD='C9A84C';
const bc={style:BorderStyle.SINGLE,size:4,color:'CCCCCC'};
const ba={top:bc,bottom:bc,left:bc,right:bc};

function p(text,opts={}){
  const runs=typeof text==='string'
    ?[new TextRun({text,font:'Calibri',size:opts.size||22,bold:opts.bold||false,color:opts.color||'000000',italics:opts.italic||false})]
    :text.map(t=>typeof t==='string'?new TextRun({text:t,font:'Calibri',size:22}):t);
  return new Paragraph({children:runs,alignment:opts.align||AlignmentType.LEFT,
    spacing:{before:opts.before||0,after:opts.after||80},
    indent:opts.indent?{left:opts.indent}:undefined});
}
function h1(t){return new Paragraph({children:[new TextRun({text:t,font:'Calibri',size:28,bold:true,color:TEAL})],
  spacing:{before:280,after:120},border:{bottom:{style:BorderStyle.SINGLE,size:8,color:TEAL,space:2}}});}
function h2(t){return new Paragraph({children:[new TextRun({text:t,font:'Calibri',size:24,bold:true,color:TEAL})],
  spacing:{before:200,after:80}});}
function bullet(text){return new Paragraph({numbering:{reference:'bullets',level:0},
  children:[new TextRun({text,font:'Calibri',size:22})],spacing:{before:30,after:30}});}
function sep(){return new Paragraph({children:[],border:{bottom:{style:BorderStyle.SINGLE,size:4,color:'CCCCCC',space:2}},spacing:{before:160,after:160}});}
function pb(){return new Paragraph({children:[new PageBreak()],spacing:{before:0,after:0}});}

function tbl(headers,rows,colW){
  const hw=colW.reduce((a,b)=>a+b,0);
  const hdr=new TableRow({children:headers.map((h,i)=>new TableCell({
    borders:ba,width:{size:colW[i],type:WidthType.DXA},
    shading:{fill:TEAL,type:ShadingType.CLEAR},
    margins:{top:80,bottom:80,left:120,right:120},
    children:[new Paragraph({children:[new TextRun({text:h,font:'Calibri',size:20,bold:true,color:'FFFFFF'})],alignment:AlignmentType.CENTER})]
  }))});
  const drs=rows.map((row,ri)=>new TableRow({children:row.map((cell,ci)=>{
    const bold=cell.includes('>>>')||cell.includes('POSITIVO')||cell.includes('H PROGETTO')||cell.includes('TOTALE');
    const color=cell.includes('POSITIVO')?'006600':cell.includes('NON CONF')?'CC0000':'000000';
    return new TableCell({
      borders:ba,width:{size:colW[ci],type:WidthType.DXA},
      shading:{fill:ri%2===0?'FFFFFF':GRAY_H,type:ShadingType.CLEAR},
      margins:{top:60,bottom:60,left:120,right:120},
      children:[new Paragraph({children:[new TextRun({text:cell,font:'Calibri',size:20,bold,color})],
        alignment:ci===0?AlignmentType.LEFT:AlignmentType.CENTER})]
    });
  })}));
  return new Table({width:{size:hw,type:WidthType.DXA},columnWidths:colW,rows:[hdr,...drs]});
}

function box(lines){return lines.map(l=>new Paragraph({
  children:[new TextRun({text:l,font:'Calibri',size:21,bold:l.includes('>>>'),color:TEAL})],
  shading:{fill:TEAL_L,type:ShadingType.CLEAR},spacing:{before:40,after:40},indent:{left:240,right:240}}));}

// ══ COPERTINA ══════════════════════════════════════════════════════════════
const cover=[
  new Paragraph({children:[],spacing:{before:1200,after:0}}),
  new Paragraph({children:[new TextRun({text:'ACQUALAB srl',font:'Calibri',size:56,bold:true,color:TEAL})],alignment:AlignmentType.CENTER,spacing:{after:120}}),
  new Paragraph({children:[new TextRun({text:'\u201cNon solo una piscina\u201d',font:'Calibri',size:28,italics:true,color:'555555'})],alignment:AlignmentType.CENTER,spacing:{after:60}}),
  new Paragraph({children:[new TextRun({text:'Master Pool Building \u2014 Massima Eccellenza d\u2019Arte',font:'Calibri',size:22,color:GOLD})],alignment:AlignmentType.CENTER,spacing:{after:600}}),
  new Paragraph({children:[],border:{bottom:{style:BorderStyle.SINGLE,size:12,color:TEAL,space:4}},spacing:{after:0}}),
  new Paragraph({children:[],spacing:{before:600,after:0}}),
  new Paragraph({children:[new TextRun({text:'RELAZIONE TECNICA',font:'Calibri',size:48,bold:true,color:TEAL})],alignment:AlignmentType.CENTER,spacing:{after:120}}),
  new Paragraph({children:[new TextRun({text:'Dimensionamento Impianto Piscina',font:'Calibri',size:32,color:'333333'})],alignment:AlignmentType.CENTER,spacing:{after:480}}),
  new Paragraph({children:[new TextRun({text:'Cliente:',font:'Calibri',size:26,bold:true,color:'444444'})],alignment:AlignmentType.CENTER,spacing:{after:60}}),
  new Paragraph({children:[new TextRun({text:'Sig. MARCO B',font:'Calibri',size:34,bold:true,color:TEAL})],alignment:AlignmentType.CENTER,spacing:{after:400}}),
  new Paragraph({children:[new TextRun({text:`Data: ${new Date().toLocaleDateString('it-IT',{day:'2-digit',month:'long',year:'numeric'})}`,font:'Calibri',size:22,color:'555555'})],alignment:AlignmentType.CENTER,spacing:{after:400}}),
  new Paragraph({children:[new TextRun({text:'Viale Aldo Moro 2, 50023 Impruneta (FI) \u2014 Tel. (+39) 055 0136621 \u2014 (+39) 351 9227533',font:'Calibri',size:18,color:'666666'})],alignment:AlignmentType.CENTER,spacing:{after:40}}),
  new Paragraph({children:[new TextRun({text:'www.acqua-lab.it \u2014 info@acqua-lab.it \u2014 P.I. 02281140976 \u2014 Cod. univoco: TULURSB',font:'Calibri',size:18,color:'666666'})],alignment:AlignmentType.CENTER}),
  pb()
];

// ══ 1. PREMESSA ════════════════════════════════════════════════════════════
const s1=[
  h1('1. Premessa e Filosofia Progettuale'),
  p('\u201cLa qualit\u00e0 dipende soprattutto da ci\u00f2 che non si vede.\u201d',{italic:true,bold:true,size:24,color:TEAL,after:120}),
  p('L\u2019invisibile determina la durata nel lungo periodo: quote, impermeabilizzazioni, idraulica, drenaggi, locale tecnico, portate, spessori, dettagli nascosti. Una piscina non \u00e8 un prodotto: \u00e8 un sistema tecnico che deve funzionare in equilibrio. Se una sola parte \u00e8 sbagliata \u2014 struttura, filtrazione, idraulica, trattamento \u2014 tutto il sistema si destabilizza.',{after:80}),
  p('La riuscita del progetto dipende dall\u2019organizzazione del cantiere e dal coordinamento tra le fasi. Risparmiare all\u2019inizio significa spesso spendere molto di pi\u00f9 dopo.',{after:80}),
  p('La presente relazione documenta il dimensionamento esecutivo dell\u2019impianto idraulico per la piscina del Sig. Marco B. Ogni scelta progettuale \u00e8 supportata da calcolo numerico e riferimento normativo.',{after:120}),
];

// ══ 2. QUADRO NORMATIVO ════════════════════════════════════════════════════
const s2=[
  h1('2. Quadro Normativo'),
  tbl(['Norma','Ambito di applicazione','Ruolo nel progetto'],[
    ['UNI EN 16582-1/2/3','Sicurezza piscine \u2014 aspirazioni sommerse','Norma primaria: N\u22652 prese di fondo in parallelo, Q/(N-1) \u2264 Q max griglia, v griglia \u2264 0,5 m/s'],
    ['UNI EN 16713-2:2016','Piscine private \u2014 circolazione e filtrazione','T ricircolo (fino a 8h per domestiche), ripartizione 2/3 superficie + 1/3 fondo'],
    ['UNI EN 16713-3','Qualit\u00e0 acqua piscine private','Parametri chimici e microbiologici di riferimento (indicativi)'],
    ['UNI EN 13451-3:2022','Attrezzatura \u2014 prese di fondo (rif. prodotto)','Velocit\u00e0 massima sulla griglia delle prese di fondo'],
    ['D.Lgs. 152/2006 Tab.3 All.5','Acque reflue in fognatura','Conformit\u00e0 scarichi impianto filtrazione a cartuccia'],
  ],[1400,2800,4872]),
  p(''),
  p('Nota: i limiti di velocit\u00e0 nelle tubazioni (1,7 m/s aspirazione / 2,5 m/s mandata) sono criteri progettuali Acqualab per silenziosit\u00e0 e durata. Non derivano da UNI EN 13451, che disciplina esclusivamente la velocit\u00e0 sulla griglia delle prese di fondo.',{italic:true,color:'444444',after:120}),
];

// ══ 3. DESCRIZIONE IMPIANTO ════════════════════════════════════════════════
const s3=[
  h1("3. Descrizione dell'Impianto"),
  h2('3.1 Geometria Vasca'),
  tbl(['Parametro','Valore'],[
    ['Dimensioni vasca','9 \u00d7 5 m'],['Superficie specchio d\u2019acqua','45,0 m\u00b2'],['Perimetro','28,0 m'],
    ['Profondit\u00e0','Costante 1,50 m (100% vasca)'],['Volume totale','62,0 m\u00b3'],
    ['Costruzione','Calcestruzzo armato'],['Tipo circolazione','Skimmer sfioratore'],
    ['Tipo filtrazione','Cartuccia'],['Tubo interrato per tratto','A = flex  |  PF = flex  |  C = rigido  |  M = flex'],
  ],[3600,5472]),
  p(''),h2('3.2 Elementi Speciali'),
  bullet('Scala: 4 gradini, larghezza 1 m \u2014 volume sottratto 0,800 m\u00b3'),
  bullet('Spiaggetta: 4 \u00d7 1 m, profondit\u00e0 costante 1,28 m'),
  p(''),h2('3.3 Quote di Riferimento'),
  tbl(['Quota','Valore (rif. 0,00)'],[
    ['Livello acqua vasca','+0,10 m'],['Asse pompa','\u22120,50 m'],['Livello bordo vasca','0,00 m'],['Dislivello statico pompa\u2013vasca','0,00 mca'],
  ],[4536,4536]),
  p(''),h2('3.4 Schema Idraulico'),
  p('Vasca (skimmer + prese fondo) \u2192 Coll. asp. D.110 \u2192 Tratto C D.75 rigido \u2192 Pompa \u2192 Filtro \u2192 Coll. man. D.110 \u2192 Bocchette restituzione',{indent:360,color:'333333',after:80}),
  p('La cella di elettrolisi \u00e8 installata su by-pass dedicato a valle della pompa/filtro.',{italic:true,color:'444444',after:120}),
];

// ══ 4. PORTATE ══════════════════════════════════════════════════════════════
const s4=[
  h1('4. Calcolo della Portata di Progetto'),
  new Paragraph({children:[
    new TextRun({text:'Q progetto = V / T = 62,0 / 5 = ',font:'Calibri',size:22}),
    new TextRun({text:'12,4 m\u00b3/h',font:'Calibri',size:22,bold:true,color:TEAL}),
    new TextRun({text:'  (T = 5h \u2014 scelta progettuale Acqualab; UNI EN 16713-2 ammette fino a 8h)',font:'Calibri',size:20,color:'555555'}),
  ],indent:{left:360},spacing:{before:60,after:120}}),
  tbl(['Condizione','Portata','Note'],[
    ['Q progetto (requisito igienico minimo)','12,4 m\u00b3/h','V / T = 62,0 / 5'],
    ['Q DIMENSIONAMENTO (filtro pulito, convergata)','18,6 m\u00b3/h','Portata max reale \u2014 dimensionamento tubazioni, griglie PF, sicurezza'],
    ['Q effettiva a filtro a met\u00e0 vita','16,2 m\u00b3/h','Funzionamento normale \u2014 T = 3,8 h (\u2264 5h \u2713)'],
    ['>>> Q MEDIA DI ESERCIZIO','17,40 m\u00b3/h','DATO DI RIFERIMENTO \u2014 (16,2 + 18,6) / 2'],
  ],[2800,2100,4172]),
  p(''),
  ...box(['>>> Q MEDIA DI ESERCIZIO: 17,40 m\u00b3/h  \u2014  T ricircolo medio: 3,56 h  \u2014  Q media per skimmer: 5,80 m\u00b3/h cad.',
          'Portata rappresentativa del funzionamento reale dell\u2019impianto.']),
  p(''),
  h2('Ripartizione Superficie / Fondo (UNI EN 16713-2:2016)'),
  tbl(['Zona','Quota','Portata a Q dim. (18,6 m\u00b3/h)'],[
    ['Superficie (skimmer)','67%','12,4 m\u00b3/h'],['Fondo (prese di fondo)','33%','6,2 m\u00b3/h'],
  ],[3024,3024,3024]),
  p('Nessun gioco d\u2019acqua \u2014 portata aggiuntiva = 0 m\u00b3/h.',{italic:true,color:'444444',after:120}),
];

// ══ 5. TUBAZIONI ════════════════════════════════════════════════════════════
const s5=[
  h1('5. Dimensionamento Idraulico delle Tubazioni'),
  h2('5.1 Metodo e Criteri'),
  p('Metodo: Hazen-Williams con C = 150 (PVC liscio). Le tubazioni sono dimensionate alla portata MASSIMA della pompa a filtro pulito (18,6 m\u00b3/h), che rappresenta il flusso fisico reale pi\u00f9 gravoso.',{after:80}),
  tbl(['Criterio','Aspirazione','Mandata'],[
    ['Perdita di carico J (criterio primario)','J \u2264 40 mm/m','J \u2264 70 mm/m'],
    ['Velocit\u00e0 v (criterio Acqualab)','v \u2264 1,7 m/s','v \u2264 2,5 m/s'],
    ['Velocit\u00e0 griglia PF (UNI EN 13451-3)','v \u2264 0,5 m/s','\u2014'],
  ],[3200,2936,2936]),
  p('D. = diametro esterno nominale. I calcoli usano il diametro interno effettivo (tubo flessibile o PN16).',{italic:true,color:'444444',after:120}),
  h2('5.2 Tabella Tratti'),
  tbl(['Tr.','Descrizione','D.','L tubo','Raccordi','Leq','Leq tot.','Q perd.','Q dim. DN','v','J','H tratto'],[
    ['A','Skimmer\u2192coll.asp.','D.63','27,8 m','4\u00d790\u00b0 2\u00d745\u00b0 1VS 1TD','12,1 m','39,9 m','4,1','4,1 m\u00b3/h','0,483 m/s','4,9 mm/m','0,194 mca'],
    ['PF','PF\u2192coll.asp.\n(DN a Qmax)','D.75','21,9 m','4\u00d790\u00b0 1VS 2TD','14,7 m','36,6 m','4,1','12,4 m\u00b3/h','0,318 m/s','1,8 mm/m','0,064 mca'],
    ['C','Coll.asp.\u2192Pompa','D.75','6,7 m','12\u00d790\u00b0 1TD','25,2 m','31,9 m','12,4','12,4 m\u00b3/h','0,954 m/s','13,4 mm/m','0,429 mca'],
    ['M','Coll.man.\u2192Bocc.','D.50','21,0 m','5\u00d790\u00b0 1VS 1TD','10,8 m','31,8 m','3,1','3,1 m\u00b3/h','0,593 m/s','9,5 mm/m','0,301 mca'],
  ],[320,820,420,520,900,500,570,520,680,680,680,670]),
  p(''),
  h2('5.3 Collettori'),
  tbl(['Collettore','Diametro','Velocit\u00e0','Rapporto sezioni','Note'],[
    ['Aspirazione','D.110 PN10','0,43 m/s','2,25\u00d7','Calcolo automatico (1 uscita D.75, criterio 1,5\u00d7 sezioni uscenti)'],
    ['Mandata','D.110 PN10','0,47 m/s','1,27\u00d7','Override progettuale (calcolo auto: D.125)'],
  ],[1400,1200,1000,1000,4472]),
  p('Metodo collettori: Sez_coll > \u03a3(sezioni rami USCENTI) \u00d7 1,5 — fonte: ProfessioneAcqua.it.',{italic:true,color:'444444',after:120}),
];

// ══ 6. PREVALENZA ═══════════════════════════════════════════════════════════
const s6=[
  h1('6. Calcolo della Prevalenza'),
  tbl(['Componente','Valore (mca)','Note'],[
    ['H tratto A (ramo skimmer peggiore)','0,194','Q = 4,1 m\u00b3/h \u2014 D.63 flex'],
    ['H tratto PF (linea prese fondo)','0,064','Q = 4,1 m\u00b3/h \u2014 D.75 flex'],
    ['H tratto C (coll.asp. \u2192 pompa)','0,429','Q = 12,4 m\u00b3/h \u2014 D.75 rigido'],
    ['H aspirazione (ramo peg. + C)','0,623','max(A, PF) + C = 0,194 + 0,429'],
    ['H tratto M (mandata bocchetta)','0,301','Q = 3,1 m\u00b3/h \u2014 D.50 flex'],
    ['H filtro cartuccia (met\u00e0 vita)','7,000','Condizione di riferimento progettuale'],
    ['H filtro cartuccia (pulito)','2,000','Per verifica curva impianto reale'],
    ['H prefiltro pompa','0,750','Prefiltro a cestello standard'],
    ['H dislivello statico','0,000','Pompa e vasca praticamente alla stessa quota'],
    ['Margine di sicurezza','0,500','Incertezze di calcolo e invecchiamento raccorderia'],
    ['H accessori in linea (elettrolisi)','0,200','2 tee derivazione by-pass sul circuito principale'],
    ['H BASE (senza accessori)','9,17 mca',''],
    ['H PROGETTO (filtro met\u00e0 vita, con acc.)','9,37 mca','PREVALENZA DI PROGETTO'],
  ],[3400,2000,3672]),
  p(''),
  ...box(['H PROGETTO: 9,37 mca  (filtro a met\u00e0 vita + accessori)',
          'Curva impianto a filtro pulito: H = 4,37 mca  \u2014  usata per verifica Q max pompa']),
  p('',{after:120}),
];

// ══ 7. POMPA ════════════════════════════════════════════════════════════════
const s7=[
  h1('7. Selezione della Pompa'),
  tbl(['Parametro','Valore'],[
    ['Modello','KS EVO 100M (1HP) \u2014 TASCO'],['Alimentazione','230 V monofase IE2'],
    ['Potenza nominale','1 HP'],['Numero pompe','1'],['Fornitore','TASCO'],
  ],[3600,5472]),
  p(''),
  h2('Punti di Lavoro e Verifica'),
  tbl(['Condizione','H impianto','Q erogata','Esito'],[
    ['Filtro a met\u00e0 vita (H progetto)','9,37 mca','16,2 m\u00b3/h','\u2713  Q \u2265 12,4 m\u00b3/h richiesti'],
    ['Filtro pulito (curva impianto reale)','4,37 mca','18,6 m\u00b3/h','\u2713  18,6 \u2264 25 m\u00b3/h max filtro \u2014 ESITO POSITIVO'],
  ],[2600,1700,1900,3072]),
  p(''),
  ...box([
    '>>> Q MEDIA DI ESERCIZIO: 17,40 m\u00b3/h  \u2014  dato di riferimento principale del progetto',
    '    Media tra funzionamento a filtro pulito (18,6 m\u00b3/h) e a filtro a met\u00e0 vita (16,2 m\u00b3/h)',
    '    T ricircolo medio: 3,56 h  |  Q media per skimmer: 5,80 m\u00b3/h cad. (< 7,5 raccomandata \u2713)',
  ]),
  p('',{after:120}),
];

// ══ 8. FILTRO ═══════════════════════════════════════════════════════════════
const s8=[
  h1('8. Selezione del Filtro'),
  tbl(['Parametro','Valore'],[
    ['Modello','SwimClear Mono C150SE \u2014 TASCO'],
    ['Numero filtri','1'],
    ['Superficie filtrante','14 m\u00b2 per filtro'],
    ['Portata di dimensionamento','18,6 m\u00b3/h (Q max pompa a filtro pulito, +15% su Q progetto)'],
    ['Velocit\u00e0 di filtrazione','1,33 m\u00b3/h/m\u00b2  (18,6 / 14)'],
    ['Portata max dichiarata (costruttore)','25 m\u00b3/h'],
    ['Verifica Q max impianto \u2264 Q max filtro','18,6 m\u00b3/h \u2264 25 m\u00b3/h  \u2713  ESITO POSITIVO'],
    ['Valvola','Inclusa nel filtro'],
  ],[3600,5472]),
  p('',{after:120}),
];

// ══ 9. FILTRAZIONE A CARTUCCIA ══════════════════════════════════════════════
const s9=[
  h1('9. Vantaggi della Filtrazione a Cartuccia'),
  new Paragraph({children:[new TextRun({text:'Fonte: \u201cSistemi di Filtrazione e Disinfezione EcoFriendly \u2014 NOTA TECNICA\u201d \u2014 Acqualab srl',font:'Calibri',size:18,italics:true,color:'666666'})],spacing:{after:120}}),
  h2('Efficienza Idrica \u2014 Eliminazione del Controlavaggio'),
  p('La filtrazione a cartuccia elimina completamente il controlavaggio. Negli impianti con sabbia silicea, ogni ciclo di rigenerazione produce mediamente 3\u20135 m\u00b3 di refluo.',{after:60}),
  bullet('Nessuno scarico idrico aggiuntivo durante il ciclo di esercizio \u2014 nessun refluo da trattare'),
  bullet('Per piscine domestiche (UNI EN 16713-2:2016): unico scarico = svuotamento stagionale'),
  bullet('Conformit\u00e0 scarichi in fognatura: Tab. 3 All. 5 D.Lgs. 152/2006'),
  bullet('Riduzione del consumo idrico e dei reflui convogliati in fognatura'),
  p(''),
  h2('Qualit\u00e0 di Filtrazione'),
  tbl(['Tecnologia','Finezza di filtrazione','Torbidità tipica'],[
    ['Cartuccia (questo impianto)','20\u201330 micron','< 0,5 NTU'],
    ['Sabbia silicea','50 micron','0,5\u20131 NTU'],
  ],[3024,3024,3024]),
  p(''),
  h2('Ciclo di Vita e Variabilit\u00e0 della Perdita di Carico'),
  bullet('Pulizia manuale a bassa pressione \u2014 nessun prodotto chimico aggressivo'),
  bullet('Sostituzione rapida senza svuotare il circuito idraulico'),
  bullet('La perdita di carico aumenta progressivamente nel ciclo (2 mca a filtro pulito \u2192 7 mca a met\u00e0 vita): il progetto dimensiona pompa e impianto tenendo conto di questa variabilit\u00e0, verificando il punto di lavoro in entrambe le condizioni'),
  p('',{after:120}),
];

// ══ 10. COMPONENTI ══════════════════════════════════════════════════════════
const s10=[
  h1('10. Componenti di Circolazione'),
  tbl(['Componente','Modello','Qt.','Specifiche tecniche'],[
    ['Skimmer sfioratore','Skimmer NORM Astral (bianco) \u2014 ABS','2','Q raccomandata: 7,5 m\u00b3/h | Attacco D.63\nQ media esercizio: 5,80 m\u00b3/h/cad. (< 7,5 \u2713)'],
    ['Presa di fondo','Scarico fondo NORM Astral griglia piana (bianco) \u2014 ABS','3','Q max griglia: 15 m\u00b3/h (v \u2264 0,5 m/s, UNI EN 13451-3) | Attacco D.50'],
    ["Bocchetta mandata","Pool's Bocch. ABS sfera orient. cem/PVC \u2014 ABS",'4','Q max: 5 m\u00b3/h | Attacco D.50 | Orientabile 360\u00b0'],
  ],[1500,2900,400,4272]),
  p(''),
  bullet('Distanza tra i bordi delle prese di fondo: \u2265 1 m (piscine private \u2014 UNI EN 16582)'),
  bullet('Distanza dalle pareti verticali: \u2265 1 m'),
  p('',{after:120}),
];

// ══ 11. SICUREZZA ═══════════════════════════════════════════════════════════
const s11=[
  h1('11. Verifica di Sicurezza \u2014 Aspirazioni Sommerse'),
  h2('11.1 Verifica Anti-Intrappolamento (UNI EN 16582)'),
  p('La verifica \u00e8 eseguita alla portata MASSIMA (filtro pulito = 18,6 m\u00b3/h), condizione pi\u00f9 gravosa.',{after:80}),
  tbl(['Parametro','Valore','Limite','Esito'],[
    ['Prese di fondo installate','3','\u2265 2 (obbligatorio)','\u2713'],
    ['Configurazione','Parallelo idraulico','\u2014','\u2713'],
    ['Q pompa (filtro pulito)','18,6 m\u00b3/h','\u2014','\u2014'],
    ['Q per presa con 1 ostruita (N\u22121 = 2)','18,6 / 2 = 9,3 m\u00b3/h','\u2014','\u2014'],
    ['Q max griglia (costruttore, v \u2264 0,5 m/s)','15 m\u00b3/h','\u2014','\u2014'],
    ['Verifica: 9,3 m\u00b3/h \u2264 15 m\u00b3/h','POSITIVO','< Q max griglia','\u2713 ESITO POSITIVO'],
  ],[2800,2200,2000,2072]),
  p(''),
  ...box(['>>> Q MEDIA DI ESERCIZIO = 17,40 m\u00b3/h (DATO DI RIFERIMENTO)',
          'In condizioni normali: Q per presa = 17,40 / 3 = 5,80 m\u00b3/h cad.',
          'La verifica \u00e8 sempre eseguita a Qmax per conservativit\u00e0 (caso peggiore assoluto).']),
  p(''),
  h2('11.2 Verifica Velocit\u00e0 Tubo PF (D.75)'),
  tbl(['Scenario operativo','Q (m\u00b3/h)','v (m/s)','Esito v \u2264 1,7 m/s'],[
    ['Esercizio normale (quota fondo)','4,1','0,318','\u2713 OK'],
    ['Filtro pulito / Q max','18,6','1,431','\u2713 OK'],
    ['Skimmer ostruiti (caso peggiore)','18,6','1,431','\u2713 OK'],
    ['>>> Q MEDIA TUBO PF','11,4','0,877','\u2713 OK \u2014 DATO DI RIFERIMENTO'],
  ],[2800,1700,1700,2872]),
  p('Il tratto C (collettore asp.\u2192pompa) porta sempre la portata totale della pompa: Q = Qmax = 18,6 m\u00b3/h.',{italic:true,color:'444444',after:120}),
];

// ══ 12. ELETTROLISI ═════════════════════════════════════════════════════════
const s12=[
  h1("12. Vantaggi dell'Elettrolisi a Sale a Bassa Salinit\u00e0"),
  new Paragraph({children:[new TextRun({text:'Fonte: \u201cSistemi di Filtrazione e Disinfezione EcoFriendly \u2014 NOTA TECNICA\u201d \u2014 Acqualab srl',font:'Calibri',size:18,italics:true,color:'666666'})],spacing:{after:120}}),
  h2('Sicurezza e Semplicit\u00e0 di Stoccaggio'),
  bullet('Prodotti clorati tradizionali classificati H314 corrosivo e H400 pericoloso per l\u2019ambiente acquatico'),
  bullet('Con elettrolisi: unico approvvigionamento = sale da cucina (NaCl) \u2014 prodotto non pericoloso'),
  bullet('Nessun obbligo D.Lgs. 81/2008 n\u00e9 D.Lgs. 105/2015 (soglie Seveso) per piscine private'),
  p(''),
  h2('Tecnologia di Nuova Generazione'),
  tbl(['Parametro','Questo impianto (nuova gen.)','Vecchia generazione'],[
    ['Salinit\u00e0 acqua','1,5 kg/m\u00b3','4\u20135 kg/m\u00b3'],
    ['Produzione Cl\u2082 attivo','30 g/h (sufficiente fino a 200 m\u00b3)','\u2014'],
    ['Scarico in fognatura','Semplificato (bassa salinit\u00e0)','Soggetto a limitazioni'],
    ['Corrosione metalli','Minima','Significativa'],
  ],[3024,3024,3024]),
  p(''),
  h2('Installazione su By-Pass Dedicato'),
  p('Schema: tee derivazione \u2192 valvola sfera \u2192 curva 90\u00b0 \u2192 cella \u2192 valvola sfera \u2192 tee di ritorno',{indent:360,bold:true,color:TEAL,after:80}),
  bullet('Perdita di carico sul circuito principale: soli 2 tee di derivazione \u2248 0,20 mca \u2014 VS, curve 90\u00b0 e cella sono sul ramo by-pass e non gravano sulla prevalenza principale'),
  bullet('Regolazione automatica pH SEMPRE inclusa: sonda analitica in lettura continua + dosatore automatico acido correttivo'),
  bullet('UNI EN 16713-2:2016 (domestica): non vieta la clorazione salina; i dosatori elettromagnetici sono obbligatori solo per Tipo 2 (uso pubblico/collettivo)'),
  p('',{after:120}),
];

// ══ 13. ACCESSORI ═══════════════════════════════════════════════════════════
const s13=[
  h1('13. Accessori in Linea'),
  tbl(['Accessorio','Descrizione','\u0394H (mca)'],[
    ['Elettrolisi sale a bassa salinit\u00e0','Salinit\u00e0 1,5 kg/m\u00b3 \u2014 30 g/h Cl\u2082 \u2014 regolazione pH automatica\nCella su by-pass: tee \u2192 VS \u2192 curva 90\u00b0 \u2192 cella \u2192 VS \u2192 tee\nPerdita circuito principale: 2 tee derivazione (flusso dritto)','0,20'],
    ['TOTALE accessori in linea','','0,20'],
  ],[2000,6072,1000]),
  p('La perdita di 0,20 mca \u00e8 inclusa nella prevalenza di progetto: H = 9,37 mca = 9,17 (base) + 0,20 (accessori).',{italic:true,color:'444444',after:120}),
];

// ══ 14. DISTINTA MATERIALI ══════════════════════════════════════════════════
const s14=[
  h1('14. Distinta Materiali \u2014 Listino 2025 IVA Esclusa'),
  tbl(['Componente','Modello / Descrizione','Fornitore','Qt.','Prezzo unit.','Totale'],[
    ['Filtro cartuccia','SwimClear Mono C150SE','TASCO','1','da listino','—'],
    ['Pompa circolazione','KS EVO 100M (1HP) 230V IE2','TASCO','1','da listino','—'],
    ['Skimmer sfioratore','Skimmer NORM Astral (bianco) ABS','Astral Pool','2','da listino','—'],
    ['Presa di fondo','Scarico fondo NORM Astral griglia piana (bianco) ABS \u2014 Q max 15 m\u00b3/h','Astral Pool','3','da listino','—'],
    ["Bocchetta mandata","Pool's Bocch. ABS sfera orient. cem/PVC",'Pools','4','da listino','—'],
    ['Tubi e raccorderia PVC','Diametri vari \u2014 metratura da rilievo cantiere','\u2014','\u2014','\u2014','\u2014'],
  ],[1800,3600,1200,500,1000,972]),
  p('I prezzi unitari sono da confermare con i fornitori al momento dell\u2019ordine.',{italic:true,color:'444444',after:120}),
];

// ══ 15. PARAMETRI ACQUA ═════════════════════════════════════════════════════
const s15=[
  h1('15. Parametri Acqua e Avviamento'),
  h2('Parametri di Qualit\u00e0 (UNI EN 16713-3 \u2014 indicativi per domestiche)'),
  tbl(['Parametro','Valore target','Unit\u00e0','Frequenza controllo'],[
    ['pH','7,0 \u2013 7,4','\u2014','Giornaliera (automatica con elettrolisi)'],
    ['Cloro libero','0,6 \u2013 1,5','mg/l','Giornaliera'],
    ['Cloro combinato (max)','0 \u2013 0,5','mg/l','Settimanale'],
    ['Alcalinit\u00e0','80 \u2013 120','mg/l CaCO\u2083','Settimanale'],
    ['Durezza','150 \u2013 300','mg/l CaCO\u2083','Mensile'],
    ['Torbidità (max)','0 \u2013 1','NTU','Settimanale'],
    ['Temperatura','24 \u2013 32','\u00b0C','Continua (se riscaldata)'],
    ['Acido cianurico (max)','0 \u2013 100','mg/l','Mensile'],
  ],[2000,1600,1600,3872]),
  p(''),
  h2('Checklist Avviamento Stagionale'),
  bullet('Pulizia e ispezione vasca e locale tecnico'),
  bullet('Verifica tenuta idraulica collettori e raccorderia'),
  bullet('Riempimento vasca con acqua di rete'),
  bullet('Prima messa in moto \u2014 verifica portata e pressioni'),
  bullet('Verifica salinit\u00e0 (target 1,5 kg/m\u00b3) \u2014 integrazione con sale da cucina se necessario'),
  bullet('Primo controllo parametri chimici (pH, cloro, alcalinit\u00e0)'),
  bullet('Regolazione cella elettrolisi e impostazione dosaggio pH automatico'),
  p('',{after:120}),
];

// ══ 16. ICT ═════════════════════════════════════════════════════════════════
const s16=[
  h1('16. Indice di Conformit\u00e0 Tecnica (ICT)'),
  ...box(['ICT = 100/100  \u2014  Classe A (Eccellente)']),
  p(''),
  tbl(['Criterio di valutazione','Peso','Score','Note tecniche'],[
    ['Sicurezza aspirazioni (UNI EN 16582)','30%','30/30','3 prese \u2265 2 \u2713 | Q/(N-1) = 9,3 \u2264 15 m\u00b3/h \u2713'],
    ['Idraulica tubazioni','25%','25/25','Tutte le velocit\u00e0 e perdite di carico nei limiti \u2713'],
    ['Filtrazione','25%','25/25','T = 3,8 h \u2264 5h \u2713 | Q pompa 18,6 \u2264 25 m\u00b3/h \u2713'],
    ['Componenti','20%','20/20','Q/bocchetta = 18,6/4 = 4,65 \u2264 5 m\u00b3/h \u2713 | Q/skimmer = 5,80 < 7,5 m\u00b3/h \u2713'],
    ['TOTALE','100%','100/100','Classe A \u2014 Eccellente'],
  ],[2800,900,900,4472]),
  p(''),
  tbl(['Classe','Punteggio','Significato'],[
    ['A','\u2265 90','Eccellente \u2014 impianto ottimizzato su tutti i criteri'],
    ['B  (questo progetto)','75 \u2013 89','Buono \u2014 impianto conforme e ben dimensionato'],
    ['C','60 \u2013 74','Accettabile \u2014 conforme con margini di miglioramento'],
    ['D','40 \u2013 59','Insufficiente \u2014 non conforme su alcuni criteri'],
    ['E','< 40','Non conforme \u2014 intervento necessario prima dell\u2019uso'],
  ],[1200,1800,6072]),
  p('',{after:120}),
];

// ══ 17. SCELTE PROGETTUALI ══════════════════════════════════════════════════
const s17=[
  h1('17. Scelte Progettuali \u2014 Override rispetto al Calcolo Automatico'),
  tbl(['Parametro','Calcolo automatico','Scelta progettuale','Motivazione'],[
    ['Collettore mandata','D.125 (4 uscite D.50 flex, criterio 1,5\u00d7 sezioni uscenti)','D.110 override','Scelta progettuale deliberata \u2014 velocit\u00e0 e perdite di carico comunque nei limiti normativi'],
  ],[1800,2500,1800,3072]),
  p('Tutti gli altri parametri (collettore aspirazione, tratti locali tecnici, numero componenti, diametri rami) sono calcolati automaticamente.',{italic:true,color:'444444',after:120}),
];

// ══ 18. CONCLUSIONI ═════════════════════════════════════════════════════════
const s18=[
  h1('18. Conclusioni'),
  tbl(['Parametro','Valore','Conformit\u00e0'],[
    ['Q progetto','12,4 m\u00b3/h (T = 5h)','\u2713 UNI EN 16713-2'],
    ['Q effettiva a filtro a met\u00e0 vita','16,2 m\u00b3/h (T = 3,8h)','\u2713'],
    ['Q media di esercizio','17,40 m\u00b3/h (T medio 3,56h)','\u2713 Dato di riferimento'],
    ['Prevalenza di progetto','9,37 mca','\u2713 KS EVO 100M adeguata'],
    ['Sicurezza aspirazioni','Q/presa = 9,3 m\u00b3/h \u2264 15 m\u00b3/h','\u2713 UNI EN 16582'],
    ['ICT','100/100 \u2014 Classe A','\u2713 Eccellente'],
  ],[3000,3000,3072]),
  p(''),
  new Paragraph({children:[new TextRun({text:'\u201cTi mostrano l\u2019estetica. Nessuno ti spiega ci\u00f2 che la sostiene.',font:'Calibri',size:22,italics:true,color:TEAL})],spacing:{before:240,after:0},indent:{left:360}}),
  new Paragraph({children:[new TextRun({text:'Noi partiamo da l\u00ec: dal metodo, dalle scelte invisibili e dal lavoro che non si improvvisa.',font:'Calibri',size:22,italics:true,color:TEAL})],spacing:{after:0},indent:{left:360}}),
  new Paragraph({children:[new TextRun({text:'\u00c8 questo che fa la differenza tra una piscina bella oggi e una piscina affidabile domani.\u201d',font:'Calibri',size:22,italics:true,bold:true,color:TEAL})],spacing:{after:240},indent:{left:360}}),
  p(''),
  new Paragraph({children:[new TextRun({text:'ACQUALAB srl \u2014 Viale Aldo Moro 2, 50023 Impruneta (FI) \u2014 www.acqua-lab.it \u2014 info@acqua-lab.it',font:'Calibri',size:18,color:'555555'})],alignment:AlignmentType.CENTER}),
];

// ══ ASSEMBLAGGIO ════════════════════════════════════════════════════════════
const all=[...cover,...s1,sep(),...s2,sep(),...s3,sep(),...s4,sep(),...s5,sep(),...s6,sep(),
  ...s7,sep(),...s8,sep(),...s9,sep(),...s10,sep(),...s11,sep(),...s12,sep(),
  ...s13,sep(),...s14,sep(),...s15,sep(),...s16,sep(),...s17,sep(),...s18];

const doc=new Document({
  numbering:{config:[{reference:'bullets',levels:[{level:0,format:LevelFormat.BULLET,text:'\u2022',
    alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:360}}}}]}]},
  sections:[{
    properties:{page:{size:{width:11906,height:16838},margin:{top:1417,right:1417,bottom:1417,left:1417}}},
    children:all
  }]
});

Packer.toBuffer(doc).then(buf=>{
  fs.writeFileSync('/home/claude/rt_marco_b.docx',buf);
  console.log('OK');
}).catch(e=>{console.error(e);process.exit(1);});
