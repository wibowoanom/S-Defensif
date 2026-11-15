import yfinance as yf
import pandas as pd
import numpy as np
import os
import time
import warnings
from google.colab import drive

warnings.filterwarnings('ignore')

# Tampilkan semua baris/kolom tabel (tanpa terpotong "...")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 250)

# ==========================================
# 1. SETUP & MOUNT GOOGLE DRIVE
# ==========================================
print("Mounting Google Drive...")
drive.mount('/content/drive')
output_dir = '/content/drive/MyDrive/IDX_Screening_Result'
os.makedirs(output_dir, exist_ok=True)
print(f"Output akan disimpan di: {output_dir}\n")

# ==========================================
# 2. DAFTAR TICKER IDX2 BENAR (561 SAHAM)
# ==========================================
idx_tickers = [
    "AADI.JK", "ACRO.JK", "ACST.JK", "ADCP.JK", "ADES.JK", "ADMF.JK", "ADMR.JK",
    "AEGS.JK", "AGAR.JK", "AGII.JK", "AGRS.JK", "AHAP.JK", "AISA.JK", "AKKU.JK",
    "AKPI.JK", "AKSI.JK", "ALDO.JK", "ALII.JK", "ALKA.JK", "ALMI.JK", "ALTO.JK",
    "AMAG.JK", "AMAN.JK", "AMAR.JK", "AMIN.JK", "AMMN.JK", "AMMS.JK", "AMOR.JK",
    "APIC.JK", "APII.JK", "APLI.JK", "ARCI.JK", "AREA.JK", "ARGO.JK", "ARKA.JK",
    "ARKO.JK", "ARTA.JK", "ASGR.JK", "ASHA.JK", "ASJT.JK", "ASLC.JK", "ASLI.JK",
    "ASMI.JK", "ASPI.JK", "ASPR.JK", "ATAP.JK", "ATIC.JK", "ATLA.JK", "AVIA.JK",
    "AWAN.JK", "AXIO.JK", "AYAM.JK", "AYLS.JK", "BABP.JK", "BABY.JK", "BACA.JK",
    "BAIK.JK", "BAJA.JK", "BANK.JK", "BAPI.JK", "BATR.JK", "BAUT.JK", "BBLD.JK",
    "BBSI.JK", "BBSS.JK", "BCIC.JK", "BDKR.JK", "BEBS.JK", "BEEF.JK", "BEER.JK",
    "BELI.JK", "BELL.JK", "BESS.JK", "BHAT.JK", "BIKE.JK", "BIMA.JK", "BINA.JK",
    "BINO.JK", "BKDP.JK", "BLES.JK", "BLOG.JK", "BLTZ.JK", "BLUE.JK", "BMBL.JK",
    "BMHS.JK", "BMSR.JK", "BMTR.JK", "BNBR.JK", "BOAT.JK", "BOBA.JK", "BOGA.JK",
    "BOLA.JK", "BPFI.JK", "BPII.JK", "BPTR.JK", "BRAM.JK", "BREN.JK", "BRRC.JK",
    "BSBK.JK", "BSML.JK", "BTEK.JK", "BTON.JK", "BUAH.JK", "BUDI.JK", "BUKK.JK",
    "BUVA.JK", "CAKK.JK", "CAMP.JK", "CANI.JK", "CARS.JK", "CASA.JK", "CBDK.JK",
    "CBPE.JK", "CBRE.JK", "CBUT.JK", "CCSI.JK", "CDIA.JK", "CFIN.JK", "CGAS.JK",
    "CHEK.JK", "CHEM.JK", "CHIP.JK", "CINT.JK", "CLAY.JK", "CLPI.JK", "CMNP.JK",
    "CMNT.JK", "CMPP.JK", "CNMA.JK", "COAL.JK", "COCO.JK", "COIN.JK", "CPRO.JK",
    "CRAB.JK", "CRSN.JK", "CSIS.JK", "CSMI.JK", "CSRA.JK", "CTBN.JK", "CUAN.JK",
    "CYBR.JK", "DAAZ.JK", "DADA.JK", "DATA.JK", "DAYA.JK", "DEFI.JK", "DEPO.JK",
    "DEWI.JK", "DFAM.JK", "DGIK.JK", "DGNS.JK", "DGWG.JK", "DIGI.JK", "DIVA.JK",
    "DKHH.JK", "DMMX.JK", "DMND.JK", "DNET.JK", "DOOH.JK", "DPNS.JK", "DPUM.JK",
    "DRMA.JK", "DSFI.JK", "DSSA.JK", "DYAN.JK", "EAST.JK", "ECII.JK", "ELIT.JK",
    "ELPI.JK", "ELTY.JK", "EMAS.JK", "ENAK.JK", "ENZO.JK", "EPAC.JK", "EPMT.JK",
    "ERAL.JK", "ERTX.JK", "ESTA.JK", "ESTI.JK", "EURO.JK", "FAPA.JK", "FILM.JK",
    "FIMP.JK", "FIRE.JK", "FISH.JK", "FITT.JK", "FLMC.JK", "FOLK.JK", "FOOD.JK",
    "FORE.JK", "FORU.JK", "FPNI.JK", "FUJI.JK", "FWCT.JK", "GDST.JK", "GEMA.JK",
    "GGRM.JK", "GGRP.JK", "GLVA.JK", "GMFI.JK", "GOLD.JK", "GOLF.JK", "GPSO.JK",
    "GRIA.JK", "GRPH.JK", "GRPM.JK", "GSMF.JK", "GTRA.JK", "GULA.JK", "GUNA.JK",
    "HAIS.JK", "HAJJ.JK", "HALO.JK", "HATM.JK", "HBAT.JK", "HDFA.JK", "HDIT.JK",
    "HEXA.JK", "HGII.JK", "HILL.JK", "HOMI.JK", "HOPE.JK", "HRME.JK", "HUMI.JK",
    "HYGN.JK", "IATA.JK", "IBFN.JK", "IBOS.JK", "ICON.JK", "IDEA.JK", "IFII.JK",
    "IFSH.JK", "IKAI.JK", "IKAN.JK", "IKBI.JK", "IKPM.JK", "IMAS.JK", "IMJS.JK",
    "INCF.JK", "INCI.JK", "INDO.JK", "INDR.JK", "INDX.JK", "INOV.JK", "INPS.JK",
    "INTA.JK", "INTD.JK", "IOTF.JK", "IPAC.JK", "IPCC.JK", "IPPE.JK", "IPTV.JK",
    "IRRA.JK", "IRSX.JK", "ISAP.JK", "ISEA.JK", "ITIC.JK", "JARR.JK", "JAST.JK",
    "JATI.JK", "JAWA.JK", "JAYA.JK", "JGLE.JK", "JIHD.JK", "JKON.JK", "JMAS.JK",
    "JSPT.JK", "JTPE.JK", "KAEF.JK", "KAQI.JK", "KARW.JK", "KBAG.JK", "KBLV.JK",
    "KDTN.JK", "KEEN.JK", "KETR.JK", "KICI.JK", "KING.JK", "KINO.JK", "KIOS.JK",
    "KJEN.JK", "KKES.JK", "KLAS.JK", "KLIN.JK", "KMDS.JK", "KMTR.JK", "KOBX.JK",
    "KOCI.JK", "KOKA.JK", "KONI.JK", "KOTA.JK", "KRAS.JK", "KREN.JK", "KRYA.JK",
    "KSIX.JK", "KUAS.JK", "LABA.JK", "LABS.JK", "LAJU.JK", "LAND.JK", "LAPD.JK",
    "LCKM.JK", "LFLO.JK", "LIFE.JK", "LIVE.JK", "LMAX.JK", "LMPI.JK", "LOPI.JK",
    "LPIN.JK", "LPLI.JK", "LPPS.JK", "LUCY.JK", "MAHA.JK", "MAIN.JK", "MANG.JK",
    "MAPA.JK", "MAPB.JK", "MARI.JK", "MARK.JK", "MASB.JK", "MAXI.JK", "MAYA.JK",
    "MBMA.JK", "MBTO.JK", "MCOL.JK", "MCOR.JK", "MDIA.JK", "MDIY.JK", "MDKI.JK",
    "MDLA.JK", "MDRN.JK", "MEDS.JK", "MEGA.JK", "MEJA.JK", "MENN.JK", "MERI.JK",
    "MGLV.JK", "MGNA.JK", "MGRO.JK", "MICE.JK", "MIDI.JK", "MINA.JK", "MINE.JK",
    "MKAP.JK", "MKNT.JK", "MKTR.JK", "MLPL.JK", "MMIX.JK", "MMLP.JK", "MOLI.JK",
    "MPIX.JK", "MPRO.JK", "MPXL.JK", "MRAT.JK", "MSIE.JK", "MSIN.JK", "MSJA.JK",
    "MSKY.JK", "MSTI.JK", "MTEL.JK", "MTMH.JK", "MTPS.JK", "MTWI.JK", "MUTU.JK",
    "MYTX.JK", "NAIK.JK", "NANO.JK", "NASA.JK", "NASI.JK", "NATO.JK", "NAYZ.JK",
    "NCKL.JK", "NEST.JK", "NETV.JK", "NICE.JK", "NICK.JK", "NICL.JK", "NINE.JK",
    "NPGF.JK", "NSSS.JK", "NTBK.JK", "NZIA.JK", "OASA.JK", "OBAT.JK", "OBMD.JK",
    "OILS.JK", "OKAS.JK", "OLIV.JK", "OMED.JK", "OPMS.JK", "PACK.JK", "PADA.JK",
    "PAMG.JK", "PANI.JK", "PANR.JK", "PART.JK", "PBRX.JK", "PBSA.JK", "PDES.JK",
    "PDPP.JK", "PEVE.JK", "PGJO.JK", "PGUN.JK", "PICO.JK", "PIPA.JK", "PJHB.JK",
    "PLAN.JK", "PLIN.JK", "PMJS.JK", "PMMP.JK", "PMUI.JK", "PNBN.JK", "PNSE.JK",
    "POLA.JK", "POLI.JK", "POLU.JK", "POLY.JK", "PPGL.JK", "PPRE.JK", "PPRI.JK",
    "PRAY.JK", "PRDA.JK", "PRIM.JK", "PSAT.JK", "PSGO.JK", "PSKT.JK", "PTDU.JK",
    "PTMP.JK", "PTMR.JK", "PTPS.JK", "PTPW.JK", "PTSP.JK", "PUDP.JK", "PURA.JK",
    "PURI.JK", "PZZA.JK", "RAAM.JK", "RAFI.JK", "RALS.JK", "RATU.JK", "RBMS.JK",
    "RCCC.JK", "REAL.JK", "RELF.JK", "RGAS.JK", "RISE.JK", "RLCO.JK", "RMKE.JK",
    "RMKO.JK", "ROCK.JK", "RONY.JK", "RSCH.JK", "RSGK.JK", "RUNS.JK", "SAGE.JK",
    "SAMF.JK", "SAPX.JK", "SATU.JK", "SBMA.JK", "SCCO.JK", "SCNP.JK", "SDPC.JK",
    "SEMA.JK", "SICO.JK", "SILO.JK", "SINI.JK", "SKBM.JK", "SKRN.JK", "SLIS.JK",
    "SMBR.JK", "SMGA.JK", "SMIL.JK", "SMKL.JK", "SMKM.JK", "SMLE.JK", "SMMA.JK",
    "SMSM.JK", "SNLK.JK", "SOFA.JK", "SOLA.JK", "SONA.JK", "SOSS.JK", "SOTS.JK",
    "SOUL.JK", "SPMA.JK", "SPRE.JK", "SPTO.JK", "SQMI.JK", "SRAJ.JK", "SSIA.JK",
    "STAA.JK", "STAR.JK", "STRK.JK", "STTP.JK", "SUNI.JK", "SUPA.JK", "SUPR.JK",
    "SURI.JK", "SWAT.JK", "SWID.JK", "TALF.JK", "TAYS.JK", "TBMS.JK", "TCID.JK",
    "TCPI.JK", "TEBE.JK", "TFAS.JK", "TGKA.JK", "TGRA.JK", "TGUK.JK", "TIFA.JK",
    "TINS.JK", "TIRA.JK", "TLDN.JK", "TMPO.JK", "TNCA.JK", "TOOL.JK", "TOPS.JK",
    "TOSK.JK", "TPIA.JK", "TRGU.JK", "TRIN.JK", "TRIS.JK", "TRON.JK", "TRUE.JK",
    "TRUK.JK", "TRUS.JK", "TYRE.JK", "UANG.JK", "UCID.JK", "UDNG.JK", "UFOE.JK",
    "UNIQ.JK", "UNTD.JK", "UVCR.JK", "VAST.JK", "VERN.JK", "VICO.JK", "VISI.JK",
    "VIVA.JK", "VTNY.JK", "WAPO.JK", "WBSA.JK", "WEHA.JK", "WGSH.JK", "WICO.JK",
    "WIDI.JK", "WINE.JK", "WINR.JK", "WINS.JK", "WMPP.JK", "WOMF.JK", "WOWS.JK",
    "XCIS.JK", "YOII.JK", "YULE.JK", "YUPI.JK", "ZATA.JK", "ZBRA.JK", "ZONE.JK",
    "ZYRX.JK"
]

# ==========================================
# 3. DOWNLOAD DATA HISTORIS (HARGA & VOLUME)
# ==========================================
print("Downloading historical price and volume data (2 Years)...")
# Download data untuk perhitungan MA200, Avg Value, dan RS Rank
data = yf.download(idx_tickers, period="2y", interval="1d", threads=True, progress=False)
prices = data['Close']
volumes = data['Volume']

# Hapus ticker yang tidak memiliki data harga
valid_tickers = prices.dropna(axis=1, how='all').columns
prices = prices[valid_tickers]
volumes = volumes[valid_tickers]

# ==========================================
# 4. HITUNG PARAMETER TEKNIKAL
# ==========================================
current_price = prices.iloc[-1]
ma200 = prices.rolling(window=200).mean().iloc[-1]

# Avg Value 20d (Nilai Transaksi = Close * Volume)
transaction_value = prices * volumes
avg_value_20d = transaction_value.rolling(window=20).mean().iloc[-1]

# RS Rank (Relative Strength) berdasarkan return 1 tahun (252 hari)
returns_1y = prices.pct_change(periods=252).iloc[-1]
rs_rank = returns_1y.rank(pct=True) * 100

df_technical = pd.DataFrame({
    'Price': current_price,
    'MA200': ma200,
    'Avg_Value_20d': avg_value_20d,
    'RS_Rank': rs_rank
})

# ==========================================
# 5. DOWNLOAD DATA FUNDAMENTAL
# ==========================================
print("Downloading fundamental data (this may take a few minutes)...")
fundamentals = []
for i, ticker in enumerate(valid_tickers):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        roe = info.get('returnOnEquity', None)
        der = info.get('debtToEquity', None)
        div_yield = info.get('dividendYield', None)
        market_cap = info.get('marketCap', None)
        
        # PERBAIKAN 1: yfinance versi sekarang memberi dividendYield dalam persen
        # (9.42 = 9.42%). Dibagi 100 agar menjadi desimal (0.0942) sehingga
        # filter > 0.05 benar-benar berarti 5%.
        if div_yield is not None:
            div_yield = div_yield / 100.0
        
        # PERBAIKAN 2: yfinance selalu memberi debtToEquity dalam persen,
        # jadi selalu dibagi 100 agar menjadi rasio (tanpa kondisi tambahan).
        if der is not None:
            der = der / 100.0
            
        fundamentals.append({
            'Ticker': ticker,
            'ROE': roe,
            'DER': der,
            'Div_Yield': div_yield,
            'Market_Cap': market_cap
        })
    except Exception:
        fundamentals.append({
            'Ticker': ticker,
            'ROE': None, 'DER': None, 'Div_Yield': None, 'Market_Cap': None
        })
        
    # Progress indicator & sleep untuk menghindari rate limit Yahoo Finance
    if (i+1) % 50 == 0:
        print(f"Processed {i+1}/{len(valid_tickers)} tickers...")
    time.sleep(0.05)

df_fund = pd.DataFrame(fundamentals).set_index('Ticker')

# ==========================================
# 6. GABUNGKAN DATA & SCREENING (MODUL 1-4)
# ==========================================
df_all = pd.concat([df_fund, df_technical], axis=1)

# --- PERBAIKAN 4: SANITY CHECK DIVIDEND YIELD ---
div_valid = df_all['Div_Yield'].dropna()
print("\n=== SANITY CHECK DIVIDEND YIELD ===")
print(f"Jumlah ticker dengan Div_Yield tidak None: {len(div_valid)}")
if len(div_valid) > 0:
    print(f"Nilai maksimum Div_Yield (desimal): {div_valid.max():.4f}")
    print("5 ticker dengan Div_Yield tertinggi:")
    print(div_valid.sort_values(ascending=False).head(5))
    if div_valid.max() > 0.5:
        print("PERINGATAN: Div_Yield maksimum > 50%. Skala yield dari yfinance kemungkinan berubah lagi.")
print("===================================\n")

# --- MODUL 1: QUALITY ---
mask_q = (df_all['ROE'] > 0.15) & (df_all['DER'] < 1) & (df_all['Div_Yield'] > 0.05)
df_q = df_all[mask_q].copy()
df_q_out = pd.DataFrame({
    'Emiten': df_q.index,
    'ROE (%)': (df_q['ROE'] * 100).round(2),
    'DER': df_q['DER'].round(2),
    'Div Yield (%)': (df_q['Div_Yield'] * 100).round(2)
})

# --- MODUL 2: INSTITUTIONAL ---
mask_i = (df_all['Market_Cap'] > 10_000_000_000_000) & (df_all['Avg_Value_20d'] > 10_000_000_000)
df_i = df_all[mask_i].copy()
df_i_out = pd.DataFrame({
    'Emiten': df_i.index,
    'Market Cap (T IDR)': (df_i['Market_Cap'] / 1e12).round(2),
    'Avg Value 20d (M IDR)': (df_i['Avg_Value_20d'] / 1e9).round(1)
})

# --- MODUL 3: TREND ---
mask_t = (df_all['Price'] > df_all['MA200']) & (df_all['RS_Rank'] > 70)
df_t = df_all[mask_t].copy()
df_t_out = pd.DataFrame({
    'Emiten': df_t.index,
    'Price': df_t['Price'].round(2),
    'MA200': df_t['MA200'].round(2),
    'RS Rank': df_t['RS_Rank'].round(1)
})

# --- MODUL 4: MASTER FILTER ---
mask_m = mask_q & mask_i & mask_t
df_m = df_all[mask_m].copy()
df_m_out = pd.DataFrame({
    'Emiten': df_m.index,
    'ROE (%)': (df_m['ROE'] * 100).round(2),
    'DER': df_m['DER'].round(2),
    'Div Yield (%)': (df_m['Div_Yield'] * 100).round(2),
    'Market Cap (T IDR)': (df_m['Market_Cap'] / 1e12).round(2),
    'Avg Value 20d (M IDR)': (df_m['Avg_Value_20d'] / 1e9).round(1),
    'Price': df_m['Price'].round(2),
    'MA200': df_m['MA200'].round(2),
    'RS Rank': df_m['RS_Rank'].round(1)
})

# ==========================================
# 7. OUTPUT KE LAYAR & SIMPAN KE DRIVE
# ==========================================
print("\n" + "="*50)
print("HASIL SCREENING SAHAM IDX")
print("="*50)

print("\n🟢 1. Modul 1 - Quality (ROE > 15%, DER < 1, DY > 5%)")
print(f"Ditemukan {len(df_q_out)} emiten (ditampilkan maks. 10 terbaik: ROE tertinggi).")
display(df_q_out.sort_values('ROE (%)', ascending=False).head(10))
df_q_out.to_csv(f"{output_dir}/Module1_Quality.csv", index=False)

print("\n🔵 2. Modul 2 - Institutional (Market Cap > 10T, Avg Value > 10B)")
print(f"Ditemukan {len(df_i_out)} emiten (ditampilkan maks. 10 terbaik: Avg Value 20d tertinggi).")
display(df_i_out.sort_values('Avg Value 20d (M IDR)', ascending=False).head(10))
df_i_out.to_csv(f"{output_dir}/Module2_Institutional.csv", index=False)

print("\n🟡 3. Modul 3 - Trend (Price > MA200, RS Rank > 70)")
print(f"Ditemukan {len(df_t_out)} emiten (ditampilkan maks. 10 terbaik: RS Rank tertinggi).")
display(df_t_out.sort_values('RS Rank', ascending=False).head(10))
df_t_out.to_csv(f"{output_dir}/Module3_Trend.csv", index=False)

print("\n🔴 4. Modul 4 - Quality & Institutional & Trend")
print(f"Ditemukan {len(df_m_out)} emiten (ditampilkan maks. 10 terbaik: RS Rank tertinggi).")
display(df_m_out.sort_values('RS Rank', ascending=False).head(10))
df_m_out.to_csv(f"{output_dir}/Module4_Master_Filter.csv", index=False)

print("\n✅ SELESAI! Semua file CSV telah disimpan di Google Drive Anda:")
print(f"📂 {output_dir}")