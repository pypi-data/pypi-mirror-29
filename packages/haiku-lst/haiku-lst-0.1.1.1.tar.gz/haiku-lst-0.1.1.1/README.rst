=======
Haiku
=======

Introduce
============

A Modification of LibShortText_ and LIBLINEAR_.

- Uses Wissen Text Analyzer
- Feature Selection
- API Exported by Skitai App Engine
- Win32 support (need MSVC)

.. _LibShortText: https://www.csie.ntu.edu.tw/~cjlin/libshorttext/
.. _LIBLINEAR: https://www.csie.ntu.edu.tw/~cjlin/liblinear/


Installation
=============

.. code:: bash

  git clone https://gitlab.com/hansroh/haiku
  cd haiku
  python setup.py build install


Basic Usage
=============

.. code:: python

  import haiku
  
  model_path = "./golforbed"  
  analyzer =  haiku.StandardAnalyzer (max_term = 200, stem_level = 2, make_lower_case = 1)
 
  trainset = [
      ('Golf', "cloudy cold calm"),
      ('Golf', "sunny warm"),
      ('Bed', "rainy hot"),
      ('Golf', "sunny hot windy"),
      ('Bed', "windy cloudy cold"),
      ('Bed', "rainy cloudy cold"),
  ]
  
  # training
  h = haiku.Haiku (model_path, haiku.CL_L2, analyzer)
  # pruning by document frequency and scoring by meth (FS_CF means category frequency)
  h.select (data, mindf = 0, maxdf = 0, top = 0, meth = haiku.FS_CF)
  # set training options: uni/bigram and feature representation
  h.train (haiku.BIGRAM, haiku.FT_BIN)
  h.close ()
  
  # guessing
  h = haiku.Haiku (model_path, haiku.CL_L2, analyzer)
  h.load ()
  print (h.guess ("sunny cold windy"))
  h.close ()


Exporting API through Skitai App Engine
===========================================

Place model data into *app_root/resources/haikus/golforbed*.

.. code:: python

  import haiku
  import skitai
  
  if __name__ == "__main__":
    
    pref = skitai.pref ()
    pref.config.resource_dir = skitai.joinpath ('resources')
    skitai.mount ("/", haiku, "app", pref)
    skitai.run (port = 5005)

Go to http://127.0.0.1:5000/haiku/golforbed/guess?q=sunny%20cold%20windy.

