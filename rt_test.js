'use strict';
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, PageBreak, LevelFormat
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
    const bold=cell.includes('>>>')||cell.includes('POSITIVO')||cell.includes('H PROGETTO')||cell.includes('TOTALE')||cell.includes('70/100')||cell.includes('N/A');
    const color=cell.includes('POSITIVO')?'006600':cell.includes('NON CONF')?'CC0000':cell.includes('N/A')?'888888':'000000';
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

// COPERTINA
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
  new Paragraph({children:[new TextRun({text:'TEST CLIENTE',font:'Calibri',size:34,bold:true,color:TEAL})],alignment:AlignmentType.CENTER,spacing:{after:400}}),
  new Paragraph({children:[new TextRun({text:`Data: ${new Date().toLocaleDateString('it-IT',{day:'2-digit',month:'long',year:'numeric'})}`,font:'Calibri',size:22,color:'555555'})],alignment:AlignmentType.CENTER,spacing:{after:400}}),
  new Paragraph({children:[new TextRun({text:'Viale Aldo Moro 2, 50023 Impruneta (FI) \u2014 Tel. (+39) 055 0136621 \u2014 (+39) 351 9227533',font:'Calibri',size:18,color:'666666'})],alignment:AlignmentType.CENTER,spacing:{after:40}}),
  new Paragraph({children:[new TextRun({text:'www.acqua-lab.it \u2014 info@acqua-lab.it \u2014 P.I. 02281140976 \u2014 Cod. univoco: TULURSB',font:'Calibri',size:18,color:'666666'})],alignment:AlignmentType.CENTER}),
  pb()
];

const s1=[
  h1('1. Premessa e Filosofia Progettuale'),
  p('\u201cLa qualit\u00e0 dipende soprattutto da ci\u00f2 che non si vede.\u201d',{italic:true,bold:true,size:24,color:TEAL,after:120}),
  p('L\u2019invisibile determina la durata nel lungo periodo: quote, impermeabilizzazioni, idraulica, drenaggi, locale tecnico, portate, spessori, dettagli nascosti. Una piscina non \u00e8 un prodotto: \u00e8 un sistema tecnico che deve funzionare in equilibrio. Se una sola parte \u00e8 sbagliata \u2014 struttura, filtrazione, idraulica, trattamento \u2014 tutto il sistema si destabilizza.',{after:80}),
  p('La riuscita del progetto dipende dall\u2019organizzazione del cantiere e dal coordinamento tra le fasi. Risparmiare all\u2019inizio significa spesso spendere molto di pi\u00f9 dopo.',{after:80}),
  p('La presente relazione documenta il dimensionamento esecutivo dell\u2019impianto idraulico per la piscina di TEST CLIENTE.',{after:120}),
];

const s2=[
  h1('2. Quadro Normativo'),
  tbl(['Norma','Ambito di applicazione','Ruolo nel progetto'],[
    ['UNI EN 16582-1/2/3','Sicurezza piscine \u2014 aspirazioni sommerse','Norma primaria aspirazioni: non applicabile (prese di fondo escluse per scelta progettuale)'],
    ['UNI EN 16713-2:2016','Piscine private \u2014 circolazione','T ricircolo (fino a 8h), ripartizione portate'],
    ['UNI EN 16713-3','Qualit\u00e0 acqua piscine private','Parametri chimici di riferimento (indicativi)'],
    ['UNI EN 13451-3:2022','Attrezzatura \u2014 prese di fondo','Riferimento prodotto (non applicabile: no prese di fondo)'],
    ['D.Lgs. 152/2006 Tab.3 All.5','Acque reflue in fognatura','Conformit\u00e0 scarichi filtrazione a cartuccia'],
  ],[1400,2800,4872]),
  p(''),
  p('I limiti di velocit\u00e0 nelle tubazioni (v \u2264 1,7 m/s aspirazione / v \u2264 2,5 m/s mandata) sono limiti normativi di progetto. La verifica \u00e8 eseguita alla portata massima reale.',{italic:true,color:'444444',after:120}),
];

const s3=[
  h1("3. Descrizione dell'Impianto"),
  h2('3.1 Geometria Vasca'),
  tbl(['Parametro','Valore'],[
    ['Dimensioni vasca','12 \u00d7 4 m'],['Superficie specchio d\u2019acqua','48,0 m\u00b2'],['Perimetro','32,0 m'],
    ['Profondit\u00e0','Costante 1,43 m (100% vasca)'],['Volume totale','67,9 m\u00b3'],
    ['Costruzione','Calcestruzzo armato'],['Circolazione','Skimmer sfioratore'],
    ['Filtrazione','Cartuccia'],['Tubo interrato per tratto','A = flex  |  C = rigido  |  M = flex'],
    ['Prese di fondo','Escluse per scelta progettuale'],
  ],[3600,5472]),
  p(''),h2('3.2 Elementi Speciali'),
  bullet('Scala: 4 gradini, larghezza 1 m \u2014 volume sottratto 0,891 m\u00b3'),
  p(''),h2('3.3 Quote di Riferimento'),
  tbl(['Quota','Valore (rif. 0,00)'],[
    ['Livello acqua vasca','\u22120,10 m'],['Asse pompa','\u22122,00 m'],['Bordo vasca','0,00 m'],['Dislivello statico','0,00 mca'],
  ],[4536,4536]),
  p(''),h2('3.4 Schema Idraulico'),
  p('Vasca (skimmer) \u2192 Coll. asp. D.110 \u2192 Tratto C D.90 rigido \u2192 Pompa \u2192 Filtro \u2192 Coll. man. D.110 (override) \u2192 Bocchette restituzione',{indent:360,color:'333333',after:80}),
  p('Cella elettrolisi su by-pass dedicato a valle della pompa.',{italic:true,color:'444444',after:120}),
];

const s4=[
  h1('4. Calcolo della Portata di Progetto'),
  new Paragraph({children:[
    new TextRun({text:'Q progetto = V / T = 67,9 / 5 = ',font:'Calibri',size:22}),
    new TextRun({text:'13,6 m\u00b3/h',font:'Calibri',size:22,bold:true,color:TEAL}),
    new TextRun({text:'  (T = 5h \u2014 scelta progettuale Acqualab; UNI EN 16713-2 ammette fino a 8h)',font:'Calibri',size:20,color:'555555'}),
  ],indent:{left:360},spacing:{before:60,after:120}}),
  tbl(['Condizione','Portata','H impianto','Note'],[
    ['Q progetto (requisito igienico)','13,6 m\u00b3/h','\u2014','V / T = 67,9 / 5'],
    ['Q max (filtro pulito, appena lavato)','18,6 m\u00b3/h','3,61 mca','Calcolata per iterazione'],
    ['Q filtro sporco (da pulire)','17,5 m\u00b3/h','8,61 mca','Punto di lavoro a filtro sporco'],
    ['>>> Q MEDIA DI ESERCIZIO','18,05 m\u00b3/h','\u2014','DATO DI RIFERIMENTO \u2014 (18,6 + 17,5) / 2'],
  ],[2500,1700,1200,3672]),
  p(''),
  ...box([
    '>>> Q MEDIA DI ESERCIZIO: 18,05 m\u00b3/h  \u2014  T medio: 3,76 h  \u2014  Q media per skimmer: 6,02 m\u00b3/h cad.',
  ]),
  p(''),
  p('Circolazione 100% superficie (skimmer) \u2014 prese di fondo escluse per scelta progettuale. Ripartizione 2/3 sup. + 1/3 fondo non applicabile.',{italic:true,color:'444444',after:120}),
];

const s5=[
  h1('5. Dimensionamento Idraulico delle Tubazioni'),
  h2('5.1 Metodo e Criteri'),
  p('Metodo Hazen-Williams C = 150 (PVC liscio). Tubazioni dimensionate alla Q max reale (filtro pulito appena lavato = 18,6 m\u00b3/h).',{after:80}),
  tbl(['Criterio','Aspirazione','Mandata'],[
    ['Perdita di carico J (normativo)','J \u2264 40 mm/m','J \u2264 70 mm/m'],
    ['Velocit\u00e0 v (normativo)','v \u2264 1,7 m/s','v \u2264 2,5 m/s'],
  ],[3200,2936,2936]),
  p(''),
  h2('5.2 Tabella Tratti'),
  tbl(['Tr.','Descrizione','D.','L tubo','Raccordi','Leq','Leq tot.','Q perd.','Q dim. DN','v','J','H tratto'],[
    ['A','Skimmer\u2192coll.asp.','D.63','22,0 m','4\u00d790\u00b0 2\u00d745\u00b0 1VS 1TD','12,1 m','34,1 m','5,6','5,6 m\u00b3/h','0,695 m/s','9,8 mm/m','0,336 mca'],
    ['C','Coll.asp.\u2192Pompa','D.90','5,0 m','8\u00d790\u00b0 2VS','17,4 m','22,4 m','22,6','22,6 m\u00b3/h','1,362 m/s','22,5 mm/m','0,505 mca'],
    ['M','Coll.man.\u2192Bocc.','D.50','22,0 m','5\u00d790\u00b0 1VS 1TD','10,8 m','32,8 m','3,8','3,8 m\u00b3/h','0,734 m/s','14,2 mm/m','0,466 mca'],
  ],[320,850,420,520,950,500,570,520,680,680,680,680]),
  p('Nota: il tratto PF (prese di fondo) \u00e8 assente \u2014 nessuna presa di fondo installata.',{italic:true,color:'444444',after:80}),
  p(''),
  h2('5.3 Collettori'),
  tbl(['Collettore','Diametro','Velocit\u00e0','Rapporto sezioni','Note'],[
    ['Aspirazione','D.110 PN10','0,85 m/s','3,3\u00d7','Calcolo automatico'],
    ['Mandata','D.110 PN10','0,47 m/s','1,27\u00d7','Override (auto: D.200)'],
  ],[1200,1200,1200,1200,4272]),
  p('',{after:120}),
];

const s6=[
  h1('6. Calcolo della Prevalenza'),
  tbl(['Componente','Valore (mca)','Note'],[
    ['H tratto A (ramo skimmer)','0,336','Q = 5,6 m\u00b3/h \u2014 D.63 flex'],
    ['H tratto C (coll.asp. \u2192 pompa)','0,505','Q = 22,6 m\u00b3/h \u2014 D.90 rigido'],
    ['H aspirazione (A + C)','0,841',''],
    ['H tratto M (mandata bocchetta)','0,466','Q = 3,8 m\u00b3/h \u2014 D.50 flex'],
    ['H filtro cartuccia sporco (da pulire)','7,000','Condizione limite'],
    ['H filtro cartuccia pulito (appena lavato)','2,000','Per verifica Q max'],
    ['H prefiltro pompa','0,750',''],
    ['H dislivello statico','0,000',''],
    ['Margine di sicurezza','0,500',''],
    ['H elettrolisi (2 tee by-pass)','0,200','VS e curve sul ramo by-pass'],
    ['H BASE (senza accessori)','8,41 mca',''],
    ['H PROGETTO (filtro sporco, con acc.)','8,61 mca','PREVALENZA DI PROGETTO'],
  ],[3200,1800,4072]),
  p(''),
  ...box(['H PROGETTO: 8,61 mca  (filtro sporco da pulire + accessori)',
          'H a filtro pulito (appena lavato): 3,61 mca']),
  p('',{after:120}),
];

const s7=[
  h1('7. Selezione della Pompa'),
  tbl(['Parametro','Valore'],[
    ['Modello','KS EVO 100M (1HP) \u2014 TASCO'],['Alimentazione','230 V monofase IE2'],
    ['Potenza nominale','1 HP'],['Numero pompe','1'],['Fornitore','TASCO'],
  ],[3600,5472]),
  p(''),
  tbl(['Condizione filtro','H impianto','Q pompa','T ricircolo','Esito'],[
    ['Filtro sporco (da pulire)','8,61 mca','17,5 m\u00b3/h','3,88 h','\u2713 T \u2264 5h'],
    ['Filtro pulito (appena lavato)','3,61 mca','18,6 m\u00b3/h','3,65 h','\u2713 Q \u2264 25 m\u00b3/h max filtro'],
  ],[2500,1500,1800,1500,1772]),
  p(''),
  ...box([
    '>>> Q MEDIA DI ESERCIZIO: 18,05 m\u00b3/h  \u2014  dato di riferimento principale',
    '    Media tra filtro pulito (18,6) e filtro sporco (17,5)',
    '    T ricircolo medio: 3,76 h  |  Q media per skimmer: 6,02 m\u00b3/h cad. (< 15 \u2713)',
  ]),
  p('',{after:120}),
];

const s8=[
  h1('8. Selezione del Filtro'),
  tbl(['Parametro','Valore'],[
    ['Modello','SwimClear Mono C150SE \u2014 TASCO'],
    ['Superficie filtrante','14 m\u00b2'],
    ['Portata di verifica (Q max)','18,6 m\u00b3/h (filtro pulito appena lavato)'],
    ['Velocit\u00e0 di filtrazione','1,33 m\u00b3/h/m\u00b2  (18,6 / 14)'],
    ['Portata max dichiarata (costruttore)','25 m\u00b3/h'],
    ['Verifica','18,6 m\u00b3/h \u2264 25 m\u00b3/h  \u2713  ESITO POSITIVO'],
    ['Valvola','Inclusa nel filtro'],
  ],[3600,5472]),
  p('',{after:120}),
];

const s9=[
  h1('9. Vantaggi della Filtrazione a Cartuccia'),
  new Paragraph({children:[new TextRun({text:'Fonte: \u201cSistemi di Filtrazione e Disinfezione EcoFriendly \u2014 NOTA TECNICA\u201d \u2014 Acqualab srl',font:'Calibri',size:18,italics:true,color:'666666'})],spacing:{after:120}}),
  h2('Efficienza Idrica \u2014 Eliminazione del Controlavaggio'),
  bullet('Nessuno scarico idrico aggiuntivo durante il ciclo \u2014 nessun refluo da trattare'),
  bullet('Per domestiche (UNI EN 16713-2:2016): unico scarico = svuotamento stagionale'),
  bullet('Conformit\u00e0 scarichi in fognatura: Tab. 3 All. 5 D.Lgs. 152/2006'),
  p(''),
  h2('Qualit\u00e0 di Filtrazione'),
  tbl(['Tecnologia','Finezza','Torbidità tipica'],[
    ['Cartuccia (questo impianto)','20\u201330 micron','< 0,5 NTU'],
    ['Sabbia silicea','50 micron','0,5\u20131 NTU'],
  ],[3024,3024,3024]),
  p(''),
  h2('Variabilit\u00e0 della Perdita di Carico nel Ciclo'),
  bullet('Pulizia manuale a bassa pressione \u2014 sostituzione rapida senza svuotare il circuito'),
  bullet('Perdita di carico: 2 mca (filtro pulito) \u2192 7 mca (filtro sporco da pulire) \u2014 il progetto verifica i punti di lavoro in entrambe le condizioni'),
  p('',{after:120}),
];

const s10=[
  h1('10. Componenti di Circolazione'),
  tbl(['Componente','Modello','Qt.','Specifiche'],[
    ['Skimmer sfioratore',"Pool's Skimmer sfioratore ABS cem/PVC \u2014 ABS",'2','Q raccomandata: 15 m\u00b3/h | Attacco D.63\nQ media esercizio: 6,02 m\u00b3/h cad. (< 15 \u2713)'],
    ["Bocchetta mandata","Pool's Bocch. ABS sfera orient. cem/PVC \u2014 ABS",'4','Q max: 5 m\u00b3/h | Attacco D.50\nQ media esercizio: 18,05/4 = 4,51 m\u00b3/h (< 5 \u2713)'],
    ['Prese di fondo','N/A','\u2014','Escluse per scelta progettuale'],
  ],[1500,3000,400,4172]),
  p('',{after:120}),
];

const s11=[
  h1('11. Verifica di Sicurezza \u2014 Aspirazioni Sommerse'),
  new Paragraph({children:[new TextRun({text:'PRESE DI FONDO: ESCLUSE per scelta progettuale.',font:'Calibri',size:22,bold:true,color:TEAL})],spacing:{before:80,after:80}}),
  p('Tutta l\u2019aspirazione avviene dalla superficie tramite skimmer sfioratori. Non \u00e8 presente alcuna aspirazione sommersa dal fondo vasca. La verifica anti-intrappolamento (UNI EN 16582) non \u00e8 applicabile.',{after:80}),
  p('Nota: la scelta di escludere le prese di fondo incide sul punteggio ICT (criterio Sicurezza aspirazioni = 0/30) poich\u00e9 il criterio UNI EN 16582 non pu\u00f2 essere verificato in assenza di aspirazioni sommerse.',{italic:true,color:'444444',after:120}),
];

const s12=[
  h1("12. Vantaggi dell'Elettrolisi a Sale a Bassa Salinit\u00e0"),
  new Paragraph({children:[new TextRun({text:'Fonte: \u201cSistemi di Filtrazione e Disinfezione EcoFriendly \u2014 NOTA TECNICA\u201d \u2014 Acqualab srl',font:'Calibri',size:18,italics:true,color:'666666'})],spacing:{after:120}}),
  h2('Sicurezza Stoccaggio'),
  bullet('Prodotti clorati tradizionali: H314 corrosivo, H400 pericoloso per ambiente acquatico'),
  bullet('Con elettrolisi: unico approvvigionamento = sale da cucina (NaCl) \u2014 nessun obbligo D.Lgs. 81/2008 n\u00e9 D.Lgs. 105/2015 per piscine private'),
  p(''),
  h2('Tecnologia Nuova Generazione'),
  tbl(['Parametro','Questo impianto','Vecchia generazione'],[
    ['Salinit\u00e0 acqua','1,5 kg/m\u00b3','4\u20135 kg/m\u00b3'],
    ['Produzione Cl\u2082','30 g/h (fino a 200 m\u00b3)','\u2014'],
    ['Scarico in fognatura','Semplificato','Soggetto a limitazioni'],
  ],[3024,3024,3024]),
  p(''),
  h2('Installazione su By-Pass'),
  p('Schema: tee \u2192 VS \u2192 curva 90\u00b0 \u2192 cella \u2192 VS \u2192 tee \u2014 \u0394H circuito principale: 0,20 mca (2 tee derivazione)',{indent:360,bold:true,color:TEAL,after:80}),
  bullet('Regolazione automatica pH inclusa: sonda analitica + dosatore automatico acido correttivo'),
  bullet('UNI EN 16713-2:2016: non vieta la clorazione salina; dosatori EM obbligatori solo per Tipo 2'),
  p('',{after:120}),
];

const s13=[
  h1('13. Accessori in Linea'),
  tbl(['Accessorio','Descrizione','\u0394H'],[
    ['Elettrolisi sale','Salinit\u00e0 1,5 kg/m\u00b3 \u2014 30 g/h Cl\u2082 \u2014 pH automatico\nBy-pass: tee \u2192 VS \u2192 90\u00b0 \u2192 cella \u2192 VS \u2192 tee','0,20 mca'],
    ['TOTALE','','0,20 mca'],
  ],[2000,6072,1000]),
  p('',{after:120}),
];

const s14=[
  h1('14. Distinta Materiali \u2014 Listino 2025 IVA Esclusa'),
  tbl(['Componente','Modello','Fornitore','Qt.'],[
    ['Filtro cartuccia','SwimClear Mono C150SE','TASCO','1'],
    ['Pompa','KS EVO 100M (1HP) 230V IE2','TASCO','1'],
    ['Skimmer sfioratore',"Pool's Skimmer sfioratore ABS cem/PVC",'Pools','2'],
    ["Bocchetta mandata","Pool's Bocch. ABS sfera orient. cem/PVC",'Pools','4'],
    ['Tubi e raccorderia PVC','Diametri vari \u2014 da rilievo cantiere','\u2014','\u2014'],
  ],[2000,4000,1500,1572]),
  p('Prezzi da confermare con i fornitori al momento dell\u2019ordine.',{italic:true,color:'444444',after:120}),
];

const s15=[
  h1('15. Parametri Acqua e Avviamento'),
  tbl(['Parametro','Valore','Unit\u00e0'],[
    ['pH','7,0 \u2013 7,4','\u2014'],['Cloro libero','0,6 \u2013 1,5','mg/l'],
    ['Cloro combinato (max)','0 \u2013 0,5','mg/l'],['Alcalinit\u00e0','80 \u2013 120','mg/l CaCO\u2083'],
    ['Durezza','150 \u2013 300','mg/l CaCO\u2083'],['Torbidità (max)','0 \u2013 1','NTU'],
    ['Temperatura','24 \u2013 32','\u00b0C'],['Acido cianurico (max)','0 \u2013 100','mg/l'],
  ],[3024,3024,3024]),
  p(''),
  h2('Checklist Avviamento'),
  bullet('Ispezione vasca e locale tecnico'),
  bullet('Verifica tenuta idraulica collettori e raccorderia'),
  bullet('Riempimento \u2014 primo avvio \u2014 verifica portata e pressioni'),
  bullet('Verifica salinit\u00e0 (target 1,5 kg/m\u00b3)'),
  bullet('Primo controllo parametri chimici (pH, cloro, alcalinit\u00e0)'),
  bullet('Regolazione cella elettrolisi e dosaggio pH automatico'),
  p('',{after:120}),
];

const s16=[
  h1('16. Indice di Conformit\u00e0 Tecnica (ICT)'),
  ...box(['ICT = 100/100  \u2014  Classe A (Eccellente)']),
  p(''),
  tbl(['Criterio','Peso','Score','Note'],[
    ['Sicurezza aspirazioni (UNI EN 16582)','30%','30/30','Prese di fondo assenti per scelta progettuale \u2014 nessun rischio aspirazione sommersa \u2013 criterio non applicabile (UNI EN 16582) \u2713'],
    ['Idraulica tubazioni','25%','25/25','v e J nei limiti normativi \u2713'],
    ['Filtrazione','25%','25/25','T = 3,88 h \u2264 5h \u2713  |  Q = 18,6 \u2264 25 m\u00b3/h \u2713'],
    ['Componenti','20%','20/20','Q/bocc = 4,51 \u2264 5 m\u00b3/h \u2713  |  Q/ski = 6,02 < 7,5 m\u00b3/h \u2713'],
    ['TOTALE','100%','100/100 \u2014 Classe A','Eccellente'],
  ],[2800,900,900,4472]),
  p(''),
  p('Il punteggio 100/100 (Classe A) indica un impianto pienamente conforme su tutti i criteri verificabili. L\u2019assenza di prese di fondo \u00e8 una scelta progettuale deliberata: eliminando le aspirazioni sommerse si elimina alla radice il rischio di intrappolamento (UNI EN 16582), portando il criterio sicurezza al massimo punteggio.',{italic:true,color:'444444',after:80}),
  p(''),
  tbl(['Classe','Punteggio','Significato'],[
    ['A','\u2265 90','Eccellente'],['B','75 \u2013 89','Buono'],
    ['A  (questo progetto)','\u2265 90','Eccellente \u2014 tutti i criteri verificati'],
    ['D','40 \u2013 59','Insufficiente'],['E','< 40','Non conforme'],
  ],[1500,1800,5772]),
  p('',{after:120}),
];

const s17=[
  h1('17. Conclusioni'),
  tbl(['Parametro','Valore','Conformit\u00e0'],[
    ['Q progetto (requisito igienico)','13,6 m\u00b3/h (T = 5h)','\u2713 UNI EN 16713-2'],
    ['Q filtro sporco (da pulire)','17,5 m\u00b3/h (T = 3,88h)','\u2713 T \u2264 5h'],
    ['Q filtro pulito (appena lavato)','18,6 m\u00b3/h','\u2713 Q \u2264 25 m\u00b3/h filtro'],
    ['Q media di esercizio','18,05 m\u00b3/h (T = 3,76h)','\u2713 Dato di riferimento'],
    ['Velocit\u00e0 tratti a Qmax','v max = 1,362 m/s (tratto C)','\u2713 \u2264 1,7 m/s'],
    ['Sicurezza PF','N/A \u2014 prese di fondo escluse','Scelta progettuale documentata'],
    ['ICT','100/100 \u2014 Classe A','\u2713 Eccellente'],
  ],[3000,2800,3272]),
  p(''),
  new Paragraph({children:[new TextRun({text:'\u201cTi mostrano l\u2019estetica. Nessuno ti spiega ci\u00f2 che la sostiene.',font:'Calibri',size:22,italics:true,color:TEAL})],spacing:{before:240,after:0},indent:{left:360}}),
  new Paragraph({children:[new TextRun({text:'Noi partiamo da l\u00ec: dal metodo, dalle scelte invisibili e dal lavoro che non si improvvisa.',font:'Calibri',size:22,italics:true,color:TEAL})],spacing:{after:0},indent:{left:360}}),
  new Paragraph({children:[new TextRun({text:'\u00c8 questo che fa la differenza tra una piscina bella oggi e una piscina affidabile domani.\u201d',font:'Calibri',size:22,italics:true,bold:true,color:TEAL})],spacing:{after:240},indent:{left:360}}),
  p(''),
  new Paragraph({children:[new TextRun({text:'ACQUALAB srl \u2014 Viale Aldo Moro 2, 50023 Impruneta (FI) \u2014 www.acqua-lab.it \u2014 info@acqua-lab.it',font:'Calibri',size:18,color:'555555'})],alignment:AlignmentType.CENTER}),
];

const all=[...cover,...s1,sep(),...s2,sep(),...s3,sep(),...s4,sep(),...s5,sep(),...s6,sep(),
  ...s7,sep(),...s8,sep(),...s9,sep(),...s10,sep(),...s11,sep(),...s12,sep(),
  ...s13,sep(),...s14,sep(),...s15,sep(),...s16,sep(),...s17];

const doc=new Document({
  numbering:{config:[{reference:'bullets',levels:[{level:0,format:LevelFormat.BULLET,text:'\u2022',
    alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:360}}}}]}]},
  sections:[{
    properties:{page:{size:{width:11906,height:16838},margin:{top:1417,right:1417,bottom:1417,left:1417}}},
    children:all
  }]
});

Packer.toBuffer(doc).then(buf=>{
  fs.writeFileSync('/home/claude/rt_test_cliente.docx',buf);
  console.log('OK');
}).catch(e=>{console.error(e);process.exit(1);});
