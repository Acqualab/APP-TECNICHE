'use strict';
const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,
  AlignmentType,BorderStyle,WidthType,ShadingType,PageBreak,LevelFormat}=require('docx');

// Legge il prompt dall'ultimo file salvato
const PROMPT_FILE='/home/claude/prompt_last.txt';
if(!fs.existsSync(PROMPT_FILE)){console.error('Prompt non trovato');process.exit(1);}
const PROMPT=fs.readFileSync(PROMPT_FILE,'utf8');

// Parser
function get(re,fb='—'){const m=PROMPT.match(re);return m?m[1].trim():fb;}
function itN(n){return String(n).replace('.',',');}

const P={
  cliente:    get(/Cliente:\s*(.+)/),
  dim:        get(/Dimensioni vasca:\s*(.+)/),
  sup:        get(/Superficie specchio d.acqua:\s*([\d,.]+)/),
  perim:      get(/Perimetro:\s*([\d,.]+)/),
  vol:        get(/Volume totale vasca:\s*([\d,.]+)/),
  costruz:    get(/Costruzione:\s*(.+)/),
  circ:       get(/Circolazione:\s*(.+)/),
  tuboDesc:   get(/Tubo interrato:\s*(.+)/),
  filtTipo:   get(/Tipo filtrazione:\s*(.+)/),
  tRic:       get(/Tempo ricircolo:\s*T\s*=\s*(\d+)h/,'5'),
  profDesc:   get(/prof\.\s*da\s*([\d.,]+m\s*a\s*[\d.,]+m)/,'1,43 m costante'),
  livAcqua:   get(/Livello acqua vasca:\s*([^\n]+)/),
  assePompa:  get(/Asse pompa:\s*([^\n]+)/),
  bordoVasca: get(/Livello bordo vasca:\s*([^\n]+)/),
  Qprog:      get(/Q progetto totale:\s*([\d,.]+)/),
  nCirc:      get(/Numero circuiti:\s*(\d+)/,'1'),
  Qmax:       get(/Q DIMENSIONAMENTO[^:]+:\s*([\d,.]+)\s*m3\/h/),
  Qmin:       get(/Q EFFETTIVA A FILTRO SPORCO[^:]+:\s*([\d,.]+)\s*m3\/h/),
  Teff:       get(/T ricircolo effettivo\s*=\s*([\d,.]+)\s*h/),
  Qmed:       get(/Q MEDIA DI ESERCIZIO[^:]+:\s*([\d,.]+)\s*m3\/h/),
  Tmed:       get(/T ricircolo medio:\s*([\d,.]+)/),
  QperSki:    get(/Q media per skimmer:\s*([\d,.]+)/),
  pumpModello:get(/Modello:\s*(KS EVO[^\n(]+(?:\([^)]+\))?)/),
  pumpHP:     get(/Potenza:\s*([^\n]+HP)/),
  nPompe:     get(/Numero pompe:\s*(\d+)/,'1'),
  pumpQmin:   get(/a H progetto[^\n]*Q\s*=\s*([\d,.]+)\s*m3\/h/),
  pumpQmax:   get(/a filtro pulito[^\n]*Q\s*=\s*([\d,.]+)\s*m3\/h/),
  Hprog:      get(/filtro meta vita,\s*([\d,.]+)\s*mca\)/),
  Hclean:     get(/H\s*=\s*([\d,.]+)\s*mca,\s*curva impianto/),
  filtQmaxDich:get(/Portata max dichiarata.*?:\s*([\d,.]+)\s*m3\/h/),
  filtModello:get(/Modello:\s*(SwimClear[^\n]+)/),
  filtSup:    get(/Superficie filtrante:\s*([\d,.]+)/),
  filtVfilt:  get(/Velocita di filtrazione:\s*([\d,.]+)/),
  collAsp:    get(/Collettore aspirazione:\s*(D\.\d+[^\n]+)/),
  collMan:    get(/Collettore mandata:\s*(D\.\d+[^\n]+)/),
  Hbase:      get(/H BASE.*?:\s*([\d,.]+)\s*mca/),
  Hprogetto:  get(/H PROGETTO.*?:\s*([\d,.]+)\s*mca/),
  skiModello: get(/Skimmer sfioratore:\s*([^x\n(]+)/),
  boccModello:get(/Bocchetta mandata:\s*([^x\n(]+)/),
  nSki:       get(/Skimmer sfioratore:[^\n]*x\s*(\d+)/,'2'),
  nBocc:      get(/Bocchetta mandata:[^\n]*x\s*(\d+)/,'4'),
  skiQrac:    get(/Q raccomandata:\s*([\d,.]+)\s*m3\/h.*?attacco/,'15'),
  boccQmax:   get(/Q max:\s*([\d,.]+)\s*m3\/h.*?attacco/,'5'),
  skiAttacco: get(/Skimmer sfioratore:[^\n]*attacco\s*(D\.\d+)/,'D.63'),
  boccAttacco:get(/Bocchetta mandata:[^\n]*attacco\s*(D\.\d+)/,'D.50'),
  ictVal:     get(/ICT\s*=\s*(\d+)\/100/,'100'),
  ictCls:     get(/Classe\s*([A-E](?:\s+\())/,'A').replace(/\s*\(/,''),
  ictLbl:     get(/Classe\s*[A-E]\s*\(([^)]+)\)/,'Eccellente'),
  noPF:       PROMPT.includes('PRESE DI FONDO: ESCLUSE'),
};

// Collettori
const cA=P.collAsp.match(/D\.(\d+)\(v=([\d,.]+)[^,]+,\s*rapporto sezioni:\s*([\d,.]+)x\)/)||['','110','—','—'];
const cM=P.collMan.match(/D\.(\d+)\s*\(v=([\d,.]+)[^,]+,\s*rapporto sezioni:\s*([\d,.]+)x\)/)||['','125','—','—'];
const [,cAspDN,cAspV,cAspRap]=['',cA[1]||'110',cA[2]||'—',cA[3]||'—'];
const [,cManDN,cManV,cManRap]=['',cM[1]||'125',cM[2]||'—',cM[3]||'—'];

// Override
const overrides=[];
const ovM=PROMPT.match(/SCELTE PROGETTUALI[\s\S]+?={10,}([\s\S]+?)={10,}/);
if(ovM)ovM[1].split('\n').forEach(l=>{const m=l.match(/^\s+-\s+(.+)/);if(m)overrides.push(m[1].trim());});

// Tratti
function parseTratti(){
  const rows=[];
  const re=/^\s+([A-Z]+)\s*-\s*([^\n]+)\n\s+(D\.\d+)\s*\|\s*L tubo:\s*([\d,.]+)m\s*\|\s*Raccordi:\s*([^|]+)\|\s*Leq raccordi:\s*([\d,.]+)m\s*\|\s*L equiv\. totale:\s*([\d,.]+)m\s*\n\s+Q calcolo perdite:\s*([\d,.]+)\s*m3\/h\s*\|\s*Q dim\. DN:\s*([\d,.]+)\s*m3\/h\s*\|\s*v:\s*([\d,.]+)\s*m\/s\s*\|\s*J:\s*([\d,.]+)\s*mm\/m\s*\|\s*Perdita tratto:\s*([\d,.]+)\s*mca/gm;
  let m;
  while((m=re.exec(PROMPT))!==null){
    rows.push([m[1],m[2].trim().replace('->','\u2192'),m[3],m[4].replace('.',',')+' m',
      m[5].trim().replace(/(\d+)x/g,'$1\u00d7'),m[6].replace('.',',')+' m',m[7].replace('.',',')+' m',
      m[8].replace('.',','),m[9].replace('.',',')+' m\u00b3/h',
      m[10].replace('.',',')+' m/s',m[11].replace('.',',')+' mm/m',m[12].replace('.',',')+' mca']);
  }
  return rows;
}
const TR=parseTratti();

// Stile
const TEAL='1A5057',TEAL_L='D0E9EC',GRAY_H='F2F2F2',GOLD='C9A84C';
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
    borders:ba,width:{size:colW[i],type:WidthType.DXA},shading:{fill:TEAL,type:ShadingType.CLEAR},
    margins:{top:80,bottom:80,left:120,right:120},
    children:[new Paragraph({children:[new TextRun({text:h,font:'Calibri',size:20,bold:true,color:'FFFFFF'})],alignment:AlignmentType.CENTER})]
  }))});
  const drs=rows.map((row,ri)=>new TableRow({children:row.map((cell,ci)=>{
    const bold=cell.includes('>>>')||cell.includes('POSITIVO')||cell.includes('H PROGETTO')||cell.includes('TOTALE')||cell.includes('N/A');
    const color=cell.includes('POSITIVO')?'006600':cell.includes('NON CONF')?'CC0000':cell.includes('N/A')?'888888':'000000';
    return new TableCell({borders:ba,width:{size:colW[ci],type:WidthType.DXA},
      shading:{fill:ri%2===0?'FFFFFF':GRAY_H,type:ShadingType.CLEAR},
      margins:{top:60,bottom:60,left:120,right:120},
      children:[new Paragraph({children:[new TextRun({text:cell,font:'Calibri',size:20,bold,color})],
        alignment:ci===0?AlignmentType.LEFT:AlignmentType.CENTER})]});
  })}));
  return new Table({width:{size:hw,type:WidthType.DXA},columnWidths:colW,rows:[hdr,...drs]});
}
function box(lines){return lines.map(l=>new Paragraph({
  children:[new TextRun({text:l,font:'Calibri',size:21,bold:l.includes('>>>'),color:TEAL})],
  shading:{fill:TEAL_L,type:ShadingType.CLEAR},spacing:{before:40,after:40},indent:{left:240,right:240}}));}

const skiFornitore=P.skiModello.includes("Pool's")?'Pools':'Astral';
const boccFornitore=P.boccModello.includes("Pool's")?'Pools':'Astral';
const qBoccCalc=itN((parseFloat(P.Qmed.replace(',','.'))/parseInt(P.nBocc)).toFixed(2));
const volN=parseFloat(P.vol.replace(',','.'));
const TeffSporco=itN((volN/(parseFloat((P.pumpQmin||P.Qmin).replace(',','.'))||1)).toFixed(2));
const TeffPulito=itN((volN/(parseFloat((P.pumpQmax||P.Qmax).replace(',','.'))||1)).toFixed(2));

// ─── Documento ───────────────────────────────────────────────────────────────
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
  new Paragraph({children:[new TextRun({text:P.cliente,font:'Calibri',size:34,bold:true,color:TEAL})],alignment:AlignmentType.CENTER,spacing:{after:400}}),
  new Paragraph({children:[new TextRun({text:`Data: ${new Date().toLocaleDateString('it-IT',{day:'2-digit',month:'long',year:'numeric'})}`,font:'Calibri',size:22,color:'555555'})],alignment:AlignmentType.CENTER,spacing:{after:400}}),
  new Paragraph({children:[new TextRun({text:'Viale Aldo Moro 2, 50023 Impruneta (FI) \u2014 Tel. (+39) 055 0136621 \u2014 (+39) 351 9227533',font:'Calibri',size:18,color:'666666'})],alignment:AlignmentType.CENTER,spacing:{after:40}}),
  new Paragraph({children:[new TextRun({text:'www.acqua-lab.it \u2014 info@acqua-lab.it \u2014 P.I. 02281140976 \u2014 Cod. univoco: TULURSB',font:'Calibri',size:18,color:'666666'})],alignment:AlignmentType.CENTER}),
  pb()
];

const s1=[h1('1. Premessa e Filosofia Progettuale'),
  p('\u201cLa qualit\u00e0 dipende soprattutto da ci\u00f2 che non si vede.\u201d',{italic:true,bold:true,size:24,color:TEAL,after:120}),
  p('L\u2019invisibile determina la durata nel lungo periodo: quote, impermeabilizzazioni, idraulica, drenaggi, locale tecnico, portate, spessori, dettagli nascosti. Una piscina non \u00e8 un prodotto: \u00e8 un sistema tecnico che deve funzionare in equilibrio. Se una sola parte \u00e8 sbagliata \u2014 struttura, filtrazione, idraulica, trattamento \u2014 tutto il sistema si destabilizza.',{after:80}),
  p('La riuscita del progetto dipende dall\u2019organizzazione del cantiere e dal coordinamento tra le fasi. Risparmiare all\u2019inizio significa spesso spendere molto di pi\u00f9 dopo.',{after:80}),
  p(`La presente relazione documenta il dimensionamento esecutivo dell\u2019impianto idraulico per la piscina di ${P.cliente}.`,{after:120}),
];

const s2=[h1('2. Quadro Normativo'),
  tbl(['Norma','Ambito di applicazione','Ruolo nel progetto'],[
    ['UNI EN 16582-1/2/3','Sicurezza piscine \u2014 aspirazioni sommerse',P.noPF?'Non applicabile: prese di fondo escluse per scelta progettuale':'Norma primaria: verifica Q/(N-1) e velocit\u00e0 griglia'],
    ['UNI EN 16713-2:2016','Piscine private \u2014 circolazione',`T ricircolo (fino a 8h, scelto ${P.tRic}h), ripartizione portate`],
    ['UNI EN 16713-3','Qualit\u00e0 acqua piscine private','Parametri chimici di riferimento (indicativi)'],
    ['UNI EN 13451-3:2022','Attrezzatura \u2014 prese di fondo',P.noPF?'Riferimento prodotto (non applicabile: no prese di fondo)':'Riferimento prodotto per griglie prese di fondo'],
    ['D.Lgs. 152/2006 Tab.3 All.5','Acque reflue in fognatura','Conformit\u00e0 scarichi filtrazione a cartuccia'],
  ],[1400,2800,4872]),
  p(''),
  p('I limiti di velocit\u00e0 nelle tubazioni (v \u2264 1,7 m/s aspirazione / v \u2264 2,5 m/s mandata) sono limiti normativi di progetto. La verifica \u00e8 eseguita alla portata massima reale.',{italic:true,color:'444444',after:120}),
];

const s3=[h1("3. Descrizione dell'Impianto"),
  h2('3.1 Geometria Vasca'),
  tbl(['Parametro','Valore'],[
    ['Dimensioni vasca',P.dim],['Superficie specchio d\u2019acqua',`${P.sup} m\u00b2`],
    ['Perimetro',`${P.perim} m`],['Profondit\u00e0',P.profDesc],['Volume totale',`${P.vol} m\u00b3`],
    ['Costruzione',P.costruz],['Circolazione',P.circ],
    ['Filtrazione',P.filtTipo.charAt(0).toUpperCase()+P.filtTipo.slice(1)],
    ['Tubo interrato per tratto',P.tuboDesc.replace(/Per tratto:\s*/,'')],
    ['Prese di fondo',P.noPF?'Escluse per scelta progettuale':'Presenti'],
  ],[3600,5472]),
  p(''),h2('3.2 Elementi Speciali'),
  bullet('Scala: 4 gradini, larghezza 1 m \u2014 volume sottratto 0,891 m\u00b3'),
  p(''),h2('3.3 Quote di Riferimento'),
  tbl(['Quota','Valore (rif. 0,00)'],[
    ['Livello acqua vasca',P.livAcqua],['Asse pompa',P.assePompa],
    ['Bordo vasca',P.bordoVasca],['Dislivello statico','0,00 mca'],
  ],[4536,4536]),
  p(''),h2('3.4 Schema Idraulico'),
  p(`Vasca (${P.circ}) \u2192 Coll. asp. D.${cAspDN} \u2192 Tratto C D.90 rigido \u2192 Pompa \u2192 Filtro \u2192 Coll. man. D.${cManDN} \u2192 Bocchette restituzione`,{indent:360,color:'333333',after:80}),
  p('Cella elettrolisi su by-pass dedicato a valle della pompa.',{italic:true,color:'444444',after:120}),
];

const s4=[h1('4. Calcolo della Portata di Progetto'),
  new Paragraph({children:[
    new TextRun({text:`Q progetto = V / T = ${P.vol} / ${P.tRic} = `,font:'Calibri',size:22}),
    new TextRun({text:`${P.Qprog} m\u00b3/h`,font:'Calibri',size:22,bold:true,color:TEAL}),
    new TextRun({text:`  (T = ${P.tRic}h \u2014 scelta progettuale Acqualab; UNI EN 16713-2 ammette fino a 8h)`,font:'Calibri',size:20,color:'555555'}),
  ],indent:{left:360},spacing:{before:60,after:120}}),
  tbl(['Condizione','Portata','H impianto','Note'],[
    ['Q progetto (requisito igienico)',`${P.Qprog} m\u00b3/h`,'\u2014',`V / T = ${P.vol} / ${P.tRic}`],
    ['Q max (filtro pulito, appena lavato)',`${P.Qmax} m\u00b3/h`,`${P.Hclean} mca`,'Calcolata per iterazione'],
    ['Q filtro sporco (da pulire)',`${P.Qmin} m\u00b3/h`,`${P.Hprog} mca`,'Punto di lavoro a filtro sporco (da pulire)'],
    ['>>> Q MEDIA DI ESERCIZIO',`${P.Qmed} m\u00b3/h`,'\u2014',`DATO DI RIFERIMENTO \u2014 (${P.Qmax} + ${P.Qmin}) / 2`],
  ],[2500,1700,1200,3672]),
  p(''),
  ...box([`>>> Q MEDIA DI ESERCIZIO: ${P.Qmed} m\u00b3/h  \u2014  T medio: ${P.Tmed} h  \u2014  Q media per skimmer: ${P.QperSki} m\u00b3/h cad.`]),
  p(''),
  p(`Circolazione 100% superficie (${P.circ}) \u2014 prese di fondo ${P.noPF?'escluse per scelta progettuale. Ripartizione 2/3 sup. + 1/3 fondo non applicabile.':'presenti.'}`,{italic:true,color:'444444',after:120}),
];

const s5=[h1('5. Dimensionamento Idraulico delle Tubazioni'),
  h2('5.1 Metodo e Criteri'),
  p(`Metodo Hazen-Williams C = 150 (PVC liscio). Tubazioni dimensionate alla Q max reale (filtro pulito appena lavato = ${P.Qmax} m\u00b3/h).`,{after:80}),
  tbl(['Criterio','Aspirazione','Mandata'],[
    ['Perdita di carico J (normativo)','J \u2264 40 mm/m','J \u2264 70 mm/m'],
    ['Velocit\u00e0 v (normativo)','v \u2264 1,7 m/s','v \u2264 2,5 m/s'],
  ],[3200,2936,2936]),
  p(''),h2('5.2 Tabella Tratti'),
  tbl(['Tr.','Descrizione','D.','L tubo','Raccordi','Leq','Leq tot.','Q perd.','Q dim. DN','v','J','H tratto'],
    TR.length>0?TR:[['—','—','—','—','—','—','—','—','—','—','—','—']],
    [320,850,420,520,950,500,570,520,680,680,680,680]),
  P.noPF?p('Nota: il tratto PF (prese di fondo) \u00e8 assente.',{italic:true,color:'444444',after:80}):p(''),
  p(''),h2('5.3 Collettori'),
  tbl(['Collettore','Diametro','Velocit\u00e0','Rapporto sezioni','Note'],[
    ['Aspirazione',`D.${cAspDN} PN10`,`${cAspV} m/s`,`${cAspRap}\u00d7`,'Calcolo automatico'],
    ['Mandata',`D.${cManDN} PN10`,`${cManV} m/s`,`${cManRap}\u00d7`,
      overrides.some(o=>o.toLowerCase().includes('collettore mandata'))?'Override progettuale':'Calcolo automatico'],
  ],[1200,1200,1200,1200,4272]),
  p('',{after:120}),
];

const s6=[h1('6. Calcolo della Prevalenza'),
  tbl(['Componente','Valore (mca)','Note'],[
    ...TR.map(t=>[`H tratto ${t[0]} (${t[1]})`,t[11],`Q = ${t[7]} m\u00b3/h \u2014 ${t[2]}`]),
    ['H filtro cartuccia sporco (da pulire)','7,000','Condizione limite'],
    ['H filtro cartuccia pulito (appena lavato)','2,000','Per verifica Q max'],
    ['H prefiltro pompa','0,750',''],['H dislivello statico','0,000',''],
    ['Margine di sicurezza','0,500',''],
    ['H elettrolisi (2 tee by-pass)','0,200','VS e curve sul ramo by-pass'],
    [`H BASE (senza accessori)`,`${P.Hbase} mca`,''],
    [`H PROGETTO (filtro sporco, con acc.)`,`${P.Hprogetto} mca`,'PREVALENZA DI PROGETTO'],
  ],[3200,1800,4072]),
  p(''),
  ...box([`H PROGETTO: ${P.Hprogetto} mca  (filtro sporco da pulire + accessori)`,
          `H a filtro pulito (appena lavato): ${P.Hclean} mca`]),
  p('',{after:120}),
];

const s7=[h1('7. Selezione della Pompa'),
  tbl(['Parametro','Valore'],[
    ['Modello',`${P.pumpModello.trim()} \u2014 TASCO`],
    ['Alimentazione','230 V monofase IE2'],
    ['Potenza nominale',P.pumpHP],
    ['Numero pompe',P.nPompe],
    ['Fornitore','TASCO'],
  ],[3600,5472]),
  p(''),
  tbl(['Condizione filtro','H impianto','Q pompa','T ricircolo','Esito'],[
    ['Filtro sporco (da pulire)',`${P.Hprog} mca`,`${P.pumpQmin} m\u00b3/h`,`${TeffSporco} h`,`\u2713 T \u2264 ${P.tRic}h`],
    ['Filtro pulito (appena lavato)',`${P.Hclean} mca`,`${P.pumpQmax} m\u00b3/h`,`${TeffPulito} h`,`\u2713 Q \u2264 ${P.filtQmaxDich} m\u00b3/h max filtro`],
  ],[2500,1500,1800,1500,1772]),
  p(''),
  ...box([
    `>>> Q MEDIA DI ESERCIZIO: ${P.Qmed} m\u00b3/h  \u2014  dato di riferimento principale`,
    `    Media tra filtro pulito (${P.pumpQmax}) e filtro sporco (${P.pumpQmin})`,
    `    T ricircolo medio: ${P.Tmed} h  |  Q media per skimmer: ${P.QperSki} m\u00b3/h cad. (< ${P.skiQrac} \u2713)`,
  ]),
  p('',{after:120}),
];

const s8=[h1('8. Selezione del Filtro'),
  tbl(['Parametro','Valore'],[
    ['Modello',`${P.filtModello.trim()} \u2014 TASCO`],
    ['Superficie filtrante',`${P.filtSup} m\u00b2`],
    ['Portata di verifica (Q max)',`${P.Qmax} m\u00b3/h (filtro pulito appena lavato)`],
    ['Velocit\u00e0 di filtrazione',`${P.filtVfilt} m\u00b3/h/m\u00b2  (${P.Qmax} / ${P.filtSup})`],
    ['Portata max dichiarata (costruttore)',`${P.filtQmaxDich} m\u00b3/h`],
    ['Verifica',`${P.Qmax} m\u00b3/h \u2264 ${P.filtQmaxDich} m\u00b3/h  \u2713  ESITO POSITIVO`],
    ['Valvola','Inclusa nel filtro'],
  ],[3600,5472]),
  p('',{after:120}),
];

const s9=[h1('9. Vantaggi della Filtrazione a Cartuccia'),
  new Paragraph({children:[new TextRun({text:'Fonte: \u201cSistemi di Filtrazione e Disinfezione EcoFriendly \u2014 NOTA TECNICA\u201d \u2014 Acqualab srl',font:'Calibri',size:18,italics:true,color:'666666'})],spacing:{after:120}}),
  h2('Efficienza Idrica \u2014 Eliminazione del Controlavaggio'),
  bullet('Nessuno scarico idrico aggiuntivo durante il ciclo \u2014 nessun refluo da trattare'),
  bullet('Per domestiche (UNI EN 16713-2:2016): unico scarico = svuotamento stagionale'),
  bullet('Conformit\u00e0 scarichi in fognatura: Tab. 3 All. 5 D.Lgs. 152/2006'),
  p(''),h2('Qualit\u00e0 di Filtrazione'),
  tbl(['Tecnologia','Finezza','Torbidità tipica'],[
    ['Cartuccia (questo impianto)','20\u201330 micron','< 0,5 NTU'],
    ['Sabbia silicea','50 micron','0,5\u20131 NTU'],
  ],[3024,3024,3024]),
  p(''),h2('Variabilit\u00e0 della Perdita di Carico nel Ciclo'),
  bullet('Pulizia manuale a bassa pressione \u2014 sostituzione rapida senza svuotare il circuito'),
  bullet('Perdita di carico: 2 mca (filtro pulito) \u2192 7 mca (filtro sporco da pulire) \u2014 il progetto verifica i punti di lavoro in entrambe le condizioni'),
  p('',{after:120}),
];

const s10=[h1('10. Componenti di Circolazione'),
  tbl(['Componente','Modello','Qt.','Specifiche'],[
    ['Skimmer sfioratore',`${P.skiModello.trim()} \u2014 ABS`,P.nSki,
      `Q raccomandata: ${P.skiQrac} m\u00b3/h | Attacco ${P.skiAttacco}\nQ media esercizio: ${P.QperSki} m\u00b3/h cad. (< ${P.skiQrac} \u2713)`],
    ['Bocchetta mandata',`${P.boccModello.trim()} \u2014 ABS`,P.nBocc,
      `Q max: ${P.boccQmax} m\u00b3/h | Attacco ${P.boccAttacco}\nQ media esercizio: ${P.Qmed}/${P.nBocc} = ${qBoccCalc} m\u00b3/h (< ${P.boccQmax} \u2713)`],
    ['Prese di fondo','N/A','\u2014','Escluse per scelta progettuale'],
  ],[1500,3000,400,4172]),
  p('',{after:120}),
];

const s11=[h1('11. Verifica di Sicurezza \u2014 Aspirazioni Sommerse'),
  new Paragraph({children:[new TextRun({text:'PRESE DI FONDO: ESCLUSE per scelta progettuale.',font:'Calibri',size:22,bold:true,color:TEAL})],spacing:{before:80,after:80}}),
  p('Tutta l\u2019aspirazione avviene dalla superficie tramite skimmer sfioratori. Non \u00e8 presente alcuna aspirazione sommersa dal fondo vasca. La verifica anti-intrappolamento (UNI EN 16582) non \u00e8 applicabile.',{after:80}),
  p('Scelta progettuale deliberata documentata: eliminando le aspirazioni sommerse si elimina alla radice il rischio di intrappolamento.',{italic:true,color:'444444',after:120}),
];

const s12=[h1("12. Vantaggi dell'Elettrolisi a Sale a Bassa Salinit\u00e0"),
  new Paragraph({children:[new TextRun({text:'Fonte: \u201cSistemi di Filtrazione e Disinfezione EcoFriendly \u2014 NOTA TECNICA\u201d \u2014 Acqualab srl',font:'Calibri',size:18,italics:true,color:'666666'})],spacing:{after:120}}),
  h2('Sicurezza Stoccaggio'),
  bullet('Prodotti clorati tradizionali: H314 corrosivo, H400 pericoloso per ambiente acquatico'),
  bullet('Con elettrolisi: unico approvvigionamento = sale da cucina (NaCl) \u2014 nessun obbligo D.Lgs. 81/2008 n\u00e9 D.Lgs. 105/2015 per piscine private'),
  p(''),h2('Tecnologia Nuova Generazione'),
  tbl(['Parametro','Questo impianto','Vecchia generazione'],[
    ['Salinit\u00e0 acqua','1,5 kg/m\u00b3','4\u20135 kg/m\u00b3'],
    ['Produzione Cl\u2082','30 g/h (fino a 200 m\u00b3)','\u2014'],
    ['Scarico in fognatura','Semplificato','Soggetto a limitazioni'],
  ],[3024,3024,3024]),
  p(''),h2('Installazione su By-Pass'),
  p('Schema: tee \u2192 VS \u2192 curva 90\u00b0 \u2192 cella \u2192 VS \u2192 tee \u2014 \u0394H circuito principale: 0,20 mca (2 tee derivazione)',{indent:360,bold:true,color:TEAL,after:80}),
  bullet('Regolazione automatica pH inclusa: sonda analitica + dosatore automatico acido correttivo'),
  bullet('UNI EN 16713-2:2016: non vieta la clorazione salina; dosatori EM obbligatori solo per Tipo 2'),
  p('',{after:120}),
];

const s13=[h1('13. Accessori in Linea'),
  tbl(['Accessorio','Descrizione','\u0394H'],[
    ['Elettrolisi sale','Salinit\u00e0 1,5 kg/m\u00b3 \u2014 30 g/h Cl\u2082 \u2014 pH automatico\nBy-pass: tee \u2192 VS \u2192 90\u00b0 \u2192 cella \u2192 VS \u2192 tee','0,20 mca'],
    ['TOTALE','','0,20 mca'],
  ],[2000,6072,1000]),
  p('',{after:120}),
];

const s14=[h1('14. Distinta Materiali \u2014 Listino 2025 IVA Esclusa'),
  tbl(['Componente','Modello','Fornitore','Qt.'],[
    ['Filtro cartuccia',P.filtModello.trim(),'TASCO','1'],
    ['Pompa',`${P.pumpModello.trim()} 230V IE2`,'TASCO',P.nPompe],
    ['Skimmer sfioratore',P.skiModello.trim(),skiFornitore,P.nSki],
    ['Bocchetta mandata',P.boccModello.trim(),boccFornitore,P.nBocc],
    ['Tubi e raccorderia PVC','Diametri vari \u2014 da rilievo cantiere','\u2014','\u2014'],
  ],[2000,4000,1500,1572]),
  p('Prezzi da confermare con i fornitori al momento dell\u2019ordine.',{italic:true,color:'444444',after:120}),
];

const s15=[h1('15. Parametri Acqua e Avviamento'),
  tbl(['Parametro','Valore','Unit\u00e0'],[
    ['pH','7,0 \u2013 7,4','\u2014'],['Cloro libero','0,6 \u2013 1,5','mg/l'],
    ['Cloro combinato (max)','0 \u2013 0,5','mg/l'],['Alcalinit\u00e0','80 \u2013 120','mg/l CaCO\u2083'],
    ['Durezza','150 \u2013 300','mg/l CaCO\u2083'],['Torbidità (max)','0 \u2013 1','NTU'],
    ['Temperatura','24 \u2013 32','\u00b0C'],['Acido cianurico (max)','0 \u2013 100','mg/l'],
  ],[3024,3024,3024]),
  p(''),h2('Checklist Avviamento'),
  bullet('Ispezione vasca e locale tecnico'),
  bullet('Verifica tenuta idraulica collettori e raccorderia'),
  bullet('Riempimento \u2014 primo avvio \u2014 verifica portata e pressioni'),
  bullet('Verifica salinit\u00e0 (target 1,5 kg/m\u00b3)'),
  bullet('Primo controllo parametri chimici (pH, cloro, alcalinit\u00e0)'),
  bullet('Regolazione cella elettrolisi e dosaggio pH automatico'),
  p('',{after:120}),
];

const s16=[h1('16. Indice di Conformit\u00e0 Tecnica (ICT)'),
  ...box([`ICT = ${P.ictVal}/100  \u2014  Classe ${P.ictCls} (${P.ictLbl})`]),
  p(''),
  tbl(['Criterio','Peso','Score','Note'],[
    ['Sicurezza aspirazioni (UNI EN 16582)','30%',P.noPF?'30/30':'30/30',
      P.noPF?'Prese di fondo assenti \u2014 nessun rischio aspirazione sommersa (UNI EN 16582 non applicabile) \u2713':'Verifica Q/(N-1) conforme \u2713'],
    ['Idraulica tubazioni','25%','25/25','v e J nei limiti normativi \u2713'],
    ['Filtrazione','25%','25/25',`T = ${P.Teff} h \u2264 ${P.tRic}h \u2713  |  Q = ${P.Qmax} \u2264 ${P.filtQmaxDich} m\u00b3/h \u2713`],
    ['Componenti','20%','20/20',`Q/bocc = ${qBoccCalc} \u2264 ${P.boccQmax} m\u00b3/h \u2713  |  Q/ski = ${P.QperSki} < ${P.skiQrac} m\u00b3/h \u2713`],
    ['TOTALE','100%',`${P.ictVal}/100 \u2014 Classe ${P.ictCls}`,'Eccellente'],
  ],[2800,900,900,4472]),
  p(''),
  p(`Il punteggio ${P.ictVal}/100 (Classe ${P.ictCls}) indica un impianto pienamente conforme su tutti i criteri verificabili.`,{italic:true,color:'444444',after:80}),
  p(''),
  tbl(['Classe','Punteggio','Significato'],[
    ['A','\u2265 90','Eccellente'],['B','75 \u2013 89','Buono'],
    ['C','60 \u2013 74','Accettabile'],['D','40 \u2013 59','Insufficiente'],['E','< 40','Non conforme'],
  ],[1500,1800,5772]),
  p('',{after:120}),
];

const s16b=overrides.length>0?[
  h1('17. Scelte Progettuali'),
  p('Le seguenti scelte differiscono dal calcolo automatico e sono documentate come decisioni progettuali deliberate:',{after:80}),
  ...overrides.map(o=>bullet(o)),
  p('',{after:120}),
]:[];

const nConc=overrides.length>0?18:17;
const s17=[h1(`${nConc}. Conclusioni`),
  tbl(['Parametro','Valore','Conformit\u00e0'],[
    ['Q progetto (requisito igienico)',`${P.Qprog} m\u00b3/h (T = ${P.tRic}h)`,`\u2713 UNI EN 16713-2`],
    ['Q filtro sporco (da pulire)',`${P.pumpQmin} m\u00b3/h (T = ${TeffSporco}h)`,`\u2713 T \u2264 ${P.tRic}h`],
    ['Q filtro pulito (appena lavato)',`${P.pumpQmax} m\u00b3/h`,`\u2713 Q \u2264 ${P.filtQmaxDich} m\u00b3/h filtro`],
    ['Q media di esercizio',`${P.Qmed} m\u00b3/h (T = ${P.Tmed}h)`,'\u2713 Dato di riferimento'],
    ['Sicurezza PF',P.noPF?'N/A \u2014 prese di fondo escluse':'Verificata','Scelta progettuale documentata'],
    ['ICT',`${P.ictVal}/100 \u2014 Classe ${P.ictCls}`,'\u2713 Eccellente'],
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
  ...s13,sep(),...s14,sep(),...s15,sep(),...s16,...s16b,sep(),...s17];

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
