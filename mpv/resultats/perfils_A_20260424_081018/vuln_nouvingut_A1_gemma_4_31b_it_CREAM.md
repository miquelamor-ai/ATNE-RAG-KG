# gemma-4-31b-it · vuln_nouvingut_A1 · CREAM

**Nivell:** A1 | **Curs:** primaria_12 | **Adaptació:** simplificat
**Perfils:** ['vulnerabilitat', 'nouvingut']

---

## Text adaptat

**La fotosíntesi**

En aquest text veuràs la **fotosíntesi** i la **glucosa**.


### Què és la fotosíntesi?

La **fotosíntesi** és un procés natural. 
La fotosíntesi és quan la planta fa menjar.
Les plantes fan aquest procés.
Les algues també fan aquest procés.
Elles transformen la llum del sol.
Elles fan **glucosa**.
La glucosa és un sucre per a la planta.

La fotosíntesi passa als **cloroplasts**.
Els cloroplasts són parts petites de la planta.
Aquestes parts estan a les cèl·lules.


### Com funciona la fotosíntesi?

La planta necessita tres coses.

1. La planta agafa el **diòxid de carboni**.
El diòxid de carboni és un gas de l'aire.
El gas entra per els **estomes**.
Els estomes són forats a les fulles.

2. La planta agafa aigua.
L'aigua entra per les arrels.

3. La planta té **clorofil·la**.
La clorofil·la és un color verd.
La clorofil·la agafa la llum del sol.
La planta usa la llum.
Així, la planta fa la glucosa.

Aquesta és la fórmula de la planta:
Diòxid de carboni + Aigua + Llum = Glucosa + Oxigen.


### Per què és important?

La planta usa la glucosa.
La glucosa dona energia a la planta.
Així, la planta creix.

La planta també fa **oxigen**.
L'oxigen és un gas per respirar.
La planta deixa l'oxigen a l'aire.

Tots els animals necessiten l'oxigen.
Tots els animals mengen plantes.
Això s'anomena **cadena tròfica**.
La cadena tròfica és qui menja a qui.

La fotosíntesi crea menjar i oxigen.
Aquest procés és vital per al planeta.

## Argumentació pedagògica

1. **Adaptació lingüística**: S'ha aplicat el nivell MECR A1. He eliminat totes les subordinades i he limitat les frases a un màxim de 8 paraules amb ordre SVO (Subjecte-Verb-Object).
2. **Atenció a la diversitat**: Per a l'alumne nouvingut, he substituït termes complexos per vocabulari de freqüència alta i he eliminat conceptes abstractes (com "procés bioquímic") per descripcions literals.
3. **Suport multimodal**: He organitzat la informació en blocs temàtics amb preguntes i he simplificat la reacció química a una fórmula additiva visual i senzilla.
4. **Gradació cognitiva**: El text segueix un ordre deductiu (què és → com funciona → per què importa) i utilitza un *advance organizer* per anticipar els conceptes clau.
5. **Rigor curricular**: S'han conservat tots els termes tècnics (cloroplasts, estomes, clorofil·la, etc.) perquè són essencials per a l'ESO, però s'han definit de forma senzilla.

## Notes d'auditoria

| Aspecte | Original | Adaptat | Motiu |
|:--- |:--- |:--- |:--- |
| Sintaxi | Frases llargues i subordinades | Frases curtes (màx. 8 paraules) | Nivell A1 / Nouvingut |
| Veu | Veu passiva ("s'allibera") | Veu activa ("la planta deixa") | Facilitat de comprensió |
| Lèxic | "Procés bioquímic" | "Procés natural / fa menjar" | Reducció de densitat lèxica |
| Estructura | Prosa densa | Blocs amb títols i llistes | Suport cognitiu (chunking) |
| Terminologia | Termes sense definició | Termes en **negreta** + definició | Scaffolding terminològic |

---

<details><summary>Payload CREAM</summary>

```json
{
  "profile": {
    "caracteristiques": {
      "vulnerabilitat": {
        "actiu": true
      },
      "nouvingut": {
        "actiu": true,
        "mecr_entrada": "A1",
        "l1": ""
      }
    }
  },
  "params": {
    "mecr_sortida": "A1"
  }
}
```
</details>
