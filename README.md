# DiscEval: Discourse-Based Evaluation of Language Understanding

This is a data/code release accompanying this paper:

- Title: "Discourse-Based Evaluation of Language Understanding"
- Authors: Damien Sileo, Tim Van de Cruys, Camille Pradel and Philippe Muller
- article coming very soon

# Contents

DiscEval is a compilation of 11 evaluation datasets with a focus on discourse, that can be used for evaluation of English Natural Language Understanding, or as auxiliary training tasks for NLP models.

Previous evaluation frameworks have no clear way to evaluate how models deal with implicatures or different kinds of speech acts. Instead of using semantics-centered tasks like Natural Language Inference of Semantic Similarity, we propose a discourse-centered evaluation with a focus on meaning as use. 



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

### Clone DiscEval

`git clone https://github.com/synapse-developpement/DiscEval.git`

The preprocessed datasets are available in the disceval folder in tsv format. 



### Build DiscEval 1.0 from source files

You can also build the dataset from the sources if you want to change the preprocessing

Run the `bash get_data.bash` in `data` to download dataset from the sources

Run the notebook `Make DiscEval 1.0` after having specified `disceval_base_path` in the third cell to perform preprocessing and exports.

# Contact

For further information, you can contact:

damien dot sileo at synapse-fr dot com
