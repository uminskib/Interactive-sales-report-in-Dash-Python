import pandas as pd 
import os
import glob

#Importowanie danych i ich łączenie
l = [pd.read_csv(filename,encoding="utf-16",sep="\t") for filename in glob.glob(os.getcwd()+"\\Dane_do_raportow\\*.txt")]
dane = pd.concat(l, axis=0,ignore_index=True)
dane=dane.sort_values(by="Tydzien").reset_index(drop=True)

#Przygotowanie danych według marki do raportu
new=dane["Wojewodztwo-Miasto"].str.split(pat="-",n=1,expand=True)
dane["Wojewodztwo"]=new[0]
dane["Miasto"]=new[1] 
dane.drop(columns =["Wojewodztwo-Miasto"], inplace = True)
dane.to_csv(os.getcwd()+"\\Dane_do_strony\\dane_wszystko.csv")
brand_podsumowanie=dane.groupby(["Brand"])
brand_podsumowanie=brand_podsumowanie.agg({"Sprzedaz":"sum"})
brand_podsumowanie.to_csv(os.getcwd()+"\\Dane_do_strony\\brand_podsumowanie.csv")

#Przygotowanie danych w podziale na Produkt
produkt_podsumowanie=dane.groupby(["Produkt"]).agg({"Sprzedaz":"mean"})
produkt_podsumowanie=produkt_podsumowanie.round(2)
produkt_podsumowanie=produkt_podsumowanie.reset_index()
produkt_podsumowanie.to_csv(os.getcwd()+"\\Dane_do_strony\\produkt_podsumowanie.csv",index=False)

#Podział na wojewodztwa
woj_sprzedaz=dane.groupby(["Wojewodztwo"]).agg({"Sprzedaz":"sum"})
woj_sprzedaz=woj_sprzedaz.reset_index()
woj = pd.DataFrame({"Wojewodztwo":['Kujawsko-Pomorskie','Warminsko-Mazurskie'], 
                    "Sprzedaz":[0,0]}) 
woj_sprzedaz=woj_sprzedaz.append(woj,ignore_index=True)
woj_sprzedaz.to_csv(os.getcwd()+"\\Dane_do_strony\\woj_sprzedaz.csv",index=False)