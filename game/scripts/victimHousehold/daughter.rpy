label adaMain:
    $ adaNote.isActive = True
    if lastSpokenWith == "":
        $ lisbeth.say("Nejsem si jistá, jestli bude zrovna ona něco vědět… ale jak chcete. Pojďte dál a já vám ji zavolám.")
        call victimHouseInterior
    else:
        $ lisbeth.say("Nejsem si jistá, jestli bude zrovna ona něco vědět… ale jak chcete. Dojdu pro ni.")
    $ ada.say("S čím vám můžu pomoct?")

    $ lastSpokenWith = "ada"
    $ origAsked = ada.asked.copy()
    call adaIntro
    call adaOptions
    $ time.addMinutes((len(ada.asked) - len(origAsked)) * 3)
    jump victimHouseholdConversationEnded
    return

label adaIntro:
    if ("zairis dealt with" in status and "ada confrontation zairis" not in status) or ("kaspar and lisbeth ratted out" in status and "ada confrontation lisbeth" not in status):
        "Paní Lisbeth přivede zamračenou Adu a nechá vám soukromí."
        "Jakmile je její matka mimo doslech a než se stihneš začít ptát, Ada na tebe vyštěkne vlastní otázku."
        $ ada.say("To musíš kvůli zatraceným botám strkat nos do cizích vztahů? Co jsi přesně tátovi řekl, že tak vyletěl?", "angry")
        show mcPic at menuImage
        menu:
            "Co jsem mu měl říct?" if gender == "M":
                hide mcPic
                $ ada.say("Neměl jsi mu říkat nic, co není o těch jeho hloupých botách.", "angry")
                if "zairis dealt with" in status and "ada confrontation zairis" not in status:
                    $ ada.say("Co jste ti se Zairisem udělali?", "angry")
                else:
                    $ ada.say("Co ti máma udělala?", "angry")
            "Co jsem mu měla říct?" if gender == "F":
                hide mcPic
                $ ada.say("Neměla jsi mu říkat nic, co není o těch jeho hloupých botách.", "angry")
                if "zairis dealt with" in status:
                    $ ada.say("Co jste ti se Zairisem udělali?", "angry")
                else:
                    $ ada.say("Co ti máma udělala?", "angry")
            "...o mistru Kasparovi?" if "kaspar and lisbeth ratted out" in status:
                hide mcPic
                if "zairis dealt with" in status and "ada confrontation zairis" not in status and "kaspar and lisbeth ratted out" in status and "ada confrontation lisbeth" not in status:
                    $ ada.asked.append("lisbeth first")
                elif "ada confrontation lisbeth" in status:
                    $ ada.say("To taky, ale myslím ještě potom. O Zairisovi!", "angry")
                    $ ada.say("To se snažíš zničit život co nejvíc lidem, nebo co?", "angry")
                else:
                    $ ada.say("Chudák máma!", "angry")
            "...o Zairisovi?":
                hide mcPic
                if "zairis dealt with" in status and "ada confrontation zairis" not in status and "kaspar and lisbeth ratted out" in status and "ada confrontation lisbeth" not in status:
                    $ ada.asked.append("zairis first")
                elif "ada confrontation zairis" in status:
                    $ ada.say("To taky, ale myslím ještě potom. O mámě!", "angry")
                    $ ada.say("To se snažíš zničit život co nejvíc lidem, nebo co?", "angry")
                else:
                    if gender == "M":
                        $ ada.say("Proč jsi do toho musel šťourat?", "angry")
                    else:
                        $ ada.say("Proč jsi do toho musela šťourat?", "angry")
            "...o Rumelinovi?" if "rumelin exposed" in victim.asked:
                hide mcPic
                if "zairis dealt with" in status:
                    $ ada.say("Ten mě vůbec nezajímá. O Zairisovi!", "angry")
                else:
                    $ ada.say("Ten mě vůbec nezajímá. O mámě!", "angry")

        if "zairis dealt with" in status and "ada confrontation zairis" not in status and "kaspar and lisbeth ratted out" in status and "ada confrontation lisbeth" not in status:
            if "lisbeth first" in ada.asked:
                call adaConfrontationLisbeth
                $ ada.say("A pak ještě Zairis... To se snažíš zničit život co nejvíc lidem, nebo co?", "angry")
                call adaConfrontationZairis
            else:
                call adaConfrontationZairis
                $ ada.say("A pak ještě máma... To se snažíš zničit život co nejvíc lidem, nebo co?", "angry")
                call adaConfrontationLisbeth
        elif "zairis dealt with" in status and "ada confrontation zairis" not in status:
            call adaConfrontationZairis
        else:
            call adaConfrontationLisbeth

        $ ada.say("Ale to je tobě asi jedno. Jsi jako otec.", "angry")
    else:
        "Paní Lisbeth přivede asi čtrnáctiletou dívku se zvědavým výrazem."
    return

label adaConfrontationLisbeth:
    $ ada.say("Každému kromě tebe a mého otce přece musí být jasné, že by nikdy neudělala nic špatného. Nic proti Olwenovi, proti tomu, co se považuje za slušné, nic proti chlapovi, kterého asi pořád ještě miluje!", "angry")
    $ status.append("ada confrontation lisbeth")
    show mcPic at menuImage
    menu:
        "Omlouvám se, nedošlo mi, jak to vezme.":
            hide mcPic
            if gender == "M":
                $ ada.say("A to sis nevšiml, jak vždycky vyletí, když se mu něco nelíbí?", "angry")
            else:
                $ ada.say("A to sis nevšimla, jak vždycky vyletí, když se mu něco nelíbí?", "angry")
        "Kaspar byl v jeho dílně, to jsem přece říct musel." if gender == "M":
            hide mcPic
            $ ada.say("A už jsi ho zatknul? Jestli ne, tak to asi tak důležité nebylo.", "angry")
        "Kaspar byl v jeho dílně, to jsem přece říct musela." if gender == "F":
            hide mcPic
            $ ada.say("A už jsi ho zatkla? Jestli ne, tak to asi tak důležité nebylo.", "angry")
        "Má přece právo vědět, s kým se jeho žena baví.":
            hide mcPic
            $ mc.say("Zvlášť, když to jako nevěra opravdu vypadá.")
            $ ada.trust -= 2
            $ ada.say("A ty zase vypadáš jako osel. Půjdeš mu to taky hned říct?", "angry")
    return

label adaConfrontationZairis:
    $ ada.say("Táta si to s ním šel vyřídit, prý vtrhl do jeho domu jako velká voda, potom se do toho vložil Rovien... to jsou všichni v hlídce tak pitomí? Nebo vám prostě jenom nezáleží, co se komu stane?", "angry")
    $ status.append("ada confrontation lisbeth")
    show mcPic at menuImage
    menu:
        "Omlouvám se, nedošlo mi, co tvůj otec udělá.":
            hide mcPic
            if gender == "M":
                $ ada.say("A to sis nevšiml, jak vždycky vyletí, když se mu něco nelíbí?", "angry")
            else:
                $ ada.say("A to sis nevšimla, jak vždycky vyletí, když se mu něco nelíbí?", "angry")
        "Je to tvůj otec, má právo vědět, s kým se stýkáš":
            hide mcPic
            $ ada.trust -= 2
            if gender == "M":
                $ ada.say("A to sis nevšiml, jak vždycky vyletí, když se mu něco nelíbí?", "angry")
            else:
                $ ada.say("A to sis nevšimla, jak vždycky vyletí, když se mu něco nelíbí?", "angry")
        "Chtěl jsem očistit Zerana, aby mohl dokončit učení." if gender == "M":
            hide mcPic
            $ ada.say("A to nešlo nějak jinak?", "angry")
        "Chtěla jsem očistit Zerana, aby mohl dokončit učení." if gender == "F":
            hide mcPic
            $ ada.say("A to nešlo nějak jinak?", "angry")
    $ ada.say("Teď ani jeden z nás nesmí na krok z domu a kdo ví, co s ním jeho rodiče ještě provedou.", "sad")
    return

label adaOptions:
    call adaOptionsRemainingCheck
    if adaOptionsRemaining == 0:
        $ mc.say("To je všechno, můžeš zase jít.")
        "Dívka pokrčí rameny a odejde."
        return

    show mcPic at menuImage
    menu:
        "Všimla sis včera večer něčeho nebo někoho podezřelého?" if "anything suspicious" not in ada.asked:
            hide mcPic
            $ ada.asked.append("anything suspicious")
            "Dívka zavrtí hlavou."
            $ ada.say("Ne, tady se nikdy nic neděje.")
            $ mc.say("Zkus se zamyslet, každý detail může být důležitý.")
            "Dívka se kousne do rtu, ale pak opět jen zavrtí hlavou."
        "Byl někdo po odchodu mistra Heinricha v jeho dílně?" if "workshop empty" not in ada.asked:
            hide mcPic
            $ ada.asked.append("workshop empty")
            "Dívka na moment zaváhá a pak zavrtí hlavou."
            $ ada.say("Ne. Totiž… nedívala jsem se tam, ale myslím, že ne.")
            if liese.alreadyMet == True:
                $ mc.say("Ale prý se tam potom ještě dlouho svítilo.")
                $ ada.say("Možná… tam kluci ještě uklízeli?")
                $ ada.say("Táta je náročný, tak jim to občas trvá.")
        "Pije tvůj otec často ještě po příchodu domů?" if "anything suspicious" in lisbeth.asked and "drunkard" not in ada.asked:
            hide mcPic
            $ ada.asked.append("drunkard")
            $ ada.say("Občas, většinou i s přáteli, když je z hospody vyhodí a oni ještě nemají dost. Většinou po nich potom musím ráno uklízet.")
            $ mc.say("Včera také? Tvá matka říkala něco o ztracených lahvích.")
            $ ada.say("Dnes ráno jsem si žádných lahví nevšimla. A táta po sobě neuklízí nikdy.")
            $ ada.say("Prý to je ženská práce.", "angry")
        "Tušíš, jaký vztah mají tví rodiče?" if lotte.alreadyMet == True and "parents relationship" not in ada.asked:
            hide mcPic
            $ ada.asked.append("parents relationship")
            $ ada.say("Táta si myslí, že když občas mámě koupí drahý šperk, spraví se tím to všechno ostatní. Vůbec nechápe, že žena občas potřebuje třeba báseň, nebo něco jiného od srdce.")
            "Dívka se mírně začervená."
        "To je ze zkušenosti?" if "parents relationship" in ada.asked and "experience" not in ada.asked:
            hide mcPic
            $ ada.asked.append("experience")
            "Dívka zaváhá a rozhlédne se kolem sebe, jestli jste opravdu sami."
            $ ada.say("Možná trochu…", "blushing")
        "A kdo je ten šťastlivec?" if "experience" in ada.asked and "boyfriend" not in ada.asked:
            hide mcPic
            $ ada.asked.append("boyfriend")
            $ ada.say("To vám tak budu říkat. Řeknete to tátovi a budou z toho problémy.")
        "Je možné, že by tvoje matka měla milence?" if lotte.alreadyMet == True and "secret lover" not in ada.asked:
            hide mcPic
            $ ada.asked.append("secret lover")
            "Dívka zavrtí hlavou."
            $ ada.say("Máma? To fakt ne. Ta je na podobné věci moc nudná. A až moc miluje pořádek.")
        "Je někdo, s kým si tvoje matka rozumí?" if lotte.alreadyMet == True and "lisbeth friends" not in ada.asked:
            hide mcPic
            $ ada.asked.append("lisbeth friends")
            $ ada.say("S většinou ženských z ulice a manželek lidí z cechu. Vyměňují si recepty a tak.")
            $ mc.say("A je někdo, s kým si je blíž než s ostatními? A třeba spolu mluví i o osobních věcech?")
            "Dívka se zamyslí."
            $ ada.say("Možná mistr Kaspar? Baví se spolu dost a půjčují si knížky. Zrovna včera jsem šla pro jednu, kterou máma chtěla vrátit.")
            $ ada.say("Olwenova cesta - sbírka mravoučných příběhů. Nuda na nudu, ale co čekat od mámy.")
            if "night meeting" in lisbeth.asked:
                if gender == "M":
                    $ mc.say("Já myslel, že tu vrátil mistr Kaspar sám, někdy včera pozdě večer.")
                else:
                    $ mc.say("Já myslela, že tu vrátil mistr Kaspar sám, někdy včera pozdě večer.")
                "Ada zavrtí hlavou."
                $ ada.say("Ne, já ji mámě přinesla. Zkusila jsem i nakouknout dovnitř, ale bylo to opravdu tak hrozné, jak to zní.")
                $ ada.say("Kdo to říkal?")
                $ mc.say("Tvoje matka, prý se tady s ní mistr Kaspar stavil.")
                $ ada.say("Aha. Tak… se možná spletla? A on přinesl něco jiného?")
                $ ada.say("Názvy těhle věcí zní všechny stejně...")
                $ ada.say("Nebo jsem se spletla já? Už vlastně nevím.")
                $ lisbeth.cluesAgainst += 1
        "Jak dobře ses znala se Zeranem?" if "Zeran offense" in clues and "Zeran" not in ada.asked:
            hide mcPic
            $ ada.asked.append("Zeran")
            $ ada.say("Tak… normálně. Přes dva roky jsme spolu bydleli, jasně, že jsme se občas bavili. Vyprávěl mi elfí legendy a tak.")
            $ ada.say("Ale nic mezi námi nebylo.")
            $ clues.append("Zeran innocent")
            show mcPic at menuImage
            menu:
                "Prý vás spolu viděli a někdo ti posílal dopisy...":
                    hide mcPic
                    $ ada.trust -= 1
                    $ ada.say("Ale to nebyl...")
                    "Dívka se zamračí a pokrčí rameny."
                    $ ada.say("Stejně mi tady nikdo nevěří.", "angry")
                "Já ti věřím.":
                    hide mcPic
                    $ ada.trust += 1
                    $ ada.say("Vážně? Tak to jste první.")
        "Takže ti ty dopisy posílal někdo jiný?" if "Zeran" in ada.asked and "love letters" not in ada.asked:
            hide mcPic
            $ ada.asked.append("love letters")
            "Dívka se zarazí těsně před tím, než stihne odpovědět."
            $ ada.say("Proč bych vám vlastně měla něco říkat? Stejně mi tady nikdo nevěří.", "angry")
            show mcPic at menuImage
            menu:
                "Protože by to mohlo pomoct Zeranovi.":
                    hide mcPic
                    $ ada.say("To jsem zkoušela. A nijak to nepomohlo, ať jsem říkala cokoliv. Táta si radši myslel, že to chci hodit na někoho jiného, než aby změnil názor.", "angry")
                "Protože na pravdě záleží.":
                    hide mcPic
                    "Ada pokrčí rameny s výrazem, který nevypadá ani trochu přesvědčeně."
                    $ ada.say("Možná vám, ale v tomhle domě nikomu. Když jsem zkusila říct pravdu tátovi, tak to všechno jenom zhoršilo.", "sad")
            $ mc.say("Jestli mi řekneš, kdo...")
            $ ada.say("Tak to řeknete tátovi a on jenom zase vypění. Znova to vážně zkoušet nebudu.", "angry")
        "Můžeš mi aspoň říct, o čem jste si psali?" if "love letters" in ada.asked and "letters topic" not in ada.asked:
            hide mcPic
            $ ada.asked.append("letters topic")
            "Ada se na chvíli zamyslí, ale pak pokrčí rameny."
            $ ada.say("To asi můžu, to táta stejně ví. Ale k ničemu vám to nebude.")
            $ ada.say("Psal mi básně, opravdu krásné. A vyprávěl o zajímavých místech, která navštívil. Jednou dokonce viděl Amadisův hrob, to jsem trochu záviděla.", "blushing")
            $ ada.say("Doma se o historii nikdo nezajímá a rytířským ideálům by se jenom vysmáli. I máma čte jenom nudné mravoučné hlouposti, pro tátu je hrdina jenom ten, kdo vyrobí lepší botu, a kluci nic neberou vážně.", "angry")
            $ ada.say("Nikdo z nich Amadisův život nemůže pochopit.")
        "A proč se tvůj tajný ctitel nepřihlásil sám, když tolik obdivuje Amadise?" if "letters topic" in ada.asked and "lover conscience" not in ada.asked:
            hide mcPic
            $ ada.asked.append("lover conscience")
            $ ada.say("Říkal, že i Amadis musel čekat, než Gisellin otec konečně souhlasil s jejich svatbou. A přijít moc brzo by tátu opravdu jenom rozzuřilo.")
            $ mc.say("Ale Amadis by určitě nenechal za svoje rozhodnutí platit někoho jiného.")
            if ada.trust > 0 and "flowers achievement" in status:
                "Ada se zamračí."
                $ ada.say("To je pravda. A jemu by možná i táta věřil víc než mně...", "angry")
                $ ada.say("Asi se ho na to dojdu zeptat.", "angry")
                $ status.append("Ada confronts Zairis")
                $ zairis.imageParameter = beaten
            else:
                $ ada.say("Jediný, kdo tady o něčem rozhodoval, byl táta. A neposlouchal vůbec nikoho.", "angry")
        "Myslíš, že by Zeran ukradl střevíce tvého otce?" if "Zeran offense" in clues and "Zeran thief" not in ada.asked:
            hide mcPic
            $ ada.asked.append("Zeran thief")
            $ ada.say("To si nemyslím. Komu by to pomohlo?")
            $ mc.say("Mohl by se chtít pomstít tvému otci, za vyhazov a zkaženou pověst.")
            "Dívka se zamyslí."
            $ ada.say("Nevím. Možná, ale musel by se za ten měsíc hodně změnit.")
        "Prý si byl Zairis promluvit s tvým otcem." if "zairis confessed" in status:
            hide mcPic
            show mcPic at menuImage
            menu:
                "Doufám, že to Zeranovi umožní pokračovat v učení.":
                    hide mcPic
                    $ ada.say("To by si zasloužil. Když už mě teď táta drží v domácím vězení a nevypadá, že by chtěl rychle vychladnout jako vždycky, tak ať to aspoň Zeranovi pomůže. Ale podle mě ho táta zpátky nevezme.", "sad")
                    $ mc.say("Proč? Má teď přece důkaz, že v tom byl nevinně.")
                    $ ada.say("To by se potom musel každý den dívat na připomínku toho, že udělal chybu, a to on nesnese. On musí mít vždycky pravdu, bez ohledu na zbytek světa.", "angry")
                    $ ada.say("A i kdyby ho někdo přinutil, odnesl by to nejvíc zase Zeran.", "sad")
                    $ ada.say("Asi by mu ale mohl vrátit peníze za učení. Pak by Zeran mohl dokončit učení u nějakého jiného mistra. To by mu pomohlo dost.")
                    $ ada.say("“A pak odejde na tovaryšské putování a na jeho konci se nejspíš usadí někde daleko odtud.", "sad")
                "Doufám, že se mu nic nestalo.":
                    hide mcPic
                    $ ada.trust += 1
                    $ ada.say("Táta je hulvát a surovec a pokusil se ho zmlátit. Na ulici před domem, před všemi sousedy. Naštěstí ho zastavili dřív, než Zairisovi stihl opravdu ublížit, ale stejně.", "angry")
        "To je všechno, můžeš zase jít.":
            hide mcPic
            "Dívka pokrčí rameny a odejde."
            return
    jump adaOptions

###

label adaOptionsRemainingCheck:
    $ adaOptionsRemaining = 0
    if "anything suspicious" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "workshop empty" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "anything suspicious" in lisbeth.asked and "drunkard" not in ada.asked:
        $ adaOptionsRemaining += 1
    if lotte.alreadyMet == True and "parents relationship" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "parents relationship" in ada.asked and "experience" not in ada.asked:
        $ adaOptionsRemaining += 1
    if lotte.alreadyMet == True and "secret lover" not in ada.asked:
        $ adaOptionsRemaining += 1
    if lotte.alreadyMet == True and "lisbeth friends" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "Zeran offense" in clues and "Zeran" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "Zeran" in ada.asked and "love letters" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "Zeran offense" in clues and "Zeran thief" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "love letters" in ada.asked and "letters topic" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "letters topic" in ada.asked and "lover conscience" not in ada.asked:
        $ adaOptionsRemaining += 1
    if "zairis confessed" in status:
        $ adaOptionsRemaining += 1
    return
