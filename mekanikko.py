import random
import time

# --- Konfiguraatio ---
TUNTIVELOITUS = 60  # €/h

CVT_HIHNA_UUSI_HINTA = 80
CVT_HIHNA_HALPA_HINTA = 40
JARRUPALAT_HINTA = 50
JARRUNESTE_HINTA = 15
AKKU_HINTA = 90
POLTTIMO_HINTA = 10
ÖLJY_HINTA = 25

VARAOSAT_SAATAVUUS = {
    "cvt_hihna_laadukas": True,
    "cvt_hihna_halpa": True,
    "jarrupalat": True,
    "jarruneste": True,
    "akku": False,
    "polttimo": True,
    "öljy": True,
}

MALLIT = [
    {"nimi": "Ligier JS50", "tyypilliset_vikat": ["cvt_kuluminen", "etuvalojen johdotus", "jarrupalat"]},
    {"nimi": "Aixam City", "tyypilliset_vikat": ["akku_heikko", "öljy_vuoto", "jarruneste"]},
    {"nimi": "Chatenet CH26", "tyypilliset_vikat": ["cvt_likainen", "jarrujen ilmaa", "valot_pimeänä"]},
]

class CVT:
    def __init__(self, malli_vika=False):
        self.kulumaprosentti = random.randint(10, 95)
        if malli_vika:
            self.kulumaprosentti = random.randint(50, 100)
        self.väärä_hihnamalli = random.choice([True, False, False])
        self.asennusvirhe = False
        self.likainen = random.choice([True, False])
        if malli_vika and random.random() < 0.5:
            self.likainen = True
        self.rullat_kuluneet = False

    def oireet(self):
        oireet = []
        if self.kulumaprosentti > 70:
            oireet.append("CVT vinkuu ja kiihtyy huonosti, kierrokset nousee mutta vauhti ei.")
        elif self.kulumaprosentti > 40:
            oireet.append("Kiihtyvyys on hieman laiska, mutta vielä siedettävä.")
        if self.väärä_hihnamalli:
            oireet.append("Välitykset tuntuvat oudoilta, kiihtyvyys epätasainen.")
        if self.likainen:
            oireet.append("Voimansiirrosta kuuluu rahinaa, CVT-kotelo on pölyinen ja likainen.")
        if self.asennusvirhe:
            oireet.append("CVT:ssä tuntuu nykimistä, asennus ei ole ihan kohdallaan.")
        if self.rullat_kuluneet:
            oireet.append("CVT:n rullat ovat kuluneet, välitykset eivät toimi tasaisesti.")
        return oireet

class Jarrut:
    def __init__(self, malli_vika=False):
        self.palat_kulumaprosentti = random.randint(0, 100)
        if malli_vika:
            self.palat_kulumaprosentti = random.randint(60, 100)
        self.neste_vahissa = random.choice([True, False])
        if malli_vika and random.random() < 0.5:
            self.neste_vahissa = True
        self.ilmaa_jarjestelmassa = random.choice([True, False]) if self.neste_vahissa else False

    def oireet(self):
        oireet = []
        if self.palat_kulumaprosentti > 80:
            oireet.append("Jarrut pitää kovaa ääntä ja jarrutusmatka on pitkä.")
        elif self.palat_kulumaprosentti > 50:
            oireet.append("Jarrut tuntuvat hieman heikoilta, mutta vielä toimivat.")
        if self.neste_vahissa:
            oireet.append("Jarrupoljin tuntuu pehmeältä, jarrut ei ota heti.")
        if self.ilmaa_jarjestelmassa:
            oireet.append("Jarrut tuntuvat 'pumppaavilta', poljin menee välillä pohjaan.")
        return oireet

class Sähkö:
    def __init__(self, malli_vika=False):
        self.etuvalot_pimeänä = random.choice([True, False])
        if malli_vika and random.random() < 0.5:
            self.etuvalot_pimeänä = True
        self.johdotus_huono = random.choice([True, False]) if self.etuvalot_pimeänä else False
        self.akku_heikko = random.choice([True, False])
        if malli_vika and random.random() < 0.5:
            self.akku_heikko = True

    def oireet(self):
        oireet = []
        if self.etuvalot_pimeänä:
            oireet.append("Etuvalot eivät toimi, välillä vilkkuvat kun töyssyyn ajetaan.")
        if self.johdotus_huono:
            oireet.append("Valojen johdotus näyttää huonolta, liittimet löysiä.")
        if self.akku_heikko:
            oireet.append("Käynnistys on tahmea, valot himmenee käynnistäessä.")
        return oireet

class Moottori:
    def __init__(self, malli_vika=False):
        self.öljy_vähissä = random.choice([True, False])
        self.öljy_likaista = random.choice([True, False])
        if malli_vika and random.random() < 0.5:
            self.öljy_vähissä = True
            self.öljy_likaista = True
        self.naputus = self.öljy_vähissä or self.öljy_likaista

    def oireet(self):
        oireet = []
        if self.öljy_vähissä:
            oireet.append("Öljyvalo vilkkuu välillä, varsinkin kiihdyttäessä.")
        if self.öljy_likaista:
            oireet.append("Moottorista kuuluu hieno naputus, erityisesti kylmänä.")
        return oireet

class Mopoauto:
    def __init__(self, id, historiadata=None):
        self.id = id
        self.malli = random.choice(MALLIT)
        self.maine_vaikutus = 0
        self.historiadata = historiadata or {}
        tyypilliset = self.malli["tyypilliset_vikat"]

        self.cvt = CVT(malli_vika=("cvt_kuluminen" in tyypilliset or "cvt_likainen" in tyypilliset))
        self.jarrut = Jarrut(malli_vika=("jarrupalat" in tyypilliset or "jarruneste" in tyypilliset or "jarrujen ilmaa" in tyypilliset))
        self.sahko = Sähkö(malli_vika=("etuvalojen johdotus" in tyypilliset or "valot_pimeänä" in tyypilliset or "akku_heikko" in tyypilliset))
        self.moottori = Moottori(malli_vika=("öljy_vuoto" in tyypilliset))

        if self.historiadata.get("huono_korjaus"):
            if random.random() < 0.5:
                self.sahko.johdotus_huono = True
            if random.random() < 0.5:
                self.cvt.asennusvirhe = True

    def kuvaus(self):
        oireet = []
        oireet.append(f"Malli: {self.malli['nimi']}")
        oireet.append("Asiakas kertoo oireet:")
        oireet += self.cvt.oireet()
        oireet += self.jarrut.oireet()
        oireet += self.sahko.oireet()
        oireet += self.moottori.oireet()
        if not any([self.cvt.oireet(), self.jarrut.oireet(), self.sahko.oireet(), self.moottori.oireet()]):
            oireet.append("Asiakas sanoo: 'En tiedä, tarkista vaan että kaikki on kunnossa.'")
        return "\n".join(oireet)

class KorjaamoPeli:
    def __init__(self):
        self.raha = 0
        self.asiakas_id = 1
        self.maine = 0
        self.asiakashistoria = {}
        self.tilastot = {
            "korjatut": 0,
            "huonot_korjaukset": 0,
            "mallit": {"Ligier JS50": 0, "Aixam City": 0, "Chatenet CH26": 0},
            "laskut": [],
        }

    def erikoiskeissi_ligier_cvt(self, mopoauto):
        print("\n=== ERIKOISKEISSI: Ligier JS50 – CVT-hihnan vaihto ===")
        print("Asiakas: 'Tää ei enää liiku kunnolla, kierrokset huutaa ja haisee palaneelle.'")
        print("Tämä on kiireellinen työ – asiakas odottaa korjaamon aulassa.")

        mopoauto.cvt.kulumaprosentti = random.randint(90, 100)
        mopoauto.cvt.likainen = True
        mopoauto.cvt.väärä_hihnamalli = False
        mopoauto.cvt.asennusvirhe = False
        mopoauto.cvt.rullat_kuluneet = True

        print("\nCVT-tila:")
        print("- Hihna täysin loppu")
        print("- Kotelo täynnä pölyä")
        print("- Rullat kuluneet")
        print("- Asiakas odottaa → nopeus vaikuttaa maineeseen")

        print("\nVaihtoehdot:")
        print("1) Vaihda hihna + puhdista kotelo + vaihda rullat (täydellinen korjaus)")
        print("2) Vaihda vain hihna (nopea, mutta riskialtis)")
        print("3) Puhdista kotelo ja säädä (halpa, mutta ei korjaa ongelmaa)")

        valinta = input("Valinta (1/2/3): ").strip()

        if valinta == "1":
            print("\nTeet täydellisen CVT-huollon.")
            print("Asiakas on erittäin tyytyväinen.")
            self.raha += 160
            self.maine += 3
            mopoauto.maine_vaikutus += 3

        elif valinta == "2":
            print("\nVaihdat vain hihnan.")
            print("Auto toimii hetken hyvin, mutta rullat aiheuttavat pian ongelmia.")
            print("Asiakas palaa myöhemmin valittamaan.")
            self.raha += 80
            self.maine -= 2
            mopoauto.maine_vaikutus -= 2
            self.asiakashistoria[mopoauto.id] = {"huono_korjaus": True}

        elif valinta == "3":
            print("\nPuhdistat kotelon ja säädät CVT:tä.")
            print("Ongelma ei ratkea. Asiakas on pettynyt.")
            self.raha += 20
            self.maine -= 3
            mopoauto.maine_vaikutus -= 3
            self.asiakashistoria[mopoauto.id] = {"huono_korjaus": True}

        else:
            print("Et tehnyt mitään. Asiakas lähtee vihaisena.")
            self.maine -= 5
            mopoauto.maine_vaikutus -= 5
            self.asiakashistoria[mopoauto.id] = {"huono_korjaus": True}

        print(f"\nRahatilanne: {self.raha} €, maine: {self.maine}")
        print("=== Erikoiskeissi päättyy ===\n")

    def aloita(self):
        print("=== Täysi mopoautokorjaamo tilastoilla ja erikoiskeissillä ===")
        print("Mallit: Ligier JS50, Aixam City, Chatenet CH26\n")

        while True:
            print("Päävalikko:")
            print("1) Seuraava asiakas")
            print("2) Näytä tilastot")
            print("3) Näytä maine ja rahatilanne")
            print("4) Lopeta")
            komento = input("Valinta (1-4): ").strip().lower()

            if komento == "4" or komento == "lopeta":
                print(f"\nPeli päättyi. Tienasit yhteensä {self.raha:.1f} €. Maine: {self.maine}.")
                break
            elif komento == "2":
                self.nayta_tilastot()
            elif komento == "3":
                print(f"\nMaine: {self.maine}, rahatilanne: {self.raha:.1f} €\n")
            elif komento == "1" or komento == "":
                historiadata = self.asiakashistoria.get(self.asiakas_id)
                mopoauto = Mopoauto(self.asiakas_id, historiadata)
                self.tilastot["mallit"][mopoauto.malli["nimi"]] += 1

                # Erikoiskeissi Ligierille
                if mopoauto.malli["nimi"] == "Ligier JS50" and random.random() < 0.20:
                    self.erikoiskeissi_ligier_cvt(mopoauto)

                self.kasittele_asiakas(mopoauto)
                self.asiakas_id += 1
            else:
                print("Virheellinen valinta.\n")

    def nayta_tilastot(self):
        print("\n=== Korjaamon tilastot ===")
        print(f"Korjattuja mopoautoja yhteensä: {self.tilastot['korjatut']}")
        print("Mallit:")
        for malli, määrä in self.tilastot["mallit"].items():
            print(f"- {malli}: {määrä} kpl")
        print(f"Huonoja korjauksia: {self.tilastot['huonot_korjaukset']}")

        if self.tilastot["laskut"]:
            keski = sum(self.tilastot["laskut"]) / len(self.tilastot["laskut"])
            print(f"Keskimääräinen lasku per asiakas: {keski:.1f} €")
        else:
            print("Ei vielä laskuja.")
        print("===\n")

    def kasittele_asiakas(self, mopoauto: Mopoauto):
        print(f"\n--- Asiakas #{mopoauto.id} saapui korjaamolle ---")
        if mopoauto.historiadata:
            print("Tämä asiakas on käynyt aiemmin. Hän muistaa edellisen työn.")
        time.sleep(0.5)
        print(mopoauto.kuvaus())

        lasku = 0
        tyotunnit = 0

        while True:
            print("\nAsiakasvalikko:")
            print("1) Diagnostiikka")
            print("2) Korjaustoimenpide")
            print("3) Luovuta mopoauto asiakkaalle")
            valinta = input("Valinta (1/2/3): ").strip()

            if valinta == "1":
                tunnit = self.diagnostiikka(mopoauto)
                tyotunnit += tunnit
                lasku += tunnit * TUNTIVELOITUS
            elif valinta == "2":
                tunnit, osat_hinta, maine_muutos, tilaus = self.korjaus(mopoauto)
                tyotunnit += tunnit
                lasku += tunnit * TUNTIVELOITUS + osat_hinta
                mopoauto.maine_vaikutus += maine_muutos
                self.maine += maine_muutos
                if tilaus:
                    self.asiakashistoria[mopoauto.id] = {"huono_korjaus": False, "tilattu_osa": tilaus}
            elif valinta == "3":
                self.luovutus(mopoauto, lasku, tyotunnit)
                break
            else:
                print("Virheellinen valinta.")

    def diagnostiikka(self, mopoauto: Mopoauto):
        print("\n=== Diagnostiikka ===")
        print("Valitse mitä tutkit (0.5–1 h):")
        print("1) CVT ja voimansiirto")
        print("2) Jarrut")
        print("3) Sähkö ja valot")
        print("4) Moottori ja öljy")

        valinta = input("Valinta (1/2/3/4): ").strip()
        tunnit = random.uniform(0.5, 1.0)

        if valinta == "1":
            cvt = mopoauto.cvt
            print("\nTutkit CVT:n kotelon, hihnan ja rullat:")
            print(f"- Hihnan kuluma: {cvt.kulumaprosentti} %")
            print(f"- Väärä hihnamalli: {'KYLLÄ' if cvt.väärä_hihnamalli else 'EI'}")
            print(f"- Likaisuus: {'Likainen' if cvt.likainen else 'Puhdas'}")
            print(f"- Asennusvirhe: {'KYLLÄ' if cvt.asennusvirhe else 'EI'}")
            print(f"- Rullat kuluneet: {'KYLLÄ' if cvt.rullat_kuluneet else 'EI'}")
        elif valinta == "2":
            j = mopoauto.jarrut
            print("\nTutkit jarrut:")
            print(f"- Jarrupalojen kuluma: {j.palat_kulumaprosentti} %")
            print(f"- Jarruneste vähissä: {'KYLLÄ' if j.neste_vahissa else 'EI'}")
            print(f"- Ilmaa järjestelmässä: {'KYLLÄ' if j.ilmaa_jarjestelmassa else 'EI'}")
        elif valinta == "3":
            s = mopoauto.sahko
            print("\nTutkit sähköt:")
            print(f"- Etuvalot pimeänä: {'KYLLÄ' if s.etuvalot_pimeänä else 'EI'}")
            print(f"- Johdotus huono: {'KYLLÄ' if s.johdotus_huono else 'EI'}")
            print(f"- Akun kunto: {'Heikko' if s.akku_heikko else 'OK'}")
        elif valinta == "4":
            m = mopoauto.moottori
            print("\nTutkit moottorin ja öljyn:")
            print(f"- Öljy vähissä: {'KYLLÄ' if m.öljy_vähissä else 'EI'}")
            print(f"- Öljy likaista: {'KYLLÄ' if m.öljy_likaista else 'EI'}")
            print(f"- Naputus: {'KYLLÄ' if m.naputus else 'EI'}")
        else:
            print("Virheellinen valinta diagnostiikassa.")
            tunnit = 0

        print(f"Diagnostiikka vei noin {tunnit:.1f} h.")
        return tunnit

    def korjaus(self, mopoauto: Mopoauto):
        print("\n=== Korjaustoimenpiteet ===")
        print("Valitse mitä teet:")
        print("1) Vaihda CVT-hihna")
        print("2) Puhdista CVT-kotelo")
        print("3) Vaihda jarrupalat")
        print("4) Lisää jarrunestettä ja ilmaus")
        print("5) Vaihda akku")
        print("6) Korjaa valot / johdotus")
        print("7) Vaihda öljyt")
        print("8) Pikahuolto")

        valinta = input("Valinta (1-8): ").strip()
        tunnit = 0
        osat_hinta = 0
        maine_muutos = 0
        tilattu_osa = None

        cvt = mopoauto.cvt
        j = mopoauto.jarrut
        s = mopoauto.sahko
        m = mopoauto.moottori

        if valinta == "1":
            print("\nValitse hihnamalli:")
            print("1) Laadukas, oikea hihna")
            print("2) Halpa yleismalli")
            h_valinta = input("Valinta (1/2): ").strip()
            tunnit = random.uniform(1.0, 1.5)

            if h_valinta == "1":
                if VARAOSAT_SAATAVUUS["cvt_hihna_laadukas"]:
                    osat_hinta += CVT_HIHNA_UUSI_HINTA
                    cvt.kulumaprosentti = random.randint(0, 10)
                    cvt.väärä_hihnamalli = False
                    cvt.asennusvirhe = random.choice([False, False, True])
                    print("Asennat laadukkaan hihnan. CVT toimii hyvin.")
                    maine_muutos += 2
                else:
                    print("Laadukas hihna ei ole hyllyssä, joudut tilaamaan sen.")
                    tilattu_osa = "cvt_hihna_laadukas"
                    maine_muutos -= 1
            elif h_valinta == "2":
                if VARAOSAT_SAATAVUUS["cvt_hihna_halpa"]:
                    osat_hinta += CVT_HIHNA_HALPA_HINTA
                    cvt.kulumaprosentti = random.randint(0, 30)
                    cvt.väärä_hihnamalli = random.choice([True, False])
                    cvt.asennusvirhe = random.choice([False, True])
                    print("Asennat halvan hihnan. Toimii, mutta ei ehkä täydellisesti.")
                    if cvt.väärä_hihnamalli or cvt.asennusvirhe:
                        maine_muutos -= 1
                else:
                    print("Halpaa hihnaa ei ole hyllyssä, joudut tilaamaan.")
                    tilattu_osa = "cvt_hihna_halpa"
                    maine_muutos -= 1
            else:
                print("Et valinnut hihnaa.")
                tunnit = 0

        elif valinta == "2":
            tunnit = random.uniform(0.5, 1.0)
            if cvt.likainen:
                cvt.likainen = False
                print("Puhdistat CVT-kotelon. Äänet vähenevät.")
                maine_muutos += 1
            else:
                print("CVT oli jo melko puhdas.")

        elif valinta == "3":
            tunnit = random.uniform(0.7, 1.2)
            if VARAOSAT_SAATAVUUS["jarrupalat"]:
                osat_hinta += JARRUPALAT_HINTA
                if j.palat_kulumaprosentti > 60:
                    j.palat_kulumaprosentti = random.randint(0, 10)
                    print("Vaihdat jarrupalat uusiin. Jarrutus paranee.")
                    maine_muutos += 2
                else:
                    print("Jarrupalat eivät olleet kovin kuluneet.")
                    maine_muutos -= 1
            else:
                print("Jarrupalat loppu varastosta, joudut tilaamaan.")
                tilattu_osa = "jarrupalat"
                maine_muutos -= 1

        elif valinta == "4":
            tunnit = random.uniform(0.8, 1.3)
            if VARAOSAT_SAATAVUUS["jarruneste"]:
                osat_hinta += JARRUNESTE_HINTA
                if j.neste_vahissa or j.ilmaa_jarjestelmassa:
                    j.neste_vahissa = False
                    j.ilmaa_jarjestelmassa = False
                    print("Lisäät jarrunestettä ja ilmaat järjestelmän.")
                    maine_muutos += 2
                else:
                    print("Jarruneste oli jo kunnossa.")
                    maine_muutos -= 1
            else:
                print("Jarrunestettä ei ole, joudut tilaamaan.")
                tilattu_osa = "jarruneste"
                maine_muutos -= 1

        elif valinta == "5":
            tunnit = random.uniform(0.5, 1.0)
            if VARAOSAT_SAATAVUUS["akku"]:
                osat_hinta += AKKU_HINTA
                if s.akku_heikko:
                    s.akku_heikko = False
                    print("Vaihdat akun uuteen. Käynnistys paranee.")
                    maine_muutos += 2
                else:
                    print("Akku oli kunnossa, vaihto turha.")
                    maine_muutos -= 2
            else:
                print("Akku ei ole hyllyssä, joudut tilaamaan.")
                tilattu_osa = "akku"
                maine_muutos -= 1

        elif valinta == "6":
            tunnit = random.uniform(0.4, 1.0)
            if VARAOSAT_SAATAVUUS["polttimo"]:
                osat_hinta += POLTTIMO_HINTA
                if s.etuvalot_pimeänä or s.johdotus_huono:
                    s.etuvalot_pimeänä = False
                    s.johdotus_huono = False
                    print("Korjaat johdotuksen ja vaihdat polttimot. Valot toimivat.")
                    maine_muutos += 2
                else:
                    print("Valot olivat jo kunnossa.")
                    maine_muutos -= 1
            else:
                print("Polttimoja ei ole, joudut tilaamaan.")
                tilattu_osa = "polttimo"
                maine_muutos -= 1

        elif valinta == "7":
            tunnit = random.uniform(0.7, 1.5)
            if VARAOSAT_SAATAVUUS["öljy"]:
                osat_hinta += ÖLJY_HINTA
                if m.öljy_vähissä or m.öljy_likaista:
                    m.öljy_vähissä = False
                    m.öljy_likaista = False
                    m.naputus = False
                    print("Vaihdat öljyt ja tarkistat vuodon. Moottori rauhoittuu.")
                    maine_muutos += 2
                else:
                    print("Öljy oli jo kunnossa.")
            else:
                print("Öljyä ei ole, joudut tilaamaan.")
                tilattu_osa = "öljy"
                maine_muutos -= 1

        elif valinta == "8":
            tunnit = random.uniform(0.3, 0.6)
            print("Teet pikahuollon: tarkistat perusasiat.")
            if random.random() < 0.3:
                print("Löydät pienen piilevän vian ja korjaat sen.")
                maine_muutos += 1
            else:
                print("Et löydä mitään erityistä.")
        else:
            print("Virheellinen valinta.")
            tunnit = 0

        print(f"\nTyöaika: {tunnit:.1f} h, osat: {osat_hinta} €, maine-muutos: {maine_muutos}")
        return tunnit, osat_hinta, maine_muutos, tilattu_osa

    def luovutus(self, mopoauto: Mopoauto, lasku: float, tyotunnit: float):
        print("\n=== Luovutus asiakkaalle ===")
        jäljellä_oireita = []
        jäljellä_oireita += mopoauto.cvt.oireet()
        jäljellä_oireita += mopoauto.jarrut.oireet()
        jäljellä_oireita += mopoauto.sahko.oireet()
        jäljellä_oireita += mopoauto.moottori.oireet()

        if mopoauto.maine_vaikutus > 1 and len(jäljellä_oireita) <= 3:
            tyytyvaisyys = "erittäin tyytyväinen"
            bonus = 20
            huono_korjaus = False
        elif mopoauto.maine_vaikutus >= 0 and len(jäljellä_oireita) <= 6:
            tyytyvaisyys = "melko tyytyväinen"
            bonus = 5
            huono_korjaus = False
        else:
            tyytyvaisyys = "epäilevä ja hieman tyytymätön"
            bonus = -10
            huono_korjaus = True

        maksu = max(0, lasku + bonus)
        self.raha += maksu
        self.tilastot["korjatut"] += 1
        self.tilastot["laskut"].append(maksu)
        if huono_korjaus:
            self.tilastot["huonot_korjaukset"] += 1

        self.asiakashistoria[mopoauto.id] = {"huono_korjaus": huono_korjaus}

        print(f"Asiakas on {tyytyvaisyys}.")
        print(f"Lasku: työt {tyotunnit:.1f} h x {TUNTIVELOITUS} €/h + osat ≈ {lasku:.1f} €")
        print(f"Asiakas maksaa lopulta: {maksu:.1f} €")
        print(f"Korjaamon rahatilanne: {self.raha:.1f} €, maine: {self.maine}")
        print("--- Asiakas poistuu korjaamolta ---\n")


if __name__ == "__main__":
    peli = KorjaamoPeli()
    peli.aloita()
