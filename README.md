# I-Git-Cloner
Cloning and collecting stats of a git repository made easy.

## Requirements
---
```
1. Python (Version >=3.7)
2. Git
```

## Installation
---
```
git clone https://github.com/sarvesh4396/I-Git-Cloner.git
cd "I-Git-Cloner"
pip install -r requirements.txt
```
## Usage
---
```
python clone.py -h

usage: clone.py [-h] [-n NAME] [-g {pie,bar}] [-o OUTPUT] [-t TOPIC] [-trl TOPIC_REP_LIMIT] [--stats]
                [--onlystats] [--wayback]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --names NAME
                        name of the account with git repositry
  -g {pie,bar}, --graph {pie,bar}
                        graph format (default bar)
  -o OUTPUT, --output OUTPUT
                        cloning path
  -t TOPIC, --topics TOPIC
                        topics to search
  -trl TOPIC_REP_LIMIT, --rep_limit TOPIC_REP_LIMIT
                        topic search repository limit (default 30)
  --stats               stats of particular profile.
  --onlystats           only stats of a profile.
  --wayback             fetch profiles from searched topic repositries
  ```

A detailed usage guide is available on [Usage](https://github.com/sarvesh4396/I-Git-Cloner/wiki) section of the Wiki.

# Usage Notes
If you are using Anaconda in Windows use `python clone.py`.
If you are using Linux use `python3 clone.py`.

# Detailed Output
A detailed usage guide is available on [Output](https://github.com/sarvesh4396/I-Git-Cloner/wiki/Output) section of the Wiki.

# Contribution & License
You can contribute in following ways:

* Report bugs
* Develop plugins
* Give suggestions to make it better
* Fix issues & submit a pull request

Please read the [guidelines](https://github.com/sarvesh4396/I-Git-Cloner/wiki/Guidelines) before submitting a pull request or issue.

I-Git-Cloner is licensed under [GPL v3.0 license](https://www.gnu.org/licenses/gpl-3.0.en.html)
