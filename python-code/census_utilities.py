"""
census_utlities.py
"""



def money2float(s):
   #Converts "$XXX, YYY" to XXXYYY
    try:
        return float( s[1:].replace(",","") )
    except:
       return s


def WMAEscore( prediction, response, weights):
    return abs( weights*(prediction-response) ).sum()/weights.sum()
    
    

def preprocess_dataframe( dataframe ):
    """
    Use this to preprocess crossvalidation data and testing data.
    
    """

    to_remove = ['Mail_Return_Rate_CEN_2010', 'State', 'State_name', 'County_name', 
             'County', 'GIDBG', 'Tract', 'Block_Group', 'Flag', 'weight']
    for to_rm in to_remove:
        try:
            del dataframe[to_rm]
        except:
            pass

        
    to_convert_to_float = ['Med_HHD_Inc_BG_ACS_06_10', 'Med_HHD_Inc_BG_ACSMOE_06_10', 'Med_HHD_Inc_TR_ACS_06_10', 'Med_HHD_Inc_TR_ACSMOE_06_10',
     'Aggregate_HH_INC_ACS_06_10', 'Aggregate_HH_INC_ACSMOE_06_10', 'Med_House_Val_BG_ACS_06_10','Med_House_Val_BG_ACSMOE_06_10','Med_house_val_tr_ACS_06_10',
    'Med_house_val_tr_ACSMOE_06_10', 'Aggr_House_Value_ACS_06_10', 'Aggr_House_Value_ACSMOE_06_10']

    for to_cn in to_convert_to_float:
        dataframe[to_cn] = dataframe[to_cn].map( money2float )
        

    #do a naive filling of missing data
    dataframe.fillna( method="bfill", inplace=True)
    dataframe.fillna( method="ffill", inplace=True)
    
    return dataframe
    

    
def cv( model, data, response, K=5):
    """
    model is the scikitlearn model, with parameters already set.
    """
    kf = KFold( len(response), K , indices = False) 
    print kf

    cv_scores = np.empty( K )
    i = 1
    for train, test in kf:

        training_data = data[ train]
        training_response = response[ train ]
        
        testing_data = data[ test ]
        testing_response = response[test]

        testing_weights = weights[ test ]
        training_weights = weights[ train ]



        model.fit( training_data, training_response )
        prediction = model.predict( testing_data )
        
        
        cv_scores[i-1] = WMAEscore( prediction, testing_response, testing_weights ) 
        print "%d Cross validation: %f" %(i, cv_scores[i-1] )
        i+=1
        
    print "Accuracy: %0.2f (+/- %0.2f)" % (cv_scores.mean(), cv_scores.std() / 2)



    