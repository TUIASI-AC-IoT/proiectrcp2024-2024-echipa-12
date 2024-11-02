# Controlul fluxului prin intermediul unui protocol cu fereastră glisantă.

### • Protocolul UDP (User Datagram Protocol)
UDP este un protocol de comunicare utilizat pentru aplicațiile time-sensitive.

**Modul în care funcționează:**
Protocolul UDP este o metodă standard de transmitere a informației între două calculatoare. Transmiterea pachetelor se face direct către computer-ul țintă fără a stabili înainte o conexiune fermă cu acesta, fără a indica ordinea pachetelor și fără a aștepta un răspuns de la țintă înainte de a trimite un nou pachet.

**Header**
Header-ul UDP-ului este format din 8 octeți:
-  **Source Port** (2 octeți) - utilizați pentru a identifica numărul portului sursă;
-  **Destination Port** (2 octeți) - utilizați pentru a indentifica portul  destinație;
-  **Lungimea** (2 octeți) - incluzând atât header-ul, cât și datele;
-  **Checksum** (2 octeți) - nu este obligatorie la protocolul UDP.

<p style="text-align:center">
<img src="https://hackmd.io/_uploads/HJbVDW4WJx.png" style="position:absolute; transform:translate(50%)">
</p>

**Avantaje:**
- viteză și eficiență;
- util priviind operațiile la care pierderea unor informații este insesizabilă (ex. streaming, real-time multiplayer games, etc.);
- cost scăzut de implementare;
- pachete mai mici decât ale altor protocoale (ex. TCP);
- are un design simplificat față de alte protocoale (ex. TCP).

**Dezavantaje:**
- pierderea de informație;
- nu se garantează ordinea corectă a pachetelor trimise;
- vulnerabilități la anumite tipuri de atacuri;
- cazuri limitate de utilizare: nu poate fi folosit pentru aplicații care nu tolerează pierderea de date (ex. transfer de date, trimitere de email-uri, etc.).


### • Fereastra Glisanta




### • Bibliografie
* https://www.geeksforgeeks.org/user-datagram-protocol-udp/
* https://www.fortinet.com/resources/cyberglossary/user-datagram-protocol-udp
* https://pcom.pages.upb.ro/notite-cb/curs7/curs.html
