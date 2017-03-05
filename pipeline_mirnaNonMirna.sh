#!/bin/bash

#path definitions
SCRIPT_PATH=scripts/
STEP_1_SCRIPT=$SCRIPT_PATH/create_train_test_datasets.py
BASE_FOLDER=experiments/mirnaNonMirna/
DAP_FOLDER=svmlin_dap
LLINEAR_T=$DAP_FOLDER/sklearn_liblinear_training.py
LLINEAR_V=$DAP_FOLDER/sklearn_liblinear_validation.py
RF_T=$DAP_FOLDER/sklearn_rf_training.py
RF_V=$DAP_FOLDER/sklearn_rf_validation.py
OUT1=$BASE_TEMP/out1

BASE_TEMP=datasets/mirnaNonMirna/
#define file variables	
TEST_SAMPLES_BASE=$BASE_TEMP/train
TEST_LABELS_BASE=$BASE_TEMP/train.labels
VALIDATION_SAMPLES_BASE=$BASE_TEMP/test
VALIDATION_LABELS_BASE=$BASE_TEMP/test.labels
TEST_SAMPLES=$BASE_FOLDER/train
TEST_LABELS=$BASE_FOLDER/train.labels
VALIDATION_SAMPLES=$BASE_FOLDER/test
VALIDATION_LABELS=$BASE_FOLDER/test.labels

#start the run!
echo "[+][+] --- Start to run, oh Forrest!"
    #split the dataset
	python $STEP_1_SCRIPT
    #move dataset in place
	mv $TEST_SAMPLES_BASE $TEST_SAMPLES
	mv $TEST_LABELS_BASE $TEST_LABELS
	mv $VALIDATION_SAMPLES_BASE $VALIDATION_SAMPLES
	mv $VALIDATION_LABELS_BASE $VALIDATION_LABELS
	#define Args for scikit
	LT_ARGS=''
	LV_ARGS=--tslab=$VALIDATION_LABELS
	RFT_ARGS=''
	RFV_ARGS=--tslab=$VALIDATION_LABELS
    NAME=svm
    #llinear
	echo '[+][+] --- Running LLinear-Test for ' 
    python $LLINEAR_T $LT_ARGS $TEST_SAMPLES $TEST_LABELS $BASE_FOLDER/$NAME/llinear
    #llinear validation
    for fname in $BASE_FOLDER/$NAME/llinear/*.log
    do
        CONFIG_FILE=$fname
        echo 'config file: ' $CONFIG_FILE
    done;
	echo '[+][+] --- Running LLinear-Validation for ' $NAME
	python $LLINEAR_V $LV_ARGS $CONFIG_FILE $VALIDATION_SAMPLES $BASE_FOLDER/$NAME/llinear/validation/
    NAME=rf
	echo '[+][+] --- Running RF-Test for ' 
	mkdir -p $BASE_FOLDER/$NAME/rf
    python $RF_T $RFT_ARGS $TEST_SAMPLES $TEST_LABELS $BASE_FOLDER/$NAME/rf
    for fname in $BASE_FOLDER/$NAME/rf/*.log
    do
        CONFIG_FILE=$fname
        echo 'config file: ' $CONFIG_FILE
    done;
	echo '[+][+] --- Running RF-Validation for ' $NAME
	python $RF_V $RFV_ARGS $CONFIG_FILE $VALIDATION_SAMPLES $BASE_FOLDER/$NAME/rf/validation/    

