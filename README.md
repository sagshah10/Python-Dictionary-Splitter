# PYTHON DICTIONARY SPLITTER (JSON SPLITTER)

As a recent graduate I have been constantly looking for ways to develop my skills. This project has been one such project where I wished to try and attempt to create something challenging that would not only, help me develop and put my skills to the test, but could also help other people. Before working on this project, I learnt about web scraping with python, and while I was learning it, I found that using the python dictionary (for accessing) / json (for offline storage) was a much more convenient way for handling data being scraped from the web. However, one major issue with python dictionary or json objects, is that they require to be constantly stored in RAM when a program is running, for it to be accessed, and this can lead to memory issues should a lot of data be held in it.

Therefore, this gave me the idea of developing my module, where I aim to split large and/or nested dictionaries into separate files, and then have a convenient way to only access the data you want at any given point in time. As I mentioned I am a recent graduate, and I know this final submitted work doesn’t seem so, but this project took me, about 4 months to fully develop. The code that I have uploaded today is simply a completed and mostly refactored version of the original code. The reason why it took so long was because, initially I was using either several different loops or functions to perform actions or functions within the module, however, I found this to be very long and confusing to look back and debug. I later found that converting aspects of my code to a recursive function, reduced the challenges of reading, understanding and debugging the code. However, recursive functions also brought along their own problems, such as data being wrongly handled, or errors caused due to "endless recursion" of a function or between functions.

However, I am finally happy to have it developed to a stage where it works as intended, and now I feel that there will be less bug fixing over increase or improved functionality for this module.


## How It Works?
** The aim for this module was for it to be imported for other scripts to use. Therefore, the following is based on a user having used "import dictSplit" on their script.

When the module is run for the first time, it creates the following path "Resources > JSONData > setup.json" on the currently worked on directory. here the "setup.json" file stores temporary information such as availableCount (which is what I use to keep track of splits), the path location and the maximum length of a single dictionary before it is split.

The following sample dictionary will be used to explain how my module works:

    d = {
           "a" : {"b" : 1, "c": 2},
           "d" : 3
        }

### CRUD (Create, Retrieve, Update Delete)

CRUD was one of the simplest and most straight forward concepts I learnt about in databases, and therefore I thought using such an approach would possibly make my module easy to operate. Therefore, with this in mind, my module has 4 major functions for a user:


#### 1) Create

The create function is intended to be used by the user only once, to either convert an existing dictionary into a split dictionary, or to create a foundation from which point further splits can occur.

To use this function simply call:

    dictSplit.Create(#Here is where you pass an existing dictionary or leave it blank for it initialise necessary files to begin further splitting.)

NOTE: this is intended to be used by the user once!! calling it after it has already been executed, will result to the current split dictionaries being deleted and a new one being created on its place (literally, I have set it to delete the whole JSONData folder, and then it recreates a new split, regardless of whether a new dictionary is parsed or not.)

Below shows examples of the ways this function can be called or executed:

    jsonDict.Create()

    OR

    d = {A Python Dictionary}
    jsonDict.Create(d)

Both methods begin by creating a "main.json" file within the JSONData folder, and any nest are further split out based on a tracked split number, whilst if the length of a dictionary or split out dictionary was greater than the max limit identified on "setup.json", then the excess is split out into individual files called as "mainSplit1.json" or "0Split1.json" depending on the split number.


#### 2) Retrieve

The retrieve function retrieves either the entire dictionary (if called without any parameters being parsed), or the data stored at a specific location based on the keys parsed by a user.

    To retrieve the entire dictionary, simply call:
        dictSplit.Retrieve()

    OR

    To access particular dictionary data stored within keys, for example:
        "d['a']['b']" would return 1, if d was stored in memory as the program was running.

    The same can be achieved by doing:
        "dictSplit.Retrieve('a', 'b')" to get the value 1.


##### Just want to retrieve keys Only?
If you would like to just retrieve a list of key names from the dictionary, you simply need to call:

    dictSplit.getKeys()     - By parsing no parameters it returns the keys stored on the "main.json" which is the parent to all other nests.
                            - This would return ["a", "d"]

    OR...

    dictSplit("a")      - to get ["b", "c"] as a return.

#### 3) Update

As I mentioned above the Create function can and must only be called once by the user, after that any further changes or modifications, must be made using this update function.

Implementing update frankly, was the hardest and most challenging aspect of this module for me, because I had to ensure I had incorporated functionality to adhere to several different types of scenarios that would be expected for this system to handle. One aspect of programming I really enjoy is to try and make complex actions simple, and I feel I have once again managed to do that with this Update function.

The Update function is contains 3 parameters and is defined as Update(Value, *Keys, replace = False):

a) Value - Here any type of data can be sent for value, whether it is a str, int, bool, array, dictionary, etc.., I have ensured I do the necessary work to adequately update the right data at the right location within the split dictionary (This is also why it was challenging).

b) *Keys - This is used to identify the exact location where data must be updated.

c) replace - by default this is set to "False". Setting it to "True" means, that you want to replace all the contents of the location where you wish to update your data, with the values you have given to me.

Example of how to use this module to get the same result, as you would, using python:


Example 1 - Emptying the Dictionary!
    "d = {}" - This changes the dictionary back to an empty Dictionary in python

    Ideally just use: "dictSplit.Create()" - as it is quicker, but you can also use:

    dictSplit.Update({}, Replace = True)   - This would also do the same, however it would take a lot longer


    OR!!

    "d['a'] = {}"   - This makes the nested dictionary empty.

    For this only the Update method can work, so don’t use Create().

    dictSplit.Update({}, "a", Replace = True)

    NOTE: By setting Replace to True, informs that you wish to replace all the contents of the location where you wish to make the Update, with the given value.



Example 2 - Changing the data type of a value:

    d["a"] = 2  - This would remove the entire nest and substitute it with 2 on the above dictionary d.

    dictSplit.Update(2, "a", replace = "True")    - This would perform the same, by removing all the split out nested dictionaries, and replacing it with another value.

    NOTE: It would have shown an error if replace was not set to True, because you cannot add a non-dictionary value to an existing dictionary.

    I have tried my best to replicate all the standards ways of manipulating python dictionaries using python, to hopefully try and make it easier and more natural for the user to learn and use.


Example 3 - Adding new keys and values to existing dictionary:

    d["g"] = "h" - This assigns a new key "g" and value "h" to the main dictionary

    dictSplit.Update({"g" : "h"}) - This would produce the same result, however both key "g" and value "h" must be enclosed within aa dictionary, and then parsed as a part of the value parameter. By Parsing no keys, states that you wish to update new values to the main parent dictionary.

    OR

    d["a"]["g"] = "h"   - Here a new Key "g" and value "h" is added to the nested dictionary d["a"]

    dictSplit.Update({"g" : "h"}, "a") - This is similar to the above solution, however, the key "a" also had to be parsed, to inform the module the exact location where you wish to add this new dictionary values.


    NOTE: Remember if "replace = True" was parsed, then this value would overwrite all other values stored within d["a"].


#### 4) Delete

Deleting items from the split dictionary is also just as simple.

    similar to "del d"
    using "splitDict.Delete()" - Would delete all contents within the split dictionaries.

    OR

    Similar to "del d['a']"
    using splitDict.Delete('a') - Would delete key "a" and all the items associated with key "a"


# CONCLUSION

I have tried my best to explain how to incorporate my module, however should there be any more questions, please don't hesitate to ask.

I am new to GitHub, and this is my first ever major project that I developed on my own without any other support except for general resources found online, therefore I would really love to hear all feedback or opinions about me or my work.

I have already identified areas of improvement, but I may implement these features later, or should people request me to do so. These new features include, a possible array splitter, for splitting large arrays into separate files, and a more convenient way to allow users to change the default path and max limit before splitting a dictionary.

The speed at which this module operates is definitely not as fast as when the whole JSON or Dictionary file is stored in RAM, however based on a few tests, where I used a 5Mb sized JSON file with several nested dictionaries, I found that:

(Time Readings based on time given by Sublime Text 3, after processing)
 - Converting the dictionary to a split version took a couple of seconds
 - Reading was extremely quick, usually around 0.3 seconds
 - Writing can vary, 0.2 seconds if simply writing and not deleting or, up to 1.2 seconds when I attempted to substitute a large set of nested dictionaries with a single integer value.

Which although was 3 times slower, was still fairly quick in my opinion.

I will later try to do more realistic tests, which test speed and memory use, and then hopefully I can share those results at a later stage.
