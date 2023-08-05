cd haiku\classifier\learner
nmake -f Makefile.win
cd liblinear
nmake -f Makefile.win clean all
nmake -f Makefile.win lib
cd ..\..\..\..
