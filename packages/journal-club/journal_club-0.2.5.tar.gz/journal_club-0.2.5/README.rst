A command line interface to a  weighted scheme to select a person to present at a journal club

Install with ``pip install journal_club``
Use with:

`$ jc choose person1 person2 person3 ...`

This creates a csv (if it's not there already) with 3 people 
and then chooses between them. 
The act of choosing updates the record of who was there.

Run again with `$ jc choose person3 new_person ...`.

All information is automatically updated and stored. 
`choose` is usually the only command you need.