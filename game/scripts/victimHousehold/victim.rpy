label victimMain:
    if lastSpokenWith == "":
        $ lisbeth.say("Dojdu pro něj, pojďte zatím dál.")
        call victimHouseInterior
    else:
        $ lisbeth.say("Dojdu pro něj.")

    $ lastSpokenWith = "victim"
    call victimIntro

    label victimQuestions:
    $ origAsked = victim.asked.copy()
    call victimOptions

    label victimEnd:
    $ time.addMinutes((len(victim.asked) - len(origAsked)) * 3)
    if leaveOption == "none":
        $ leaveOption = "normal"
    else:
        jump victimHouseholdConversationEnded
    return


label victimIntro:
    "Mistr Heinrich vejde do místnosti s výrazem jako by se napil kyselého piva."

    if "firefighter" in status and "firefighter" not in victim.asked:
        $ victim.asked.append("firefighter")
        "Když tě ale uvidí, jeho výraz se trochu projasní."
        if gender == "M":
            $ victim.say("Včera jsi kolem toho ohně udělal spoustu dobré práce. Kdyby byla hlídka vždycky takhle užitečná, možná bychom si tu na ni zvykli.", "happy")
            $ victim.say("Ale nepřišel jsi, abych ti mazal med kolem huby.")
        else:
            $ victim.say("Včera jsi kolem toho ohně udělala spoustu dobré práce. Kdyby byla hlídka vždycky takhle užitečná, možná bychom si tu na ni zvykli.", "happy")
            $ victim.say("Ale nepřišla jsi, abych ti mazal med kolem huby.")
        show mcPic at menuImage
        menu:
            "Ve skutečnosti bych si s vámi o tom ohni rád promluvil." if gender == "M":
                hide mcPic
                $ victim.asked.append("fireshow")
                $ victim.say("No dobře, o co jde?")
                call heinrichFireshow
            "Ve skutečnosti bych si s vámi o tom ohni ráda promluvila." if gender == "F":
                hide mcPic
                $ victim.asked.append("fireshow")
                $ victim.say("No dobře, o co jde?")
                call heinrichFireshow
            "Ve skutečnosti jsem se vám přišel omluvit, pokud jsem vás nějak urazil." if "victim expects apology" in status and gender == "M":
                hide mcPic
                $ victim.trust += 1
                $ victim.say("No co si budeme povídat, choval ses jako hulvát. Ale po včerejšku ti jsem ochotný dát ještě šanci.")
                call afterApologyReactionPositive
            "Ve skutečnosti jsem se vám přišla omluvit, pokud jsem vás nějak urazila." if "victim expects apology" in status and gender == "F":
                hide mcPic
                $ victim.trust += 1
                $ victim.say("No co si budeme povídat, chovala ses jako hulvát. Ale po včerejšku ti jsem ochotný dát ještě šanci.")
                call afterApologyReactionPositive
            "To je pravda. Můžu vám ještě položit pár otázek?":
                hide mcPic
                $ victim.say("Bez toho to asi vyšetřit nemůžeš, tak do toho.")
        if "victim expects apology" in status:
            $ status.remove("victim expects apology")
    else:
        if "burned evidence seen" in victim.asked:
            $ victim.say("Už víš, kdo se opovážil hodit moje dílo do mého vlastního krbu?")
        else:
            $ victim.say("Neseš mi zpátky můj ztracený výrobek?")
        if "carrying key" in status:
            $ mc.say("Zatím ne, ale nesu vám od Eckharda zpět klíč od vaší dílny.")
            call returningKey
        elif "victim expects apology" in status:
            $ status.remove("victim expects apology")
            if gender == "M":
                $ mc.say("Zatím ne, ale dělám vše pro to, abych ho našel.")
                show mcPic at menuImage
                menu:
                    "Jdu se vám omluvit, pokud jsem vás nějak urazil.":
                        hide mcPic
                        $ victim.trust += 1
                        if "burned evidence seen" in victim.asked:
                            $ victim.say("No co si budeme povídat, choval ses jako hulvát. Chci jenom základní respekt a aby sis hleděl své práce. Tak hlavně najdi toho zatraceného vandala.")
                        else:
                            $ victim.say("No co si budeme povídat, choval ses jako hulvát. Chci jenom základní respekt a aby sis hleděl své práce. Tak hlavně najdi můj mistrovský výrobek.")
                        show mcPic at menuImage
                        call afterApologyReaction
                    "Můžu vám ještě položit pár otázek?":
                        hide mcPic
                        if victim.trust > -2:
                            $ victim.say("Když to musí být... tak se ptej.")
                        else:
                            $ victim.say("Mám sto chutí tě rovnou vyhodit... ale ptej se.", "angry")
            else:
                $ mc.say("Zatím ne, ale dělám vše pro to, abych ho našla.")
                show mcPic at menuImage
                menu:
                    "Jdu se vám omluvit, pokud jsem vás nějak urazila.":
                        hide mcPic
                        $ victim.trust += 1
                        if "burned evidence seen" in victim.asked:
                            $ victim.say("No co si budeme povídat, chovala ses jako hulvát. Chci jenom základní respekt a aby sis hleděla své práce. Tak hlavně najdi toho zatraceného vandala.", "angry")
                        else:
                            $ victim.say("No co si budeme povídat, chovala ses jako hulvát.  Chci jenom základní respekt a aby sis hleděla své práce. Tak hlavně najdi můj mistrovský výrobek.", "angry")
                        call afterApologyReaction
                    "Můžu vám ještě položit pár otázek?":
                        hide mcPic
                        if victim.trust > -2:
                            $ victim.say("Když to musí být... tak se ptej.")
                        else:
                            $ victim.say("Mám sto chutí tě rovnou vyhodit... ale ptej se.", "angry")
        else:
            if gender == "M":
                $ mc.say("Zatím ne, ale dělám vše pro to, abych ho našel. Můžu vám ještě položit pár otázek?")
            else:
                $ mc.say("Zatím ne, ale dělám vše pro to, abych ho našla. Můžu vám ještě položit pár otázek?")


        if "retrieving workshop key" in status:
            $ victim.say("A co ten klíč, který jsi slíbil donést?")
            if gender == "M":
                $ mc.say("Ještě jsem se pro něj nedostal…")
            else:
                $ mc.say("Ještě jsem se pro něj nedostala…")
            if time.isBefore(keyVeryLateAfter):
                if gender == "M":
                    $ victim.say("A to si myslíš, že můžu nechat svou dílnu odemčenou celý den, nebo co? Kdybys to nesliboval, mohl jsem si za Eckhardem dojít sám.", "angry")
                else:
                    $ victim.say("A to si myslíš, že můžu nechat svou dílnu odemčenou celý den, nebo co? Kdybys to neslibovala, mohl jsem si za Eckhardem dojít sám.", "angry")
                $ victim.trust -= 1
            else:
                $ victim.say("Tak už se neobtěžuj. Už jsem si za Eckhardem došel sám a vyzvedl si ho osobně.", "angry")
                $ victim.say("To si myslíš, že když se ztratil můj mistrovský výrobek, můžu teď nechat svou dílnu odemčenou celý den, nebo co?", "angry")
                $ victim.trust -= 3
                $ status.remove("retrieving workshop key")
                $ status.append("not reliable")
            $ mc.say("Těch pár otázek…?")
            $ victim.say("Mám sto chutí tě rovnou vyhodit… ale ptej se.", "angry")
        else:
            if victim.trust > -2:
                $ victim.say("Když to musí být... tak se ptej.")
            else:
                $ victim.say("Mám sto chutí tě rovnou vyhodit... ale ptej se.", "angry")
    return

label returningKey:
    $ lastSpokenWith = "victim"
    if "retrieving workshop key" in status:

        if time.isBefore(keySlightlyLateAfter):
            $ victim.trust += 1
            $ solian.trust += 1
            "Mistr Heinrich si klíč převezme s úsměvem, za kterým je vidět mírné překvapení."
            if "burned evidence seen" in victim.asked:
                $ victim.say("Vida, hlídka přeci jen k něčemu je. Za ušetření cesty děkuju, ale teď se vrať ke své práci a přines mi toho vandala v zubech.", "happy")
            else:
                $ victim.say("Vida, hlídka přeci jen k něčemu je. Za ušetření cesty děkuju, ale teď se vrať ke své práci a najdi toho zloděje.", "happy")
            call rumelinReminder

        elif time.isBefore(keyVeryLateAfter):
            $ solian.trust += 1
            "Mistr Heinrich si klíč převezme, ale jeho výraz se velmi brzy změní zpět na zamračený."
            if "burned evidence seen" in victim.asked:
                $ victim.say("No ale že ti to trvalo. A teď se vrať ke své práci a přines mi toho vandala v zubech.")
            else:
                $ victim.say("No ale že ti to trvalo. A teď se vrať ke své práci a najdi toho zloděje.")
            call rumelinReminder
        else:

            $ victim.trust -= 3
            "Když vidí klíč v tvé ruce, mistr Heinrich se zamračí ještě víc než předtím."
            if gender == "M":
                $ victim.say("Kde všude ses s klíčem od mé dílny poflakoval? Když jsem tě pro něj poslal, myslel jsem, že mi ho opravdu přineseš.", "angry")
                $ victim.say("Dokonce jsem za Eckhardem zašel sám, ale ten mi řekl, že už jsi tam byl. A jenom ses neobtěžoval dojít až za mnou. To si myslíš, že můžu nechat svou dílnu odemčenou celý den, nebo co?", "angry")
            else:
                $ victim.say("Kde všude ses s klíčem od mé dílny poflakovala? Když jsem tě pro něj poslal, myslel jsem, že mi ho opravdu přineseš.", "angry")
                $ victim.say("Dokonce jsem za Eckhardem zašel sám, ale ten mi řekl, že už jsi tam byla. A jenom ses neobtěžovala dojít až za mnou. To si myslíš, že můžu nechat svou dílnu odemčenou celý den, nebo co?", "angry")
            call apologyForLateness from _call_apologyForLateness
    else:

        if time.isBefore(keyVeryLateAfter):
            $ victim.trust += 1
            "Mistr Heinrich vejde do místnosti s mírně zmateným výrazem, ale jakmile zahlédne klíč, téměř ti ho vytrhne z ruky."
            if gender == "M":
                $ victim.say("To je klíč od mé dílny! Jak ses k němu dostal?")
            else:
                $ victim.say("To je klíč od mé dílny! Jak ses k němu dostala?")
            $ mc.say("Posílá mě s ním Eckhard. Prý by přišel sám, ale je mu špatně.")
            if "burned evidence seen" in victim.asked:
                $ victim.say("No dobře. Tak děkuju, ale teď se vrať ke své práci a přines mi toho vandala v zubech.", "happy")
            else:
                $ victim.say("No dobře. Tak děkuju, ale teď se vrať ke své práci a najdi toho zloděje.", "happy")
            call rumelinReminder
        else:

            $ victim.trust -= 2
            "Mistr Heinrich ti klíč skoro vytrhne z ruky, ale pak se zamračí ještě víc."
            $ victim.say("Co děláš s klíčem od mojí dílny?", "angry")
            $ mc.say("Eckhard ho měl u sebe a napadlo mě…")
            $ victim.say("A kdo se tě prosil o takové nápady? Když jsem konečně našel čas za Eckhardem dojít, řekl mi, že můj klíč předal náhodnému strážnému. Který se očividně neobtěžoval dojít až za mnou.", "angry")
            $ victim.say("To si myslíš, že můžu nechat svou dílnu odemčenou celý den, nebo co?", "angry")
            call apologyForLateness

    $ status.remove("carrying key")
    if "retrieving workshop key" in status:
        $ status.remove("retrieving workshop key")
    $ status.append("key delivered")

    show mcPic at menuImage
    menu:
        "Vrátím se k případu.":
            hide mcPic
            $ victim.say("To je to nejlepší, co můžeš udělat.")
            $ time.addMinutes(5)
            jump victimEnd
        "Můžu vám ještě položit pár otázek?":
            hide mcPic
            if victim.trust > -2:
                $ victim.say("Když to musí být... tak se ptej.")
            else:
                $ victim.say("Mám sto chutí tě rovnou vyhodit... ale ptej se.", "angry")
            jump victimQuestions
    return

label victimOptions:
    call zeranInnocentOptionsRemainingCheck
    call victimOptionsRemainingCheck
    if victimOptionsRemaining == 0:
        $ mc.say("Děkuji, to je všechno.")
        $ victim.say("Tak hlavně pohni, slavnosti jsou už za chvíli a já tam pořád nemám co představit.")
        return

    if victim.trust > 5 and "relationship upgrade" not in victim.asked:
        "Mistr Heinrich se na tebe dlouze podívá a pak se k tvému překvapení trochu usměje."
        $ victim.say("Nečekal bych, že to někdy řeknu, ale na hlídkaře vlastně nejsi úplně nejhorší.", "happy")
        $ victim.asked.append("relationship upgrade")

    show mcPic at menuImage
    menu:
        "Můžete mi popsat ztracenou věc?" if "shoes description" not in clues:
            hide mcPic
            $ clues.append("shoes description")
            $ victim.asked.append("shoes description")
            $ victim.say("Jsou to nádherné dámské střevíce z nejjemnější kůže. Precizně tvarované, složité šněrování, barvené drahou fialovou barvou. Zlaté stuhy a jemné zdobení. Druhé takové ve městě určitě nejsou.")
        "Máte ve městě s někým spory?" if "enemies" not in victim.asked:
            hide mcPic
            $ victim.asked.append("enemies")
            $ victim.say("S každým, kdo si dostatečně neváží mé práce. Rumelin ví, že ho chci nahradit v čele cechu a bojí se o svoje teplé místečko, Kaspar si brousí zuby na tu samou židli, i když na to nemá schopnosti… no a potom kdokoli mi hází klacky pod nohy.")
            $ victim.say("Ale největší důvod znemožnit mě na slavnostech mají myslím tihle dva.")
            $ kasparNote.isActive = True
        "Slyšel jsem, že jste vyhodil několik učedníků?" if "enemies" in rumelin.asked and "fired apprentices" not in victim.asked and gender == "M":
            hide mcPic
            $ victim.asked.append("fired apprentices")
            $ victim.say("A co jiného jsem s nimi měl dělat, když nebyli schopní žádné pořádné práce? Tak dobře mi jejich rodiče nezaplatili.")
        "Slyšela jsem, že jste vyhodil několik učedníků?" if "enemies" in rumelin.asked and "fired apprentices" not in victim.asked and gender == "F":
            hide mcPic
            $ victim.asked.append("fired apprentices")
            $ victim.say("A co jiného jsem s nimi měl dělat, když nesplnili ani základní očekávání? Tak dobře mi jejich rodiče nezaplatili.")
        "Co přesně provedli?" if "fired apprentices" in victim.asked and "fired apprentices offense" not in victim.asked:
            hide mcPic
            $ victim.asked.append("fired apprentices offense")
            $ victim.say("Škoda mluvit.")
            $ victim.say("Gerd si myslel, že rozumí řemeslu líp než já. Tak teď může plýtvat materiálem u Njala, ten se v nesmyslných nápadech a rádoby vylepšeních vyžívá. Jako by bylo něco špatně na tom, když někdo udělá poctivou, obyčejnou, prověřenou botu.")
            $ victim.say("Sigi byl prostě neschopný. Nejspíš rozmazlený mazánek bohatého tatínka, ale proč bych se s tím měl mazat já?")
            $ victim.say("A Zeran...")
            "Mistr Heinrich se zamračí."
            $ victim.say("Chodil mi za dcerou. Kluk, který by měl skládat tovaryšské zkoušky a bude svádět mou malou holčičku. Myslím, že z toho vyvázl ještě dost snadno.")
            $ victim.say("A to už bylo mnohem víc slov, než si kterýkoliv z nich zaslouží.")
            $ clues.append("Zeran offense")
            $ adaNote.isActive = True
        "Víte, kde je najít?" if "fired apprentices" in victim.asked and "fired apprentices" not in clues:
            hide mcPic
            $ victim.asked.append("fired apprentices location")
            $ clues.append("fired apprentices")
            $ victim.say("Gerda si vzal k sobě Njal. Vážně nevím, co z toho má, je dost schopný na to, aby si mohl vybírat.")
            $ victim.say("Ty druhé dva nikdo rozumný nechtěl. Jeden šel pryč z města, teď je myslím v Sehnau, nebo někde tím směrem. A ten zmetek Zeran… zkuste to v dočasné čtvrti, mezi ostatními budižkničemy.")
            $ gerdNote.isActive = True
            $ zeranNote.isActive = True
        "Jak vlastně víte, že mezi Zeranem a vaší dcerou něco bylo?" if "fired apprentices offense" in victim.asked and "proof against Zeran" not in victim.asked:
            hide mcPic
            $ victim.asked.append("proof against Zeran")
            $ victim.say("Kromě toho, že je spolu hned několik lidí vidělo? Našel jsem pár dopisů, které ten zmetek Adě psal. Samé sladké řečičky a sliby, dokonce ji chtěl vzít z města.")
        "Mohl bych vidět ty dopisy, které Zeran psal vaší dceři?" if "proof against Zeran" in victim.asked and "Zeran's letters" not in victim.asked and gender == "M":
            hide mcPic
            $ victim.asked.append("Zeran's letters")
            call zeranLettersResponse
        "Mohla bych vidět ty dopisy, které Zeran psal vaší dceři?" if "proof against Zeran" in victim.asked and "Zeran's letters" not in victim.asked and gender == "F":
            hide mcPic
            $ victim.asked.append("Zeran's letters")
            call zeranLettersResponse
        "Tohle vypadá jako drahý papír. Mohl by si ho učedník jako Zeran dovolit?" if "letters for Ada seen" in status and "expensive paper" not in victim.asked:
            hide mcPic
            $ victim.asked("expensive paper")
            $ mc.say("Nebo tady podobné papíry máte?")
            $ victim.say("To opravdu nemám. Co bych dělal s papírem s kudrlinkami? Taková zbytečnost.", "angry")
            $ mc.say("A jak by se k němu tedy Zeran dostal?")
            $ victim.say("To nevím a vůbec mě to nezajímá. Je mi jedno, na co ty svoje nesmysly psal, mojí malé holčičce je nemá co psát vůbec.")
        "Nemáte na práci i tovaryše?" if "journeymen" not in victim.asked:
            hide mcPic
            $ victim.asked.append("journeymen")
            $ victim.say("Ne od té doby, co se Eckhard stal mistrem.")
            $ victim.say("Tovaryši jsou nevděčná cháska. Neposlouchají, pořád si na něco stěžují a dožadují se nějakých práv a přitom buď běhají za děvčaty a posedávají po hospodách, nebo si stěžují na věk a špatné oči. Učedníky si aspoň můžu kdykoli srovnat.")
        "Takže Eckhard býval váš tovaryš?" if "journeymen" in victim.asked and "Eckhard relationship" not in victim.asked:
            hide mcPic
            $ victim.asked.append("Eckhard relationship")
            $ victim.say("Nějakou dobu, ale známe se už od učednických let.")
            $ victim.say("Oba jsme začínali z ničeho. Já jsem si svou dílnu vydupal ze země a Eckhard čekal, že ho cech nechá tovaryšem celý život.")
            $ victim.say("Za Velina byly pro lidské mistry tvrdší podmínky a většina míst byla stejně vyhrazená jenom pro elfy a hobity. Až po požáru se to uvolnilo a Eckhard měl šanci na vlastní dílnu.")
            $ victim.say("Rumelin možná tvrdí, že způsob vedení cechu změnil, ale dokud bude v čele on, nebudu tomu věřit.", "angry")
        "Takhle se vypracovat určitě nebylo snadné." if "Eckhard relationship" in victim.asked and "flattery" not in victim.asked:
            hide mcPic
            $ victim.asked.append("flattery")
            $ victim.trust += 1
            $ victim.say("To nebylo.")
            $ victim.say("Mistr, u kterého jsme byli v učení, nám nic neodpustil. Vstávali jsme ještě za tmy, pracovali až do noci, a netoleroval nám žádné lajdáctví. Ale kromě řemesla nás to naučilo vážit si poctivé práce.")
            $ victim.say("Během cesty na zkušenou jsem se naučil nové postupy a co nejvíc svoje schopnosti zdokonalil. To by mělo být normální, ale ne všichni to tak dělají.")
            $ victim.say("Znal jsem jednoho, co cestoval spíš po hospodách než po dílnách a z města odcházel když nadělal moc velké dluhy... ten bude třeba tovaryš celý život, pokud neskončí ještě hůř.")
            $ victim.say("Stát se mistrem v elfím městě znamenalo muset být lepší, než všichni místní elfové dohromady, když jsem nechal za sebe mluvit svou práci, nikdo mi nemohl upřít.")
            $ victim.say("Já vždycky říkám, že pokud se někdo nedokáže vyhrabat z bídy, tak asi nepracuje dost tvrdě.")
        "Kde by se vaše ukradené boty daly nejlépe prodat?" if "best sale" not in victim.asked:
            hide mcPic
            $ victim.asked.append("best sale")
            $ victim.say("V jiném městě. Tady mou práci všichni znají, každý kupec by měl otázky.")
            $ victim.say("Ale jsem si dost jistý, že o peníze nešlo. V dílně mám drahý materiál, spoustu dalších bot a jiných věcí a to všechno tam zůstalo.")
        "Jaký máte vlastně vztah se svou ženou?" if lotte.alreadyMet == True and "relationship" not in victim.asked:
            hide mcPic
            $ victim.asked.append("relationship")
            call heinrichMaritalRelationship
        "Je někdo, s kým si vaše žena obzvlášť rozumí?" if lotte.alreadyMet == True and "lisbeth friends" not in victim.asked:
            hide mcPic
            $ victim.asked.append("lisbeth friends")
            $ victim.say("To se zeptejte jí, ne?")
            $ victim.say("Ve městě nějaké kamarádky má, ale pořád se to mění, někdo má dítě, někdo se provdá někam daleko, někdo se začne chovat hrozně, už jsem dávno ztratil přehled.")
            $ victim.say("Tyhle ženské záležitosti nejsou nic pro mě.")
        "Je možné, že by vaše žena měla milence?" if lotte.alreadyMet == True and "secret lover" not in victim.asked:
            hide mcPic
            $ victim.asked.append("secret lover")
            $ victim.say("Cože?! Co má tahle otázka znamenat? Proč by moje žena měla mít milence? Doufám, že máš opravdu dobrý důvod, proč o tom začínáš.", "angry")
            show mcPic at menuImage
            menu:
                "Já se jen tak ptal..." if gender == "M":
                    hide mcPic
                    $ victim.trust -= 3
                    $ victim.say("Tak se přestaň jen tak ptát a hleď si své opravdové práce.")
                "Já se jen tak ptala..." if gender == "F":
                    hide mcPic
                    $ victim.trust -= 3
                    $ victim.say("Tak se přestaň jen tak ptát a hleď si své opravdové práce.")
                "Snažím se myslet na všechno.":
                    hide mcPic
                    $ victim.trust -= 1
                    $ mc.say("Kdyby někdo takový byl, byl by to způsob, jak se dostat do domu.")
                    $ mc.say("Ostatně kdyby někdo chodil třeba za někým z kluků, bylo by to totéž.")
                    $ victim.say("Jednou pro vždy si prosím zapamatuj, že my jsme slušný dům a žádné pochybné osoby sem nechodí.", "angry")
                "Jedna ze sousedek viděla, jak se vaše žena u dveří vítá s cizím mužem a pak jdou oba dovnitř.":
                    hide mcPic
                    $ victim.say("To musela kecat. Nebo se fakt blbě plést. Znáte ženský, klevetí, pomlouvá a kdo ví, co vlastně viděla.")
                    "Mistr Heinrich se otočí k odchodu, ale po chvíli se obrátí zpátky k tobě."
                    $ victim.say("Která sousedka to vlastně byla?", "angry")
                    $ mc.say("Lotte, bydlí na konci ulice.")
                    $ victim.say("Ta Lotta, jejíž manžel mi dodal šmejd? No to se dalo čekat. Budu muset Karstenovi vysvětlit, že ji má zfackovat, ať s těmi pomluvami přestane.")
                    $ victim.say("Kdyby radši přemýšlela, jak sehnat pořádné zboží a nedělat si ostudu.")
        "Mohl by tenhle kousek stuhy být od vašich střevíců?" if "burned evidence" in clues and "shoes description" in clues and "burned evidence seen" not in victim.asked:
            hide mcPic
            "Mistr Heinrich si ohořelý útržek prohlédne a zamračí se."
            call burnedEvidenceSeenVictim
        "Máte nějaký spor s mistrem Njalem?" if "join forces clueless" in njal.asked and "stolen idea" not in clues and "conflict with Njal" not in victim.asked:
            hide mcPic
            $ victim.asked.append("conflict with Njal")
            $ victim.say("S Njalem? Ne, o ničem nevím. Proč bych měl mít spor zrovna s ním?", "angry")
            if gender == "M":
                $ mc.say("Mluvil jsem s ním o vás a působil vůči vám nepřátelsky.")
            else:
                $ mc.say("Mluvila jsem s ním o vás a působil vůči vám nepřátelsky.")
            $ victim.say("Co já vím, co se mu v té jeho trpasličí palici mohlo vylíhnout. Všichni ho mají za podivína z nějakého důvodu.", "angry")
            $ victim.say("Třeba o mně ten budižkničemu Gerd vykládal nějaké pomluvy. Nebo měl prostě zrovna špatnou náladu. Je to důležité?")
            $ mc.say("To zatím nevím. Dám vědět, jestli se to s něčím spojí.")
        "Ohledně toho odstřižku z krbu..." if "burned evidence seen" in victim.asked and "calm Heinrich" in status and "burned evidence not as bad" not in victim.asked:
            hide mcPic
            $ victim.asked.append("burned evidence not as bad")
            $ status.remove("calm Heinrich")
            $ son.trust += 1
            $ optimist.trust += 1
            $ yesman.trust += 1
            $ ada.trust += 1
            if gender == "M":
                $ victim.say("Už jsi našel toho zmetka, co to má na svědomí?", "angry")
            else:
                $ victim.say("Už jsi našla toho zmetka, co to má na svědomí?", "angry")
            show mcPic at menuImage
            menu:
                "Nemohl by to být odstřižek nebo zbytek z výroby?":
                    hide mcPic
                    $ victim.say("Všechny podobné odstřižky by měly být už dávno uklizené. A to rozhodně ne v krbu.", "angry")
                    $ mc.say("Ale možné to je?")
                    $ victim.say("Možné asi. Ale to neznamená, že tomu věřím.")
                "Nemohla z něčeho podobného vaše manželka nebo dcera vyšívat?" if adaNote.isActive == True:
                    hide mcPic
                    $ victim.trust -= 1
                    $ victim.say("I kdyby z nějakého nepochopitelného důvodu chtěly házet drahé látky do krbu, tak do mé dílny ani jedna z nich nesmí.")
                "Chci jen říct, že věřím, že se vaše střevíce najdou celé.":
                    hide mcPic
                    $ victim.say("Tak se přestaň zdržovat zbytečnými řečmi a přines mi je.")
        "Nechci zbytečně plašit, ale je možné, že vaše střevíce nenajdeme neporušené." if time.days > 1 and "plan B" not in victim.asked:
            hide mcPic
            $ victim.asked.append("plan B")
            $ clues.append("plan B")
            $ victim.trust -= 1
            $ mc.say("Máte pro jistotu připravený nějaký náhradní výrobek na slavnosti?")
            $ victim.say("Jak to myslíš, že je možná nenajdeš? Od čeho tady hlídku máme, když nedokáže ani najít zloděje a jenom se vymlouvá?", "angry")
            $ mc.say("Ne, zloději jsem na stopě. Jen si nemůžeme být jistí, co s vaším výrobkem provedl.")
            $ victim.say("Spoléhám na to, že mi ty střevíce v pořádku přineseš.")
            $ victim.say("Náhradní výrobek nemám, ale ať vezmu ve své dílně cokoli, bude to lepší práce, než přinese půlka cechu.")
        "Zjistil jsem, kdo vám vypil velkou část vašich zásob vína." if "confession" in boysAsked and "lost bottles solved rumelin" not in victim.asked and "lost bottles solved boys" not in victim.asked and gender == "M":
            call victimLostBottlesSolved
            if leaveOption == "none":
                return
        "Zjistila jsem, kdo vám vypil velkou část vašich zásob vína." if "confession" in boysAsked and "lost bottles solved rumelin" not in victim.asked and "lost bottles solved boys" not in victim.asked and gender == "F":
            call victimLostBottlesSolved
            if leaveOption == "none":
                return
        "Zjistil jsem, že cechmistr Rumelin se snažil poškodit jednoho z ostatních mistrů." if "confession" in rumelin.asked and "rumelin exposed" not in victim.asked and gender == "M":
            hide mcPic
            call rumelinExposedVictim
        "Zjistila jsem, že cechmistr Rumelin se snažil poškodit jednoho z ostatních mistrů." if "confession" in rumelin.asked and "rumelin exposed" not in victim.asked and gender == "F":
            hide mcPic
            call rumelinExposedVictim
        "Zajímalo by mne, jak jste se dostal ke střihu mistra Njala." if "stolen idea" in clues and "stolen idea" not in victim.asked:
            hide mcPic
            $ victim.asked.append("stolen idea")
            $ victim.say("Jaký střih myslíte?")
            if "break-in" in clues:
                $ mc.say("Ten, který byl ve vylomené zásuvce vašeho stolu.")
            $ mc.say("Mistr Njal přiznal, že si ho včera v noci spolu s Gerdem vzali zpátky.")
            $ victim.say("Tak to byl on! Přemýšlel jsem, kdo mohl...")
            $ mc.say("Jak se k vám ten střih dostal?")
            show mcPic at menuImage
            menu:
                "Ukradl jste ho sám, nebo pro něj někoho poslal?":
                    hide mcPic
                    $ victim.trust -= 2
                    $ victim.say("Takhle se nenechám urážet. Nikdy v životě jsem nic neukradl a rozhodně bych neokradl jiného mistra svého cechu.", "angry")
                "Věděl jste, že je kradený?":
                    hide mcPic
            $ victim.say("Přinesl mi ho Eckhard. Prý se s ním Njal chlubil u Salmy a já bych ho dokázal zpracovat daleko lépe.")
            $ mc.say("Věděl jste, že je kradený?")
            $ victim.say("Na podrobnosti jsem se neptal.")
            $ victim.say("Původně jsem si ho ani nechtěl vzít, ale pak jsem si ho prohlédl a musel jsem dát Eckhardovi za pravdu. Opravdu skvělá práce. A velmi náročná práce, opravdu dobře to ušít by nezvládl hned tak někdo.")
        "Víte, že za krádež střihu bych měl Eckharda zatknout?" if "stolen idea" in victim.asked and "should arrest eckhard" not in victim.asked and gender == "M":
            call victimArrestEckhard
        "Víte, že za krádež střihu bych měla Eckharda zatknout?" if "stolen idea" in victim.asked and "should arrest eckhard" not in victim.asked and gender == "F":
            call victimArrestEckhard
        "Nechtěl byste se na Einionovy slavnosti spojit s mistrem Njalem?" if "own work" in njal.asked and "plan B" in clues and "join forces" not in victim.asked:
            call victimJoinForces
        "Zjišťoval jsem, jak by se lidi ve městě tvářili, kdybyste na slavnosti přinesl výrobek společně s mistrem Njalem." if "join forces victim pending" in status and "join forces survey" in status and gender == "M":
            call joinForcesSurveyResults
        "Zjišťovala jsem, jak by se lidi ve městě tvářili, kdybyste na slavnosti přinesl výrobek společně s mistrem Njalem." if "join forces victim pending" in status and "join forces survey" in status and gender == "F":
            call joinForcesSurveyResults
        "Mluvil jsem s mistrem Njalem ohledně vaší spolupráce." if "join forces victim approves" in status and "join forces" in njal.asked and "join forces go-ahead" not in victim.asked and gender == "M":
            $ victim.asked.append("join forces go-ahead")
            call joinForcesGoAhead
        "Mluvila jsem s mistrem Njalem ohledně vaší spolupráce." if "join forces victim approves" in status and "join forces" in njal.asked and "join forces go-ahead" not in victim.asked and gender == "F":
            $ victim.asked.append("join forces go-ahead")
            call joinForcesGoAhead
        "Mluvil jsem s mistrem Njalem ohledně vaší spolupráce." if "join forces victim approves" in status and "join forces clueless" in njal.asked and "join forces" not in njal.asked and "join forces go-ahead clueless" not in victim.asked and gender == "M":
            $ victim.asked.append("join forces go-ahead clueless")
            call joinForcesGoAhead
        "Mluvila jsem s mistrem Njalem ohledně vaší spolupráce." if "join forces victim approves" in status and "join forces clueless" in njal.asked and "join forces" not in njal.asked and "join forces go-ahead clueless" not in victim.asked and gender == "F":
            $ victim.asked.append("join forces go-ahead clueless")
            call joinForcesGoAhead
        "Rád bych s vámi mluvil o tom, jak kousek odtud byl oheň na ulici." if "fireshow" in status and "fireshow" not in victim.asked:
            hide mcPic
            $ victim.asked.append("fireshow")
            $ victim.say("No dobře, o co jde?")
            call heinrichFireshow
        "Mám důkaz, že Zeran vaši dceru nesváděl." if "zeran innocent" not in victim.asked and "zeran cleared" not in status and zeranInnocentOptionsRemaining > 0:
            hide mcPic
            $ victim.asked.append("zeran innocent")
            if "Ada confronts Zairis":
                $ status.append("zairis confessed")
            if "zairis confessed" in status:
                $ victim.say("To už vím. Byl tady ten holomek od Roviena a přiznal se k tomu.", "angry")
                $ victim.say("Tak jsem mu vysvětlil, ať už se k tomuhle domu ani nikomu z mojí rodiny ani nepřibližuje. Jestli má v té svojí palici aspoň trochu rozumu, tak to udělá.", "angry")
                $ victim.say("Prý že si chtěl promluvit jako chlap s chlapem. Tak dostal, co chtěl.", "angry")
                $ victim.say("Víc se tím špinavcem nemíním zabývat.", "angry")
                $ status.append("zeran cleared")
            else:
                $ victim.say("Neříkal jsem ti, že jméno toho zmetka v tomhle domě už nechci nikdy slyšet?", "angry")
                $ mc.say("I když je nevinný?")
                $ victim.say("Nevinný nebo ne, málem zničil život mojí malé holčičce.", "angry")
                call zeranInnocentOptions
        "Mám důkaz, že ty milostné dopisy psal vaší dceři Rovienův syn Zairis."  if "zairis guilty" not in victim.asked and "zeran cleared" not in status and zairisGuiltyOptionsRemaining > 0:
            label zairisGuilty:
            hide mcPic
            $ victim.asked.append("zairis guilty")
            if "Ada confronts Zairis":
                $ status.append("zairis confessed")
            if "zairis confessed" in status:
                $ victim.say("To už vím. Byl tady a přiznal se, vypadal na to skoro hrdý, holomek jeden.", "angry")
                $ victim.say("Tak jsem mu vysvětlil, ať už se k tomuhle domu ani nikomu z mojí rodiny ani nepřibližuje. Jestli má v té svojí palici aspoň trochu rozumu, tak to udělá.", "angry")
                $ victim.say("Prý že si chtěl promluvit jako chlap s chlapem. Tak dostal, co chtěl.", "angry")
                $ victim.say("Víc se tím špinavcem nemíním zabývat.", "angry")
                $ status.append("zeran cleared")
            else:
                $ victim.say("On se k tomu přiznal?")
                if "confession" in zairis.asked:
                    $ mc.say("Když viděl všechny důkazy, tak nakonec ano.")
                    $ victim.say("A tomu mám jako věřit? To by mohl říct každý.", "angry")
                    $ mc.say("Můžu ty důkazy vysvětlit i vám, jestli chcete.")
                else:
                    $ mc.say("Zatím ne, ale mám důkazy.")
                $ victim.say("Tak to si chci poslechnout.")

                python:
                    patience = max(victim.trust - 4, 0)

                call zairisGuiltyOptions
        "Děkuji, to je všechno.":
            hide mcPic
            $ victim.say("Tak hlavně pohni, slavnosti jsou už za chvíli a já tam pořád nemám co představit.")
            return
    if refusedBy == "victim":
        return
    jump victimOptions

label zairisGuiltyOptions:
    call zairisGuiltyOptionsRemainingCheck
    if zairisGuiltyOptionsRemaining == 0:
        $ mc.say("To je všechno, co mám.")
        $ victim.trust -= 1
        if gender == "M":
            $ victim.say("To jsi mě tedy nepřesvědčil. Doufal bych, že když už do mě chceš hučet, budeš aspoň mít něco v rukávu. Ale to bych asi od hlídky čekal moc.", "angry")
            $ victim.say("Pořád jsi mi nenašel moje boty. Zkus zase chvíli dělat svoji skutečnou práci. A lépe, než ti šlo orodování za toho všiváka.", "angry")
        else:
            $ victim.say("To jsi mě tedy nepřesvědčila. Doufal bych, že když už do mě chceš hučet, budeš aspoň mít něco v rukávu. Ale to bych asi od hlídky čekal moc.", "angry")
            $ victim.say("Pořád jsi mi nenašla moje boty. Zkus zase chvíli dělat svoji skutečnou práci. A lépe, než ti šlo orodování za toho všiváka.", "angry")
        return

    show mcPic at menuImage
    menu:
        "Zairisovo písmo odpovídá tomu na dopisech pro vaši dceru." if "Zairis handwriting checked" in status and "zairis guilty handwriting" not in victim.asked:
            hide mcPic
            $ victim.asked.append("zairis guilty handwriting")
            $ zeran.cluesAgainst += 1
            if "zeran handwriting checked" in status:
                $ mc.say("Zeranovo vypadá úplně jinak.")
            if "zeran innocent handwriting" not in victim.asked:
                $ victim.say("Zeran škrábe jako kočka, ale i on by se snad v milostném dopise trochu snažil.", "angry")
                $ mc.say("Vy přece také dokážete rozlišit, co jste psal vy a co paní Lisbeth, například.")
                $ mc.say("Jde o sklon písma, úhlednost, tvar některých písmen... Překvapivě hodně těchto znaků zůstává stejných, i když třeba píšete ve spěchu.")
                if gender == "M":
                    $ victim.say("Ty jsi teda chytrej. No dobře, dobře. Ale také přece mohl Zeran schválně napodobit Zairisovo písmo. To není žádný důkaz.", "angry")
                else:
                    $ victim.say("Ty jsi teda chytrá. No dobře, dobře. Ale také přece mohl Zeran schválně napodobit Zairisovo písmo. To není žádný důkaz.", "angry")
                $ mc.say("To ve skutečnosti není tak jednoduché.")
                $ victim.say("Nepodceňuj toho špinavce.")
            else:
                $ victim.say("Jo, to je ta tvoje teorie, že každý píše úplně jinak.", "angry")
                $ mc.say("To není jenom moje teorie...")
                $ victim.say("Ale také přece mohl Zeran schválně napodobit Zairisovo písmo. To není žádný důkaz.", "angry")
                $ mc.say("To ve skutečnosti není tak jednoduché.")
                $ victim.say("Nepodceňuj toho špinavce.")
        "Dopisy se hodně odkazují na Amadise a popisují návštěvu jeho hrobu. Zairis Amadise velmi obdivuje a u jeho hrobu byl." if "Amadis grave" in zairis.asked and "zairis guilty amadis grave" not in victim.asked:
            hide mcPic
            $ victim.asked.append("zairis guilty amadis grave")
            $ patience -= 1
            $ victim.say("Tam ale mohla být spousta elfů. A obdivuje ho taky každý lajdák a nekňuba, co místo práce chodí koukat na komedianty.", "angry")
            $ victim.say("A potom o tom velmi rádi povykládají každému podvodníkovi, co se chce tvářit, že tam byl také.", "angry")
        "V těch dopisech jsou docela dobré básně. Ty by nedokázal napsat každý, ale Zairis se o poezii hodně zajímá." if "letters for Ada seen" and "poetry" in zairis.asked and "zairis guilty poetry" not in victim.asked:
            hide mcPic
            $ victim.asked.append("zairis guilty poetry")
            $ patience -= 1
            $ victim.say("Mně přišly jako snůška nesmyslů a sladkých řečiček. Jak víš, že jsou tak zvláštní?", "angry")
            "TODO"
        "Ty dopisy jsou psané vytříbeným stylem, který vyžaduje určité vzdělání. Zairis ho má, ale kde by k němu přišel Zeran? " if "letters for Ada seen" and "zairis guilty style" not in victim.asked:
            hide mcPic
            $ victim.asked.append("zairis guilty style")
            $ patience -= 1
            $ victim.say("Se vzděláním se tady vytahuje každý druhý elf, oni si na to potrpí. A hlavně rodina toho špinavce bývala dřív docela bohatá.", "angry")
            $ victim.say("Ten si mohl sehnat všechny knížky, co potřeboval, aby mohl slušným mladým holkám plést hlavu.", "angry")
        "Ty dopisy jsou psané na velmi drahém papíře, který si Zeran těžko může dovolit. Zairis mi ale napsal nějakou poznámku na přesně stejný druh papíru."  if "Zairis handwriting checked" in status and "zairis guilty paper" not in victim.asked:
            hide mcPic
            $ victim.asked.append("zairis guilty paper")
            $ zeran.cluesAgainst += 1
            $ victim.say("Ten kašpar mohl ten papír ukradnout, nepotřeboval ho tolik. Ani to nemuselo být od Zairise, tolik druhů zdobeného papíru se přece ve městě sehnat nedá.", "angry")
        "To je všechno, co mám.":
            hide mcPic
            $ victim.trust -= 1
            if gender == "M":
                $ victim.say("To jsi mě tedy nepřesvědčil. Doufal bych, že když už do mě chceš hučet, budeš aspoň mít něco v rukávu. Ale to bych asi od hlídky čekal moc.", "angry")
                if "case solved" not in status:
                    $ victim.say("Pořád jsi mi nenašel moje boty. Zkus zase chvíli dělat svoji skutečnou práci. A lépe, než ti šlo orodování za toho všiváka.", "angry")
            else:
                $ victim.say("To jsi mě tedy nepřesvědčila. Doufal bych, že když už do mě chceš hučet, budeš aspoň mít něco v rukávu. Ale to bych asi od hlídky čekal moc.", "angry")
                if "case solved" not in status:
                    $ victim.say("Pořád jsi mi nenašla moje boty. Zkus zase chvíli dělat svoji skutečnou práci. A lépe, než ti šlo orodování za toho všiváka.", "angry")
            return

    if zeran.cluesAgainst == 3:
        $ victim.say("Zatracená práce, takže abych si to ujasnil, ty říkáš...", "surprised")
        $ mc.say("...že ty dopisy jsou psané Zairisovým písmem na papíře, který Zairis používá, a že v něm jsou básně, které by tímto způsobem moc jiných lidí nenapsalo, jestli vůbec někdo.")
        $ victim.say("Takže to byl on.", "angry")
        $ mc.say("Všechno tomu nasvědčuje.")
        $ victim.say("Mizera jeden. To si s ním vyřídím.", "angry")
        $ mc.say("A Zeran...")
        $ victim.say("...mu posloužil jako obětní beránek. Zbabělec jeden. To mu neprojde.", "angry")
        $ victim.say("Musím teď z domu. Lisbeth tě vyprovodí.", "angry")
        $ mc.say("Nebylo by...")
        $ victim.say("Jindy.")
        "Mistr Heinrich zavolá manželku, řekne jí pár slov a zmizí v domě. Paní Lisbeth si vás oba přeměří tázavým a poněkud znepokojeným pohledem, nenaléhá však a způsobně ti ukáže cestu ke dveřím."
        scene bg heinrich outside
        "Venku před domem potom znovu spatříš mistra Heinricha, jak vyrazí ze dveří a rázným krokem se vydá pryč. Na tebe se ani nepodívá."
        $ status.append("zairis dealt with")
        jump victimEnd
    elif patience < 1:
        $ victim.say("Upřímně, mám dojem, že jsme těmi dopisy už ztratili až moc času.", "angry")
        if zeran.cluesAgainst == 2:
            $ victim.say("Něco, co říkáš, by možná znělo rozumně, ale zapomínáš, že tady se bavíme o Zeranovi. Ten je schopný každé podlosti.", "angry")
        else:
            $ victim.trust -= 1
            $ victim.say("A tedy doufal jsem, že když už mě nutíš se bavit o tom špinavci Zeranovi, budeš mít aspoň připravené nějaké rozumné důvody, ale těch jsem tedy moc neslyšel.", "angry")
        $ victim.say("Takže mě ušetři toho utrpení v tomhle dál pokračovat a jdi zase chvíli dělat něco, za co tě město platí. Jako třeba věnovat se té zatracené krádeži.", "angry")
        $ victim.say("Slavnosti budou brzy.", "angry")

    jump zairisGuiltyOptions

label zeranInnocentOptions:
    call zeranInnocentOptionsRemainingCheck
    if zeranInnocentOptionsRemaining == 0:
        $ mc.say("To je všechno, co mám.")
        $ victim.say("Takže pořádný důkaz žádný.", "angry")
        $ victim.say("Někdo za Adou chodil a psal jí dopisy. Zjisti, kdo jiný to teda byl, a pak se můžeme bavit. Ale Zeran je jediný elf, se kterým jsem ji viděl já.", "angry")

    show mcPic at menuImage
    menu:
        "Jeho písmo vůbec neodpovídá tomu na dopisech." if "zeran handwriting checked" in status and "zeran innocent handwriting" not in victim.asked:
            hide mcPic
            $ victim.asked.append("zeran innocent handwriting")
            $ victim.say("Jak může písmo neodpovídat? Písmo je písmo, ne? I kdyby tam měl třeba chyby.", "angry")
            $ mc.say("Vy přece také dokážete rozlišit, co jste psal vy a co paní Lisbeth, například.")
            $ mc.say("Jde o sklon písma, úhlednost, tvar některých písmen... Překvapivě hodně těchto znaků zůstává stejných, i když třeba píšete ve spěchu.")
            if gender == "M":
                $ victim.say("Ty jsi teda chytrej. No dobře, dobře. Ale přece mohl schválně psát jinak. To není žádný důkaz.", "angry")
            else:
                $ victim.say("Ty jsi teda chytrá. No dobře, dobře. Ale přece mohl schválně psát jinak. To není žádný důkaz.", "angry")
            $ mc.say("To ve skutečnosti není tak jednoduché.")
            $ victim.say("Nepodceňuj toho špinavce.", "angry")
            if "letters for Ada shown" not in victim.asked and "letters for Ada slip up" not in victim.asked:
                call lettersForAdaSlipUp
        "V jednom z dopisů se mluví o Amadisově hrobě, tam se přece Zeran nemohl nikdy dostat." if "Amadis grave" in zeran.asked and "zeran innocent amadis grave" not in victim.asked:
            hide mcPic
            $ victim.asked.append("zeran innocent amadis grave")
            $ victim.say("A tebe překvapuje, že ten zmetek Adě lhal? Stejně jako nám všem ostatním?", "angry")
            if "letters for Ada shown" not in victim.asked and "letters for Ada slip up" not in victim.asked:
                call lettersForAdaSlipUp
            else:
                $ mc.say("Já si myslím, že nelhal...")
                $ victim.say("A máš i nějaký opravdový důkaz? Nebo si to jenom myslíš?", "angry")
        "Ty dopisy jsou psané na velmi drahém papíře, který si Zeran těžko může dovolit." if "letters for Ada seen" in status and "expensive paper" not in victim.asked:
            hide mcPic
            $ victim.asked.append("expensive paper")
            $ victim.say("Mohl ho ukrást. Nebo mu stálo za to si na něj našetřit.")
            $ victim.say("Nezapomeň, že ten špinavec dal všanc svoje učednické místo a porušil zákony pohostinství a veškerou slušnost. Dát si práci se sehnáním papíru už je to nejmenší.", "angry")
            if "letters for Ada shown" not in victim.asked and "letters for Ada slip up" not in victim.asked:
                call lettersForAdaSlipUp
        "Navíc vím, kdo za Adou chodil opravdu - byl to Rovienův syn Zairis." if "zairis guilty" not in victim.asked and "zeran cleared" not in status and zairisGuiltyOptionsRemaining > 0:
            jump zairisGuilty
        "To je všechno, co mám.":
            hide mcPic
            $ victim.say("Takže pořádný důkaz žádný.", "angry")
            $ victim.say("Někdo za Adou chodil a psal jí dopisy. Zjisti, kdo jiný to teda byl, a pak se můžeme bavit. Ale Zeran je jediný elf, se kterým jsem ji viděl já.", "angry")
            return
    jump zeranInnocentOptions

label lettersForAdaSlipUp:
    $ victim.asked.append("letters for Ada slip up")
    $ victim.say("O jakých dopisech to vlastně mluvíš?", "angry")
    $ mc.say("O těch pro vaši dceru...")
    if gender == "M":
        $ victim.say("A ty jsi měl dopisy pro Adu někdy v ruce?", "angry")
    else:
        $ victim.say("A ty jsi měla dopisy pro Adu někdy v ruce?", "angry")
    $ victim.say("Nebo se ze mě snažíš dělat vola?")
    return

label heinrichFireshow:
    "TODO"
    return

label afterApologyReaction:
    show mcPic at menuImage
    menu:
        "Samozřejmě. Jdu se zas vrátit k případu.":
            hide mcPic
            $ time.addMinutes(5)
            jump victimEnd
        "Samozřejmě. Můžu vám ještě položit pár otázek?":
            hide mcPic
            $ victim.say("Když to musí být... tak se ptej.")
            return
    return

label afterApologyReactionPositive:
    show mcPic at menuImage
    menu:
        "Toho si vážím. Jdu se zas vrátít k případu.":
            hide mcPic
            $ time.addMinutes(5)
            jump victimEnd
        "Toho si vážím. Můžu vám ještě položit pár otázek?":
            hide mcPic
            $ victim.say("Bez toho to asi vyšetřit nemůžeš, tak do toho.")
            return
    return

label rumelinReminder:
    if gender == "M":
        $ victim.say("Už jsi vyslechl Rumelina?")
    else:
        $ victim.say("Už jsi vyslechla Rumelina?")
    if rumelin.alreadyMet == True:
        $ mc.say("Ano, ale sleduji všechny stopy, na které narazím.")
    else:
        $ mc.say("Nejdřív se na něj chci pořádně připravit.")
    return

label apologyForLateness:
    if gender == "M":
        $ mc.say("Omlouvám se, zabral jsem se do vyšetřování…")
    else:
        $ mc.say("Omlouvám se, zabrala jsem se do vyšetřování…")
    $ victim.say("Znamená to, že zloděje už máš?", "angry")
    $ mc.say("Ještě ne, ale…")
    $ victim.say("Tak se přestaň flákat a najdi ho.", "angry")
    return

label zeranLettersResponse:
    if victim.trust < 5:
        $ victim.say("Spálil jsem je.")
        $ mc.say("Proč? Mohl to být důkaz…")
        $ victim.say("A taky to mohlo mé holčičce zničit život a na tom mi záleží víc, než na nějakých důkazech.", "angry")
    else:
        "Mistr Heinrich se dlouze zamyslí."
        $ victim.say("Dobře, přinesu je. Ale ber je jako přísně důvěrnou věc, která může zničit život nevinné holce. Jestli zjistím, že je viděl někdo další, ještě o tom uslyšíš.")
        $ mc.say("To samozřejmě chápu a budu na to myslet.")
        "Mistr Heinrich přikývne a po chvíli ti přinese několik listů papíru svázaných tenkou koženou šňůrkou."
        call loveLetters
        $ status.append("letters for Ada seen")
        $ victim.asked.append("letters for Ada shown")
    return

label heinrichMaritalRelationship:
    $ victim.say("Co je tohle za otázky? Je to moje žena. Kdybychom spolu neměli dobrý vztah, nejsme manželé.", "angry")
    if victim.trust > 0:
        $ victim.say("Navíc bez ní a toho, jak vede domácnost, bych možná nebyl nejlepší švec v celém Marendaru.")
        show mcPic at menuImage
        menu:
            "Omlouvám se, nechtěl jsem vás urazit." if gender == "M":
                hide mcPic
                $ victim.say("Tak se koukej vrátit k vyšetřování a přestaň řešit moje soukromí.", "angry")
            "Omlouvám se, nechtěla jsem vás urazit." if gender == "F":
                hide mcPic
                $ victim.say("Tak se koukej vrátit k vyšetřování a přestaň řešit moje soukromí.", "angry")
            "Jak často jí to říkáte?":
                hide mcPic
                if victim.trust < 5:
                    if gender == "M":
                        $ victim.say("Co je ti do toho? Jsi tady jenom od toho, abys našel můj ztracený výrobek, tak sebou pohni a nenavážej se do mého soukromí, nebo si budu stěžovat u tvého velitele.", "angry")
                    else:
                        $ victim.say("Co je ti do toho? Jsi tady jenom od toho, abys našla můj ztracený výrobek, tak sebou pohni a nenavážej se do mého soukromí, nebo si budu stěžovat u tvého velitele.", "angry")
                else:
                    "Mistr Heinrich se zamračí a chvíli nad odpovědí přemýšlí."
                    $ victim.say("Možná…")
                    if "burned evidence seen" in victim.asked:
                        $ victim.say("Do toho ti nic není. Vrať se k pátrání a přines mi moje ztracené střevíce. Nebo aspoň toho vandala v zubech.")
                    else:
                        $ victim.say("Do toho ti nic není. Vrať se k pátrání a přines mi moje ztracené střevíce. Nebo aspoň toho zloděje v zubech.")
                    $ lisbeth.relationships["victim"] += 1
                    $ ada.trust += 1
                    $ status.append("fresh flowers")
                    $ status.append("flowers achievement")
    else:
        if gender == "M":
            $ mc.say("Omlouvám se, nechtěl jsem vás urazit.")
            $ victim.say("Ale urazil, tak se koukej vrátit k vyšetřování a nenavážej se do mého soukromí.", "angry")
        else:
            $ mc.say("Omlouvám se, nechtěla jsem vás urazit.")
            $ victim.say("Ale urazila, tak se koukej vrátit k vyšetřování a nenavážej se do mého soukromí.", "angry")
    return

label rumelinExposedVictim:
    $ victim.asked.append("rumelin exposed")
    $ victim.trust += 5
    "Heinrichovy oči se rozzáří škodolibou radostí."
    if "burned evidence seen" in victim.asked:
        $ victim.say("Kromě zničení mých střevíců? To mě velmi zajímá. Našel se někdo další, kdo ohrožuje jeho pozici?", "happy")
    else:
        $ victim.say("Kromě krádeže mých střevíců? To mě velmi zajímá. Našel se někdo další, kdo ohrožuje jeho pozici?", "happy")
    $ mc.say("Mistr Njal chtěl na slavnostech představit stejný typ střevíců jako vy a mistr Rumelin se bál skandálu.")
    $ victim.say("To si myslel, že moje práce neobstojí v tom srovnání?", "angry")
    $ mc.say("Myslím, že mu šlo spíš o…")
    $ victim.say("Takové urážky si nenechám líbit. Rumelin sám sotva ušije obyčejný škrpál, brání v práci někomu stokrát lepšímu, a ještě si bude brát do huby moje výrobky?", "angry")
    $ victim.say("Postarám se, aby odteď ve městě nikomu nestál ani za pozdrav.", "happy")
    $ status.append("rumelin exposed")
    return

label victimJoinForces:
    hide mcPic
    $ victim.asked.append("join forces")
    $ mc.say("Pracovali jste na stejném typu bot a ty jeho kvůli snaze mistra Rumelina ještě nejsou hotové.")
    if "rumelin exposed" in status:
        show mcPic at menuImage
        menu:
            "Celý cech by to pochopil jako reakci na cechmistrovy špinavé machinace.":
                hide mcPic
                $ victim.say("To je pravda… spojit se proti němu by ke slovům přidalo i jasné gesto.")
                $ victim.say("Zajdu za ním a nabídnu mu pomoc.")
                call joinForcesVictimApproves
                return
            "Před slavnostmi už není moc času a oba na nich potřebujete něco představit...":
                hide mcPic
    else:
        $ mc.say("Před slavnostmi už není moc času a oba na nich potřebujete něco představit...")
    $ victim.say("Takže bych za ním měl jít ze zoufalství, s prosbou o pomoc?", "angry")
    if gender == "M":
        $ mc.say("Tak jsem to nemyslel.")
    else:
        $ mc.say("Tak jsem to nemyslela.")
    if victim.trust > 4:
        $ victim.say("A jak tedy?", "angry")
        $ mc.say("Že by v této situaci mohlo být pro vás oba výhodnější spojit síly a vytvořit společně něco mimořádného.")
        $ victim.say("A vzali by to lidi opravdu tak? Nechtěl bych, aby mě pomlouvali, že jsem líný přijít s vlastním výrobkem.")
        $ mc.say("Tak by to určitě nevypadalo...")
        if gender == "M":
            $ victim.say("Hele, jsi na hlídkaře celkem správný chlap, ale promiň, tomuhle nerozumíš.")
        else:
            $ victim.say("Hele, jsi na hlídkaře celkem správná ženská, ale promiň, tomuhle nerozumíš.")
        $ victim.say("Radši mi najdi moje boty. Nebo toho prevíta, co mi je sebral.")
        $ status.append("join forces victim pending")
    else:
        $ victim.say("Tak přestaň přemýšlet nad věcmi, které s tebou vůbec nesouvisí, a věnuj se své práci.", "angry")
    return

label joinForcesSurveyResults:
    hide mcPic
    $ victim.say("Opravdu? ... a jak to dopadlo?", "surprised")
    show mcPic at menuImage
    menu:
        "Nepřijali by to." if "join forces" in rumelin.asked or "join forces" in nirevia.asked or "join forces" in kaspar.asked:
            hide mcPic
            $ victim.say("Přesně to jsem čekal. Každý musí Einiona uctít sám svou vlastní prací, žádné zkratky a zjednodušení.")
            if gender == "M":
                $ victim.say("S kým jsi vlastně mluvil?")
            else:
                $ victim.say("S kým jsi vlastně mluvila?")
            show mcPic at menuImage
            menu:
                "Říkal to cechmistr Rumelin." if "join forces" in rumelin.asked:
                    hide mcPic
                    $ victim.trust -= 2
                    $ victim.say("Vážně se chceš spoléhat na toho, kdo mi nejspíš ukradl ten první výrobek a kdo mě pomlouvá, kudy chodí?", "angry")
                "Říkala to paní Nirevia." if "join forces" in nirevia.asked:
                    hide mcPic
                    $ victim.trust -= 1
                    $ victim.say("Té tak budu věřit. Tváří se jako dáma, ale je jedna ruka s manželem a všichni víme, co ten je zač.", "angry")
                "Říkal to mistr Kaspar." if "join forces" in kaspar.asked:
                    hide mcPic
                    if "affair exposed" in status:
                        $ victim.trust -= 4
                        $ victim.say("Tohle jméno přede mnou ani nevyslovuj, nebo za ním půjdu znovu a tentokrát mu všechno vysvětlím pořádně.", "angry")
                        $ victim.say("Vůbec nechápu, proč s ním ztrácíš čas, a už vůbec ne, proč s ním mluvíš o mně.", "angry")
                    else:
                        $ victim.trust -= 1
                        $ victim.say("Kaspar je budižkničemu, co umí jen pomlouvat a lichotit a doufá, že to z něj udělá cechmistra. Tomu, co řekne, nepřikládám žádnou váhu.", "angry")
        "Vážili by si toho." if "join forces" in eckhard.asked or "join forces" in salma.asked:
            hide mcPic
            $ victim.say("Opravdu?", "surprised")
            $ victim.say("To jsem nečekal. To bych asi mohl...")
            $ victim.say("Kdo to vlastně říkal?")
            show mcPic at menuImage
            menu:
                "Říkal to mistr Eckhard." if "join forces" in eckhard.asked:
                    hide mcPic
                    $ victim.say("No jo, Eckhard. Na toho je spoleh. Jeden z mála lidí, co mě opravdu uznává. Takových kamarádů bych klidně měl víc.", "happy")
                    "Mistr Heinrich se na chvíli zamyslí a pak zavrtí hlavou."
                    $ victim.say("V tomhle na něj ale dát nemůžu. Ne všichni vidí věci jako on a on si to často neuvědomuje.")
                "Říkala to Salma." if "join forces" in salma.asked:
                    hide mcPic
                    $ victim.trust += 3
                    $ victim.say("Proč Salma? Ta přece není v cechu...", "surprised")
                    $ victim.say("Hm...", "angry")
                    $ victim.say("Je pravda, že nás všechny zná už dlouho, ale zároveň nemá důvod hrát nějaké hry.")
                    $ victim.say("Co že přesně říkala?")
                    $ mc.say("Že z lenosti nebo pohodlnosti by zrovna vás rozhodně nikdo nepodezříval, ale naopak by spolupráce s mistrem Njalem udělala velmi dobrý dojem.")
                    $ victim.say("Po těch letech, co k ní chodíme, už by mohla vědět, co říká...")
                    $ victim.say("Hned za Njalem zajdu, ať můžeme začít co nejdřív.")
                    call joinForcesVictimApproves
        "Nikdo nic užitečného neví.":
            hide mcPic
            $ victim.say("Tak to potom nemá smysl zkoušet.")
    $ status.remove("join forces victim pending")
    $ status.remove("join forces survey")
    return

label joinForcesVictimApproves:
    if "join forces njal approves" in status:
        $ mc.say("S mistrem Njalem už jsem mluvil a vypadá tomu nakloněný. Nemělo by být těžké se dohodnout.")
        $ victim.say("Ty mě pořád překvapuješ. V tom případě se hned pustíme do práce.")
        $ mc.say("Budu vám držet palce.")
        if not achievement.has(achievement_name['jointMasterpiece'].name):
            $ Achievement.add(achievement_name['jointMasterpiece'])
    else:
        $ mc.say("Možná raději chvíli počkejte. Zkusím nejdřív zjistit, jestli by souhlasil i on, ať víte, na čem jste.")
        $ victim.say("Dobře, ale pospěš si prosím. Slavnosti jsou brzy nesmíme ztrácet čas.")
        $ mc.say("Spolehněte se.")
    $ status.append("join forces victim approves")
    return

label joinForcesGoAhead:
    hide mcPic
    if "join forces go-ahead clueless" in victim.asked and "join forces go-ahead" in victim.asked:
        $ victim.asked.append("join forces go-ahead")
        $ victim.say("Znova? A řekl k tomu něco nového?")

    if "join forces njal approves" in status:
        $ victim.trust += 1
        $ mc.say("Vypadá tomu nakloněný. Pokud za ním zajdete, určitě se domluvíte.")
        $ victim.say("To rád slyším. V tom případě se hned pustíme do práce.")
        $ mc.say("Budu vám držet palce.")
    else:
        if "join forces njal pending" in status:
            show mcPic at menuImage
            menu:
                "Mistr Njal bude ochotný spolupracovat, jen pokud dostane spravedlnost za krádež svého střihu.":
                    hide mcPic
                    $ victim.say("Jak to myslíš, pokud dostane spravedlnost? To chce na oplátku nějaký střih ode mě, nebo co?", "angry")
                    $ mc.say("Chce zloděje toho střihu před soudem.")
                    "Mistr Heinrich se zamračí."
                    $ victim.say("Pak je to očividně ještě větší blázen, než se o něm říká. A s blázny já spolupracovat nebudu.", "angry")
                    $ mc.say("Pořád si myslím, že by vám ta spolupráce pomohla ohromit celé město. Pravděpodobně byste se pak konečně stal cechmistrem…")
                    $ victim.say("Nejsem jako Rumelin, abych kvůli jedné židli podrážel jiné lidi.", "angry")
                    $ victim.say("Máš ještě něco, nebo se konečně vrátíš k pátrání po tom zatraceném zloději?", "angry")
                "Bohužel to vypadá, že on o spolupráci nemá zájem.":
                    hide mcPic
                    $ victim.say("Já si od začátku myslel, že to nemá smysl...", "angry")
                    $ victim.say("Tak se vrať ke své opravdové práci a aspoň najdi toho zatraceného zloděje.", "angry")
        else:
            $ mc.say("Bohužel to vypadá, že on o spolupráci nemá zájem.")
            $ victim.say("Já si od začátku myslel, že to nemá smysl...", "angry")
            $ victim.say("Tak se vrať ke své opravdové práci a aspoň najdi toho zatraceného zloděje.", "angry")
    return

label victimLostBottlesSolved:
    hide mcPic
    $ victim.say("Tak to mě opravdu zajímá. Nech mě hádat, byl to Rumelin, aby mě o to víc naštval, když už tady byl pro ty boty, že ano?", "angry")
    show mcPic at menuImage
    menu:
        "Ano, byl to Rumelin.":
            hide mcPic
            $ victim.asked.append("lost bottles solved rumelin")
            if gender == "M":
                $ victim.say("A proč jsi to ještě nezatkl?", "angry")
            else:
                $ victim.say("A proč jsi to ještě nezatkla?", "angry")
            $ mc.say("Zatím proti němu sbírám důkazy.")
            $ victim.say("Tak s tím pohni, ať ho stihnou odsoudit ještě před slavnostmi.", "angry")
        "Byl to váš syn a učedníci.":
            hide mcPic
            $ victim.asked.append("lost bottles solved boys")
            $ mc.say("S botami to zřejmě vůbec nesouvisí, jenom chtěli upít a pak se nezastavili.")
            $ victim.say("Tak já je vezmu pod svou střechu, chovám se k nim jako k vlastním a oni mě za tu dobrotu ještě okradou? Ti poletí z domu. A ještě předtím je přerazím. A Aachima dvojnásob, holomka nevděčného.", "angry")
            show mcPic at menuImage
            menu:
                "To už je záležitost vaší domácnosti, ve které vám nechci nijak radit. Chtěl jsem jenom, abyste o tom věděl." if gender == "M":
                    call victimPunishBoysForDrinking
                    return
                "To už je záležitost vaší domácnosti, ve které vám nechci nijak radit. Chtěla jsem jenom, abyste o tom věděl." if gender == "F":
                    call victimPunishBoysForDrinking
                    return
                "Nemohl byste si to ještě rozmyslet?":
                    hide mcPic
                    $ victim.say("Co bych si na tom měl rozmýšlet?", "angry")
                    $ mc.say("Jsou to mladí kluci, kteří jednou zapomněli přemýšlet. Vyhodit je z domu je velmi přísný trest.")
                    $ victim.say("Kradli pod mou střechou! Celé město by v tom stálo za mnou, jakkoli mě nemají rádi.", "angry")
                    $ mc.say("Určitě. Ale pořád to znamená, že by skončili jako věční nádeníci kvůli jednomu nerozumu. Možná si zaslouží dostat ještě příležitost.")
                    $ victim.say("Aby to nebyla příležitost k další krádeži.", "angry")
                    $ mc.say("Myslím, že rychle poznáte, jestli se učedníci snaží sekat dobrotu.")
                    $ victim.say("Hm. Budiž, dám tomu pár dní. Aby se neřeklo.")
                    $ victim.say("Doufám, že to aspoň Rumelinovi vezme vítr z plachet, až mě zase někde bude pomlouvat.")
    return

label victimPunishBoysForDrinking:
    hide mcPic
    $ status.append("boys punished for drinking")
    $ victim.trust += 2
    $ son.trust -= 2
    $ optimist.trust -= 2
    $ yesman.trust -= 2
    $ ada.trust -= 1
    $ lisbeth.trust -= 1
    $ victim.say("To je také v pořádku. Teď mě ale omluv, jdu si to s nimi vyřídit.")
    "Mistr Heinrich ti pokyne a ty vyjdeš ven na ulici. Krátce zahlédneš paní Lisbeth, která tě chtěla vyprovodit, jak se překvapeně a znepokojeně dívá na svého manžela. Pak za tebou dveře domu zapadnou."
    $ leaveOption ="none"
    return

label victimArrestEckhard:
    hide mcPic
    $ victim.asked.append("should arrest eckhard")
    $ victim.trust -= 1
    $ victim.say("Za krádež střihu? A kdo ho za něco takového bude žalovat?", "surprised")
    $ mc.say("Mistr Njal. Vypadal, že na tom bude trvat.")
    $ victim.say("Zatracený trpasličí přivandrovalec.", "angry")
    $ victim.say("Myslím tím, nedalo by se mu domluvit, že v Marendaru máme jiné zákony než u nich na severu... nebo odkud přišel?")
    show mcPic at menuImage
    menu:
        "Krádež je krádež, tam moc rozdílů nevidím.":
            hide mcPic
            $ rauvin.trust += 1
            $ victim.say("Ale přece jste říkal, že už má ten svůj střih zase zpátky, takže se nestala žádná škoda.")
        "Pokusím se s ním promluvit.":
            hide mcPic
            $ victim.trust += 2
            $ victim.say("Výborně, aspoň někdo tady má rozum. Tak s ním promluv a nějak to urovnej.")
        "Můžu se o to pokusit, ale musel byste také prokázat dobrou vůli.":
            hide mcPic
            if victim.trust < 4:
                $ victim.say("Dobrou vůli? A to má jako znamenat co? To mě ten trpaslík chce vydírat, nebo jak to mám chápat?", "angry")
                if gender == "M":
                    $ mc.say("Tak jsem to nemyslel...")
                else:
                    $ mc.say("Tak jsem to nemyslela...")
                $ victim.say("A jak tedy?", "angry")
                $ victim.say("Nebo víš co? Radši přestaň myslet na blbosti a začni konečně dělat svou práci.", "angry")
                $ victim.say("A to je hledání zloděje, ne zatýkání slušných lidí.", "angry")
            else:
                $ victim.say("No dobře, dobrou vůli, ale jak? Mám mu zase já půjčit nějaký svůj střih?")
                show mcPic at menuImage
                menu:
                    "Já můžu zapomenout na krádež a přesvědčit o tom i Njala, pokud vy zapomenete na jednu hloupou klukovinu." if "confession" in boysAsked or "confession" in son.asked:
                        hide mcPic
                        $ victim.say("O čem to mluvíš? Jakou klukovinu?", "angry")
                        label heinrichDealMischiefOptions:
                        show mcPic at menuImage
                        menu:
                            "Myslím tu jejich malou pitku." if "lost bottles solved boys" in victim.asked and "someone got drunk..." not in victim.asked:
                                hide mcPic
                                $ victim.say("Tu, za kterou je chci vyhodit? To není žádná klukovina, to je krádež pod střechou jejich mistra.", "angry")
                                $ mc.say("Co kdyby se z vašich soukromých zásob nic neztratilo, stejně jako mistru Njalovi nikdo neukradl jeho střih? Jestli si rozumíme.")
                                call heinrichDealMischief2
                            "Kdyby se třeba někdo opil..." if "someone got drunk..." not in victim.asked:
                                hide mcPic
                                $ victim.asked.append("someone got drunk...")
                                if "alcoholic" in eckhard.asked or "alcoholic" in salma.asked or "alcoholic" in lisbeth.asked:
                                    $ victim.say("“Jestli se mě snažíš urazit, tak si mě nepřej!", "angry")
                                    $ mc.say("Vás samozřejmě nemyslím.")
                                    $ victim.say("Tak co tím myslíš?", "angry")
                                else:
                                    $ victim.say("Koho tím myslíš? Doufám, že se nesnažíš nic naznačit.", "angry")
                                jump heinrichDealMischiefOptions
                            "Kdyby třeba někdo z vašich učedníků...":
                                hide mcPic
                                $ victim.asked("accusing apprentices")
                                $ victim.say("Co zase provedli, holomci?", "angry")
                                call heinrichDealMischief1
                            "Kdyby třeba váš syn...":
                                hide mcPic
                                $ victim.asked("accusing son")
                                $ victim.say("Jestli ten budižkničemu něco provedl, tak ať si mě nepřeje!", "angry")
                                call heinrichDealMischief1
                    "Mohl byste například méně pít." if "confession" in boysAsked:
                        hide mcPic
                        $ victim.say("Co má moje pití s čím společného? To se mě snažíš urazit, nebo jak to mám brát?", "angry")
                        if gender == "M":
                            $ mc.say("To ne, jenom jsem si všiml, že...")
                        else:
                            $ mc.say("To ne, jenom jsem si všimla, že...")
                        "Mistr Heinrich tě nechá mluvit, ale z jeho pohledu se dá jasně vyčíst varování."
                        show mcPic at menuImage
                        menu:
                            "...vám to ve městě dělá špatné jméno.":
                                hide mcPic
                                $ victim.say("Moje jméno je jenom moje věc. A rozhodně nepotřebuju rady od nějakého náhodného strážného.", "angry")
                                if "burned evidence seen" in victim.asked:
                                    $ victim.say("Vrať se radši ke své práci a najdi už konečně moje ztracené boty. Nebo aspoň toho holomka, co mi je zničil.", "angry")
                                else:
                                    $ victim.say("Vrať se radši ke své práci a najdi už konečně moje ztracené boty. Nebo aspoň toho holomka, co mi je ukradl.", "angry")
                            "...si z toho bere příklad váš syn a učedníci.":
                                hide mcPic
                                if "lost bottles solved boys" in victim.asked:
                                    $ victim.say("No dovol?! Já piju jen to, na co si sám vlastníma rukama vydělám!", "angry")
                                    $ mc.say("To by Aachim určitě také rád, přeci jen je to váš syn, ale jak by si ve svém věku mohl pořádně vydělat?")
                                    $ mc.say("Z vlastního si může dát tak nanejvýš nějaký patok pro chudinu.")
                                    $ victim.say("Tak ať nepije vůbec. Nebo ať aspoň nepije tolik, že přestane znát míru.")
                                    show mcPic at menuImage
                                    menu:
                                        "Paní Lisbeth říká, že to se často stává i vám...":
                                            hide mcPic
                                            $ victim.trust -= 3
                                            $ rauvin.trust -=3
                                            $ hayfa.trust -=3
                                            $ solian.trust -= 4
                                            "Mistr Heinrich na tebe jen několik okamžiků upřeně hledí."
                                            $ victim.say("Ven.", "angry")
                                            $ victim.say("Na vyřešení případu máš zhruba tolik času, než dojdu na strážnici si na tebe stěžovat, tak sebou konečně pohni.", "angry")
                                            "Přes veškerou tvou snahu mistr zůstane zcela nesmlouvavý a ty se vzápětí ocitneš na ulici před jeho domem."
                                            $ refusedBy = "victim"
                                            $ leaveOption = "none"
                                        "To by měl, ale nemá vaše zkušenosti. A ty nemůže získat od nikoho lepšího než od vás.":
                                            hide mcPic
                                            $ victim.say("No pít s ním nezačnu, jestli míříš tímhle směrem.")
                                            $ victim.say("Až se vrátí z tovaryšské cesty na zkušenou, tak ano. Do té doby nesmí zapomenout, že je hlavně učedník a já jeho mistr. To by nedělalo dobrotu.")
                                            $ mc.say("Samozřejmě. Mohl by potom být méně ochotný vám naslouchat.")
                                            $ victim.say("Přesně. Ale vysvětlit mu pár věcí můžu. Ať mi nedělá ostudu.")
                                        "Nemá vaše zkušenosti. Možná si myslí, že pil jen tolik, jak často vidí pít vás.":
                                            hide mcPic
                                            $ victim.say("Takže můj vlastní syn krade a můžu za to já?", "angry")
                                            $ mc.say("Jenom se snaží vzít si z vás příklad a...")
                                            $ victim.say("Kdyby radši stejně jako já šil boty.", "angry")
                                            $ victim.say("A kdyby radši všichni dělali, co mají. Třeba hledali moje boty, místo aby strkali nos do záležitostí mojí rodiny.", "angry")
                                else:
                                    $ victim.say("Váš syn chce být jako vy. Ale to, že vy sám s alkoholem nemáte problémy, nezaručí, že na tom on bude stejně.")
                                    $ victim.say("Samozřejmě, že chce být jako já.")
                                    "Heinrich se zamračí, ale zároveň vypadá vlastně téměř potěšeně."
                                    $ victim.say("Ale do toho tobě nic není. Svého syna si srovnám sám.", "angry")
                                    $ mc.say("Na to nikdo nebude vhodnější. Ostatně zřejmě si z vás on a učedníci berou příklad i v tom, že chtějí pít jen ty nejlepší pálenky.")
                                    $ victim.say("No přece se Aachim nespokojí s kdejakou břečkou...")
                                    if gender == "M":
                                        $ victim.say("Počkej, ty jsi s nimi pil, nebo jak to víš? Nemáš pracovat na případu?", "angry")
                                        $ mc.say("Během práce na případu jsem právě zjistil, že v domě nechybí jen boty. Ale není za tím žádný zlý úmysl, jen kluci také chtěli slavit.")
                                    else:
                                        $ victim.say("Počkej, ty jsi s nimi pila, nebo jak to víš? Nemáš pracovat na případu?")
                                        if gender == "M":
                                            $ mc.say("Během práce na případu jsem právě zjistil, že ty ztracené lahve, o kterých jsme mluvili, vypil Aachim s učedníky. Ale není za tím žádný zlý úmysl, jen kluci také chtěli slavit.")
                                        else:
                                            $ mc.say("Během práce na případu jsem právě zjistila, že ty ztracené lahve, o kterých jsme mluvili, vypil Aachim s učedníky. Ale není za tím žádný zlý úmysl, jen kluci také chtěli slavit.")
                                        if "lost bottles solved rumelin" in victim.asked:
                                            $ victim.trust -= 2
                                            if gender == "M":
                                                $ victim.say("Cože? Neříkal jsi předtím, že mi je ukradl Rumelin?", "surprised")
                                            else:
                                                $ victim.say("Cože? Neříkala jsi předtím, že mi je ukradl Rumelin?", "surprised")
                                            call stupidExcuse
                                            if gender == "M":
                                                $ mc.say("Chtěl jsem jenom, abyste je nepotrestal moc přísně")
                                            else:
                                                $ mc.say("Chtěla jsem jenom, abyste je nepotrestal moc přísně")
                                            $ victim.say("S kluky si ještě promluvím, a jestli to opravdu vypili oni, tak je potrestám po zásluze. Ale na tebe si budu stěžovat u tvých nadřízených.", "angry")
                                            $ victim.say("A teď se mi kliď z očí.", "angry")
                                            $ refusedBy = "victim"
                                        else:
                                            $ victim.say("Cože? Chceš říct...", "surprised")
                                            $ mc.say("Že než někoho pozvete k sobě domů na pohárek, raději se podívejte, co mu můžete nabízet, aby to nevypadalo hloupě.")
                                            $ victim.say("Oni vypili moje zásoby?! Já je přetrhnu, víš, kolik to stálo?", "angry")
                                            $ mc.say("Tuším, že výrazně víc, než kdejaká břečka.")
                                            "Mistr Heinrich se na několik okamžiků odmlčí. Působí rozhněvaně, ale ne natolik, aby mu jeho hněv ukázal směr."
                                            $ victim.say("Tohle si budou muset odpracovat. A to při jejich šikovnosti znamená, že jako mí učedníci zešednou.", "angry")
                                            $ status.append("apprentices saved")
                    "Promluvím s Njalem, pokud napravíte tu křivdu, kterou jste udělal Zeranovi." if zeranNote.isActive:
                        hide mcPic
                        if "zeran's name cleared" in status:
                            $ victim.say("No zpátky ho brát nebudu. To by nedělalo dobrotu. Ale... no... dobře, asi mu můžu vrátit jeho peníze. Ať to zkusí jinde.")
                            $ victim.say("Ale do domu mi nesmí. Pořád si myslím, že se s Adou bavili nějak moc často.", "angry")
                            $ status.append("zeran gets money")
                        else:
                            $ victim.trust -= 5
                            "Mistr Heinrich na pár okamžiků není překvapením schopen slova."
                            $ victim.say("Cože?! Vážně?! Toho zmetka, co mi málem zprznil dceru?! Co to po mně chceš?!", "angry")
                            $ mc.say("Ale...")
                            if "burned evidence seen" in victim.asked:
                                $ victim.say("Tohle odmítám poslouchat! Vypadni z mého domu a nevracej se bez mých bot nebo toho holomka, co mi je zničil!", "angry")
                            else:
                                $ victim.say("Tohle odmítám poslouchat! Vypadni z mého domu a nevracej se bez mých bot nebo toho holomka, co mi je ukradl!", "angry")
                            $ refusedBy = "victim"
                    "Aspoň Njalovi za ten střih zaplatit. Můžu mu peníze rovnou donést.":
                        hide mcPic
                        $ victim.say("To by možná mohlo být fér… tedy podle toho, kolik ten trpaslík chce, samozřejmě.")
                        $ victim.say("Zase tak dobrý ten střih není.", "angry")
                        $ mc.say("Co třeba cena jednoho páru bot, které byste podle něj vyrobil?")
                        "Mistr Heinrich se na chvíli zamyslí."
                        $ victim.say("Tohle si ještě budu muset promyslet a propočítat. Pošlu pak kdyžtak Aachima.")
                        if gender == "M":
                            $ mc.say("Když to tak zmiňujete, vlastně nevím, jakou cenu přesně mistr Njal myslel… možná bych se ho měl nejdřív zeptat...")
                        else:
                            $ mc.say("Když to tak zmiňujete, vlastně nevím, jakou cenu přesně mistr Njal myslel… možná bych se ho měla nejdřív zeptat...")
                        $ mc.say("Rozhodně Aachima neposílejte dřív, než dám vědět.")
                        $ victim.say("Chápu. Možná bych se měl s Njalem domluvit napřímo.")
                        $ mc.say("Možná to ještě předtím zkusím nějak urovnat.")
                        $ victim.say("Tak ale pohni, slavnosti se blíží.", "angry")
                    "To si ještě nejsem jistý, ale na něco přijdu." if gender == "M":
                        hide mcPic
                        "Heinrich se zamračí a pro sebe zavrčí něco o tom, proč s tím pak vůbec začínáš, ale víc nekomentuje."
                    "To si ještě nejsem jistá, ale na něco přijdu." if gender == "F":
                        hide mcPic
                        "Heinrich se zamračí a pro sebe zavrčí něco o tom, proč s tím pak vůbec začínáš, ale víc nekomentuje."
    return

label stupidExcuse:
    show mcPic at menuImage
    menu:
        "To jsem neříkal." if gender == "M":
            hide mcPic
            $ victim.say("To mě máš za pitomce? Nenechám si lhát do očí.", "angry")
        "To jsem neříkala." if gender == "F":
            hide mcPic
            $ victim.say("To mě máš za pitomce? Nenechám si lhát do očí.", "angry")
        "Musel jsem se splést." if gender == "M":
            hide mcPic
            $ victim.say("Takže mi buď lžeš do očí, nebo jsi ještě hloupější než průměrný strážný.", "angry")
        "Musela jsem se splést." if gender == "F":
            hide mcPic
            $ victim.say("Takže mi buď lžeš do očí, nebo jsi ještě hloupější než průměrný strážný.", "angry")
        "Vyšly najevo nové okolnosti.":
            hide mcPic
            $ victim.say("Takže mi buď lžeš do očí, nebo jsi ještě hloupější než průměrný strážný.", "angry")
    return

label heinrichDealMischief1:
    if "confession" in boysAsked and "confession" in son.asked:
        show mcPic at menuImage
        menu:
            "Myslím tu jejich malou pitku." if "lost bottles solved boys" in victim.asked:
                hide mcPic
                $ victim.say("Tu, za kterou je chci vyhodit? To není žádná klukovina, to je krádež pod střechou jejich mistra.", "angry")
                $ mc.say("Co kdyby se z vašich soukromých zásob nic neztratilo, stejně jako mistru Njalovi nikdo neukradl jeho střih? Jestli si rozumíme.")
                call heinrichDealMischief2
            "Kdy jste naposled kontroloval své zásoby vína a jiného alkoholu?" if "lost bottles solved boys" not in victim.asked:
                hide mcPic
                if "accusing son" in victim.asked:
                    $ victim.say("Říkáš, že mi Aachim učednická chodí na moje soukromé zásoby?", "angry")
                else:
                    $ victim.say("Říkáš, že mi ta holota učednická chodí na moje soukromé zásoby?", "angry")
                if "lost bottles solved rumelin" in victim.asked:
                    $ victim.trust -= 2
                    if gender == "M":
                        $ victim.say("Neříkal jsi předtím, že mi ty lahve ukradl Rumelin?", "angry")
                        call stupidExcuse
                        $ mc.say("Chtěl jsem jen říct, co kdyby se z vašich soukromých zásob nic neztratilo, stejně jako mistru Njalovi nikdo neukradl jeho střih? Jestli si rozumíme.")
                    else:
                        $ victim.say("Neříkala jsi předtím, že mi ty lahve ukradl Rumelin?", "angry")
                        call stupidExcuse
                        $ mc.say("Chtěla jsem jen říct, co kdyby se z vašich soukromých zásob nic neztratilo, stejně jako mistru Njalovi nikdo neukradl jeho střih? Jestli si rozumíme.")
                    $ victim.say("Takže ty mi nejdřív lžeš a pak máš tu drzost za mnou chodit s takovouhle špinavostí? To si zkoušej u Rumelina, ale ne u mě.", "angry")
                    $ victim.say("Koukej se okamžitě vrátit k případu a vyřešit ho dřív, než si na tebe stihnu stěžovat u tvých nadřízených.", "angry")
                    $ victim.say("A moji domácnost nech mně. Do té ti nic není.", "angry")
                    $ refusedBy = "victim"
                else:
                    $ mc.say("Říkám, že se z vašich soukromých zásob nic neztratilo, stejně jako mistru Njalovi nikdo neukradl jeho střih. Jestli si rozumíme.")
                    label heinrichDealMischief2:
                    "Heinrich se zamračí."
                    $ victim.say("Rozumím tomu, že si mě asi pleteš s Rumelinem.", "angry")
                    if "accusing son" in victim.asked:
                        $ victim.say("Co je tohle vůbec za dohodu? Proč by Njalovi mělo záležet na na Aachimovi?", "angry")
                    else:
                        $ victim.say("Co je tohle vůbec za dohodu? Proč by Njalovi mělo záležet na mých učednících?", "angry")
                    show mcPic at menuImage
                    menu:
                        "Záleží mu na tom, jak se stavíte ke spravedlnosti.":
                            hide mcPic
                            $ mc.say("Když ukážete, že také dokážete odpouštět, můžu to použít při přesvědčování, že by měl odpustit i on.")
                            "Heinrich se zamyslí a pak pomalu přikývne."
                            $ victim.say("No dobře, kvůli Eckhardovi. Nic z toho se nestalo. A ty teď padej z mého domu a místo věcí, které se nestaly, vyšetři tu jednu, která se stala.")
                            $ status.append("apprentices saved")
                        "To vás nemusí zajímat. Návrh je jasný, přijměte, nebo odmítněte.":
                            hide mcPic
                            $ victim.trust -= 2
                            $ victim.say("V tom případě odmítám. Vydírat se nenechám a Eckhard taky ne.", "angry")
                            $ victim.say("“A ty se koukej vrátit ke své práci, než si dojdu promluvit s tvými nadřízenými.", "angry")
                        "Záleží na nich mně, jestli se jich nikdo jiný nezastane.":
                            hide mcPic
                            $ victim.trust -= 1
                            if gender == "M":
                                $ victim.say("A ty se jich chceš zastávat? Vždyť jsi právě řekl, že kradli pod mou střechou!", "angry")
                            else:
                                $ victim.say("A ty se jich chceš zastávat? Vždyť jsi právě řekla, že kradli pod mou střechou!", "angry")
                            $ mc.say("Nechci, aby měli zkažený celý život kvůli jedné nerozvážnosti.")
                            $ victim.say("Sahat do mých zásob není nerozvážnost, ale zlodějina. Museli dobře vědět, co dělají.", "angry")
                            $ mc.say("Jsou to mladí kluci, ti občas prostě nepřemýšlí. Já jen prosím, abyste vybral trest, který z nich neudělá věčné nádeníky, kteří ani nedokončili učení.")
                            $ victim.say("Hm. Milosrdnější než Heulwen. A Eckharda do toho taháš proč?", "angry")
                            if gender == "M":
                                $ mc.say("Chtěl jsem, abyste kromě velkorysosti měl ještě další důvod, proč nad tím celým přemýšlet.")
                            else:
                                $ mc.say("Chtěla jsem, abyste kromě velkorysosti měl ještě další důvod, proč nad tím celým přemýšlet.")
                            $ victim.say("Takže mě opravdu máš za Rumelina. No, učedníci tu zůstanou a budou mi moci dokázat, že se polepšili. A jestli proti Eckhardovi uslyším křivé slovo, vyřídím si to ne s nimi, ale s tebou osobně.", "angry")
                            if "burned evidence seen" in victim.asked:
                                $ victim.say("A teď se prosím přestaň zdržovat věcmi, do kterých ti nic není, a najdi konečně toho vandala.", "angry")
                            else:
                                $ victim.say("A teď se prosím přestaň zdržovat věcmi, do kterých ti nic není, a najdi konečně toho zloděje.", "angry")
            "Celé to byla jen nešťastná náhoda...":
                hide mcPic
                $ victim.say("Tak tohle si chci poslechnout. Co byla nešťastná náhoda?", "angry")
                if "accusing son" in victim.asked:
                    $ victim.say("Jestli s mými botami něco provedl Aachim, tak ho chci vidět na pranýři, bez ohledu na to, že to je můj syn. A ještě předtím ho vlastnoručně přetrhnu jak hada.")
                else:
                    $ victim.say("Jestli s mými botami něco provedla ta holota učednická, tak je chci vidět na pranýři, bez ohledu na to, že pak nebudou moci pracovat. A ještě předtím je vlastnoručně přetrhnu jak hada.")
                show mcPic at menuImage
                menu:
                    "Vlastně si nejsem jistý..." if gender == "M":
                        hide mcPic
                        $ victim.trust -= 1
                        $ victim.say("Tak proč tohle všechno? Nejdřív začneš o dobré vůli, pak chvíli chodíš kolem horké kaše a nakonec řekneš, že vlastně nic? To myslíš, že ani jeden z nás nemá nic lepšího na práci?", "angry")
                        $ victim.say("Koukej se radši vrátit k vyšetřování. A až budeš něco opravdu chtít, řekni to rovnou.", "angry")
                    "Vlastně si nejsem jistá..." if gender == "F":
                        hide mcPic
                        $ victim.trust -= 1
                        $ victim.say("Tak proč tohle všechno? Nejdřív začneš o dobré vůli, pak chvíli chodíš kolem horké kaše a nakonec řekneš, že vlastně nic? To myslíš, že ani jeden z nás nemá nic lepšího na práci?", "angry")
                        $ victim.say("Koukej se radši vrátit k vyšetřování. A až budeš něco opravdu chtít, řekni to rovnou.", "angry")
                    "O vaše boty nejde.":
                        hide mcPic
                        $ mc.say("Kluci zkazili nějaký materiál a báli se, co tomu řeknete.")
                        $ victim.say("To se jim stává běžně. Co to bylo zač, že jsou z toho tak vyděšení?", "angry")
                        if gender == "M":
                            $ mc.say("Já... si vlastně nejsem jistý. Pochopte, jak ševcovině nerozumím...")
                        else:
                            $ mc.say("Já... si vlastně nejsem jistá. Pochopte, jak ševcovině nerozumím...")
                        $ victim.say("Chápu. V každém případě si s nimi o tom promluvím. Jestli sahali na něco drahého a ještě to zkazili, ať si mě nepřejí.")
                        $ mc.say("Jenom se snažili pracovat co nejlépe, abyste na ně mohl být hrdý.")
                        $ victim.say("Mají dělat, co se jim řekne. Nejvíc hrdý na ně budu, až konečně ušijí pořádnou pevnou botu.", "angry")
                        $ mc.say("Jistě že to nebylo nejchytřejší, proto klukovina. Ale chtěli vám udělat radost, i když hloupě. To možná stojí za trochu dobré vůle.")
                        $ victim.say("Asi uvidíme podle toho, o co přesně šlo.")
                    "Ano, za ztrátu vašich bot může Aachim." if "accusing son" in victim.asked:
                        hide mcPic
                        if gender == "M":
                            $ victim.asked("A proč jsi ho ještě nezatkl?")
                        else:
                            $ victim.asked("A proč jsi ho ještě nezatkla?")
                    "Ano, za ztrátu vašich bot můžou učedníci." if "accusing apprentices" in victim.asked:
                        hide mcPic
                        if gender == "M":
                            $ victim.asked("A proč jsi je ještě nezatkl?")
                        else:
                            $ victim.asked("A proč jsi je ještě nezatkla?")
    return

###

label victimOptionsRemainingCheck:
    call zeranInnocentOptionsRemainingCheck
    call zairisGuiltyOptionsRemainingCheck

    $ victimOptionsRemaining = 0
    if "shoes description" not in clues:
        $ victimOptionsRemaining += 1
    if "enemies" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "enemies" in rumelin.asked and "fired apprentices" not in victim.asked and gender == "M":
        $ victimOptionsRemaining += 1
    if "enemies" in rumelin.asked and "fired apprentices" not in victim.asked and gender == "F":
        $ victimOptionsRemaining += 1
    if "fired apprentices" in victim.asked and "fired apprentices offense" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "fired apprentices" in victim.asked and "fired apprentices" not in clues:
        $ victimOptionsRemaining += 1
    if "best sale" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "fired apprentices offense" in victim.asked and "proof against Zeran" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "proof against Zeran" in victim.asked and "Zeran's letters" not in victim.asked:
        $ victimOptionsRemaining += 1
    if lotte.alreadyMet == True and "relationship" not in victim.asked:
        $ victimOptionsRemaining += 1
    if lotte.alreadyMet == True and "lisbeth friends" not in victim.asked:
        $ victimOptionsRemaining += 1
    if lotte.alreadyMet == True and "secret lover" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "confession" in rumelin.asked and "rumelin exposed" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "stolen idea" in clues and "stolen idea" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "burned evidence" in clues and "shoes description" in clues and "burned evidence seen" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "burned evidence seen" in victim.asked and "calm Heinrich" in status and "burned evidence not as bad" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "own work" in njal.asked and "plan B" in clues and "join forces" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "join forces victim pending" in status and "join forces survey" in status:
        $ victimOptionsRemaining += 1
    if time.days > 1 and "plan B" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "join forces clueless" in njal.asked and "stolen idea" not in clues and "conflict with Njal" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "join forces victim approves" in status and "join forces" in njal.asked and "join forces go-ahead" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "join forces victim approves" in status and "join forces clueless" in njal.asked and "join forces" not in njal.asked and "join forces go-ahead clueless" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "stolen idea" in victim.asked and "should arrest eckhard" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "confession" in boysAsked and "lost bottles solved rumelin" not in victim.asked and "lost bottles solved boys" not in victim.asked not in victim.asked:
        $ victimOptionsRemaining += 1
    if "journeymen" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "journeymen" in victim.asked and "Eckhard relationship" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "Eckhard relationship" in victim.asked and "flattery" not in victim.asked:
        $ victimOptionsRemaining += 1
    if "zeran innocent" not in victim.asked and "zeran cleared" not in status and zeranInnocentOptionsRemaining > 0:
        $ victimOptionsRemaining += 1
    if "zairis guilty" not in victim.asked and "zeran cleared" not in status and zairisGuiltyOptionsRemaining > 0:
        $ victimOptionsRemaining += 1
    return

label zeranInnocentOptionsRemainingCheck:
    $ zeranInnocentOptionsRemaining = 0
    call zairisGuiltyOptionsRemainingCheck
    if "zeran handwriting checked" in status and "zeran innocent handwriting" not in victim.asked:
        $ zeranInnocentOptionsRemaining += 1
    if "letters for Ada seen" in status and "Amadis grave" in zeran.asked and "zeran innocent amadis grave" not in victim.asked:
        $ zeranInnocentOptionsRemaining += 1
    if "letters for Ada seen" in status and "expensive paper" not in victim.asked:
        $ zeranInnocentOptionsRemaining += 1
    if "zairis guilty" not in victim.asked and "zeran cleared" not in status and zairisGuiltyOptionsRemaining > 0:
        $ zeranInnocentOptionsRemaining += 1
    return

label zairisGuiltyOptionsRemainingCheck:
    $ zairisGuiltyOptionsRemaining = 0
    if "Zairis handwriting checked" in status and "zairis guilty handwriting" not in victim.asked:
        $ zairisGuiltyOptionsRemaining += 1
    if "letters for Ada seen" in status and "Amadis grave" in zairis.asked and "zairis guilty amadis grave" not in victim.asked:
        $ zairisGuiltyOptionsRemaining += 1
    if "letters for Ada seen" in status and "poetry" in zairis.asked and "zairis guilty poetry" not in victim.asked:
        $ zairisGuiltyOptionsRemaining += 1
    if "letters for Ada seen" in status and "zairis guilty style" not in victim.asked:
        $ zairisGuiltyOptionsRemaining += 1
    if "Zairis handwriting checked" in status and "zairis guilty paper" not in victim.asked:
        $ zairisGuiltyOptionsRemaining += 1
    return
