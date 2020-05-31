# normalizationDataset
[hinglishNorm](https://github.com/piyushmakhija5/normalizationDataset/blob/master/hinglishNorm.json): A Hindi-English Dataset for Text Normalization

## Dataset

We are releasing our dataset for Normalization of Hindi-English Code-Mixed Text Data in JSON format.

The object/fields in the released dataset are as shown in Table below:

| Field  | Description | Example |
| :----: |:-----------:| :-----: |
| id     | Unique identifier for each datapoint | 30 |
| Text   | Filtered & cleaned but unnormalized version of user’s input text | whtas ur name |
| Annotation | Manually annotated normalized version of Text | what is your name |
| Transformation | Transformations applied to 'text' which result in 'annotation' | ['Short Form', 'Short Form', 'Looks Good'] |
