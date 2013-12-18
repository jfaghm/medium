dowload_and_analyze_medium_data.py
By: James H. Faghmous (jfagh@cs.umn.edu)
Dec 18 2013

I was a bit frustrated by the changes introduced to the blogging platform Medium (www.medium.com), which made it difficult for writers to get their pieces to readers. Essentially, you have to manually submit your writing to collections and the collections' editors will approve or reject your submission with no explanation. The biggest source of friction is in the fact that there is no good way to browse collections and no way to know which collections are a good fit. On top of that many editors rarely update collections, effectively making any time-sensitive submission virtually useless.

This code downloads 4 basic data points from ~1,000 Medium collections: name, number of followers, number of posts, and date of last activity in the collection.
The code simply takes a few keywords and searches for collections associated with these keywords -- this is the standard way to find collections to publish your Medium posts. The reason why the results from this analysis are not scientific is because I randomly wrote down some keywords and included some keywords I knew would get collections with a lot of activity (followers, posts, etc.) To do this right, one ought to have a corpus of all words in the English language and randomly sample ~500 keywords and feed them into the code (maybe in v2?)
The idea was to take a crude look at what's going on in Medium and how one might improve the publishing experience for users. This code is mostly a hack as Medium doesn't provide an API, therefore, it might break as soon as Medium changes any of their HTML.

The code is to be used as is without warranty. Please feel free to contribute, but please do not flood the Medium servers with requests. This was done for academic purposes only.

