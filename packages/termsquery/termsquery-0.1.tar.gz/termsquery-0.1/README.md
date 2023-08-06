# Terms Boolean Queries for Containers

Base example:

```python
#!/usr/bin/env python

from termsquery import TermsQuery

query = TermsQuery('a & ("term X"| b)')

container1 = {'a', 'term X'}
container2 = {'b'}

assert True == query(container1)
assert False == query(container2)
```

Library can be used to tag collection of documents: create query for each tag
and apply that query for document words.

Simple tagging example:

```python
#!/usr/bin/env python

from termsquery import TermsQuery

tags = {
    'A-not-B' : TermsQuery('A & ~B'),
    'X-and-Y' : TermsQuery('X & Y')
}

docs = [
    'A is the first letter of ...',
    'A and B letters, X and Y letters'
]

for doc in docs:
    words = doc.split()
    doc_tags = [name for (name, query) in tags.items() if query(words)]
    print(doc, doc_tags)
```
