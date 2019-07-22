
# PDTB
wget https://github.com/cgpotts/pdtb2/raw/master/pdtb2.csv.zip
unzip pdtb2.csv.zip

# Stance
wget https://github.com/thanhan/fc-aaai18/raw/master/emergent/url-versions-2015-06-14-clean.csv

# Sarcasm
wget https://github.com/ricsonc/sarcasm_machine/raw/master/sarcasm_v2.csv

# Squinky
wget http://people.rc.rit.edu/~bsm9339/corpora/squinky_corpus/mturk_merged.csv

# SwitchBoard
git clone https://github.com/NathanDuran/Switchboard-Corpus

# MRDA
git clone https://github.com/NathanDuran/MRDA-Corpus

# EmoBank
wget https://github.com/JULIELab/EmoBank/raw/master/corpus/emobank.csv

# Verifiability
wget https://facultystaff.richmond.edu/~jpark/data/jpark_aclw14.zip --no-check-certificate
unzip -d verifiability jpark_aclw14.zip

# Persuasiveness
wget http://www.hlt.utdallas.edu/~zixuan/EssayScoring/essays.zip
unzip essays.zip

# GUM
git clone https://github.com/amir-zeldes/gum
© 2019 GitHub, Inc.

# STAC (can need more than a few minutes)
wget https://www.irit.fr/STAC/situated_only_tables.zip
unzip situated_only_tables.zip
wget https://www.irit.fr/STAC/linguistic_only_tables.zip
unzip linguistic_only_tables.zip
mkdir stac_data_pickles
cp situated_only_tables/* stac_data_pickles/
cp linguistic_only_tables/* stac_data_pickles/

python3 flatten_stac.py
python3 export_stac.py
