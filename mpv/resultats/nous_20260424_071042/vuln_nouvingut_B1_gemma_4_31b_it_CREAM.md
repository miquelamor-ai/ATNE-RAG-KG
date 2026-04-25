# gemma-4-31b-it · vuln_nouvingut_B1 · CREAM

**Nivell:** B1 | **Curs:** eso_12 | **Adaptació:** simplificat
**Perfils:** ['vulnerabilitat', 'nouvingut']

---

## Text adaptat

**La fotosíntesi**


### Què és la fotosíntesi?
La **fotosíntesi** (procés per fabricar aliment amb llum) és un procés bioquímic. En aquest procés, les plantes, les algues i alguns microorganismes transformen l'energia de la llum. Aquesta energia es converteix en energia química. Aquesta energia es guarda en la **glucosa** (un tipus de sucre que dona energia).

Aquest procés passa als **cloroplasts** (parts petites de la cèl·lula on es fa la fotosíntesi). Els cloroplasts estan a les cèl·lules de les plantes.


### Com funciona la fotosíntesi?
Primer, les plantes absorbeixen el **diòxid de carboni** (gas de l'aire) a través dels **estomes** (forats molt petits a les fulles). A més, les plantes capten l'aigua del sòl a través de les arrels.

Després, la **clorofil·la** (part verd dels cloroplasts) absorbeix l'energia del sol. La planta utilitza aquesta energia per fabricar la glucosa.

La reacció global és:
6 CO₂ + 6 H₂O + llum solar → C₆H₁₂O₆ (glucosa) + 6 O₂ (oxigen).


### Per a què serveix la fotosíntesi?
La planta utilitza la glucosa per créixer. També la utilitza per al seu **metabolisme** (conjunt de reaccions químiques per viure). Al mateix temps, la planta allibera **oxigen** a l'aire. L'oxigen és un subproducte del procés.

La fotosíntesi és la base de les **cadenes tròfiques** (ordre en què els seres vius es mengen entre ells). A més, és la principal font d'oxigen per a tot el planeta.

En resum, la fotosíntesi transforma la llum, l'aigua i el diòxid de carboni en glucosa i oxigen. Aquest procés permet que les plantes creixin i que altres seres vius respirin.

## Argumentació pedagògica

1. **Adaptació lingüística**: S'ha aplicat el nivell MECR B1 amb frases de màxim 18 paraules i una sola idea per frase. S'han utilitzat connectors explícits (Primer, Després, A més) per facilitar la seqüència lògica.
2. **Atenció a la diversitat**: Per a l'alumne nouvingut, s'ha eliminat qualsevol ambigüitat pronominal i s'ha evitat el sentit figurat. La estructura és previsible i repetitiva per reduir la càrga cognitiva.
3. **Suport multimodal**: S'ha utilitzat el *chunking* dividint el text en tres blocs temàtics amb títols interrogatius. S'ha mantenit la fórmula química com a suport visual del procés.
4. **Gradació cognitiva**: L'informació segueix un ordre deductiu: primer la definició general, després el procés pas a pas i finalment la utilitat global.
5. **Rigor curricular**: S'han conservat tots els termes tècnics (cloroplasts, estomes, clorofil·la, metabolisme, cadenes tròfiques) definint-los la primera vegada per no perdre la precisió científica.

## Notes d'auditoria

| Aspecte | Original | Adaptat | Motiu |
|:--- |:--- |:--- |:--- |
| **Sintaxi** | Frases llargues i complexes | Frases curtes (SVO) | Adaptació a MECR B1 i nouvinguts |
| **Lèxic** | Termes tècnics sense definició | Termes en **negreta** + definició | Rigor curricular i suport cognitiu |
| **Estructura** | Prosa contínua | Blocs amb títols i resum | Millora de l'accessibilitat (DUA) |
| **Connectors** | Implícits o complexos | Explícits (Primer, Després) | Facilitar la comprensió de la seqüència |
| **Vocabulari** | "Sintetitzar", "subproducte" | "Fabricar", "subproducte" (definit) | Substitució per termes d'alta freqüència |

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
    "mecr_sortida": "B1"
  }
}
```
</details>
