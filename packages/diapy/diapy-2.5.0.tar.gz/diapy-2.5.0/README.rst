diapy
=====

A rough diary manager based on python.

Diapy uses cryptography.fernet to encrypt your top secret.

Installation
------------

Simple, crude.

::

    pip install diapy

Usage
-----

class Diary(path): The main instance. When path doesn't exist, it will
ask you for the title of your new diary.

Diary.DiarySpecific: The diary handler returned by get function.

Diary.DiarySpecific.save\_file(path): You can save a file from a diary
with file.

Diary.change\_pwd(): Change the main password of an opened file.

Diary.save(): Save a diary to the file on your hard-disk.

Diary.close(): Close a diary. After closing, you can't edit the diary.

Diary.get(date(s)): Date can both be a string/int length of 8 like
'20180214' or a list contains dates.

Diary.ls(mode=None, value=None, specific=True): - mode: None: returns
every date in record. 'year': classify by year, you can also change year
to month, date, tags, mood, location and weather.

-  value: None: returns everything exists. Others: depends on modes you
   choose. You can set a value so ls can only return diaries match the
   value.

-  specific: True: returns dates. False: returns the number of diary in
   each class.

Diary.edit(date, key, value): Edit one value of a date. Such as:
edit('20180214', 'mood', 'ffffffff'), and it will change the mood of
20180214 to ffffffff.

Diary.delete(date): Delete one diary of the date. **This is dangerous!**

Diary.new(content, tags, mood, date=None, time=None, location=None,
weather=None, temperature=None, file=None): - content: Your content of
this diary.

-  tags: Should be a list.

-  date: Should be a string like '20180214'

-  time: Should be a string like '23:01'

-  location: Should be a string.

-  weather: Should be a string.

-  temperature: Should be a str/int.

-  file: An additional file. Can be a photo, a text or any files
   **exists**.

Defalt None value: Diapy will try to fetch the info itself. That's
convenient.

Diary.recall(): Get a list of diary that are exactly a week/month/year
or several years ago.

Diary.export\_all(): Export your diary. Returns a dict. You can choose
whether to export your key at the same time.

Diary.import\_all(): Import diary that are exported by export\_all
function. **This will over-write your current diary!**

Diary.random(): Get a random diary.

About
-----

I am a secondary school student in China, and **i know my English is not
very good**. So if someone wants to **improve this document** i will
thank a lot! ## About(Chinese)
总算可以用中文写了。。。我还是个英语不好的孩子，如果看到上面的渣翻译有什么语法错误，各种错误请一定要指出！

什么，你问我为啥不写中文文档？因为我懒OTZ

第一次在github上传代码，我好方。。。如果有大佬来改进我的代码，我一定感激不尽。。。

Contributing
------------

I know, my code is bad too... You can improve it any time you want. I
will wait for your pull requests!

Donating
--------

...OK. That's actually unbeleavable that you will donate to my rough
code...

I don't even have an account for donating 233. If you want, you can
choose to contribute or give me some advice.
