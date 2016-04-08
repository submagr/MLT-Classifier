OBSERVATION 1
=============

Using Entire Data Set with 3:1 Train Test Ratio
Training for Kernel :  rbf  with C :  10

- Fine : 
	Number of  Bicycle  =  469
	Number of  Autorickshaw  =  32
	Number of  Rickshaw  =  55
	Number of  Motorcycle  =  437
	Number of  Person  =  1323
	Number of  Car  =  134

	Accuracy for Label :  Bicycle  is  0.923728813559
	Accuracy for Label :  Car  is  0.941176470588
	Accuracy for Label :  Person  is  0.984894259819
	Accuracy for Label :  Rickshaw  is  0.571428571429
	Accuracy for Label :  Autorickshaw  is  0.625
	Accuracy for Label :  Motorcycle  is  0.963636363636

- Coarse : 
	Number of  Four-Wheeler  =  134
	Number of  Two-Wheeler  =  906
	Number of  Pedestritian  =  1323
	Number of  Three-Wheeler  =  81

	Accuracy for Label :  Two-Wheeler  is  0.960352422907
	Accuracy for Label :  Four-Wheeler  is  0.941176470588
	Accuracy for Label :  Three-Wheeler  is  0.666666666667
	Accuracy for Label :  Pedestritian  is  0.97583081571
    Overall Accuracy =  0.957585644372

- Inferences : 
	1. Coarse vs Fine models seems to perform near each other. 
	2. Since they are performing equally well, we'll choose fine.  
