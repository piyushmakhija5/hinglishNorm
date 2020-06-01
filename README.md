# A Corpus of Hindi-English Code Mixed Sentences for Normalization
[hinglishNorm](https://github.com/piyushmakhija5/hinglishNorm/tree/master/dataset): A Hindi-English Dataset for Text Normalization

## Dataset

We are releasing our dataset for Normalization of Hindi-English Code-Mixed Text Data in JSON format.

The object/fields in the released dataset are as shown in the following table:

| Field  | Description | Example |
| :----: |:-----------:| :-----: |
| id     | Unique identifier for each datapoint | 30 |
| inputText   | Filtered & cleaned but unnormalized version of user’s input text | whtas ur name |
| normalizedText | Manually annotated normalized inputText | what is your name |
| tags | We get 'normalizedText' from 'inputText' after applying transformation according to the tags | ['Short Form', 'Short Form', 'Looks Good'] |
