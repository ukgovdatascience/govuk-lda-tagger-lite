# Tag GOV.UK documents with the LDA algorithm

This project contains several experiments that used the [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) machine learning algorithm to generate topics from pages on [GOV.UK](https://www.gov.uk) and tag them with those topics.

## Nomenclature

- **Document**: a chunk of text representing a page on GOV.UK.
- **Base path**: The relative URL to a page on GOV.UK.
- **Corpus**: a set of documents.
- **Term**: a single word, phrase, or [n-gram](https://en.wikipedia.org/wiki/N-gram). We break a document into many terms before running the LDA algorithm.
- **Dictionary**: a data structure that maps every term to an integer ID.
- **Stopwords**: terms we want the algorithm to ignore - these won't be included in the dictionary.
- **Document term matrix**: [a data structure that captures how frequently terms appear in different documents](https://en.wikipedia.org/wiki/Document-term_matrix).
- **TF-IDF**: [Term Frequency - Inverse Document Frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf). A measure that shows how important a word is to a document in a corpus.
- **LDA**: [Latent Dirichlet Allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) - the algorithm we're using to model topics.

## Install requirements

The best way to run these scripts is by using the [govuk-lda-tagger-image](https://github.com/ukgovdatascience/govuk-lda-tagger-image) docker container, which will ensure that python `2.7` and all the necessary dependencies are installed.

## Try it out

Before execution, the `EXPERIMENT_DIR` environment variable needs to be set to the folder in which you want your experiments to be saved. When using within a docker container, this should default to `/mnt/experiments` to allow the experiments to be mounted as a volume.

The `train_lda.py` script is a command line interface (CLI) to the LDA tagger. You can customise the input dataset, the preprocessing, and the parameters passed to the underlying LDA library.

### Generating topics and tags for early years

Using the early years data from the HTML pages to derive topics, and tagging every document to those topics:

```
train_lda.py import --experiment early_years input/early-years.csv
```

The `--experiment` option defines the output directory under `experiments`. It defaults to one generated from the current time.

### Using a curated dictionary

Pass a curated dictionary using the `--input-dictionary` option. By default the dictionary is generated from the corpus, excluding a number of predefined stopwords (defined in the `stopwords` directory).

```
train_lda.py import input/audits_with_content.csv --input-dictionary input/dictionary.txt
```

### Retraining using the same corpus

If you already ran an experiment, but something went wrong, you can use the `refine` subcommand to train it again, but reuse the corpus generated in the first run. The final argument is the original experiment directory name, which will be overwritten.

```
train_lda.py --numtopics 100 refine early-years
```

### Using the GensimEngine class

In `gensim_engine.py` there is a class that can be used to train and run an LDA model programatically.

This has the following API:

```
# Instantiate an object
engine = GensimEngine(documents, log=True)

# Train the model with the data provided
experiment = engine.train(number_of_topics=20)

# Tag all documents in the corpus
tags = experiment.tag()
```

`documents` is expected to be a list of dictionaries, where each dictionary has a `base_path` key and a `text` key.

### Other scripts
When we started the project we created two simple scripts to test the libraries we used.

You can run either of these to see some sample topics.

#### Using Python's lda library

Run `python run_lda.py` in order to use the LDA library to generate topics and categorise the documents listed in the input file.

#### Using Python's gensim library

Run `python run_gensim.py` in order to use the gensim library to generate topics and categorise the documents listed in the input file.

## Fetching new data

### Import indexable content from the search API

In order to fetch data from the search API, prepare a CSV input file containing
one column (with the `URL` header) and the `base_path` of the links we wish to
fetch content for.

Then run the following command:

```
python import_indexable_content.py --environemnt https://www.gov.uk input_file.csv
```

This script outputs CSV rows with the title, description, indexable content,
topic names and organisation names.

### Import PDF data

In order to fetch PDF text from a number of GOV.UK base paths, prepare a CSV
input file containing one column (with the `URL` header) and the `base_path` of
the links we wish to fetch content for.

Then, run the following command:

```
python fetch_pdf_content.py input_file.csv output_file.csv
```

The output file will include the same base paths and also the text found in all
PDF attachments, merged into one big string.

### Combine all the data

The python tool [CSVKit](https://csvkit.readthedocs.io/en/0.9.1/index.html) can be used to combine the separate CSVs into one:

Note that because the columns are very wide, you will need to increase the default maximum field size:

```
csvjoin -c url all_audits_for_education.csv all_audits_for_education_with_pdf_data.csv > all_audits_for_education_with_pdf_and_indexable_content.csv --maxfieldsize [a big number]
```

The resulting CSV can then be passed to `data_import/combine_csv_columns.py` to merge everything into one "words" column.

```
python data_import/combine_csv_columns.py < all_audits_for_education_with_pdf_and_indexable_content.csv > all_audits_for_education_words.csv
```

## Licence

[MIT License](LICENCE.txt)
