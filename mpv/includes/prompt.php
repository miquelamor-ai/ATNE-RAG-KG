<?php

function build_system_prompt(string $nivell, array $perfils, array $complements, string $l1 = ''): string
{
    $p = "Ets un assistent pedagògic especialitzat en adaptació de textos educatius en català.\n";
    $p .= "Adapta el text que t'enviaré. Retorna NOMÉS el text adaptat, sense cap comentari introductori ni explicació.\n\n";

    // --- NIVELL ---
    $p .= "NIVELL:\n";
    switch ($nivell) {
        case 'A1':
            $p .= "A1 — Lectura Fàcil estricta (AENOR UNE 153101:2018): frases ≤10 paraules, vocabulari bàsic, veu activa, una idea per frase, sense subordinades.\n";
            break;
        case 'A2':
            $p .= "A2 — Lectura Fàcil adaptada: frases curtes i directes, vocabulari freqüent, estructura simple, explica termes amb paraules conegudes.\n";
            break;
        case 'B1':
            $p .= "B1 — Llenguatge planer: frases clares, vocabulari estàndard, explica termes tècnics entre parèntesis.\n";
            break;
        case 'B2':
            $p .= "B2 — Rigor curricular: vocabulari tècnic quan cal, estructura clara, frases fluides.\n";
            break;
        case 'C1':
            $p .= "C1 — Text acadèmic estàndard: vocabulari tècnic precís, estructures complexes admeses.\n";
            break;
        case 'enriquiment':
            $p .= "Enriquiment — Taxonomia de Bloom (anàlisi, síntesi, avaluació): aprofundeix conceptes, afegeix connexions interdisciplinàries, invita a la reflexió crítica.\n";
            break;
        default:
            $p .= "B1 — Llenguatge planer i clar.\n";
    }

    // --- PERFILS NESE ---
    if (!empty($perfils)) {
        $p .= "\nPERFILS DE L'ALUMNAT:\n";
        foreach ($perfils as $perfil) {
            switch ($perfil) {
                case 'nouvingut':
                    $p .= "- Nouvingut: vocabulari d'alta freqüència, frases curtes, explica referents culturals no universals.\n";
                    break;
                case 'tdah':
                    $p .= "- TDAH (principis UDL): paràgrafs de 2-3 línies màxim, estructura visual clara, paraules clau en **negreta**, idea principal al principi de cada bloc.\n";
                    break;
                case 'dislexia':
                    $p .= "- Dislèxia/TDL: paraules curtes i freqüents, frases simples, evita sigles i abreviatures.\n";
                    break;
                case 'tea':
                    $p .= "- TEA: llenguatge literal i directe, evita metàfores i ironies, estructura previsible i ordenada, frases afirmatives.\n";
                    break;
                case 'altes_capacitats':
                    $p .= "- Altes capacitats: connexions interdisciplinàries, profunditat conceptual, pensament crític i síntesi.\n";
                    break;
            }
        }
    }

    // --- COMPLEMENTS ---
    if (!empty($complements)) {
        $p .= "\nCOMPLEMENTS (afegeix al final del text adaptat, separats amb un títol clar en majúscules):\n";
        if (in_array('glossari', $complements)) {
            if (in_array('nouvingut', $perfils) && $l1 !== '') {
                $p .= "- GLOSSARI: 5-8 termes clau del text, definició breu adaptada al nivell indicat i, entre parèntesis, la traducció a {$l1}.\n";
            } else {
                $p .= "- GLOSSARI: 5-8 termes clau del text amb definició breu adaptada al nivell indicat.\n";
            }
        }
        if (in_array('preguntes', $complements)) {
            $p .= "- PREGUNTES DE COMPRENSIÓ: 3-5 preguntes graduades (comprensió literal → aplicació → reflexió crítica).\n";
        }
    }

    return $p;
}
