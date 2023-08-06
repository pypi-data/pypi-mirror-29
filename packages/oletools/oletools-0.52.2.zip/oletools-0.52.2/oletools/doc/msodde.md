msodde
======

msodde is a script to parse MS Office documents (e.g. Word, Excel, RTF), to detect and extract **DDE links** such as 
**DDEAUTO**, that have been used to run malicious commands to deliver malware.
For Word documents, it can also extract all the other fields, and identify suspicious ones.

Supported formats:
- Word 97-2003 (.doc, .dot), Word 2007+ (.docx, .dotx, .docm, .dotm)
- Excel 97-2003 (.xls), Excel 2007+ (.xlsx, .xlsm, .xlsb)
- RTF
- CSV (exported from / imported into Excel)
- XML (exported from Word 2003, Word 2007+, Excel 2003, Excel 2007+)

For Word documents, msodde detects the use of QUOTE to obfuscate DDE commands (see 
[this article](http://staaldraad.github.io/2017/10/23/msword-field-codes/)), and deobfuscates
it automatically. 

Special thanks to Christian Herdtweck and Etienne Stalmans, who contributed large parts of 
the code.

msodde can be used either as a command-line tool, or as a python module
from your own applications.

It is part of the [python-oletools](http://www.decalage.info/python/oletools) package.

## References about DDE exploitation

- https://www.contextis.com/blog/comma-separated-vulnerabilities
- http://www.exploresecurity.com/from-csv-to-cmd-to-qwerty/
- https://pwndizzle.blogspot.nl/2017/03/office-document-macros-ole-actions-dde.html
- https://sensepost.com/blog/2017/macro-less-code-exec-in-msword/
- http://staaldraad.github.io/2017/10/23/msword-field-codes/

## Usage

```text
usage: msodde [-h] [-j] [--nounquote] [-l LOGLEVEL] [-d] [-f] [-a] FILE

positional arguments:
  FILE                  path of the file to be analyzed

optional arguments:
  -h, --help            show this help message and exit
  -j, --json            Output in json format. Do not use with -ldebug
  --nounquote           don't unquote values
  -l LOGLEVEL, --loglevel LOGLEVEL
                        logging level debug/info/warning/error/critical
                        (default=warning)

Filter which OpenXML field commands are returned:
  Only applies to OpenXML (e.g. docx) and rtf, not to OLE (e.g. .doc). These
  options are mutually exclusive, last option found on command line
  overwrites earlier ones.

  -d, --dde-only        Return only DDE and DDEAUTO fields
  -f, --filter          Return all fields except harmless ones
  -a, --all-fields      Return all fields, irrespective of their contents
```

### Examples

Scan a single file:

```text
msodde file.doc
```

Scan a Word document, extracting *all* fields:

```text
msodde -a file.doc
```


--------------------------------------------------------------------------
    
## How to use msodde in Python applications

This is work in progress. The API is expected to change in future versions. 


--------------------------------------------------------------------------

python-oletools documentation
-----------------------------

- [[Home]]
- [[License]]
- [[Install]]
- [[Contribute]], Suggest Improvements or Report Issues
- Tools:
	- [[mraptor]]
	- [[msodde]]
	- [[olebrowse]]
	- [[oledir]]
	- [[oleid]]
	- [[olemap]]
	- [[olemeta]]
	- [[oleobj]]
	- [[oletimes]]
	- [[olevba]]
	- [[pyxswf]]
	- [[rtfobj]]
