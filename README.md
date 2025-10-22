# Grapheme to Phoneme models for Norwegian Bokmål

[![lang-button](https://img.shields.io/badge/-Norsk-blue)](https://github.com/NationalLibraryOfNorway/sprakbanken-nb-g2p/blob/main/LESMEG.md) [![lang-button](https://img.shields.io/badge/-English-grey)](https://github.com/NationalLibraryOfNorway/sprakbanken-nb-g2p/blob/main/README.md)

This repo contains code to run G2P models for Norwegian bokmål[^1], which produce phonemic transcriptions for *close-to-spoken* pronunciations (such as in spontaneous conversations: `spoken`) and *close-to-written* pronunciations (such as when reading text aloud: `written`) for 5 different dialect areas:

1. East Norwegian (`e`)
2. South West Norwegian (`sw`)
3. West Norwegian (`w`)
4. Central Norwegian (Trøndersk) (`t`)
5. North Norwegian (`n`)

[^1]: Bokmål is the most widely used written standard for Norwegian. The other written standard is Nynorsk. Read more on [Wikipedia](https://en.wikipedia.org/wiki/Norwegian_orthography).

## Setup

```shell
pip install nb_g2p
```

## Usage

```python
>>> import nb_g2p
>>> list(nb_g2p.transcribe("hei på deg!"))
[('hei', 'H AEJ1'), ('på', 'P OAH0'), ('deg', 'D AEJ1')]
```

### Transcription standard

The G2P models have been trained on the NoFAbet transcription standard which is easier to read by humans than X-SAMPA. NoFAbet is in part based on [2-letter ARPAbet](https://en.wikipedia.org/wiki/ARPABET) and is made by [Nate Young](https://www.nateyoung.se/) for the National Library of Norway in connection with the development of [*NoFA*](https://www.nb.no/sprakbanken/en/resource-catalogue/oai-nb-no-sbr-59/), a forced aligner for Norwegian. The equivalence table below contains X-SAMPA, IPA and NoFAbet notatations.

### X-SAMPA-IPA-NoFAbet equivalence table

| X-SAMPA | IPA | NoFAbet | Example        |
| ------- | --- | ------- | -------------- |
| A:      | ɑː  | AA0     | b**a**d        |
| {:      | æː  | AE0     | v**æ**r        |
| {       | æ   | AEH0    | v**æ**rt       |
| {*I     | æɪ  | AEJ0    | s**ei**        |
| E*u0    | æʉ  | AEW0    | s**au**        |
| A       | ɑ   | AH0     | h**a**tt       |
| A*I     | ɑɪ  | AJ0     | k**ai**        |
| @       | ə   | AX0     | b**e**hage     |
| b       | b   | B       | **b**il        |
| d       | d   | D       | **d**ag        |
| e:      | eː  | EE0     | l**e**k        |
| E       | ɛ   | EH0     | p**e**nn       |
| f       | f   | F       | **f**in        |
| g       | g   | G       | **g**ul        |
| h       | h   | H       | **h**es        |
| I       | ɪ   | IH0     | s**i**tt       |
| i:      | iː  | II0     | v**i**n        |
| j       | j   | J       | **j**a         |
| k       | k   | K       | **k**ost       |
| C       | ç   | KJ      | **k**ino       |
| l       | l   | L       | **l**and       |
| l=      | l̩   | LX0     |
| m       | m   | M       | **m**an        |
| n       | n   | N       | **n**ord       |
| N       | ŋ   | NG      | e**ng**        |
| n=      | n̩   | NX0     |
| o:      | oː  | OA0     | r**å**         |
| O       | ɔ   | OAH0    | g**å**tt       |
| 2:      | øː  | OE0     | l**ø**k        |
| 9       | œ   | OEH0    | h**ø**st       |
| 9*Y     | œy  | OEJ0    | k**øy**e       |
| U       | u   | OH0     | f***o**rt      |
| O*Y     | ɔy  | OJ0     | konv**oy**     |
| u:      | uː  | OO0     | b**o**d        |
| @U      | oʉ  | OU0     | sh**ow**       |
| p       | p   | P       | **p**il        |
| r       | r   | R       | **r**ose       |
| d`      | ɖ   | RD      | reko**rd**     |
| l`      | ɭ   | RL      | pe**rl**e      |
| l`=     | ɭ̩   | RLX0    |
| n`      | ɳ   | RN      | ba**rn**       |
| n`=     | ɳ̩   | RNX0    |
| s`      | ʂ   | RS      | pe**rs**       |
| t`      | ʈ   | RT      | sto**rt**      |
| s       | s   | S       | **s**il        |
| S       | ʃ   | SJ      | **sj**u        |
| t       | t   | T       | **t**id        |
| u0      | ʉ   | UH0     | r**u**ss       |
| }:      | ʉː  | UU0     | h**u**s        |
| v       | ʋ   | V       | **v**ase       |
| w       | w   | W       | **W**ashington |
| Y       | y   | YH0     | n**y**tt       |
| y:      | yː  | YY0     | n**y**         |

Unstressed syllables are marked with a 0 after the vowel or syllabic consonant. The nucleus is marked with a *1* for tone 1 and a *2* for tone 2. Secondary stress is marked with *3*.

## License

These models are shared with a [Creative_Commons-ZERO (CC-ZERO)](https://creativecommons.org/publicdomain/zero/1.0/) license, and so are the lexica they are trained on. The models can be used for any purpose, as long as it is compliant with Phonetisaurus' license.
