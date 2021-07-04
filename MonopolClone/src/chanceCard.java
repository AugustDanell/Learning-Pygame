public class chanceCard {
    private int cardNumber;

    /* setCardNumber()
     * a setter function that sets the id number of a certain card.
     */
    public void setCardNumber(int n){
        cardNumber = n;
    }

    /* readCard()
    *  Returns the textstring of a card so that it might be displayed on the GUI.
    *  NOTE: ' is used by a helper function to discern where one should make a new space.
    */
    public String readCard(){
        switch (cardNumber){
            case 1:
                return "Pressbyrån har anfört dig'ett erbjudande du inte'kan motstå.'Betala 500kr för'Pressbyråns soylentkorvar.";
            case 2:
                return "Nämen se vad som ligger där!'Fru Fortuna med dig är!'Du ser 2000kr någon'har glömt på'Hallstavikbussen 641.'Inkassera 2000kr.";
            case 3:
                return "Ett gäng gymnasiumelever,'ledda av en otäcking'som kallar sig Bulten ser dig.' De ämnar att råna dig,'du kan antingen stå över en tur'" +
                        "och spöa bulten och'hans vänner (Val A) eller'så kan du'betala dem 4000kr (Val B)'";
            case 4:
                return "Willys har specialerbjudande'på Munkar, bege dit'omgående.Passerar'du Start får du pengarna.'Betala 500kr för'delikatessmunkar i finaste'choklad och vaniljkräm.";
            case 5:
                return "En isländsk man som kallar'sig Babthor Bartorsson behöver'din hjälp. Babthor behöver'gå om gymnasiet'och vill hitta vägen'till Roden(gymnasiet).'" +
                        "Du kan(A) hjälpa'honom, varvid ni direkt'går till Roden och han'skänker dig 1000 kr'från sitt välmående'företag Darklordz AB.'" +
                        "Alternativt kan du välja'val(B) att inte göra någonting.'Vill du hjälpa Babthor?,'Ja (A) eller Nej (B).";
            case 6:
                return "Du parkerade för ett tag sedan utan försyn som en handikappad utanför Kryddan (På handikappsparkering).'Nu måste du böta för ditt misstag!' Betala 2000kr";
            case 7:
                return "En attraktiv hunk utan'tröja från Örebro har snott'din pojk/- flickvän. Om du'gymmar med hunken släpper'han partnern din fri.Gå direkt' till närmsta gym!''(Obs, avstånd är i vilken' riktning som helst, dvs'dubbelriktat)";
            case 8:
                return "Du ser en vacker kvinna.'Vill du ta ut henne på en dejt' till spel och sånt?'Dejten kostar 500kr och tar dig'direkt till spel och sånt'utan att passera start.''Val(A) : Dejt'Val(B) : Nej tack";
            case 9:
                return "Efter att ha sprungit i 10 timmar'är du nu ganska trött och du vill'ha en kebabpizza med extra allt' betala 1500kr för hela kalaset,' ty vad vore pizza utan sprit, tänker'du. ymStå sedermera över 2 rundor pga'extrem bakfylla.";
            case 10:
                return "Du lagar makaroner hemma och'ditt hjärta hoppar upp liksom'du druckit 18 redbull,'ty du ser boken \"My First Rectal Exam\".'Du inser att du har glömt att'lämna tillbaka din bok,'Spring genast till Norrtälje bibliotek!";
            case 11:
                return "Som den skattesmitaren du är'har du annordnat en plan för'att undvika din nästa betalning av hyra.'Hamnar du på en annan spelares'ruta, undvik att betala denne.'Gäller endast en gång!";
            case 12:
                return "Du känner en äcklig odör och'du inser att det kommer från'något klet som fastnat på dina kläder sen'sist du åkte Rimbobussen.'Skynda dig genast till Nordic Wellness City'för att dölja den vidriga odören i ditt'egna svett medans du samtidigt gör GAINS.'Inkassera om du passerar start.";
            case 13:
                return "Inkvottering i bolagsstyrrelsen!'Inkompetenta människor från'Rimbo och Hallstavik har, under'nya regleringar, blivit inkvoterade'till chefsposter.  Betala för'varje tomt 500kr i kostnad'för ineffektivt, inkvoterat styre.";
            case 14:
                return "Din fru har blivit feminist!'Välj mellan att antingen'betala en mansskatt'på 2500 kr, eller att'göra slut med kvinnan'i ditt liv, i vilket'fall du behöver stå'över 2 turomgångar'i sörj över den mentala störning'som tagit din sockerpulla'ifrån dig.''Val(A): Betala 2500kr'Val(B): Stå över 1 runda";
            case 15:
                return "Spelnörden som går under' användarnamnet'\"Aggebagge\"'bjuder in dig till ett lan'hos \"Spel och Sånt\".'Aggebagge, som han kallar sig'är psykiskt labil och om du'inte kommer kommer han'i sin tur att kleta någonting'äckligt på ditt hus, har han sagt.'Du vågar inte riskera detta'så du beger dig till \"spel och sånt\"'samt står över en runda pga LAN'med \"Aggebagge\".";
                default: return "";
        }
    }

    /* effectOfCard()
     * Stores the effect of drawing a card with a certain index.
    */
    public void effectOfCard(player p){
        switch (cardNumber) {
            case 1:     p.pay(500);
            case 2:     p.recieve(2000);
            case 3:     p.pay(0);           // TODO: Fixa choice cases + Timer
            case 4:
                if(p.getPosition() > 6){
                    p.recieve(4000);
                }
                p.pay(500);
                p.setPosition(6);
            case 5:     p.pay(0);           // TODO choice case
            case 6:     p.pay(2000);
            case 7:     if(p.getPosition() == 7)
                            p.setPosition(16);
                        else
                            p.setPosition(20);

            case 10:
                if(p.getPosition() > 17)
                p.recieve(4000);
                p.setPosition(17);
            case 11: p.setShield(1);
            case 12:
                if(p.getPosition() > 16)
                p.recieve(4000);
                p.setPosition(16);
            case 13: p.pay(p.getOwnedProperties()*500);
            case 15:
                p.setPosition(15);
                p.passTurn(1);
        }

    }

    public void firstEffect(player p){
        switch (cardNumber){
            case 3: p.passTurn(1);
            case 5:
                p.recieve(1000);
                p.setPosition(3);
            case 14: p.pay(2500);
        }
    }

    public void secondEffect(player p){
        switch (cardNumber){
            case 3: p.pay(4000);
            case 5: // Do nothing :)
            case 14: p.passTurn(2);
        }
    }

    public int getCardNumber(){
        return cardNumber;
    }

    public boolean choiceCard(){
        switch (cardNumber){
            case 3: return true;
            case 5: return true;
            case 14: return true;
            default: return false;
        }
    }
}

