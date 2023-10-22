label njalController:
    $ origAsked = njal.asked.copy()
    if njal.alreadyMet == False:
        call njalFirst
    else:
        call njalAgain
    if njal.alreadyMet == False:
        $ njal.alreadyMet = True
    call njalOptions
    call leavingNjal

    # adjust time spent and create events
    $ time.addMinutes((len(njal.asked) - len(origAsked)) * 3)
    if "add awaiting AML merchant list" in status:
        $ status.remove("add awaiting AML merchant list")
        $ newEvent = Event(copy.deepcopy(time), "STATUS", 0, "awaiting AML merchant list", 3, "info")
        $ newEvent.when.addHours(1)
        $ eventsList.append(newEvent)
    return

label njalFirst:
    "Mistr Njal ti přisune hezky vyřezávanou židli a sám si sedne na druhou."
    $ njal.say("Nevím, jak moc budu schopný pomoct, ale ptejte se.")
    return

label njalAgain:
    "Mistr Njal se prohrábne ve vlasech tužkou, kterou právě držel v ruce, a pak ti pokyne směrem k jedné ze židlí v místnosti."
    "Můžu vám pomoct ještě s něčím?"
    return

label njalOptions:
    call gerdOptionsRemainingCheck
    call njalOptionsRemainingCheck
    if njalOptionsRemaining == 0 and gerdOptionsRemaining == 0:
        if gender == "M":
            $ mc.say("To je všechno, na co jsem se chtěl zeptat. Děkuji za váš čas.")
        else:
            $ mc.say("To je všechno, na co jsem se chtěla zeptat. Děkuji za váš čas.")
        $ njal.say("Jsem rád, že jsem mohl všechno uvést na pravou míru.")
        return

    show mcPic at menuImage
    menu:
        "Víte o tom, že váš učedník Gerd byl včera v noci v dílně mistra Heinricha?" if "fired apprentices" in clues and "which apprentice" in liese.asked and "told njal" not in gerd.asked and "workshop visit" not in njal.asked:
            hide mcPic
            $ njal.asked.append("workshop visit")
            $ njal.say("Myslel jsem, že Heinrich ho tam odmítá znovu pustit. A že Gerd je tak velmi spokojený.")
            $ mc.say("Jedna sousedka ho včera v noci viděla, popsala ho dost přesně.")
            if "workshop visit" in gerd.asked:
                $ mc.say("On sám se navíc už přiznal")
            "Njal na chvíli zaváhá."
            $ njal.say("Ano, vím, že tam byl.")
            call workshopVisitNjal
        "Je pravda, že jste včera poslal svého učedníka do dílny mistra Heinricha?" if "told njal" in gerd.asked and "workshop visit" not in njal.asked:
            hide mcPic
            $ njal.asked.append("workshop visit")
            call workshopVisitNjal
        "Proč jste ukradený střih neřešil s městskou hlídkou?" if "workshop visit" in njal.asked and "police business" not in njal.asked:
            hide mcPic
            $ njal.asked.append("police business")
            $ njal.say("Nejdřív jsem šel za cechmistrem Rumelinem a ten slíbil, že celou věc vyřeší uvnitř cechu. A dokud jsem měl jenom podezření, nemohl jsem dělat nic moc jiného.")
            $ mc.say("Kdy to asi bylo?")
            $ njal.say("Asi před dvěma měsíci, možná o něco dřív. Když se nic nedělo, nelíbilo se mi to, ale říkal jsem si, že Rumelin má bez důkazů možná také svázané ruce.")
            $ njal.say("Před necelými dvěma týdny mi ale tady Gerd moje podezření potvrdil a navíc řekl, že Heinrich se chce mým nápadem chlubit na Einionových slavnostech a ani u toho nezmínit moje jméno. Tak jsme za cechmistrem šli znovu.", "angry")
            $ njal.say("On pořád trval na tom, že nechce tahat hlídku do věcí svého cechu, a já se bál, že kdyby Heinrichovi začali na dveře bušit strážní, mohl by ty papíry prostě zničit. To by byla škoda mé práce. Trochu jsme se s Rumelinem i pohádali, já mu pohrozil, že na slavnostech představím svůj nápad také, on slíbil, že to nějak zařídí.", "angry")
            $ njal.say("Ale pak bylo měsíc ticho, slavnosti budou za pár dní... Když jsem viděl dílnu odemčenou, tak jsem se rozhodl využít příležitosti a vzít si zpět svůj majetek.")
        "Podezření? Takže jste už dřív tušil, kdo vás střih ukradl?" if "police business" in njal.asked and "suspicion" not in njal.asked:
            hide mcPic
            $ njal.asked.append("suspicion")
            $ njal.say("Nějakou dobu před tou krádeží za mnou přišel Eckhard a chtěl ten střih koupit. Heinrich by ho prý jako schopnější řemeslník využil daleko lépe než já.")
            $ njal.say("Samozřejmě jsem Eckharda poslal na ledovec, takhle urážet se nenechám.", "angry")
            $ eckhardNote.isActive = True
        "Jak se Eckhard o vašem nápadu vlastně dozvěděl?" if "suspicion" in njal.asked and "information source" not in njal.asked:
            hide mcPic
            $ njal.asked.append("information source")
            $ njal.say("Netuším. Na čem pracuji věděl jenom můj učedník, jinak nikdo.")
            $ njal.say("Nebo možná... krátce předtím přijeli na návštěvu mí rodiče z Altenbüren. Zkontrolovat, jestli jim jako syn dělám čest a držím se trpasličích tradic.")
            $ njal.say("Nelíbilo se jim už to, že jsem je vzal k Salmě, protože bychom tu přece měli mít trpasličí hospodu, bez ohledu na to, jak málo trpaslíků v Marendaru žije. Snažil jsem se jim vysvětlit, že bych konečně mohl prorazit, a možná jsem byl o něco hlasitější, než jsem chtěl.", "angry")
            $ njal.say("Jestli byl Eckhard tehdy U Salmy také, asi mohl něco zaslechnout.")
        "Mohl váš učedník v dílně mistra Heinricha vzít ještě něco dalšího?" if "workshop visit" in njal.asked and "did anything else" not in njal.asked:
            hide mcPic
            $ njal.asked.append("did anything else")
            $ njal.say("To nemám jak vědět, dovnitř jsem s ním nešel. Ale rozhodně jsem si nevšiml, že by odtamtud vynášel cokoli jiného, než můj střih.")
            if "burned evidence" in clues:
                $ mc.say("A mohl tam něco zničit? Jak dlouho tam byl?")
                $ njal.say("Asi deset minut. A Gerd je hodný, poctivý kluk.")
        "Proč jste pro svoje nákresy nešel sám?" if "workshop visit" in njal.asked and "why not go himself" not in njal.asked:
            hide mcPic
            $ njal.asked.append("why not go himself")
            $ njal.say("Nevyznám se tam, najít cokoli by mi trvalo výrazně déle než Gerdovi a snáz bych na sebe mohl upozornit. Navíc bych bez svolení nešel do dílny jiného mistra.")
            show mcPic at menuImage
            menu:
                "Ale poslat tam učedníka vám nevadilo?":
                    hide mcPic
                    $ njal.trust -= 1
                    $ njal.say("To byla výjimečná situace. Věřte mi, že kdybych měl jiné možnosti, využil bych je. Ale do slavností zbývají čtyři dny a tohle bylo jednoduché a přímočaré řešení v nouzi.")
                "Chápu.":
                    hide mcPic
        "Gerd je váš jediný učedník?" if "apprentices" not in njal.asked:
            hide mcPic
            $ njal.asked.append("apprentices")
            $ njal.say("Ještě tu je Knut, ten se mnou přišel už z Altenbüren, ale teď je tam právě na návštěvě za rodinou.")
            if gender == "M":
                $ mc.say("Zvláštní, čekal bych, že bude chtít pracovat na svém vlastním výrobku.")
            else:
                $ mc.say("Zvláštní, čekala bych, že bude chtít pracovat na svém vlastním výrobku.")
            $ njal.say("To já také, ale tvrdil, že je se svou prací spokojený, tak jsem mu nechtěl bránit jen proto, že má na víc. Rodina je koneckonců důležitá.")
        "Je pravda, že máte v poslední době potíže s nákupem materiálu?" if "less deals" in salma.asked and "less deals" not in njal.asked:
            hide mcPic
            $ njal.asked.append("less deals")
            "Njal překvapeně pozvedne obočí."
            $ njal.say("To je pravda, ale nečekal bych, že to bude vyšetřovat městská hlídka.")
            $ mc.say("Vyšetřujeme všechno, co by mohlo s případem jakkoli souviset. Zvlášť, pokud by se dohromady mělo jednat o útok na celý ševcovský cech.")
            $ njal.say("Tak mi to nepřijde. Nevím o tom, že by měl problémy kdokoli jiný z mistrů, jenom já. Navíc se mi několikrát stalo, že se mnou obchodník vyjednával jako vždycky a vycouval, až když jsem zmínil druh zboží nebo na co to potřebuju.")
            $ njal.say("Ale na kloub bych tomu přijít chtěl, takhle se nedá pracovat.")
            $ njal.say("Všechen potřebný materiál na svůj vlastní mistrovský výrobek jsem dal dokupy teprve pár dní zpátky.", "angry")
        "Takže váš výrobek na slavnosti ještě není hotový?" if "less deals" in njal.asked and "own work" not in njal.asked:
            hide mcPic
            $ njal.asked.append("own work")
            $ njal.say("Není a budu mu muset až do slavností věnovat veškerý čas, abych ho stihl dokončit. Ale bude to práce, na kterou budu moct být hrdý. A hlavně ta práce bude moje vlastní, to se o Heinrichovi říct nedá.")
        "Můžete mi o těch obchodech i tak říct něco víc? Třeba kdo všechno vám odmítl něco prodat?" if "less deals" in njal.asked and "less deals details" not in njal.asked:
            hide mcPic
            $ njal.asked.append("less deals details")
            $ njal.say("Začalo to asi před měsícem, dost z ničeho nic.")
            $ mc.say("Nepohádal jste třeba s někým?")
            $ njal.say("To bych si pamatoval, s obchodníky mám mnohem lepší vztahy než třeba Heinrich. Jedinou neshodu jsem v té době měl s Rumelinem.")
            $ mc.say("A se týkala čeho, jen pro jistotu?")
            if "police business" in njal.asked:
                $ njal.say("To byla ta hádka o mém ukradeném střihu. Takže nic, co by souviselo s obchody.")
            else:
                $ njal.say("Soukromé věci mezi námi dvěma, obávám se.")
            $ mc.say("A konkrétní obchodníci?")
            "Njal se na chvíli zamyslí."
            $ njal.say("Určitě Karsten a Rovien. Na ty další bych si musel chvíli vzpomínat, ale můžu se pokusit sestavit seznam a pak vám ho poslat.")
            $ merchantNote.isActive = True
            $ rovienNote.isActive = True
            show mcPic at menuImage
            menu:
                "Děkuji, to nám určitě pomůže.":
                    hide mcPic
                    $ njal.say("Budete ho mít co nejdříve.")
                    $ status.append("add awaiting AML merchant list")
                "To nebude potřeba, ale děkuji.":
                    hide mcPic
                    $ njal.say("Jak myslíte.")
        "Měl jste s mistrem Heinrichem v poslední době nějaké spory o dílo?" if "confession" in rumelin.asked and "stolen idea" not in clues and "less deals solved" not in njal.asked:
            hide mcPic
            $ njal.asked.append("less deals solved")
            "Mistr Njal se nejdřív zatváří překvapeně, ale pak se zamračí."
            $ njal.say("Pokud sporem o dílo myslíte krádež střihu, který jsem dlouho zdokonaloval, tak ano, měl.", "angry")
            $ njal.say("Co vás k tomu přivedlo? Rumelinovi konečně došlo, že to nevyřeší, a rozhodl se to předat hlídce?")
            $ mc.say("Cechmistr Rumelin je ten, kdo vám kvůli tomu kazil obchody. Prý nemohl dovolit, abyste na slavnostech představil stejný výrobek jako mistr Heinrich.")
            call njalLessDealsSolved
        "Podařilo se mi zjistit, kdo vám kazil obchody." if "confession" in rumelin.asked and "stolen idea" in clues and "less deals solved" not in njal.asked:
            hide mcPic
            $ njal.asked.append("less deals solved")
            $ njal.say("Opravdu? To je skvělá zpráva. Vrtalo mi hlavou, jestli jsem někoho přeci jen neurazil.", "happy")
            $ mc.say("Cechmistr Rumelin nechtěl dovolit, abyste na slavnostech představil stejný výrobek jako mistr Heinrich.")
            call njalLessDealsSolved
        "Zjistil jsem, že vaše problémy s materiálem byly jen výsledek nedorozumění." if "confession" in rumelin.asked and "less deals solved" not in njal.asked and "less deals buried" not in njal.asked and gender == "M":
            call njalLessDealsBuried
        "Zjistila jsem, že vaše problémy s materiálem byly jen výsledek nedorozumění." if "confession" in rumelin.asked and "less deals solved" not in njal.asked and "less deals buried" not in njal.asked and gender == "F":
            call njalLessDealsBuried
        "Mohl bych vidět vaše rozdělané boty?" if "own work" in njal.asked and "show work" not in njal.asked and gender == "M":
            call njalShowWork
        "Mohla bych vidět vaše rozdělané boty?" if "own work" in njal.asked and "show work" not in njal.asked and gender == "F":
            call njalShowWork
        "Nechtěl byste se na dokončení vašeho díla na slavnosti spojit s mistrem Heinrichem?" if "own work" in njal.asked and "plan B" in clues and "join forces" not in njal.asked and "join forces clueless" not in njal.asked:
            hide mcPic
            if "burned evidence" in clues and "shoes description" in clues:
                $ mc.say("Pokud váš výrobek ještě není hotový a ten jeho byl nejspíš zničený...")
            else:
                $ mc.say("Pokud váš výrobek ještě není hotový a ten jeho se stále nepodařilo najít...")
            if "stolen idea" not in clues:
                $ njal.asked.append("join forces clueless")
                $ njal.say("Já své boty dokončit stihnu. A i kdybych se s někým spojit potřeboval, určitě bych nešel zrovna za Heinrichem.", "angry")
                $ mc.say("Máte spolu nějaké spory?")
                $ njal.say("Nemohl bych se spolehnout na to, že si nebude uzurpovat veškeré zásluhy.")
            else:
                $ njal.asked.append("join forces")
                $ njal.say("Já své boty dokončit stihnu. Proč bych měl pomáhat člověku, který se chtěl chlubit mými schopnostmi?", "angry")
                call njalJoinForces
        "Chápu vaše výhrady, ale stejně si myslím, že spolupráce s mistrem Heinrichem by mohla velmi pomoci vám oběma." if "join forces clueless" in njal.asked and "stolen idea" in clues and "join forces" not in njal.asked:
            hide mcPic
            $ njal.asked.append("join forces")
            $ njal.say("Pak mi budete muset vysvětlit vaše důvody. Na mne to pořád působí jen jako pomoc někomu, kdo si ji nezaslouží.", "angry")
            call njalJoinForces
        "Eckhard byl zatčený za krádež vašeho střihu a čeká na soud." if "join forces njal pending" in status and eckhard in cells and "stolen idea" in eckhard.arrestReason:
            hide mcPic
            if "Zeran accused" in njal.asked:
                if gender == "M":
                    $ njal.say("Neříkal jste předtím, že Zeran...")
                else:
                    $ njal.say("Neříkala jste předtím, že Zeran...")
                $ njal.say("Ale samozřejmě to velmi rád slyším, už jsem nečekal, že se jakékoliv spravedlnosti dočkám.", "happy")
                $ njal.say("Samozřejmě pokud nezklame soudce.")
            else:
                $ njal.say("To velmi rád slyším, už jsem nečekal, že se jakékoliv spravedlnosti dočkám.", "happy")
                $ njal.say("Samozřejmě pokud nezklame soudce...")
            $ mc.say("Co si o spolupráci s mistrem Heinrichem myslíte teď?")
            $ njal.say("Pokud za mnou přijde s návrhem, rozhodně se nad tím zamyslím.")
            $ status.remove("join forces njal pending")
            $ status.append("join forces njal approves")
            if "join forces victim approves" in status:
                if not achievement.has(achievement_name['jointMasterpiece'].name):
                    $ Achievement.add(achievement_name['jointMasterpiece'])
        "Zeran byl zatčený za krádež vašeho střihu a čeká na soud." if "join forces njal pending" in status and zeran in cells and "stolen idea" in zeran.arrestReason:
            hide mcPic
            if "Eckhard accused" in njal.asked:
                if gender == "M":
                    $ njal.say("Neříkal jste předtím, že Eckhard...")
                else:
                    $ njal.say("Neříkala jste předtím, že Zeran...")
                $ njal.say("Ale samozřejmě to velmi rád slyším, už jsem nečekal, že se jakékoliv spravedlnosti dočkám.", "happy")
                $ njal.say("Samozřejmě pokud nezklame soudce.")
            else:
                $ njal.say("To velmi rád slyším, už jsem nečekal, že se jakékoliv spravedlnosti dočkám.", "happy")
                $ njal.say("Samozřejmě pokud nezklame soudce...")
            $ mc.say("Co si o spolupráci s mistrem Heinrichem myslíte teď?")
            $ njal.say("Pokud za mnou přijde s návrhem, rozhodně se nad tím zamyslím.")
            $ status.remove("join forces njal pending")
            $ status.append("join forces njal approves")
            if "join forces victim approves" in status:
                if not achievement.has(achievement_name['jointMasterpiece'].name):
                    $ Achievement.add(achievement_name['jointMasterpiece'])
        "Přiznám se, že jsem nečekal, že podivín pracující na různých vylepšeních bude zrovna trpaslík." if "guild relations" in nirevia.asked and "traditions" not in njal.asked and gender == "M":
            hide mcPic
            $ njal.asked.append("traditions")
            call traditions
        "Přiznám se, že jsem nečekala, že podivín pracující na různých vylepšeních bude zrovna trpaslík." if "guild relations" in nirevia.asked and "traditions" not in njal.asked and gender == "F":
            hide mcPic
            $ njal.asked.append("traditions")
            call traditions

        "Mohl bych ještě mluvit s vaším učedníkem?" if gerdOptionsRemaining > 0 and gender == "M":
            hide mcPic
            " Njal kývne na chlapce, který se celou dobu držel kus stranou a snažil se na sebe neupozorňovat."
            jump gerdController
        "Mohla bych ještě mluvit s vaším učedníkem?" if gerdOptionsRemaining > 0 and gender == "F":
            hide mcPic
            " Njal kývne na chlapce, který se celou dobu držel kus stranou a snažil se na sebe neupozorňovat."
            jump gerdController
        "To je všechno, na co jsem se chtěl zeptat. Děkuji za váš čas." if gender == "M":
            hide mcPic
            $ njal.say("Jsem rád, že jsem mohl všechno uvést na pravou míru.")
            if "less deals" in njal.asked:
                $ njal.say("A jestli zjistíte víc o těch mých obchodech, rozhodně mě to zajímá.")
            return
        "To je všechno, na co jsem se chtěla zeptat. Děkuji za váš čas." if gender == "F":
            hide mcPic
            $ njal.say("Jsem rád, že jsem mohl všechno uvést na pravou míru.")
            return
    jump njalOptions

label leavingNjal:
    if race == "dwarf" and time.hours > 17 and njal.trust > -1 and "dinner with Njal" not in dailyStatus:
        $ njal.say("Nedáte si s námi večeři? Trpaslíků v Marendaru moc nežije, vždycky si rád popovídám s někým, kdo zná staré ságy.", "happy")
    elif time.hours > 17 and njal.trust > 2 and "dinner with Njal" not in dailyStatus:
        $ njal.say("Nedáte si s námi večeři?", "happy")
    else:
        $ njal.say("Hodně štěstí ve vašem vyšetřování.")
        if "less deals" in njal.asked and "less deals solved" not in njal.asked and "less deals buried" not in njal.asked:
            $ njal.say("A jestli zjistíte víc o těch mých obchodech, rozhodně mě to zajímá.")
        return

    show mcPic at menuImage
    menu:
        "Velmi rád." if gender == "M":
            hide mcPic
            call njalDinnerAccepted
        "Velmi ráda." if gender == "F":
            hide mcPic
            call njalDinnerAccepted
        "Bohužel už jsem jedl." if any("dinner with" in str for str in dailyStatus) and gender == "M":
            hide mcPic
            call njalDinnerRefused
        "Bohužel už jsem jedla." if any("dinner with" in str for str in dailyStatus) and gender == "F":
            hide mcPic
            call njalDinnerRefused
        "Bohužel se nemůžu zdržet.":
            hide mcPic
            call njalDinnerRefused
        "Myslel jsem, že tradice odmítáte." if race == "dwarf" and gender == "M":
            hide mcPic
            $ njal.say("Odmítám si jimi nechat diktovat život. Co rozhodně neodmítám, je můj národ.")
            $ njal.say("I když je pravda, že žít uprostřed něj, vidím to možná jinak.")
            show mcPic at menuImage
            menu:
                "V tom případě rád přijímám.":
                    hide mcPic
                    call njalDinnerAccepted
                "Bohužel už jsem jedl." if any("dinner with" in str for str in dailyStatus):
                    hide mcPic
                    call njalDinnerRefused
                "Bohužel se nemůžu zdržet.":
                    hide mcPic
                    call njalDinnerRefused
        "Myslela jsem, že tradice odmítáte." if race == "dwarf" and gender == "F":
            hide mcPic
            $ njal.say("Odmítám si jimi nechat diktovat život. Co rozhodně neodmítám, je můj národ.")
            $ njal.say("I když je pravda, že žít uprostřed něj, vidím to možná jinak.")
            show mcPic at menuImage
            menu:
                "V tom případě ráda přijímám.":
                    hide mcPic
                    call njalDinnerAccepted
                "Bohužel už jsem jedla." if any("dinner with" in str for str in dailyStatus):
                    hide mcPic
                    call njalDinnerRefused
                "Bohužel se nemůžu zdržet.":
                    hide mcPic
                    call njalDinnerRefused

    $ njal.say("Hodně štěstí ve vašem vyšetřování.")
    if "less deals" in njal.asked and "less deals solved" not in njal.asked and "less deals buried" not in njal.asked:
        $ njal.say("A jestli zjistíte víc o těch mých obchodech, rozhodně mě to zajímá.")
    return

###

label njalDinnerAccepted:
    "Posadíš se ke stolu spolu s Njalem a Gerdem a v družném hovoru povečeříte hustou polévku s chlebem."
    $ dailyStatus.append("dinner with Njal")
    call dinnerAchievementCheck
    $ time.addHours(2)
    show bg njal inside
    with Fade(0.5, 1.0, 0.5)
    return

label njalDinnerRefused:
    "Njal trochu zklamaně pokrčí rameny."
    $ njal.say("Tak snad jindy.")
    return

label workshopVisitNjal:
    if "workshop visit" not in gerd.asked:
        $ mc.say("Co tam dělal?")
        $ njal.say("Vyzvedával tam můj majetek, který mi byl ukraden.")
        $ mc.say("Můžete to nějak vysvětlit?")
        $ njal.say("Asi před dvěma měsíci jsem dokončil střih na dámské boty, které by byly zároveň velmi jemné a vzdušné a zároveň pohodlné a dostatečně pevné. Propracovaný způsob šněrování... strávil jsem na tom hodně času a spotřeboval množství materiálu, než jsem vše dovedl k dokonalosti.")
        $ njal.say("Pak se ten střih ztratil z mé dílny a před dvěma týdny jsem se od Gerda dozvěděl, že Heinrich přesně na těchto botách pracuje a chce je představit na Einionových slavnostech.")
    else:
        $ njal.say("Bohužel jsem v tu chvíli neviděl jinou možnost, jak bezpečně získat zpátky svůj majetek ještě před Einionovými slavnostmi.")
        $ mc.say("Myslíte váš střih na boty?")
        $ njal.say("Ano. Strávil jsem na něm hodně času a spotřeboval množství materiálu, než jsem vše dovedl k dokonalosti. Pak se ten střih ztratil z mé dílny a před dvěma týdny jsem se od Gerda dozvěděl, že Heinrich přesně na těchto botách pracuje.")
    $ clues.append("stolen idea")
    return

label njalLessDealsSolved:
    $ njal.trust += 3
    $ njal.say("Takže jeho řešení bylo znemožnit to skutečnému autorovi a Heinricha nechat být?", "angry")
    show mcPic at menuImage
    menu:
        "Bál se skandálu, který by ublížil celému cechu, a nedokázal to řešit lépe.":
            hide mcPic
            $ njal.trust -= 2
            "Mistr Njal se zamračí, ale první reakci zřejmě spolkne."
            $ njal.say("No dobře. Ale jestli neskončí u soudu, pak se aspoň postarám, aby přišel o místo cechmistra. Kazit poctivou práci…", "angry")
            $ njal.say("Máte ještě něco?", "angry")
        "Hodláme s ním zahájit proces a budeme rádi, pokud budete svědčit.":
            hide mcPic
            $ njal.trust += 1
            $ njal.say("To samozřejmě budu. Kazit poctivou práci, za to by ho měli proklít jeho předci i potomci po deset generací.", "angry")
    return

label njalLessDealsBuried:
    hide mcPic
    $ njal.asked.append("less deals buried")
    $ njal.trust -= 1
    $ njal.say("Nedorozumění? Tak to mě opravdu zajímá.")
    $ mc.say("Cechmistr Rumelin chtěl objednat materiál pro celý cech najednou, jenom to zřejmě nedokázal dostatečně vysvětlit obchodníkům.")
    $ njal.say("To se mi úplně nezdá. Proč potom nepřišel osobně?")
    $ mc.say("Možná měl příliš práce. V každém případě tady nikde nebyl zlý úmysl.")
    $ njal.say("Pokud je tohle výsledek vašeho pátrání…")
    return

label njalShowWork:
    hide mcPic
    $ njal.asked.append("show work")
    "Mistr Njal překvapeně pozvedne obočí."
    $ njal.say("Kvůli vašemu vyšetřování, nebo z jiných důvodů?")
    show mcPic at menuImage
    menu:
        "Jen mne velmi zajímá vaše práce.":
            hide mcPic
            $ njal.say("Takových bylo v poslední době víc a jeden z nich mi dokonce ukradl můj střih.", "angry")
            $ njal.say("Nezlobte se, ale jen kvůli zájmu svůj proces nikomu ukazovat nebudu.")
        "Potřebuji vědět, jak mohly vypadat ty ukradené.":
            hide mcPic
            $ mc.say("Mistr Heinrich se mi je sice pokusil popsat, ale na boty opravdu nejsem odborník. Čím lepší představu budu mít, tím větší šance, že si všimnu něčeho podezřelého.")
            if njal.trust > 0:
                $ njal.say("To vlastně dává smysl.")
                "Mistr Njal tě dovede ke svému pracovnímu stolu. \nJeho boty budou tmavě zelené a ještě nejsou ani zdaleka došité, ale už teď si můžeš udělat představu o jejich budoucím tvaru."
                $ mc.say("Moc vám děkuji, tohle mi velmi pomůže.")
                $ status.append("WIP shoes seen")
            else:
                $ njal.say("Nezlobte se, ale svůj postup výroby ukazuji jen v opravdu nutných případech. A tenhle konkrétní střih se mi už pokusili ukrást.")
    return

label njalJoinForces:
    if "rumelin exposed" in status:
        show mcPic at menuImage
        menu:
            "Celý cech by to pochopil jako reakci na cechmistrovy špinavé machinace." if "rumelin exposed" in status:
                hide mcPic
                $ njal.trust -= 1
                $ njal.say("Další cechovní politika? Raději bych se věnoval kvalitní práci než zbytečným konfliktům.", "angry")
                $ njal.say("Bude mi stačit, když Rumelin skončí u soudu.", "angry")
            "Protože jeho schopnosti by mohly ty vaše nechat ještě více vyniknout.":
                hide mcPic
                jump njalJoinForcesReason
    else:
        $ mc.say("Protože jeho schopnosti by mohly ty vaše nechat ještě více vyniknout.")
        label njalJoinForcesReason:
        $ mc.say("Myslím, že není způsob, jak by v tomto městě mohlo vzniknout dokonalejší dílo.")
        "Mistr Njal se zamyslí a na chvíli máš pocit, že se chystá souhlasit. Pak se ale zamračí."
        $ njal.say("Jen aby se Heinrich zase nepokusil si mé schopnosti přivlastnit.", "angry")
        $ njal.say("Neříkám, že by ta spolupráce nemohla být výhodná… ale to by musel Heinrich přijít sám a s upřímnou omluvou.")
        $ njal.say("Do té doby mu nevidím důvod pomáhat a hlavně mu nemůžu důvěřovat.")
    $ njal.say("A vůbec... neměl by jít Heinrich sám k soudu za krádež mého střihu?")
    show mcPic at menuImage
    menu:
        "A co kdyby ten soud proběhl, změnilo by to váš názor?":
            hide mcPic
            $ njal.say("Asi ano, ale to se uvidí, až k tomu dojde.")
        "Váš střih pro mistra Heinricha ukradl Eckhard." if "stolen idea" in victim.asked and not (eckhard in cells and "stolen idea" in eckhard.arrestReason):
            hide mcPic
            $ njal.asked.append("Eckhard accused")
            $ mc.say("Heinrich ho nejdřív ani nechtěl přijmout.")
            $ njal.say("Pak by měl být potrestán aspoň Eckhard.", "angry")
        "Váš střih pro mistra Heinricha ukradl jeho bývalý učedník Zeran." if zeran.alreadyMet == True and not (zeran in cells and "stolen idea" in zeran.arrestReason):
            hide mcPic
            $ njal.asked.append("Zeran accused")
            $ mc.say("Heinrich ho nejdřív ani nechtěl přijmout.")
            $ njal.say("Pak by měl být potrestán aspoň Zeran.", "angry")
        "Váš střih pro mistra Heinricha ukradl Eckhard, který teď čeká na soud." if eckhard in cells and "stolen idea" in eckhard.arrestReason:
            call njalGetsSatisfaction
        "Váš střih pro mistra Heinricha ukradl jeho bývalý učedník Zeran, který teď čeká na soud." if zeran in cells and "stolen idea" in zeran.arrestReason:
            call njalGetsSatisfaction
    if "join forces njal approves" not in status:
        $ njal.say("O jakékokoli spolupráci budu uvažovat, pokud dostanu aspoň nějakou spravedlnost. Do té doby by to byla jen urážka mé práce.")
        $ status.append("join forces njal pending")
    return

label njalGetsSatisfaction:
    hide mcPic
    $ njal.say("Opravdu? Velmi rád slyším, že tu krádež bere konečně někdo vážně, už jsem ani nedoufal, že se tu dočkám jakékoliv spravedlnosti.", "surprised")
    $ njal.say("Samozřejmě pokud nezklame soudce...")
    $ mc.say("Mistr Heinrich původně střih ani nechtěl přijmout...")
    $ njal.say("Tak ho přijímat nemusel, ale pokud říkáte, že ho aspoň neukradl on sám... a že zloděj jde k soudu...")
    $ njal.say("Možná by nějaký druh spolupráce opravdu stál za úvahu. Pokud Heinrich přijde s návrhem, zamyslím se nad tím.")
    $ status.append("join forces njal approves")
    return

label traditions:
    "Njal se zamračí."
    if race == "dwarf":
        $ njal.say("Budeš mi taky vysvětlovat trpasličí tradice? Nebo popisovat zoufalství mých úctyhodných předků?", "angry")
        show mcPic at menuImage
        menu:
            "Naše tradice jsou to, co nás pojí s předky a domovem.":
                hide mcPic
                $ njal.trust -= 2
                $ personality.append("traditionalist")
                $ njal.say("Ale svět kolem nás se mění, copak naši předci chtějí, abychom zůstali uvízlí v minulosti? Správný mistr taky doufá, že ho jeho žák jednou předčí.", "angry")
                $ njal.say("No, pokud vám to nevadí, radši bych změnil téma. Můžu s vaším vyšetřováním pomoct ještě nějak?")
            "Vůbec ne, předkům dělá největší radost a čest náš dobrý a spokojený život.":
                hide mcPic
                $ njal.trust += 2
                $ personality.append("nonconformist")
                $ njal.say("Sám bych to neřekl líp! Na to si se mnou musíš připít.", "happy")
                "Můžeš se snažit odmítat, ale nakonec stejně skončíš s pohárem v ruce."
                $ njal.say("Na dobrý a spokojený život! A na změnu!", "happy")
    else:
        $ njal.trust -= 1
        if race == "elf":
            $ njal.say("A já jsem zase nečekal, že podobné otázky uslyším i od elfa. Nežijeme všichni v minulosti.", "angry")
        elif race == "hobbit":
            $ njal.say("A já jsem zase nečekal, že podobné otázky uslyším i od hobita. Nežijeme všichni v minulosti.", "angry")
        else:
            $ njal.say("A já jsem zase nečekal, že podobné otázky uslyším i od člověka. Nežijeme všichni v minulosti.", "angry")
        $ mc.say("Omlouvám se, asi to vyznělo špatně.")
        show mcPic at menuImage
        menu:
            "Jenom mě to překvapilo, trpasličí úctu k tradicím jsem vždycky obdivoval." if gender == "M":
                hide mcPic
                $ personality.append("traditionalist")
                $ njal.say("Já myslím, že by se nic nemělo obdivovat nekriticky. Ale je možné, že zvenku trpasličí tradice působí jinak, než když v nich člověk přímo žije.")
            "Jenom mě to překvapilo, trpasličí úctu k tradicím jsem vždycky obdivovala." if gender == "F":
                hide mcPic
                $ personality.append("traditionalist")
                $ njal.say("Já myslím, že by se nic nemělo obdivovat nekriticky. Ale je možné, že zvenku trpasličí tradice působí jinak, než když v nich člověk přímo žije.")
            "Také chci spíš hledat nové cesty než chodit po těch nejvyšlapanějších.":
                hide mcPic
                $ njal.trust += 2
                $ personality.append("nonconformist")
                $ njal.say("Myslím, že takových lidí je potřeba co nejvíc. Gernlinden se mění a my bychom to měli vzít jako příležitost změnit se také. Nechat si z minulosti jenom to nejlepší a posunout se dál.", "happy")
            "Mám představu, jak nepříjemný tlak jste asi musel překonat." if race == "elf" or race == "hobbit":
                hide mcPic
                "Mistr Njal se na tebe podívá s novým zájmem."
                $ njal.say("Osobní zkušenost?")
                show mcPic at menuImage
                menu:
                    "Ano, ale odmítám si nechat od rodiny cokoli diktovat.":
                        hide mcPic
                        $ njal.trust += 2
                        $ personality.append("nonconformist")
                        $ njal.say("Tak to přeji silnou vůli a úspěšný boj. Musíš si na to se mnou připít.", "happy")
                        "Můžeš se snažit odmítat, ale nakonec stejně skončíš s pohárem v ruce."
                        $ njal.say("Na dobrý a spokojený život! A na změnu!")
                    "Moje rodina je naštěstí spíš umírněná, ale tlak okolí stačí.":
                        hide mcPic
                        $ njal.trust += 1
                        $ personality.append("nonconformist")
                        $ njal.say("To máš větší štěstí než já. Odešel jsem dokonce z Altenbüren a oni pořád doufají, že se vrátím ke všem jejich tradicím...")
                        "Mistr Njal mávne rukou."
                        $ njal.say("Podle mě je hlavní dobře a spokojeně žít. Naše předky to potěší nejvíc a ty, kdo by nám to třeba nepřáli, nic nenaštve víc.")
                    "Já podle našich tradic žít chci, ale měla by to být volba.":
                        hide mcPic
                        $ njal.trust += 1
                        $ personality.append("traditionalist")
                        $ njal.say("Každému co jeho jest, to říkám já. Kdyby to tak chápali všichni...")
                        "Mistr Njal mávne rukou."
    if gender == "M":
        $ njal.say("Ale určitě ses sem nepřišel bavit o tomhle. Můžu pomoct ještě s něčím?")
    else:
        $ njal.say("Ale určitě ses sem nepřišla bavit o tomhle. Můžu pomoct ještě s něčím?")
    return

label njalOptionsRemainingCheck:
    $ njalOptionsRemaining = 0
    if "fired apprentices" in clues and "which apprentice" in liese.asked and "told njal" not in gerd.asked and "workshop visit" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "told njal" in gerd.asked and "workshop visit" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "workshop visit" in njal.asked and "police business" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "police business" in njal.asked and "suspicion" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "suspicion" in njal.asked and "information source" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "workshop visit" in njal.asked and "did anything else" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "workshop visit" in njal.asked and "why not go himself" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "less deals" in salma.asked and "less deals" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "less deals" in njal.asked and "less deals details" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "guild relations" in nirevia.asked and "traditions" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "apprentices" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "less deals" in njal.asked and "own work" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "confession" in rumelin.asked and "stolen idea" not in clues and "less deals solved" not in njal.asked and "less deals buried" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "confession" in rumelin.asked and "Stolen idea" in clues and "less deals solved" not in njal.asked and "less deals buried" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "confession" in rumelin.asked and "less deals solved" not in njal.asked and "less deals buried" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "own work" in njal.asked and "show work" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "own work" in njal.asked and "plan B" in clues and "join forces" not in njal.asked and "join forces clueless" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "join forces clueless" in njal.asked and "stolen idea" in clues and "join forces" not in njal.asked:
        $ njalOptionsRemaining += 1
    if "join forces njal pending" in status and eckhard in cells and "stolen idea" in eckhard.arrestReason:
        $ njalOptionsRemaining += 1
    if "join forces njal pending" in status and zeran in cells and "stolen idea" in zeran.arrestReason:
        $ njalOptionsRemaining += 1
    return
