# index_warrior.py

Python script to deal with GrimoireLab ES indexes.

It will allow you to:
 * make easier cleaning up the ES instances by dropping indexes based on last time it was written.
 * compare the affiliation and repos data for two enriched indexes, so you don't need to add them to kibana to see what they look like
 * list all the indexes with info about the aliases and modification dates
 * switch all the aliases from one index to another

.. and also the basic stuff:
 * list, add and delete aliases
 * list and delete indexes.


These are the dependencies:
```
certifi==2016.9.26
colorama==0.3.9
elasticsearch==5.1.0
elasticsearch-dsl==5.1.0
prettytable==0.7.2
```

The example below shows how to delete documents with a specific origin and grimoire_creation_date:
```
 >> index_warrior.py -e http://localhost:9200 index delete --origin https://github.com/bitergia/mordred --older_than now-100d git_prueba_002
  25 documens found with the condition:
  - origin == https://github.com/bitergia/mordred
  - grimoire_creation_date > now-100d

  Do you really want to remove them? (y/n): y
 25 documents were removed
```
```
index_warrior.py -e http://localhost:9200 index show
+-------------+----------------------------------------+---+-------+---------+--------------------------+--------------------------+-----------------------+
| status      | index                                  | A | count | deleted | metadata__timestamp      | metadata__updated_on     | rep/pri size/pri.size |
+-------------+----------------------------------------+---+-------+---------+--------------------------+--------------------------+-----------------------+
| yellow/open | .kibana                                |   |     2 |       0 | None                     | None                     | 1/1 11.6kb/11.6kb     |
| yellow/open | conf                                   |   |    22 |       0 | None                     | None                     | 1/5 114.7kb/114.7kb   |
| yellow/open | discourse_161121                       |   |  2099 |       0 | 2017-02-23T16:04:42.501Z | 2016-04-09T20:12:13.679Z | 1/5 56.7mb/56.7mb     |
| yellow/open | discourse_161121_enriched_161121a      |   | 14917 |       5 | 2017-02-23T16:04:42.501Z | 2016-04-09T20:12:13.679Z | 1/5 16mb/16mb         |
| yellow/open | gerrit_grimoire_161212                 |   |  2816 |       4 | 2017-02-23T15:21:34.338Z | 2017-02-23T16:20:39.000Z | 1/5 26.1mb/26.1mb     |
| yellow/open | gerrit_grimoire_161212_enriched_161212 |   |  2816 |       1 | 2017-02-23T15:21:34.338Z | 2017-02-23T16:20:39.000Z | 1/5 3.9mb/3.9mb       |
| yellow/open | git_coreos                             |   | 16435 |       3 | 2017-02-28T23:28:28.358Z | 2017-02-28T18:57:49.000Z | 1/5 35.4mb/35.4mb     |
| yellow/open | git_coreos_enriched                    |   |     0 |       0 | None                     | None                     | 1/5 795b/795b         |
| yellow/open | git_grimoire_161213                    | * |  2437 |       7 | 2017-02-23T15:21:36.797Z | 2017-02-23T11:16:30.000Z | 1/5 4.7mb/4.7mb       |
| yellow/open | git_grimoire_161223_21                 | * |  2437 |       7 | 2017-02-23T15:21:36.797Z | 2017-02-23T11:16:30.000Z | 1/5 5mb/5mb           |
| yellow/open | git_prueba_001                         |   |  2260 |     177 | 2017-02-23T15:21:36.797Z | 2017-02-23T11:16:30.000Z | 1/5 3.7mb/3.7mb       |
| yellow/open | git_prueba_002                         |   |  2412 |      25 | 2017-02-23T15:21:36.797Z | 2017-02-23T11:16:30.000Z | 1/5 4.7mb/4.7mb       |
| yellow/open | mbox_170207                            |   |     0 |       0 | None                     | None                     | 1/5 795b/795b         |
| yellow/open | mbox_170207_enriched_170207            |   |     0 |       0 | None                     | None                     | 1/5 795b/795b         |
| yellow/open | stackexchange_161202a                  | * |   120 |       1 | 2017-02-23T15:21:18.668Z | 2017-02-23T01:03:57.000Z | 1/5 3.3mb/3.3mb       |
+-------------+----------------------------------------+---+-------+---------+--------------------------+--------------------------+-----------------------+
```
Get the ES cleaner using drop to remove expired indexes:
```
index_warrior.py -e http://localhost:9200 index drop 2017-02-23T15:22:18.501Z
+-------------+----------------------------------------+---+---------+-------+--------------------------+--------------------------+
| status      | index                                  | A | expired | count | metadata__timestamp      | metadata__updated_on     |
+-------------+----------------------------------------+---+---------+-------+--------------------------+--------------------------+
| yellow/open | .kibana                                |   |         |     2 | None                     | None                     |
| yellow/open | conf                                   |   |         |    22 | None                     | None                     |
| yellow/open | discourse_161121                       |   |         |  2099 | 2017-02-23T16:04:42.501Z | 2016-04-09T20:12:13.679Z |
| yellow/open | discourse_161121_enriched_161121a      |   |         | 14917 | 2017-02-23T16:04:42.501Z | 2016-04-09T20:12:13.679Z |
| yellow/open | gerrit_grimoire_161212                 |   | YES     |  2816 | 2017-02-23T15:21:34.338Z | 2017-02-23T16:20:39.000Z |
| yellow/open | gerrit_grimoire_161212_enriched_161212 |   | YES     |  2816 | 2017-02-23T15:21:34.338Z | 2017-02-23T16:20:39.000Z |
| yellow/open | git_coreos                             |   |         | 16435 | 2017-02-28T23:28:28.358Z | 2017-02-28T18:57:49.000Z |
| yellow/open | git_coreos_enriched                    |   |         |     0 | None                     | None                     |
| yellow/open | git_grimoire_161213                    | * | YES     |  2437 | 2017-02-23T15:21:36.797Z | 2017-02-23T11:16:30.000Z |
...
The indexes marked to be remove are:
 - gerrit_grimoire_161212 -> WARNING! could be a raw index
 - gerrit_grimoire_161212_enriched_161212
 - git_grimoire_161213 -> WARNING! it is linked from an alias
...
Are you sure? (y/n):

```

Browse the help to find out the details!
```
>> index_warrior.py index -h
usage: index_warrior.py index [-h] {show,compare,drop,delete} ...

positional arguments:
  {show,compare,drop,delete}
    show                show indexes
    compare             compare two indexes
    drop                drop index by metadata__timestamp
    delete              delete index

optional arguments:
  -h, --help            show this help message and exit

>> index_warrior.py alias -h
usage: index_warrior.py alias [-h] {add,delete,show,switch} ...

positional arguments:
  {add,delete,show,switch}
    add                 add alias
    delete              delete alias
    show                show aliases
    switch              move aliases from one index to another

optional arguments:
  -h, --help            show this help message and exit

```

The logo is a public domain image created by [SeriousTux](https://openclipart.org/user-detail/SeriousTux) and published at [openclipart.org](https://openclipart.org/detail/293914/woman-knight-warrior-in-armor-holding-a-sword)
