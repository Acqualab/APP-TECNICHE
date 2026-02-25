import math

def calcola_impianto_uni10637():
    print("--- Dimensionamento Piscina UNI 10637:2024 (Tipo 2) ---")
    
    # Input dati geometrici
    L = float(input("Lunghezza totale vasca (m): "))
    W = float(input("Larghezza vasca (m): "))
    h_min = float(input("Profondità minima (m): "))
    h_max = float(input("Profondità massima (m): "))

    # Calcolo pendenza media (assumendo fondo a pendenza costante)
    pendenza = (h_max - h_min) / L
    
    def get_tempo_ricircolo(h):
        """Restituisce il tempo t in base al Prospetto 3 dell'immagine"""
        if h > 1.35: return 3.0    # Zona C
        if h > 0.6:  return 2.5    # Zona D
        if h > 0.4:  return 1.0    # Zona E
        return 0.5                 # Zona F

    # Integrazione della portata lungo la lunghezza (passo 10cm per precisione)
    passo = 0.1
    portata_totale = 0
    volume_totale = 0
    
    x = 0
    while x < L:
        # Profondità corrente in questo punto x
        h_corrente = h_min + (x * pendenza)
        t_zona = get_tempo_ricircolo(h_corrente)
        
        # Volume del piccolo segmento (V = Area_base * h)
        v_segmento = (passo * W) * h_corrente
        portata_totale += v_segmento / t_zona
        volume_totale += v_segmento
        x += passo

    # --- Dimensionamento Componenti ---
    # 1. Filtrazione (v = 30 m/h standard per Tipo 2)
    v_filtrazione = 30
    area_filtro = portata_totale / v_filtrazione
    
    # 2. Tubazioni (Velocità 1.5 m/s mandata, 1.0 m/s aspirazione)
    def diametro_tubo(Q, v):
        area = (Q / 3600) / v
        return math.sqrt(area / math.pi) * 2 * 1000

    d_mandata = diametro_tubo(portata_totale, 1.5)
    d_aspirazione = diametro_tubo(portata_totale, 1.0)

    print("\n" + "="*40)
    print(f"Volume Totale Calcolato: {volume_totale:.2f} m3")
    print(f"PORTATA TOTALE DI PROGETTO: {portata_totale:.2f} m3/h")
    print("-" * 40)
    print(f"Superficie Filtrante Necessaria: {area_filtro:.2f} m2")
    print(f"Diametro Interno Tubo Mandata: {d_mandata:.1f} mm")
    print(f"Diametro Interno Tubo Aspirazione: {d_aspirazione:.1f} mm")
    print("="*40)

calcola_impianto_uni10637()
