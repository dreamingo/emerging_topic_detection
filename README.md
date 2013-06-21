Popular Event Detection On Sina Weibo
====================================

Detect emerging topic in SYSU community on Sina Weibo

Notoice
---------------
I strongly recommend you should read this README and other dataFile of this project in linux, or in encoding UTF-8, not Windows GBK


Dependencies
------------

* Linux Platform(Ubuntu 12.04)
    * Python2.7 (Python3 is not supported)
    * python-bs4
    * python-htmllib5
    * jieba

Installation
-------------
Use the following command to install python libraries

    sudo apt-get install python-bs4
    sudo apt-get install python-htmllib5
    sudo apt-get install pip
    sudo pip install jieba


Resource files
----------------

    .
    ├── doc                         #document of the project
    │   ├── ped_report
    │   └── presentation.ppt
    │ 
    ├── README.md
    │ 
    └── src
        ├── algorithm               #The src of main algorithm
        │   ├── data
        │   ├── dataCrawler
        │   ├── debug
        │   └── ped
        │ 
        └── presentationWebsite     #The presentation website of the popular event


Data
-----------------

Because the weibo&user data was so large in this project, if you want, you can contact us: 

* dreamingo.ozm@gmail.com
* zbweng@gmail.com

Todo
------
1. More explicit of spliting the word
Since the package Jieba did not work well on the colloquial text of sina weibo. In the future we will try to train our language model to fit the colloquial text well

2. More explicit and expressive term for topic
In the future we will combine the advantage of the named entity in the paper *Open domain event extraction from twitter SIGKDD 2012*. We will try hard to let the term in one topic to be more expressive


