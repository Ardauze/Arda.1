#ARDA ÜZE 1241602088
#Bu uygulama API ie döviz verisi çekebildiğiniz , güncel olarak döviz kurları ile dönüşüm işlemleri yapabilirsiniz

from tkinter import *
import json
import http.client


#Tk oluşturdum
pen = Tk()
pen.title("Arda'nın Döviz Uygulaması")
pen.configure(bg='darkblue')
pen.geometry("700x600")

#Menubar oluşturdum 
menubar = Menu(pen)
pen.config(menu=menubar)
dosya_menu = Menu(menubar)
dosya_menu.add_command(label='Çıkış', command=pen.destroy)
menubar.add_cascade(label='Dosya', menu=dosya_menu)

#API'den veri çektim
conn = http.client.HTTPSConnection("api.collectapi.com")
headers = {
    'content-type': "application/json",
    'authorization': "apikey 5VTbbYTokDjT6dbeIsWpW9:59EXxLk1owhtM0SU96QrQS"
}
conn.request("GET", "/economy/allCurrency", headers=headers)
res = conn.getresponse()
data = res.read()
json_data = json.loads(data.decode("utf-8"))

Label(pen, text="Arda'nın Güncel Döviz Kurları", bg='yellow', font=("Arial", 14, "bold")).pack(pady=10)

#Frame yaptım 
frame = Frame(pen)
frame.pack(expand=True, fill=BOTH, padx=10, pady=5)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 12), width=70)
listbox.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=listbox.yview)

dovizler = {} 

#Bu kısım için chat gpt üzerinden taslak çalışmaları dikkate alarak hazırladım
if json_data["success"]:
    for item in json_data["result"]:
        name = item["name"]
        buying = float(item["buying"])
        selling = float(item["selling"])
        listbox.insert(END, f"{name}: {buying:.2f} ₺ / {selling:.2f} ₺")
        dovizler[name] = (buying, selling)
else:
    listbox.insert(END, " #404# Not Found ")

#Dönüştürücü için yeni frame oluşturdum 
frame2 = Frame(pen, bg='grey', padx=10, pady=10)
frame2.pack(fill=BOTH, padx=10, pady=10)

Label(frame2, text="Döviz Dönüştürücü", font=("Arial", 13, "bold"), bg='grey').grid(row=0, column=0, columnspan=2, pady=5)

Label(frame2, text="Miktar:", bg='grey').grid(row=1, column=0, sticky=W)
entry2 = Entry(frame2)
entry2.grid(row=1, column=1, sticky=E)

Label(frame2, text="Yön (₺→Döviz / Döviz→₺):", bg='grey').grid(row=2, column=0, sticky=W)
direction_var = StringVar(value="TL→Döviz")
o_menu = OptionMenu(frame2, direction_var, "TL→Döviz", "Döviz→TL")
o_menu.grid(row=2, column=1, sticky=E)

s_label = Label(frame2, text="", bg='grey', font=("Arial", 11, "bold"))
s_label.grid(row=4, column=0, columnspan=2, pady=5)

#Çeviri için fonksiyon tanımladım
#def için yapay zekadan destek aldım temel fonksiyon için pdf'lerden destek alarak yazdım
#fonksyion tanımlamadaki eksiklerimi düzeltsin diye tekrardan chat gpt den destek aldım
def donustur():
    selected = listbox.curselection()
    if not selected:
        s_label.config(text="Lütfen listeden bir döviz seçin.")
        return

    name = listbox.get(selected[0]).split(":")[0]
    try:
        miktar = float(entry2.get())
    except ValueError:
        s_label.config(text="Geçerli bir tutar girin !")
        return

    buying, selling = dovizler[name]
    direction = direction_var.get()
    if direction == "TL→Döviz":
        result = miktar / selling
        s_label.config(text=f"{miktar:.2f} ₺ = {result:.2f} {name}")
    else:
        result = miktar * buying
        s_label.config(text=f"{miktar:.2f} {name} = {result:.2f} ₺")

Button(frame2, text="Dönüştür", command=donustur, bg='gray', fg='white').grid(row=3, column=0, columnspan=2, pady=10)


pen.mainloop()
