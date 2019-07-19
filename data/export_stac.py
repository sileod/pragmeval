import pickle
import os
import pandas as pd
from tqdm import tqdm
import numpy as np
from collections import Counter
from tqdm import tqdm_notebook as tqdm

data_dir = os.getcwd() + "/stac_data_pickles/"

f = open(data_dir + 'outgoing_flat_situ.pkl', 'rb')   # 'r' for reading; can be omitted
outgoing_full = pickle.load(f , encoding = 'latin1')

fout = open(data_dir + 'incoming_flat_situ.pkl', 'rb')   # 'r' for reading; can be omitted
incoming_full = pickle.load(fout , encoding = 'latin1')

incoming_full[:2]

tmp = incoming_full[['dialogue_num', 'span_end', 'global_id']].drop_duplicates()

tmp = tmp.sort_values(['dialogue_num', 'span_end'])

tmp.reset_index(inplace=True)

new_incoming = pd.merge(incoming_full, tmp[['index', 'global_id']], on=['global_id'], how='left')

new_outgoing = pd.merge(outgoing_full, tmp[['index', 'global_id']], on=['global_id'], how='left')


#get relations table using the above dialogue list
rels_df = new_incoming[~(new_incoming['incoming_relation_id'] == 0)][['doc', 'global_id', 'incoming_relation_id', 'relation_type', 'span_end', 'turn_id', 'emitter', 'addressee', 'dialogue_act', 'surface_act', 'text', 'type', 'index']]
rels_df.rename(columns={'incoming_relation_id': 'relation_id', 'global_id': 'target_id', 'span_end': 'target_span_end', 'turn_id': 'target_turn_id', 'emitter': 'target_emitter', 'addressee': 'target_addressee', 'dialogue_act': 'target_dialogue_act', 'surface_act': 'target_surface_act', 'text': 'target_text', 'type':'target_type', 'index': 'target_index'}, inplace=True)

rels_targets = new_outgoing[~(new_outgoing['outgoing_relation_id'] == 0)][['global_id', 'outgoing_relation_id', 'dialogue_num', 'span_end', 'turn_id', 'emitter', 'addressee', 'dialogue_act', 'surface_act', 'text', 'type', 'index']]
rels_targets.rename(columns={'outgoing_relation_id': 'relation_id', 'global_id': 'source_id',  'span_end': 'source_span_end', 'turn_id': 'source_turn_id', 'emitter': 'source_emitter', 'addressee': 'source_addressee', 'dialogue_act': 'source_dialogue_act', 'surface_act': 'source_surface_act', 'text': 'source_text', 'type': 'source_type', 'index': 'source_index'}, inplace=True)

# inner merge to not have NaN on left or right
rels_final = pd.merge(rels_df, rels_targets, on='relation_id', how='inner').drop_duplicates()

rels_final[:2]

rels_final['distance'] = abs(rels_final['target_index'] - rels_final['source_index'])

#### Look At Relation Distributions:

rels_final[['relation_type', 'distance']][:1]

d = rels_final[rels_final.relation_type == 'Question_answer_pair'].groupby('distance').size()

rels_final.relation_type.drop_duplicates()


rels_final[rels_final['distance'] <=20].shape

rels_final[(rels_final.target_type == 'Segment') & (rels_final.distance > 4)].shape


rels_final.shape[0] - rels_final[['source_id', 'target_id']].drop_duplicates().shape[0]

#what are the relations?
comp = pd.DataFrame(rels_final.groupby(['target_id', 'source_id']).size()).reset_index()

doubles = comp[comp[0] > 1][['target_id', 'source_id']].get_values()

#make relation frequency dict 
rel_freq = {k:v for (k,v) in pd.DataFrame(incoming_full[~(incoming_full['relation_type'] == 0)][['global_id', 'relation_type']].drop_duplicates().groupby('relation_type').size()).reset_index().get_values()}

rel_freq['Comment']

#find the relation ids of the doubles with less frequent relation types
to_remove = [] #these are relation_ids to remove
for d in doubles:
    #print(d)
    vals = rels_final[(rels_final['target_id'] == d[0]) & (rels_final['source_id'] == d[1])][['relation_id', 'relation_type']].get_values()
    if rel_freq[vals[0][1]] > rel_freq[vals[1][1]]:
        to_remove.append(vals[1][0])
    else:
        to_remove.append(vals[0][0])

len(to_remove)

#remove these relations from the rels_final dataframe
rels_final = rels_final[~(rels_final['relation_id'].isin(to_remove))]

#make sure that the rels_final shape is always 43012
rels_final.shape

#### Create full candidates table:

working = new_incoming[['doc', 'dialogue_num', 'global_id', 'span_end', 'turn_id', 'type', 'emitter', 'addressee', 'dialogue_act', 'text', 'surface_act', 'index']].drop_duplicates()

#for dialogue
#sort by span_end number
#reset index
#for each row in the dialogue, take all rows that are after it using the index (can adjust this)
#*if same turn id, add a pair for each direction
#*if consecutive turn id and same speaker, then add pair for each direction

#for d in dialogues:
all_pairs = []
dialogues = working['dialogue_num'].drop_duplicates().tolist()
for d in tqdm(dialogues):
    tmp = working[working['dialogue_num'] == d].sort_values('span_end').reset_index(drop=True)
    ids = tmp.index.tolist()
    for i in ids:
        #get name of speaker to check for poss. backward links
        i_emitter = tmp.loc[i].emitter
        span_end_fordistance = tmp.loc[i].span_end
        pairs = [k for k in ids if k > i and k < i + 10]
        #pairs = [k for k in ids if k > i]
        if pairs:
            if i_emitter in ['UI', 'Server']:
                back_flag = 0 #changes to 0 once finds different speaker 
            else:
                back_flag = 1
            for p in pairs:
                #print("distance:", abs(tmp.loc[p].span_end - span_end_fordistance))
                left = tmp.loc[i].tolist()
                right = tmp.loc[p].tolist()[1:]
                left.extend(right)
                all_pairs.append(left)
                if back_flag:
                    if tmp.loc[p].emitter == i_emitter:
                        #put both directions
                        left = tmp.loc[p].tolist()
                        right = tmp.loc[i].tolist()[1:]
                        left.extend(right)
                        all_pairs.append(left)
                    else:
                        back_flag = 0

#down 147,857 relations from 663469
len(all_pairs)

all_pairs[0]

candidates = pd.DataFrame(all_pairs, columns=['doc', 'dialogue_num', 'source_id', 'source_span_end', 'source_turn_id', 
                                          'source_type',  'source_emitter', 'source_addressee', 
                                          'source_dialogue_act', 'source_text', 'source_surface_act', 'source_index', 'dialogue_num_y', 'target_id', 
                                          'target_span_end', 'target_turn_id', 'target_type', 'target_emitter',
                                        'target_addressee','target_dialogue_act', 'target_text', 'target_surface_act', 
                                            'target_index'])

#### Add relation type numbers

#add relation types
candidates = pd.merge(candidates, rels_final[['source_id', 'target_id', 'relation_id', 'relation_type']], on=['source_id', 'target_id'], how='left')


#replace all "NaN" by "no_relation"
candidates.fillna(value='no_relation', inplace=True)

#should have the same number of rows as before the merge
candidates.shape

rels_final.shape

candidates[~(candidates.relation_type == 'no_relation')].shape

#### <Add class numbers, etc.:_add class index and column for 1/0 attachment

#add class numbers to table
types_class = candidates.groupby('relation_type').size().reset_index().sort_values(0, ascending=False).relation_type.tolist()
relation_type_to_index = {v:k for (k,v) in dict(enumerate(types_class)).items()}

candidates['classid'] = candidates['relation_type'].map(lambda x:relation_type_to_index[x])
#add attachment column
candidates['attachment'] = candidates['relation_type'].map(lambda x:0 if (x == 'no_relation') else 1)

candidates['distance'] = abs(candidates.source_index - candidates.target_index)

candidates = candidates[['doc', 'dialogue_num', 'source_id', 'source_span_end', 'source_turn_id',
       'source_type', 'source_emitter', 'source_addressee',
       'source_dialogue_act', 'source_text', 'source_surface_act',
       'dialogue_num_y', 'target_id', 'target_span_end',
       'target_turn_id', 'target_type', 'target_emitter', 'target_addressee',
       'target_dialogue_act', 'target_text', 'target_surface_act',
       'relation_id', 'relation_type', 'classid',
       'attachment', 'distance']]

#### Split Training and Test

test_games = ['s2_leagueM_game4', 'pilot02', 's1_league3_game3', 's2_league4_game2']

test_set = (candidates.doc == 's2_leagueM_game4') | (candidates['doc'] == 'pilot02') | (candidates['doc'] == 's1_league3_game3') | (candidates['doc'] == 's2_league4_game2')
candidates_train = candidates[~(candidates['doc'].isin(test_games))]
candidates_test = candidates[(candidates['doc'].isin(test_games))]

candidates_train.shape

candidates_test.shape


#### Create full candidates table

# Save Candidates in a pickle file
#whatever path you want
new_pickle_path = data_dir
output = open(new_pickle_path + '/candidates_train_d10_ALLRELS.pkl', 'wb')
pickle.dump(candidates_train, output)

output = open(new_pickle_path + '/candidates_test_d10_ALLRELS.pkl', 'wb')
pickle.dump(candidates_test, output)
output.close()

#### <font color='5D32E8'>11. _remove all EEU-only dialogues:_<br></font>

lod = candidates_train[candidates_train.source_type == 'Segment'].dialogue_num.drop_duplicates()

lod_candidates = candidates_train[candidates_train.dialogue_num.isin(lod)]

lod_candidates = lod_candidates.reset_index(drop=True)

lod_candidates.shape

#how many participate in some relation?
len(lod_candidates[~(lod_candidates.classid == 0)].target_id.drop_duplicates())

lod_candidates[lod_candidates.source_span_end > lod_candidates.target_span_end].shape

# Save in a pickle file
stac_pickle_path = data_dir
output = open(stac_pickle_path + 'candidates_train_dropeeu_d10_ALLRELS.pkl', 'wb')
pickle.dump(lod_candidates, output)
output.close()

tlod = candidates_test[candidates_test.source_type == 'Segment'].dialogue_num.drop_duplicates()
tlod_candidates = candidates_test[candidates_test.dialogue_num.isin(tlod)]

tlod_candidates = tlod_candidates.reset_index(drop=True)

# Save in a pickle file
stac_pickle_path = data_dir
output = open(stac_pickle_path + 'candidates_test_dropeeu_d10_ALLRELS.pkl', 'wb')
pickle.dump(tlod_candidates, output)
output.close()
