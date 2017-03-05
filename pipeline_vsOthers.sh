#!/bin/bash

#path definitions
DATA_PATH=datasets/hominidate/merged
HUMAN_FILE=$DATA_PATH/Hominidae/all_hominidae #_wohs
VS_OTHERS_FOLDER=$DATA_PATH/vsOthers/*
SCRIPT_PATH=/scripts
STEP_2_SCRIPT=$SCRIPT_PATH/split_dataset_vsOther.py
STEP_1_SCRIPT=$SCRIPT_PATH/model_from_csv.py
BASE_FOLDER=experiments/vsOthers_stratified_unbalanced
DAP_FOLDER=svmlin_dap
LLINEAR_T=$DAP_FOLDER/sklearn_liblinear_training.py
LLINEAR_V=$DAP_FOLDER/sklearn_liblinear_validation.py
RF_T=$DAP_FOLDER/sklearn_rf_training.py
RF_V=$DAP_FOLDER/sklearn_rf_validation.py
BASE_TEMP=$SCRIPT_PATH/temp_stratified_unb
mkdir $BASE_TEMP
OUT1=$BASE_TEMP/out1
FEATURE_FILE=$BASE_TEMP/features
BALANCE=false
SPLIT_PERC=0.2

POS_LINES=$(cat $HUMAN_FILE | wc -l)
POS_SAMPLES=$((POS_LINES-1))

#define file variables	
TEST_SAMPLES=$BASE_TEMP/train
TEST_LABELS=$BASE_TEMP/train.labels
VALIDATION_SAMPLES=$BASE_TEMP/validation
VALIDATION_LABELS=$BASE_TEMP/validation.labels

#start the run!
echo "[+][+] --- Start to run, oh Forrest!"

#mkdir $SCRIPT_PATH/temp

for f in $VS_OTHERS_FOLDER
do
    NEG_LINES=$(cat $f | wc -l) #estrae il numero di linee
	NEG_SAMPLES=$((NEG_LINES-1))
    NAME=$(basename $f) #estrae il nome del file dal path, usato per la creazione della cartella successivamente
    echo '[+][+] --- Running on' $NAME ' - ' $NEG_SAMPLES ' samples'
	echo '[+][+] --- Creo le cartelle per gli esperimenti'
    mkdir -p $BASE_FOLDER/$NAME/validation/
    SAMPLES=$SCRIPT_PATH/temp/$NAME.samples
	LABELS=$SCRIPT_PATH/temp/$NAME.labels
	echo '[+][+] --- Running MyScript, step 1'
    python $STEP_1_SCRIPT $HUMAN_FILE $f $SAMPLES $FEATURE_FILE $LABELS #script 1: merge pos £ neg in 1 file
	echo '[+][+] --- Running MyScript, step 2'
    python $STEP_2_SCRIPT $SAMPLES $LABELS $POS_SAMPLES $NEG_SAMPLES $TEST_SAMPLES $VALIDATION_SAMPLES $TEST_LABELS $VALIDATION_LABELS $BALANCE $SPLIT_PERC #script 2: split train/test
    #exit
	echo '[+][+] --- Preparation-Scripts Ran'
		
    #copy file in places
	echo "[+][+] --- Moving stuff around"
	mv $TEST_SAMPLES $BASE_FOLDER/$NAME/
	mv $TEST_LABELS $BASE_FOLDER/$NAME/
	mv $FEATURE_FILE $BASE_FOLDER/$NAME/
	mv $VALIDATION_SAMPLES $BASE_FOLDER/$NAME/validation/
	mv $VALIDATION_LABELS $BASE_FOLDER/$NAME/validation/
	
	#define Args for scikit
	
	LT_ARGS=''
	LV_ARGS=--tslab=$BASE_FOLDER/$NAME/validation/validation.labels
	RFT_ARGS=''
	RFV_ARGS=--tslab=$BASE_FOLDER/$NAME/validation/validation.labels
	
	#Run ML Scripts
	echo '[+][+] --- Running LLinear-Test for ' $NAME
    python $LLINEAR_T $LT_ARGS $BASE_FOLDER/$NAME/train $BASE_FOLDER/$NAME/train.labels $BASE_FOLDER/$NAME/llinear
	echo '[+][+] --- Running LLinear-Validation for ' $NAME
	for fname in $BASE_FOLDER/$NAME/llinear/*.log
    do
        CONFIG_FILE=$fname
        echo 'config file: ' $CONFIG_FILE
    done;
	python $LLINEAR_V $LV_ARGS $CONFIG_FILE $BASE_FOLDER/$NAME/validation/validation $BASE_FOLDER/$NAME/llinear/validation/
	echo '[+][+] --- Running RF-Test for ' $NAME
	mkdir -p $BASE_FOLDER/$NAME/rf/validation/
    python $RF_T $RFT_ARGS $BASE_FOLDER/$NAME/train $BASE_FOLDER/$NAME/train.labels $BASE_FOLDER/$NAME/rf
	echo '[+][+] --- Running RF-Validation for ' $NAME
	for fname in $BASE_FOLDER/$NAME/rf/*.log
    do
        CONFIG_FILE=$fname
        echo 'config file: ' $CONFIG_FILE
    done;
	python $RF_V $RFV_ARGS $CONFIG_FILE $BASE_FOLDER/$NAME/validation/validation $BASE_FOLDER/$NAME/rf/validation/    
done;
