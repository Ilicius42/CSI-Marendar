label evidenceWall:
    call seeMeNoteCheck
    scene bg evidencewall
    $ noteInformation = ""
    $ chosenLocation = ""
    $ leaveOption = "normal"
    $ chosenChar = renpy.call_screen("evidenceWallScreen", _layer="screens")
    call expression chosenChar + "Notes" # load character specific info
    call displayNotes # show character specific info and give option to visit

    if "arrest in progress" in status:
        jump arrest

    call interludeController # check if something happens before returning to station
    jump evidenceWall # go back to evidence wall for next suspect choice

###

label seeMeNoteCheck:
    if "waiting for suspect list" in status:
        $ seeMeNote = True
    elif "investigating less deals" in status:
        $ seeMeNote = True
    elif "awaiting AML merchant list" in status:
        $ seeMeNote = True
    elif time.hours > 16 and "report given" not in dailyStatus:
        $ seeMeNote = True
    else:
        $ seeMeNote = False
    return

label prisonerCheck():
    python:
        returnValue = False
        if cells:
            for prisoner in cells:
                if prisoner.code == chosenChar:
                    returnValue = True
    return returnValue

label seeMeNotes:
    $ noteInformation = ""

    $ chosenLocation = "guardhouseAgain"
    return

label apprentice1Notes:
    $ noteInformation = "Učedník mistra Heinricha. "

    $ chosenLocation = "victimHouseholdController"
    return

label apprentice2Notes:
    $ noteInformation = "Učedník mistra Heinricha. "

    $ chosenLocation = "victimHouseholdController"
    return

label erleNotes:
    $ noteInformation = "Náhodná žebračka."
    if "lost bottles" in clues:
        $ noteInformation = "Donesla Salmě lahve odpovídající popisu těch, které se ztratily z domu mistra Heinricha. "

    $ chosenLocation = "erleController"
    return

label kasparNotes:
    $ noteInformation = "Jeden z ševcovských mistrů"
    if "enemies" in victim.asked or "ambitions" in kaspar.asked:
        $ noteInformation +=", který stejně jako Heinrich usiluje o místo hlavy cechu. "
    else:
        $ noteInformation += ". "
    if "secret lover" in nirevia.asked:
        $ noteInformation += "Má blízký vztah s Heinrichovou ženou."

    $ chosenLocation = "kasparController"
    return

label adaNotes:
    $ noteInformation = "Heinrichova čtrnáctiletá dcera. "
    if "fired apprentices offense" in victim.asked or "ruined life" in lisbeth.asked:
        if "proof against Zeran" in victim.asked or "ruined life" in lisbeth.asked:
            $ noteInformation += "Za milostné dopisy pro ni, podepsané písmenem Z "
        else:
            $ noteInformation += "Za údajný vztah k ní "
        $ noteInformation += "byl vyhozen Zeran, jeden z Heinrichových učedníků. "

    $ chosenLocation = "victimHouseholdController"
    return

label gerdNotes:
    if "fired apprentices" not in clues:
        $ noteInformation = "Učedník mistra Njala. "
    else:
        $ noteInformation = "Heinrichův bývalý učedník, teď u mistra Njala. "
        if "fired apprentices offense" in victim.asked or "fired apprentices" in lisbeth.asked:
            $ noteInformation += "Vyhozený, protože měl moc vlastní hlavu. "
            if "workshop visit" in gerd.asked or "workshop visit" in njal.asked:
                $ noteInformation += " V noc krádeže z Heinrichovy odemčené dílny odnesl Njalův ukradený střih na boty"
                if "forced drawer" in gerd.asked:
                    $ noteInformation += ", vylomil kvůli tomu zásuvku u stolu. "
                else:
                    $ noteInformation += ". "

    $ chosenLocation = "njalHouseController"
    return

label zeranNotes:
    $ noteInformation = "Heinrichův bývalý učedník, teď bez mistra v dočasné čtvrti. "
    if "fired apprentices offense" in victim.asked or "ruined life" in lisbeth.asked:
        $ noteInformation += "Vyhozený za údajné svádění Heinrichovy dcery Ady. "
    if "fired apprentices" in rumelin.asked:
        $ noteInformation += " Prý se dal do špatné společnosti. "

    $ chosenLocation = "sabriHouseholdController"
    return

label eckhardNotes:
    $ noteInformation = "Přítel mistra Heinricha."
    if "Eckhard" in clues:
        $ noteInformation += " Byl s ním včera v hospodě U Salmy"
        if "forgotten key" in clues:
            $ noteInformation += ", zapomněl mu vrátit klíč od dílny a měl ho celou noc u sebe. "
        else:
            $ noteInformation += "."
    if "suspicion" in njal.asked:
        $ noteInformation += " Chtěl od mistra Njala koupit střih na boty, který mu pak byl ukraden. "

    $ chosenLocation = "eckhardController"
    return

label rumelinNotes:
    $ noteInformation = "Hlava cechu ševců a obuvníků. S Heinrichem se pohádal v hospodě"
    if "pub fight topic" in clues:
        $ noteInformation += " o tom, jaké vlastnosti by měl mít cechmistr vzhledem ke svým povinnostem. "
    else:
        $ noteInformation += ". "
    if "AML" in lotte.asked:
        $ noteInformation += " Pokusil se znemožnit mistru Njalovi sehnat materiál na jeho vlastní výrobek na slavnosti"
        if "confession" in rumelin.asked:
            $ noteInformation += ", protože měl být stejný jako Heinrichův. "
        else:
            $ noteInformation += ". "

    $ chosenLocation = "rumelinController"
    return

label nireviaNotes:
    $ noteInformation = "Manželka cechmistra Rumelina. "

    $ chosenLocation = "nireviaController"
    return

label rovienNotes:
    $ noteInformation = "Bratr cechmistra Rumelina a obchodník s kvalitními látkami. "
    if "less deals details" in njal.asked:
        $ noteInformation += " Jeden z obchodníků, kteří "
        if "AML" in lotte.asked:
            $ noteInformation += "podle pokynů cechmistra Rumelina "
        $ noteInformation += "odmítli prodat materiál mistru Njalovi."

    $ chosenLocation = "rovienHouseController"
    return

label zairisNotes:
    $ noteInformation = "Rovienův syn a synovec cechmistra Rumelina. "

    $ chosenLocation = "rovienHouseController"
    return

label njalNotes:
    $ noteInformation = "Jeden z ševcovských mistrů"
    if "workshop visit" in njal.asked or "workshop visit" in gerd.asked:
        $ noteInformation += " a autor střihu, podle kterého Heinrich šil své mistrovské střevíce. "
    else:
        $ noteInformation += ". "
    if "less deals" in salma.asked:
        $ noteInformation += "Poslední dva týdny má problémy s uzavřením obchodu na nákup materiálu"
        if "confession" in rumelin.asked:
            $ noteInformation += ", tím se mu cechmistr Rumelin snažil zabránit v dokončení stejných bot, na kterých pracoval Heinrich. "
        else:
            $ noteInformation += ". "
    if gerdNote.isActive == True:
        $ noteInformation += "Vzal si k sobě jednoho z učedníků, které Heinrich vyhodil. "

    $ chosenLocation = "njalHouseController"
    return

label lotteNotes:
    if "other fights" in salma.asked and "less deals details" not in njal.asked:
        $ noteInformation += "Manželka obchodníka, kterému mistr Heinrich vyčítal dodávku nekvalitního materiálu. "
    elif "less deals details" in njal.asked:
        $ noteInformation += "Její manžel Karsten byl jeden z obchodníků, kteří "
        if "AML" in lotte.asked:
            $ noteInformation += "podle pokynů cechmistra Rumelina "
        $ noteInformation += "odmítli prodat materiál mistru Njalovi. "
        if "other fights" in salma.asked:
            $ noteInformation += "Mistr Heinrich se s jejím manželem někdy před krádeží pohádal o kvalitu dodaného materiálu. "
    if lotte.alreadyMet == True:
        $ noteInformation += "Má dům ve stejné ulici jako mistr Heinrich. "
    if "husband" in lotte.asked:
        $ noteInformation += "\nKarsten sám jel pro materiál a není ve městě. "

    $ chosenLocation = "lotteController"
    return

label merchantNotes:
    if "other fights" in salma.asked and "less deals details" not in njal.asked:
        $ noteInformation += "Obchodník, kterému mistr Heinrich vyčítal dodávku nekvalitního materiálu. "
    elif "less deals details" in njal.asked:
        $ noteInformation += "Jeden z obchodníků, kteří "
        if "AML" in lotte.asked:
            $ noteInformation += "podle pokynů cechmistra Rumelina "
        $ noteInformation += "odmítli prodat materiál mistru Njalovi. "
        if "other fights" in salma.asked:
            $ noteInformation += "Mistr Heinrich se s ním někdy před krádeží pohádal o kvalitu dodaného materiálu. "
    if lotte.alreadyMet == True:
        $ noteInformation += "Má dům ve stejné ulici jako mistr Heinrich. "

    $ chosenLocation = "lotteController"
    return

label pubNotes:
    $ noteInformation = "Hospoda, ve které se mistr Heinrich pohádal s cechmistrem Rumelinem."

    $ chosenLocation = "pubController"
    return

label sonNotes:
    $ noteInformation = "Heinrichův patnáctiletý syn se učí řemeslo a jednou po otci převezme dílnu."

    if son in cells:
        $ chosenLocation = "aachimMain"
    else:
        $ chosenLocation = "victimHouseholdController"
    return

label victimNotes:
    $ noteInformation = "Přišel za hlídkou nahlásit krádež svého výrobku na Einionovy slavnosti. "
    $ noteInformation += "Těsně před krádeží se U Salmy pohádal s cechmistrem Rumelinem"
    if "other fights" in salma.asked:
        $ noteInformation += ", o něco dříve s Karstenem o kvalitu dodaného materiálu. "
    else:
        $ noteInformation += ". "
    if "enemies" in rumelin.asked:
        $ noteInformation += "Podle cechmistra Rumelina má nejhorší vztahy uvnitř své dílny a tři učedníky už vyhodil. "
    if kaspar.alreadyMet == True:
        $ noteInformation += "Podle mistra Kaspara má problémy s pitím. "
    if "workshop visit" in njal.asked or "workshop visit" in gerd.asked:
        $ noteInformation += "Střih na jeho ukradené střevíce vytvořil mistr Njal, kterému ho někdo ukradl. "

    $ chosenLocation = "victimHouseholdController"
    return

label lisbethNotes:
    $ noteInformation = "Manželka mistra Heinricha. "
    if "secret lover" in nirevia.asked:
        $ noteInformation += "Má blízký vztah s mistrem Kasparem. "
    elif lotte.alreadyMet == True:
        $ noteInformation += "Podle jedné ze sousedek má tajného milence. "
    $ chosenLocation = "victimHouseholdController"
    return

label workshopNotes:
    $ noteInformation = "Dílna, odkud se přes noc ztratil mistrovský výrobek"
    if "workshop unlocked" in "clues":
        $ noteInformation += " byla pravděpodobně celou noc odemčená."
    elif "no forced entry" in clues:
        $ noteInformation += ". Na dveřích nejsou žádné stopy násilného vniknutí."
    else:
        $ noteInformation += "."
    if "break-in" in clues:
        if "table contents" in workshop.checked:
            $ noteInformation += " Jedna ze zásuvek stolu, ve které jsou složitější nákresy a střihy, je vylomená"
        else:
            $ noteInformation += " Jedna ze zásuvek stolu je vylomená"
        if "forced drawer" in gerd.asked:
            $ noteInformation += ", z ní Gerd odnesl střih na boty patřící mistru Njalovi."
        elif "missing stuff1" in workshop.checked:
            $ noteInformation += ", ale podle mistra nic nechybí."
        else:
            $ noteInformation += "."

    $ chosenLocation = "victimHouseholdController"
    return

label sabriNotes:
    if "why help" in sabri.asked:
        $ noteInformation = "Kněz boha Purushotamy, vede ubytovnu v Dočasné čtvrti."
    else:
        $ noteInformation = "Kněz, který vede ubytovnu v Dočasné čtvrti."

    $ chosenLocation = "sabriHouseholdController"
    return

label libraryNotes:
    $ noteInformation = "Městská knihovna, spravovaná Luisou de Vito."

    $ chosenLocation = "libraryController"
    return

###

label notFinished:
    "DEBUG: To be done"
    return


label displayNotes:
    call prisonerCheck
    show expression ("evidencewall/note [chosenChar].png") at menuImage
    menu:
        "[noteInformation]"
        "Navštívit" if _return == False:
            hide expression ("evidencewall/note [chosenChar].png")
            jump expression chosenLocation
        "Navštívit v cele" if _return == True:
            hide expression ("evidencewall/note [chosenChar].png")
            call cellsController
            jump guardhouseAgain
        "Zpět":
            hide expression ("evidencewall/note [chosenChar].png")
            jump evidenceWall
    return
