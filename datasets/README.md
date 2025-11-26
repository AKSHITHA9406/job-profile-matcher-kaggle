# Datasets

This folder is where you place **external datasets**, such as those downloaded from **Kaggle**.

## 1. Kaggle Resume Dataset

1. Go to Kaggle and download a resume dataset (for example, a dataset that has a column like `Resume` or `resume_text` containing the full resume).
2. Save the CSV file as:

```text
datasets/kaggle/resumes.csv
```

3. By default, the project expects:
   - File path: `datasets/kaggle/resumes.csv`
   - Text column: `Resume`  

   You can change the column name when running `cli_kaggle.py` using `--text-column`.

> ⚠️ Note: Kaggle datasets are under Kaggle's terms of use.  
> This repository **does not** ship any Kaggle data, only the code to use it.
