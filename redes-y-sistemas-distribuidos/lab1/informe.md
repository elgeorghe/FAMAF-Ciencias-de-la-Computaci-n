# Parte 1

## Ejemplo 1 — Búsqueda de entidades en Wikidata

### Comando: curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=zelda&language=es&format=json"| python3 -m json.tool 
{
            "id": "Q12395",
            "title": "Q12395",
            "pageid": 13976,
            "concepturi": "http://www.wikidata.org/entity/Q12395",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q12395",
            "display": {
                "label": {
                    "value": "The Legend of Zelda",
                    "language": "en"
                },
                "description": {
                    "value": "1986 action-adventure video game",
                    "language": "en"
                }
            },
            "label": "The Legend of Zelda",
            "description": "1986 action-adventure video game",
            "match": {
                "type": "alias",
                "language": "es",
                "text": "Zelda"
            },
            "aliases": [
                "Zelda"
            ]
        },

{
            "id": "Q12393",
            "title": "Q12393",
            "pageid": 13974,
            "concepturi": "http://www.wikidata.org/entity/Q12393",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q12393",
            "display": {
                "label": {
                    "value": "The Legend of Zelda",
                    "language": "en"
                },
                "description": {
                    "value": "video game series",
                    "language": "en"
                }
            },
            "label": "The Legend of Zelda",
            "description": "video game series",
            "match": {
                "type": "alias",
                "language": "en",
                "text": "Zelda"
            },
            "aliases": [
                "Zelda"
            ]
        },
#### respuestas a preguntas guia
valores clave: searchinfo.search "zelda".

"id": "Q12395",
                "label": {
                    "value": "The Legend of Zelda",
                    "language": "en"
                },
                "description": {
                    "value": "1986 action-adventure video game",
                    "language": "en"
                }

"id": "Q12393",
                "label": {
                    "value": "The Legend of Zelda",
                    "language": "en"
                },
                "description": {
                    "value": "video game series",
                    "language": "en"
                }


## Ejemplo 2 — Obtener una entidad por ID
### comando: curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q12395&format=json&props=labels|descriptions" | jq '.entities.Q12395 | {label_es: .labels.es, label_en: .labels.en,desc_es: .descriptions.es, desc_en: .descriptions.en }'

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  8468    0  8468    0     0  23522      0 --:--:-- --:--:-- --:--:-- 23522
{
  "label_es": {
    "language": "es",
    "value": "The Legend of Zelda"
  },
  "label_en": {
    "language": "en",
    "value": "The Legend of Zelda"
  },
  "desc_es": {
    "language": "es",
    "value": "videojuego de 1986"
  },
  "desc_en": {
    "language": "en",
    "value": "1986 action-adventure video game"
  }
}

#### respuestas a preguntas guia
los value fueron "filtrados" en el comando con jq y son para los labels en es y en: "value": "The Legend of Zelda". 
para desc en es: "value": "The Legend of Zelda", a diferencia de en que aparece "value": "1986 action-adventure video game".

## Ejemplo 3 — Búsqueda con otro término y límite
### comando  curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=mario&language=es&limit=5&format=json" | python3 -m json.tool


            "id": "Q12379",
            "title": "Q12379",
            "pageid": 13960,
            "concepturi": "http://www.wikidata.org/entity/Q12379",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q12379",
            "display": {
                "label": {
                    "value": "Mario",
                    "language": "en"
                },
                "description": {
                    "value": "fictional character in the Mario video game franchise",
                    "language": "en"
                }
            },

#### respuestas a preguntas guia
cuando usas limit=5 son 5 elementos.
como videojuego no se encuentra ninguno en los primeros 5, sin embargo se encuentra "fictional character in the Mario video game franchise".
su id es: "Q12379" y su descripcion es:"value": "fictional character in the Mario video game franchise",
                                                "language": "en"

## Ejemplos extra 

## consigna: buscar minecraft en wikidata y filtrar solo los juegos
### comando: curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=minecraft&language=es&format=json" \ | jq '.search[] | select(.description | contains("game"))'

{
  "id": "Q49740",
  "title": "Q49740",
  "pageid": 51784,
  "concepturi": "http://www.wikidata.org/entity/Q49740",
  "repository": "wikidata",
  "url": "//www.wikidata.org/wiki/Q49740",
  "display": {
    "label": {
      "value": "Minecraft",
      "language": "en"
    },
    "description": {
      "value": "2011 video game",
      "language": "en"
    }
  },
  "label": "Minecraft",
  "description": "2011 video game",
  "match": {
    "type": "label",
    "language": "en",
    "text": "Minecraft"
  }
}
{
  "id": "Q112863331",
  "title": "Q112863331",
  "pageid": 107715615,
  "concepturi": "http://www.wikidata.org/entity/Q112863331",
  "repository": "wikidata",
  "url": "//www.wikidata.org/wiki/Q112863331",
  "display": {
    "label": {
      "value": "Minecraft",
      "language": "en"
    },
    "description": {
      "value": "video game series",
      "language": "en"
    }
  },
  "label": "Minecraft",
  "description": "video game series",
  "match": {
    "type": "label",
    "language": "en",
    "text": "Minecraft"
  }
}
{
  "id": "Q105729297",
  "title": "Q105729297",
  "pageid": 101090914,
  "concepturi": "http://www.wikidata.org/entity/Q105729297",
  "repository": "wikidata",
  "url": "//www.wikidata.org/wiki/Q105729297",
  "display": {
    "label": {
      "value": "Minecraft: Java Edition",
      "language": "mul"
    },
    "description": {
      "value": "2011 sandbox game developed by Mojang",
      "language": "en"
    }
  },
  "label": "Minecraft: Java Edition",
  "description": "2011 sandbox game developed by Mojang",
  "match": {
    "type": "label",
    "language": "mul",
    "text": "Minecraft: Java Edition"
  }
}
{
  "id": "Q63927755",
  "title": "Q63927755",
  "pageid": 63633207,
  "concepturi": "http://www.wikidata.org/entity/Q63927755",
  "repository": "wikidata",
  "url": "//www.wikidata.org/wiki/Q63927755",
  "display": {
    "label": {
      "value": "Minecraft Earth",
      "language": "en"
    },
    "description": {
      "value": "2019 augmented reality spin-off video game of Minecraft",
      "language": "en"
    }
  },
  "label": "Minecraft Earth",
  "description": "2019 augmented reality spin-off video game of Minecraft",
  "match": {
    "type": "label",
    "language": "es",
    "text": "Minecraft Earth"
  }
}
{
  "id": "Q56884780",
  "title": "Q56884780",
  "pageid": 56801850,
  "concepturi": "http://www.wikidata.org/entity/Q56884780",
  "repository": "wikidata",
  "url": "//www.wikidata.org/wiki/Q56884780",
  "display": {
    "label": {
      "value": "Minecraft Dungeons",
      "language": "en"
    },
    "description": {
      "value": "2020 video game developed by Mojang and Double Eleven",
      "language": "en"
    }
  },
  "label": "Minecraft Dungeons",
  "description": "2020 video game developed by Mojang and Double Eleven",
  "match": {
    "type": "label",
    "language": "es",
    "text": "Minecraft Dungeons"
  }
}

## otro ejemplo 
## consigna: obtener videojuegos relacionados a minecraft

### comando: curl -G -A "LabRedes2026/1.0" \ --data-urlencode 'query=SELECT ?item ?itemLabel WHERE { ?item wdt:P31 wd:Q7889 . SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". } } LIMIT 5' \ https://query.wikidata.org/sparql

<?xml version='1.0' encoding='UTF-8'?>
<sparql xmlns='http://www.w3.org/2005/sparql-results#'>
        <head>
                <variable name='item'/>
                <variable name='itemLabel'/>
        </head>
        <results>
                <result>
                        <binding name='item'>
                                <uri>http://www.wikidata.org/entity/Q2374</uri>
                        </binding>
                        <binding name='itemLabel'>
                                <literal xml:lang='en'>Civilization III</literal>
                        </binding>
                </result>
                <result>
                        <binding name='item'>
                                <uri>http://www.wikidata.org/entity/Q2377</uri>
                        </binding>
                        <binding name='itemLabel'>
                                <literal xml:lang='es'>Civilization IV</literal>
                        </binding>
                </result>
                <result>
                        <binding name='item'>
                                <uri>http://www.wikidata.org/entity/Q2385</uri>
                        </binding>
                        <binding name='itemLabel'>
                                <literal xml:lang='es'>Civilization V</literal>
                        </binding>
                </result>
                <result>
                        <binding name='item'>
                                <uri>http://www.wikidata.org/entity/Q2387</uri>
                        </binding>
                        <binding name='itemLabel'>
                                <literal xml:lang='es'>Commandos 2: Men of Courage</literal>
                        </binding>
                </result>
                <result>
                        <binding name='item'>
                                <uri>http://www.wikidata.org/entity/Q2440</uri>
                        </binding>
                        <binding name='itemLabel'>
                                <literal xml:lang='es'>Freedom Force vs The 3rd Reich</literal>
                        </binding>
                </result>
        </results>
</sparql>