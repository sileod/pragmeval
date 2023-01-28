# PragmEval :  A Pragmatics-Centered Evaluation Framework for Natural Language Understanding

This is a data/code release accompanying this paper:

- Title: "A Pragmatics-Centered Evaluation Framework for Natural Language Understanding"
- Authors: Damien Sileo, Tim Van de Cruys, Camille Pradel and Philippe Muller
- Accepted at LREC2022
- https://arxiv.org/abs/1907.08672

# Contents

PragmEval is a compilation of 11 evaluation datasets with a focus on discourse, that can be used for evaluation of English Natural Language Understanding, or as auxiliary training tasks for NLP models.

While the idea of meaning as use permeates NLP, it's not clear that current evaluations fully account for that aspect. Previous evaluation frameworks have no clear way to evaluate how models deal with implicatures or different kinds of speech acts, and are arguably focussing on semantics (Natural Language Inference of Semantic Similarity) rather than use. 
We propose a discourse-centered evaluation with a focus on meaning as use. 



| dataset       | categories          | example                                                      | class                                      | #train |
| :------------ | :------------------ | :----------------------------------------------------------- | :----------------------------------------- | :----- |
| PDTB          | discourse relation  | *it was censorship* **/** *it was outrageous*                | conjunction                                | 13k    |
| STAC          | discourse relation  | *what ?* **/** *i literally lost*                            | question-answer-pair                       | 11k    |
| GUM           | discourse relation  | *do not drink* **/** *if underage in your country*           | condition                                  | 2k     |
| Emergent      | stance              | *a meteorite landed in nicaragua.* **/** *small meteorite hits managua* | for                                        | 2k     |
| SarcasmV2     | presence of sarcasm | *don't quit your day job* **/** *[...] i was going to sell this joke. [...]* | sarcasm                                    | 9k     |
| SwitchBoard   | speech act          | *well , a little different , actually ,*                     | hedge                                      | 19k    |
| MRDA          | speect act          | *yeah that 's that 's that 's what i meant .*                | acknowledge-answer                         | 14k    |
| Verifiability | verifiability       | *I've been a physician for 20 years.*                        | verifiable-experiential                    | 6k     |
| Persuasion    | C/E/P/S/S/R         | *Co-operation is essential for team work* **/** *lions hunt in a team* | low specificity                            | 0.6k   |
| Squinky       | I/I/F               | *boo ya.*                                                    | uninformative, high implicature, unformal, | 4k     |
| EmoBank       | V/A/D               | *I wanted to be there..*                                     | low valence, high arousal, low dominance   | 5k     |

# Instructions

### Recommended usage
```python
from datasets import load_dataset
dataset = load_dataset('pragmeval','gum')
```

Evaluate your model with this script:
https://colab.research.google.com/drive/1sg--LF4z7XR1wxAOfp0-3d4J6kQ9nj_A?usp=sharing

### Building from sources:
`git clone https://github.com/synapse-developpement/PragmEval.git`

The preprocessed datasets are available in the `pragmeval` folder in tsv format. 

Run the `bash get_data.bash` in `data` to download dataset from the sources

Run the notebook `Make PragmEval 1.0` after having specified `pragmeval_base_path` in the third cell to perform preprocessing and exports.

# Citation
```
@inproceedings{sileo-etal-2022-pragmatics,
    title = "A Pragmatics-Centered Evaluation Framework for Natural Language Understanding",
    author = "Sileo, Damien  and
      Muller, Philippe  and
      Van de Cruys, Tim  and
      Pradel, Camille",
    booktitle = "Proceedings of the Thirteenth Language Resources and Evaluation Conference",
    month = jun,
    year = "2022",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2022.lrec-1.255",
    pages = "2382--2394",
}
```

# Contact

For further information, you can contact:

damien dot sileo at gmail dot com
