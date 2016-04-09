OBSERVATION 1
=============

Using Entire Data Set with 3:1 Train Test Ratio

- Fine : 
	Tuned Parameters for SVM : Kernel = rbf  with C :  10
	Accuracy for Label :  Bicycle  is  0.898305084746
	Accuracy for Label :  Car  is  1.0
	Accuracy for Label :  Person  is  0.984894259819
	Accuracy for Label :  Rickshaw  is  0.285714285714
	Accuracy for Label :  Autorickshaw  is  0.625
	Accuracy for Label :  Motorcycle  is  0.890909090909
    Overall Accuracy =  0.931707317073

- Coarse : 
	Tuned Parameters for SVM : Kernel = poly  with C :  10
	Number of  Four-Wheeler  =  134
	Number of  Two-Wheeler  =  906
	Number of  Pedestritian  =  1323
	Number of  Three-Wheeler  =  81

	Accuracy for Label :  Two-Wheeler  is  0.973568281938
	Accuracy for Label :  Four-Wheeler  is  0.852941176471
	Accuracy for Label :  Three-Wheeler  is  0.619047619048
	Accuracy for Label :  Pedestritian  is  0.981873111782
    Overall Accuracy =  0.959216965742


- Inferences : 
	1. Coarse vs Fine models seems to perform near each other. 
	2. Since they are performing equally well, we'll choose fine.  
