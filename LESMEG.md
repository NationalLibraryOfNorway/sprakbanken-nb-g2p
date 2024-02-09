# Grafem-til-fonem-modeller for norsk bokmål

[![lang-button](https://img.shields.io/badge/-Norsk-grey)](https://github.com/Sprakbanken/g2p-nb/blob/v2/LESMEG.md) [![lang-button](https://img.shields.io/badge/-English-blue)](https://github.com/Sprakbanken/g2p-nb/blob/v2/README.md)

Dette repoet inneholder G2P-modeller for norsk bokmål, som produserer fonemiske transkripsjoner for talenære uttalevarianter (som i vanlige samtaler) eller skriftnære uttalevarianter (som i tekstopplesing) for 5 forskjellige dialektområder: 

1. Østnorsk
2. Sørvestnorsk
3. Vestnorsk
4. Trøndersk
5. Nordnorsk

## Oppsett
Følg installasjonsinstruksjoner fra [Phonetisaurus](https://github.com/AdolfVonKleist/Phonetisaurus/tree/kaldi). 
Du trenger kun å kjøre koden i disse avsnittene: 
- "Next grab and install OpenFst-1.7.2"
-  "Checkout the latest Phonetisaurus from master and compile without bindings"

## Data
[Modellene og testdata](https://www.nb.no/sbfil/verktoy/g2p_no/G2P-no-2_0.tar.gz) kan lastes ned fra Språkbankens ressurskatalog, som en komprimert `.tar.gz`-fil.

Pakk dem ut og plasser mappene "data" og "models" i din lokale klone av dette repoet. 
```
tar -xvf G2P-no-2_0.tar.gz
```

Uttaleleksikonene som ble brukt til å trene G2P-modellene er fritt tilgjengelige fra Språkbanken ressurskatalog: [NB Uttale](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-79/). 
De kan også genereres opp med data og kode fra Github-repoet [Sprakbanken/nb_uttale](https://github.com/Sprakbanken/nb_uttale).

Leksikonene ble delt i test- og treningssett med  [`sklearn.model_selection.train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) og en fordeling på 80% treningsdata/ 20% testdata.

## Bruk

```shell
phonetisaurus-apply --model models/nb_e_spoken.fst --word_list data/wordlist_test.txt  -n 1  -v  > output.txt
```

- Inndata (`--word_list`) burde være en tekstfil med linjeseparerte ord. Se for eksempel [`data/wordlist_test.txt`](./data/wordlist_test.txt). 
- De trente modellene er `.fst`-filer i `models`-mappen. I samme mappe ligger også `.corpus`-filer og 8-gram-modeller for fonemsekvenser (`.arpa`-filer) som kommer fra treningsprosessen  til Phonetisauraus.
- `-n`-argumentet angir hvor mange av de mest sannsynlige transkripsjonsforslagene som skal skrives til utdata.

## Evaluering

Det er to skript i repoet for å regne ut Word Error Rate (WER) og Phoneme Error Rate (PER), og som gir litt ulike svar pga. implementasjonen av utregningene. 

### `evaluate.py`

Regner statistikk for alle modellene dersom ingen argumenter er gitt. 

```shell
python evalutate.py
```

Med `-l`-argumentet kan du få statistikk for spesifikke modeller, f.eks. `-l e_spoken`.

- **WER** er antall feil transkripsjoner fordelt på totalt antall ord i testdata. 1 feil = 1 ord.
- **PER** er antall feil fonemer for alle transkripsjonene, fordelt på totalt antall fonemer i testdata. 1 feil = 1 fonem. 

| Model | Word Error Rate | Phoneme Error Rate |
| --- | --- | --- |
| *nb_e_written.fst* | 13.661238654564869 | 1.9681178920293207 |
| *nb_e_spoken.fst* | 13.72501038144391 | 1.9832518286152074 |
| *nb_sw_written.fst* | 13.240048644480037 | 1.8396612197218096 |
| *nb_sw_spoken.fst* | 16.422702734768936 | 2.426312206336983 |
| *nb_w_written.fst* | 13.240048644480037 | 1.8396612197218096 |
| *nb_w_spoken.fst* | 16.892833837574894 | 2.5064155890730686 |
| *nb_t_written.fst* | 13.736133357062347 | 1.98774986044724 |
| *nb_t_spoken.fst* | 16.47992288013051 | 2.5809178688066843 |
| *nb_n_written.fst* | 13.736133357062347 | 1.98774986044724 |
| *nb_n_spoken.fst* | 17.22590930999963 | 2.8209779677747715 |



### `g2p_stats.py`

Regner ut WER og PER for to inputfiler: 
1. Referansefila /testdata, f.eks. `data/NB-uttale_e_spoken_test.dict`
2. Modellens transkripsjonsforslag, f.eks. `output.txt` fra kommandoen i [Bruk](#bruk), eller `data/predicted_nb_e_spoken.dict`.


- **WER** er antall feil transkripsjoner fordelt på totalt antall ord i modellens forslag. 1 feil = 1 ord.
- **PER** er summen av PER for hver transkripsjonen, fordelt på totalt antall ord i modellens forslag. 1 feil = 1 fonem. 

> **OBS**: Denne metoden tar ikke hensyn til ulik lengde på transkripsjonene. En transkripsjon med 2 fonemer der 1 er feil får en 50% PER, mens et ord på 10 fonemer med 1 feil får 10% PER, og gjennomsnittet blir 35%. Om man regner antall feil på totalt antall fonemer, blir gjennomsnittet for de to 16,7%. 

```shell
python g2p_stats.py data/NB-uttale_e_spoken_test.dict data/predicted_nb_e_spoken.dict
# WER: 14.049209423582523
# PER: 2.714882650391985
```

| Model | Word Error Rate | Phoneme Error Rate |
| --- | --- | --- |
| *nb_e_written.fst* | 13.97114598599277 | 2.7038190765903214 |
| *nb_e_spoken.fst* | 14.049209423582523 | 2.714882650391985 |
| *nb_sw_written.fst* | 13.541060631724685 | 2.5423757844377284 |
| *nb_sw_spoken.fst* | 16.729141964989285 | 3.34063477772742 |
| *nb_w_written.fst* | 13.541060631724685 | 2.5423757844377284 |
| *nb_w_spoken.fst* | 17.186475877661337 | 3.4137304874392114 |
| *nb_t_written.fst* | 14.059519688924565  | 2.7190289235234104 |
| *nb_t_spoken.fst* | -- | -- |
| *nb_n_written.fst* | 14.059519688924565 | 2.7190289235234104 |
| *nb_n_spoken.fst* | -- | -- |

> **OBS**: *Modellforslagene fra t_spoken og n_spoken har ikke samme antall ord som testdata, som gjør at skriptet krasjer.*

### Transkripsjonsstandard

G2P-modellene har blitt trent på data med transkripsjonsstandarden NoFAbet , som er lettere å lese for mennesker enn X-SAMPA. 
NoFAbet er delvis basert på [ARPAbet](https://en.wikipedia.org/wiki/ARPABET) og ble utviklet for Nasjonalbiblioteket av [Nate Young](https://www.nateyoung.se/)

....in connection with the development of [*NoFA*](https://www.nb.no/sprakbanken/en/resource-catalogue/oai-nb-no-sbr-59/), a forced aligner for Norwegian. The equivalence table below contains X-SAMPA, IPA and NoFAbet notatations.

### X-SAMPA-IPA-NoFAbet equivalence table
X-SAMPA | IPA | NoFAbet | Example
--- | --- | --- |---
A: | ɑː | AA0 | b**a**d
{: | æː | AE0 | v**æ**r
{ | æ | AEH0 | v**æ**rt
{*I | æj | AEJ0 | s**ei**
E*u0 | æw | AEW0 | s**au**
A | ɑ | AH0 | h**a**tt
A*I | ɑj | AJ0 | k**ai**
@ | ə | AX0 | b**e**hage
b | b | B | **b**il
d | d | D | **d**ag
e: | eː | EE0 | l**e**k
E | ɛ | EH0 | p**e**nn
f | f | F | **f**in
g | g | G | **g**ul
h | h | H | **h**es
I | I | IH0 | s**i**tt
i: | iː | II0 | v**i**n
j | j | J | **j**a
k | k | K | **k**ost
C | ç | KJ | **k**ino
l | l | L | **l**and
l= | l̩ | LX0 |
m | m | M | **m**an
m= | m̩ | MX0 |
n | n | N | **n**ord
N | ŋ | NG | e**ng**
n= | n̩ | NX0 |
o: | oː | OA0 | r**å**
O | ɔ | OAH0 | g**å**tt
2: | øː | OE0 | l**ø**k
9 | œ | OEH0 | h**ø**st
9*Y | œj | OEJ0 | k**øy**e
U | u | OH0 | f***o**rt
O*Y | ɔj | OJ0 | konv**oy**
u: | uː | OO0 | b**o**d
@U | oʋ | OU0 | sh**ow**
p | p | P | **p**il
r | r | R | **r**ose
d` | ɖ | RD | reko**rd**
l` | ɭ | RL | pe**rl**e
l`= | ɭ̩ | RLX0 |
n` | ɳ | RN | ba**rn**
n`= | ɳ̩ | RNX0 |
s` | ʂ | SJ | pe**rs**
t` | ʈ | RT | sto**rt**
r= | r̩ | RX0 |
s | s | S | **s**il
S | ʂ | SJ | **sj**u
s= | s̩ | SX0 |
t | t | T | **t**id
u0 | ʉ | UH0 | r**u**ss
u0 j | ʉj | UH0_J | Anh**ui**
}: | ʉː | UU0 | h**u**s
v | v | V | **v**ase
w | w | W | **W**ashington
Y | y | YH0 | n**y**tt
y: | yː | YY0 | n**y**

Unstressed syllables are marked with a 0 after the vowel or consonant syllable nucleus. The nucleus is marked with a *1* for tone 1 and a *2* for tone 2. Secondary stress is marked with *3*. 

## License

These models are shared with a [Creative_Commons-ZERO (CC-ZERO)](https://creativecommons.org/publicdomain/zero/1.0/) license, and so are the lexica they are trained on. The models can be used for any purpose, as long as it is compliant with Phonetisaurus' license.
