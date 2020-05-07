Lambda function used to take slot intents from Amazon Lex and use them as elements of a google search
query using googlesearch and bs4 imports.

NOTE: To use with aws Lambda, site packages and .cfg file put into one zip with no additional directories. May
also possibly require files in the scripts folder, so include them to be safe as well.

Included zip can be directly imported to AWS Lambda