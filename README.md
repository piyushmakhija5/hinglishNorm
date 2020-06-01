# A Corpus of Hindi-English Code Mixed Sentences for Normalization
[hinglishNorm](https://github.com/piyushmakhija5/hinglishNorm/tree/master/dataset): A Hindi-English Dataset for Text Normalization

## License
![by-nc-sa](https://user-images.githubusercontent.com/6278238/83433933-2fd7c000-a457-11ea-956c-bfdb541cf41f.png)

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.

<!--
## Citing the corpus
If you use this corpus or its derivate resources for your research, kindly cite it as follows:
Piyush Makhija, Ankit Kumar, Anuj Gupta. "hinglishNorm - A Corpus of Hindi-English Code Mixed Sentences for Normalization" -->


## Dataset Description
We are releasing our dataset for Normalization of Hindi-English Code-Mixed Text Data in JSON format.

The object/fields in the released dataset are as shown in the following table:
| Field  | Description | Example |
| :----: |:-----------:| :-----: |
| *id*    | Unique identifier for each datapoint | 30 |
| *inputText*   | Filtered & cleaned input text | whtas ur name |
| *normalizedText* | Manually annotated normalized *inputText* | what is your name |
| *tags* | We get *normalizedText* from *inputText* after applying transformation according to the tags | ['Short Form', 'Short Form', 'Looks Good'] |
