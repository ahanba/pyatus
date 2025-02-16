# pyatus
A Python implementation of [hiatus](https://github.com/ahanba/hiatus).
Outdated functions are removed.

## Detectable errors
+ **Glossary**  
   When a glossary source term is found in a source segment, the tool checks if the corresponding glossary target term exists in the target segment. Supports RegExp for advanced matching.
  
+ **Search Source or Target Segment** (Defined as **monolingual**)  
   Searches source or target segments exclusively and reports errors if specified text is found. Supports RegExp for advanced matching.
  
+ **Inconsistency**  
   Checks for inconsistencies bidirectionally: Source-to-Target and Target-to-Source. 
  
+ **Numbers**  
   Detects numbers present in the source but missing in the target.    
  
+ **Length**  
   Flags source and target segments when their lengths differ by more than ±50%.
  
+ **Skipped Translation**  
   Reports errors for blank target segments.

+ **Identical Translation**   
   Reports errors when the source and target segments are identical.  
  
+ **Alphanumeric Strings in Target but NOT in Source** (Defined as **unsourced**)  
   Effective only when the **target** language is non-alphabetic (e.g., Japanese, Chinese, Korean).
  
+ **Alphanumeric Strings in Source but NOT in Target** (Defined as **unsourced_rev**)  
   Effective only when the **source** language is non-alphabetic (e.g., Japanese, Chinese, Korean).
  
+ **Spell**  
   Spellcheck is conducted using [pyspellchecker](https://pypi.org/project/pyspellchecker/). 

## Supported Bilingual File Formats
+ CSV
+ XLSX

## Features
+ hiatus can automatically convert dictionary forms into possible active forms for English (optional).  
  Example: Converts **write** into RegExp **(?:write|writes|writing|wrote|written)**.
+ Simple output report (XLS) that is easy to filter.

## Environment
Python 3.x.x

## Installation
```
pip install pyatus
```

## How to use hiatus?
Fill out the necessary fields in **config.yaml**. 

```
from pyatus import Pyatus

p = Pyatus('foo/config.yaml')

# To generate error report -> XLSX file is generated.
p.generate_report()

# Only to read files -> List of file info is returned.
p.read_files()

# Only to output errors -> List of error info is returned.
p.run_checker()
```

#### About config.yaml
You can find the simple config.yaml in the sample folder.
```
reader:
  folder_path: python/pyatus/sample/target_files
  source_column: "en_US" # column number (integer starting from 0) or header string. Type ("int" or "str") should be the same as target column.
  target_column: "ja_JP" # column number (integer starting from 0) or header string. Type ("int" or "str") should be the same as source column.

checker:
  source_lang: "en_US"
  target_lang: "ja_JP"
  glossary: True
  glossary_path: python/pyatus/sample/glossary
  inconsistency_s2t: False
  inconsistency_t2s: True
  skip: True
  identical: False
  spell: False
  monolingual: True
  monolingual_path: python/pyatus/sample/monolingual
  numbers: True
  unsourced: True
  unsourced_rev: False
  length: False

writer:
  output_path: python/pyatus/sample/report

```

  
### How to create Glossary file? 
Refer to the following instructions and files in the sample folder. 

#### Glossary File Format  
Four-Column TAB delimited Text in the **UTF-8** format.  

#### Structure   

| Column 1|Column 2|Column 3|Column 4|
|:-------|:-------|:--------|:-------|
|Source|Target|Option|Comment|   

|Column|Description|
|:---|:---|
|Source|Glossary source term. RegExp supported. Required|
|Target|Glossary target term. RegExp supported. Required|
|Option|Conversion option. Required|
|Comment|Comment. Optional|

#### About Options
Available options are combination of followings

|Option|Description|
|:-----|:----------|
|i|ignore case + Auto Conversion|
|z|No Conversion + No RegExp + Case-Insensitive|
|*Blank*|No Conversion + No RegExp + Case-Sensitive (= As is)|
|||
|Prefix #||
|#|Auto Conversion OFF. When you use your own RegExp, add # at the beginning of the option field|

#### Sample   
```
Server	 サーバー	z
(?:node|nodes)	ノード	#i	ノードの訳に注意
import(?:ing)	インポート	#i
Japan	日本		JapanはCase-sensitive
run	走る	i	
(?<!start¥-|end¥-)point	点	#i	Feedback No.2
```

### How to create Monolingual file?   
See below and the files in sample folder.   

#### Monolingual File Format  
Four-Column TAB delimited Text in the **UTF-8** format.  

#### Structure   

|Column 1|Column 2|Column 3|Column 4|
|:-------|:-------|:--------|:-------|
|s or t|Expression|Option|Comment|

|Column|Description|
|:---|:---|
|s or t|Segment to search. 's' is source, 't' is target segment. Required|
|Expression|Search expression. RegExp supported. Required|
|Option|Conversion option. Required|
|Comment|Comment. Optional|

#### About Option
Available options are combination of followings

|Option|Description|
|:-----|:----------|
|i|ignore case + Auto Conversion|
|z|No Conversion + No RegExp + Case-Insensitive|
|*Blank*|No Conversion + No RegExp + Case-Sensitive (= As is)|
|||
|Prefix #||
|#|Auto Conversion OFF. When you use your own RegExp, add # at the beginning of the option field|

#### Sample    
```
t	；	#	全角セミコロン；を使用しない
t	[\p{Katakana}ー]・	#	カタカナ間の中黒を使用しない
t	[０１２３４５６７８９]+	#	全角数字を禁止
s	not	z	否定文？
t	Shared Document	#i	Windows のファイル パスはローカライズする（共有ドキュメント）。
t	[あいうえお]	#	Hiragana left
```
  
  
## License
Copyright &copy; 2025 Ayumu Hanba (ayumuhamba19&lt;at_mark&gt;gmail.com)  
Distributed under the [GPL License][GPL].

[GPL]: http://www.gnu.org/licenses/gpl.html
