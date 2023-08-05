============
Overview
============

Your OCR pipeline may have various stages and may use various tools.
You need a simple way to run sample/s as a whole or piece by piece and have a way to say that the OCR accuracy is say 98%.

=========
Usage
=========

>>> pip install ocraccuracyreporter
>>> from ocraccuracyreporter.oar import oar

.. topic:: initialising the reporter

>>> oreport = oar(expected='john', given='joh', label='name')

>>> print(oreport)
>>> name,john,joh,86,100,86,86,94,1

or you may have various ocr results for the same item, so you may want to initialise the expected alone
with or without a label

>>> oreport = oar(expected='john', label='name')
>>> oreport.given = 'joh'
>>> repr(oreoprt)
if you are creating a csv report with header info
>>>label,expected,given,ratio,partial_ratio,token_sort_ratio,token_set_ratio,jaro_winkler,distance
  name,john,joh,86,100,86,86,94,1

  .. topic:: Items in the report


  ratio - uses pure Levenshtein Distance based matching
          (100 - means perfect match)

  partial_ratio - matches based on best substrings

  token_sort_ratio - tokenizes the strings and sorts them alphabetically

  token_set_ratio - tokenizes the strings and compared the intersection

  jaro_winkler - this algorithm giving more weight to common prefix
                 (for example, some parts are good, missing others)

  distance - this shows how many characters are really different in given
             compared to expected




=========
Class variables
=========

label  - a meaningful name for the ocr string.
expected - expected result
given - result you got out of ocr pipeline

total_expected_char_count - calculated expected char count
total_expected_word_count - calculated expected word count

total_given_char_count - calculated given char count
total_given_word_count - calculated given word count
