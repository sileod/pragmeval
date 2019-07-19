import pickle
import os
import pandas as pd


def flatten_tables(incoming_base_situ, outgoing_base_situ, incoming_base_spect, outgoing_base_spect):

    """
    1. for each table get dialogues
    2. for each dialogue, get distinct CDUs
    3. get the first element for each CDU
        3a.
    4. get all incoming/outgoing links
    5. attach to first element of CDU
    6. remove all rows where global_id == CDU and remove parent_schema_id, schema_composition and 'is_asymm' columns

    *** run checks: see that no 'emitter', 'turn_id', 'text' fields are 0
    *** create graphs for visual check

    :return: new incoming rows, new outgoing rows, indexes of incoming rows to be dropped, indexes of outgoing rows
    to be dropped
    """

    def get_new_rows(base_table_incoming, base_table_outgoing):

        def get_candidates(schema_id):
            """

            :param schema_id:
            :return: head of schema and marker to indicate whether the head itself is a schema
            which must be checked again
            """

            #print("schem_id", schema_id)
            # get firsts
            check_again = False

            # get node that belongs to schema which does not have an incoming id
            head_cands = base_table_incoming[(base_table_incoming['parent_schema_id'] == schema_id)
                                           & (base_table_incoming['incoming_relation_id'] == 0)][
                ['global_id', 'type', 'span_end']].drop_duplicates().get_values().tolist()

            if len(head_cands) == 1:
                head = head_cands[0][0]
                if head_cands[0][1] == 'Complex_discourse_unit':
                    check_again = True
            else:
                firste = min([h for h in head_cands], key=lambda t: t[2])
                head = firste[0]
                if firste[1] == 'Complex_discourse_unit':
                    check_again = True
            return head, check_again

        def get_first_elem(schema_id):
            """

            :param schema_id:
            :return: index of table row where head of schema is found
            """
            node, check = get_candidates(schema_id)

            #print(node, check)
            if check:
                while check:
                    schema_id = node
                    node, check = get_candidates(schema_id)
                    #print("checking", node, check)

            head_index = base_table_incoming[base_table_incoming['global_id'] == node].drop_duplicates().index.values[0]
            #print("head index", head_index)
            return head_index

        new_table_incoming = []
        new_table_outgoing = []
        in_drops = []
        out_drops = []
        cdus = base_table_incoming[base_table_incoming['type'] == 'Complex_discourse_unit']['global_id'].drop_duplicates().tolist()
        # for each cdu,
        for cdu in cdus:
            # get first element
            first = get_first_elem(cdu)
            first_elem = base_table_incoming.loc[first].tolist()
            # get incoming links and outgoing links from the CDU -- including the '0' links
            incs = base_table_incoming[base_table_incoming['global_id'] == cdu][['incoming_relation_id', 'relation_type']].get_values().tolist()
            outs = base_table_outgoing[base_table_outgoing['global_id'] == cdu][
                ['outgoing_relation_id', 'relation_type']].get_values().tolist()

            for inc in incs:
                new_elem = first_elem[:16]
                new_elem.extend(inc) # add relation type
                new_table_incoming.append(new_elem)

            for out in outs:
                new_elem = first_elem[:16]
                new_elem.extend(out) # add relation type
                new_table_outgoing.append(new_elem)

            # remove the row of the first element if there is no incoming link
            if first_elem[16] == 0:
                in_drops.append(first)
                # base_table_incoming = base_table_incoming.drop(first)

            out_first = base_table_outgoing[base_table_outgoing['parent_schema_id'] == cdu]['span_end'].idxmin()
            out_elem = base_table_outgoing.loc[out_first].tolist()
            if out_elem[16] == 0:
                out_drops.append(out_first)
                # base_table_outgoing = base_table_outgoing.drop(out_first)

        # print("list of base table incoming", list(base_table_incoming))
        # print("len new table", len(new_table_incoming[0]))
        #print(new_table_incoming[0])
        new_inc = pd.DataFrame(new_table_incoming, columns=list(base_table_incoming))
        new_out = pd.DataFrame(new_table_outgoing, columns=list(base_table_outgoing))

        return new_inc, new_out, in_drops, out_drops

    def clean_table(base_table):
        clean_table = base_table.drop(['schema_composition'], axis=1)
        clean_table = clean_table[~(clean_table['type'] == 'Complex_discourse_unit')].reset_index(drop=True)
        # add a row of 0's for schemas for graphing purposes
        clean_table['parent_schema_id'] = 0
        return clean_table

    # flatten situated tables

    add_inc, add_out, drop_in, drop_out = get_new_rows(incoming_base_situ, outgoing_base_situ)

    incoming_base_situ = incoming_base_situ.drop(incoming_base_situ.index[drop_in])
    outgoing_base_situ = outgoing_base_situ.drop(outgoing_base_situ.index[drop_out])

    incoming_base_situ = pd.concat([incoming_base_situ, add_inc])
    outgoing_base_situ = pd.concat([outgoing_base_situ, add_out])

    flat_inc_situ = clean_table(incoming_base_situ)
    flat_out_situ = clean_table(outgoing_base_situ)

    # pickle information from add_inc, add_out, drop_in, drop_out
    picks = [add_inc, add_out, drop_in, drop_out]
    output = open(pickle_path + 'flat_changes_list.pkl', 'wb')
    pickle.dump(picks, output)
    output.close()

    # flatten spect tables
    add_inc, add_out, drop_in, drop_out = get_new_rows(incoming_base_spect, outgoing_base_spect)

    incoming_base_spect = incoming_base_spect.drop(incoming_base_spect.index[drop_in])
    outgoing_base_spect = outgoing_base_spect.drop(outgoing_base_spect.index[drop_out])

    incoming_base_spect = pd.concat([incoming_base_spect, add_inc])
    outgoing_base_spect = pd.concat([outgoing_base_spect, add_out])

    flat_inc_spect = clean_table(incoming_base_spect)
    flat_out_spect = clean_table(outgoing_base_spect)

    return flat_inc_situ, flat_out_situ, flat_inc_spect, flat_out_spect


current_dir = os.getcwd()+"/stac_data_pickles/"
pickle_path = current_dir

# open situated master tables

pkl_file = open(pickle_path + 'incoming_base_situ.pkl', 'rb')
incoming_base_situ = pickle.load(pkl_file, encoding="latin-1")
pkl_file = open(pickle_path + 'outgoing_base_situ.pkl', 'rb')
outgoing_base_situ = pickle.load(pkl_file, encoding="latin-1")

# open spect master tables

pkl_file = open(pickle_path + 'incoming_base_spect.pkl', 'rb')
incoming_base_spect = pickle.load(pkl_file, encoding="latin-1")
pkl_file = open(pickle_path + 'outgoing_base_spect.pkl', 'rb')
outgoing_base_spect = pickle.load(pkl_file, encoding="latin-1")

pkl_file.close()

# get flat tables
flat_inc_situ, flat_out_situ, flat_inc_spect, flat_out_spect = \
    flatten_tables(incoming_base_situ, outgoing_base_situ, incoming_base_spect, outgoing_base_spect)

# pickle and save flat tables

output = open(pickle_path + '/incoming_flat_situ.pkl', 'wb')
pickle.dump(flat_inc_situ, output)

output = open(pickle_path + '/outgoing_flat_situ.pkl', 'wb')
pickle.dump(flat_out_situ, output)

output = open(pickle_path +'/incoming_flat_spect.pkl', 'wb')
pickle.dump(flat_inc_spect, output)

output = open(pickle_path + '/outgoing_flat_spect.pkl', 'wb')
pickle.dump(flat_out_spect, output)

output.close()

print("flattened tables created")


