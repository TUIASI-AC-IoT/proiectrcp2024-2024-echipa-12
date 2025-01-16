

# Controlul fluxului prin intermediul unui protocol cu fereastră glisantă.
## Prezentare noțiuni teoretice
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

<div align="center">
	<img src=https://hackmd.io/_uploads/HJbVDW4WJx.png>
</div>

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


### ⮚ Controlul Fluxului & Fereastră Glisantă
#### **De ce Controlul Fluxului?**
Dacă dispozitivul care transmite date este rapid/mai puțin încărcat, iar dispozitivul care ar trebui să le recepționeze este mai lent/foarte încărcat și considerăm că transmisia este fără erori, la un moment dat, receptorul nu va reuși să proceseze toate cadrele și va începe să piardpă unele dinre ele. Din acest motiv a apărut mecanismul de control al fluxului.<sup>1</sup>
#### **Prezentare generală** 
**Controlul fluxului** este o metodă de control a ratei de transmisie intre două noduri de rețea.
**Protocol cu fereastră glisantă** - este o tehnică de transmisie a mai multor cadre în acelasi timp care asigură fiabilitatea și transmisia în ordine a acestora.

**Mod de funcționare**
```
             Fereastră(pachete transmise la care se așteaptă confirmare)
                    /                           Pachete care urmează să fie trimse
                +==============+                /
...............||..............||..........................
:  1 :  2 :  3 ||  4 :  5 :  6 ||  7 :  8 :  9 :  10 :  8 : 
...............||..............||..........................
        \       +===============+
         \       
          Pachete trimise pt. care s-a primit confirmare       
```
**Selective Repeat ARQ**
Este un mecanism de tratare a erorilor în care, receptorul acceptă și pune in buffer pachetul de după unul pierdut/care are eroare. Selective repeat încearcă retransmisia doar a pachetelor pierdute.
	


<div align="center">
<img height=600px src=https://hackmd.io/_uploads/SkfwZrjW1g.png>
<br>
	<sup>Modalitate de funcționare selective repeat.</sup>
</div>

## Detalii de implementare


### ⮚ Structura Pachetelor
Pachetul este unitatea de bază a transferului de informație.


```
                                        +-----------+                   +------------------------+
                                        |   DATA    |                   | Aplication Presentation|
                                        +-----------+                   |                        |
                           +-----------++-----------+                   |                        |
                           |UDP HEADER || UDP DATA  |                   |   Session Transport    |
                           +-----------++-----------+                   |                        |
              +-----------++-----------++-----------+                   |                        |
              | IP HEADER ||        IP DATA         |                   |        Network         |
              +-----------++-----------++-----------+                   |                        |
+------------++-----------++-----------++-----------++------------+     |                        |
|FRAME HEADER||              FRAME DATA             ||    FCS     |     |   Data Link Physical   |
+------------++-----------++-----------++-----------++------------+     +------------------------+
```

> Structura detaliată a segmentului de date a pachetului 
```
+---------------------------------------------------------------------+
|                               DATA                                  |
+-----------+----------------+------------+---------------------------+    
| TYPE FLAG |  FRAME NUMBER  | COMMAND ID |          DATA             |
+-----------+----------------+------------+---------------------------+
\          / \              / \          / \                         /
  1 octet       4 octeți        1 octet      număr variabil de octeți
```
```
+-----------+-------------------+----------------+------------+-----------------------------------------+ 
| TYPE FLAG |   TIP DE PACHET   |  FRAME NUMBER  | COMMAND ID |                  DATA                   |
+-----------+-------------------+----------------+------------------------------------------------------+
: 0000 0001 :       ACK         :   Frame No.    :     -      :                    -                    :
:.............................................................:.........................................:
: 0000 0010 :    FILE CHUNK     :   Frame No.    :   00...00  :               Octeți Fișier             :
:.............................................................:.........................................:
: 0000 0100 :    ACK COMMAND    :    00...00     :   CMD ID   :                    -                    :
:           :      (No output)	:                :            :                                         :
:.............................................................:.........................................:
: 0000 1000 :    ACK COMMAND    :    00...00     :   CMD ID   :             output comandă              :
:           :   (with output)	:                :            :                                         :
:.............................................................:.........................................:
: 0001 0000 : COMMAND(no params):    00...00     :    CMD ID  :                    -                    :
:.............................................................:.........................................:
: 0010 0000 :       COMMAND     :    00...00     :    CMD ID  :           Parametrii Comenzii           :
:           :    (with params)	:                :            :                                         :
:.............................................................:.........................................:
```
```
+------------+------------------+-------------------------------------+
| COMMAND ID |      COMMAND     |             PARAMETERS              |
+------------+------------------+-------------------------------------+
|  0000 0001 |       ls         |                NONE                 |
+------------+------------------+-------------------------------------+
|  0000 0010 |       cd         |                path                 |
+------------+------------------+-------------------------------------+
|  0000 0011 |       mkdir      |             folder name             |
+------------+------------------+-------------------------------------+
|  0000 0100 |     rm/rmdir     |          folder/file name           |
+------------+------------------+-------------------------------------+
|  0000 0101 |       move       |         src path, dest path         |
+------------+------------------+-------------------------------------+
|  0000 0101 |   chg_setting    |         setting name, value         |
+------------+------------------+-------------------------------------+
|  0000 0101 |   download_req   |              file name              |
+------------+------------------+-------------------------------------+
|  0000 0101 |   upload_req     |      file name, file dimension      |
+------------+------------------+-------------------------------------+
```
### Thread-uri
- Server : 3 thread-uri(1 send, 1 receive, 1 prelucrare);
- Client : 4 thread-uri(1 user interface, 1 send, 1 receive, 1 prelucrare);
- Fereastră Glisantă : 2 thread-uri(create la cerere de server și client).

![image](https://hackmd.io/_uploads/SyGJPNiWJg.png)

### ⮚ Bibliografie
* https://www.geeksforgeeks.org/user-datagram-protocol-udp/
* https://www.fortinet.com/resources/cyberglossary/user-datagram-protocol-udp
* https://pcom.pages.upb.ro/notite-cb/curs7/curs.html
* https://nlp.unibuc.ro/courses/RdC.pdf
* https://www.techtarget.com/whatis/definition/flow-control
* https://www.liveaction.com/resources/blog-post/what-is-a-network-packet/
* https://www.youtube.com/watch?app=desktop&v=WfIhQ3o2xow
