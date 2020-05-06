import os 
import numpy as np
import pandas as pd
import itertools
import z3
import math
import opendp.whitenoise.core as wn

''' 
load data
'''
def load_data():
    # load data 
    # data = pd.read_csv(os.path.join('data', 'pums_1000.csv')) #TODO: add back after testing
    # data['agebinned'] = pd.cut(data['age'], bins = range(0, 101, 5), right = False) #TODO: add back after testing
    data = pd.read_csv(os.path.join('..', 'data', 'simplified_synthetic_pums_500.csv')) #TODO: remove after testing
    data['agebinned'] = pd.cut(data['age'], bins = range(20, 51, 5), right = False) #TODO: remove after testing
    data['race'] = data['race'].astype('category')
    data['educ'] = data['educ'].astype('category')
    data = data.drop(['age'], axis = 1)

    orig_data = data.copy() # save for comparison later
    orig_data['agebinned'] = orig_data['agebinned'].astype(str)
    orig_data['agebinned'] = [elem.replace(' ', '') for elem in orig_data['agebinned']]
    orig_data['agebinned'] = [elem.replace('[', '') for elem in orig_data['agebinned']]
    orig_data['agebinned'] = [elem.replace('(', '') for elem in orig_data['agebinned']]
    orig_data['agebinned'] = [elem.replace(']', '') for elem in orig_data['agebinned']]
    orig_data['agebinned'] = [elem.replace(')', '') for elem in orig_data['agebinned']]
    orig_data['income'] = orig_data['income'].astype(float)
    orig_data = orig_data.sort_values(by = list(orig_data.columns))

    data = pd.get_dummies(data)
    
    data['sex_1'] = data['sex']
    data['sex_0'] = 1 - data['sex_1']
    data = data.drop('sex', axis = 1)
    
    data['married_1'] = data['married']
    data['married_0'] = 1 - data['married_1']
    data = data.drop('married', axis = 1)    

    # change this to regex?
    data.columns = [col.replace(' ', '') for col in data.columns]
    data.columns = [col.replace('[', '') for col in data.columns]
    data.columns = [col.replace('(', '') for col in data.columns]
    data.columns = [col.replace(']', '') for col in data.columns]
    data.columns = [col.replace(')', '') for col in data.columns]
    return(orig_data, data)

''' 
get partial power set (without empty set) -- all combinations up to k
'''
def partial_powerset_minus_null(iterable, k):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, k + 1))

def get_plausible_variable_combinations(non_income_data):
    variable_combinations = list(partial_powerset_minus_null(non_income_data, 5))
    plausible_variable_combinations = []

    for combination in variable_combinations:
        var_prefices = [elem.split('_')[0] for elem in combination]
        if len(var_prefices) == len(set(var_prefices)):
            plausible_variable_combinations.append(combination)
    return(plausible_variable_combinations)

def create_dicts(data, non_income_data, plausible_variable_combinations):
    count_dict = dict()
    priv_count_dict = dict()

    mean_income_dict = dict()
    priv_mean_income_dict = dict()
    
    median_income_dict = dict()
    priv_median_income_dict = dict()

    min_income_dict = dict()
    priv_min_income_dict = dict()
    
    max_income_dict = dict()
    priv_max_income_dict = dict()

    # get number of data elements with each set of variable values
    for i,combination in enumerate(plausible_variable_combinations):
        # print('run {0} of {1}'.format(i+1, len(plausible_variable_combinations)))

        if len(combination) == 1:
            dt = data[non_income_data[combination[0]] == 1]

        elif len(combination) == 2:
            dt = data[(non_income_data[combination[0]] == 1) & 
                      (non_income_data[combination[1]] == 1)]

        elif len(combination) == 3:
            dt = data[(non_income_data[combination[0]] == 1) & 
                      (non_income_data[combination[1]] == 1) & 
                      (non_income_data[combination[2]] == 1)]

        elif len(combination) == 4:
            dt = data[(non_income_data[combination[0]] == 1) & 
                      (non_income_data[combination[1]] == 1) & 
                      (non_income_data[combination[2]] == 1) & 
                      (non_income_data[combination[3]] == 1)]

        elif len(combination) == 5:
            dt = data[(non_income_data[combination[0]] == 1) & 
                      (non_income_data[combination[1]] == 1) & 
                      (non_income_data[combination[2]] == 1) & 
                      (non_income_data[combination[3]] == 1) & 
                      (non_income_data[combination[4]] == 1)]

        count_dict['__'.join(combination)] = dt.shape[0]
        mean_income_dict['__'.join(combination)] = np.mean(dt['income'])
        median_income_dict['__'.join(combination)] = np.median(dt['income'])
        min_income_dict['__'.join(combination)] = np.min(dt['income'])
        max_income_dict['__'.join(combination)] = np.max(dt['income'])

        with wn.Analysis() as analysis:
            # load data
            priv_data = wn.Dataset(value = list(dt['income']), num_columns = 1)

            # estimate sample size 
            count = wn.dp_count(data = wn.cast(priv_data, 'FLOAT'),
                                privacy_usage={'epsilon': .05},
                                lower=0,
                                upper=1000)
        analysis.release()
        priv_count_dict['__'.join(combination)] = max(0, count.value)

        with wn.Analysis() as analysis:
            # load data
            priv_data = wn.Dataset(value = list(dt['income']), num_columns = 1)           
            # get mean
            mean = wn.dp_mean(data = wn.cast(priv_data, 'FLOAT'),
                                                                    privacy_usage = {'epsilon': 0.1},
                                                                    data_lower = 0.,
                                                                    data_upper = 100_000.,
                                                                    data_n = max(1, count.value)
                                                                    )
            # get median
            median = wn.dp_median(data = wn.cast(priv_data, 'FLOAT'),
                                                                    privacy_usage = {'epsilon': 0.1},
                                                                    data_lower = 0.,
                                                                    data_upper = 100_000.,
                                                                    data_n = max(1, count.value)
                                                                    )
            # get min
            _min = wn.dp_minimum(data = wn.cast(priv_data, 'FLOAT'),
                                                                    privacy_usage = {'epsilon': 0.1},
                                                                    data_lower = 0.,
                                                                    data_upper = 100_000.,
                                                                    data_n = max(1, count.value)
                                                                    )

            # get max
            _max = wn.dp_maximum(data = wn.cast(priv_data, 'FLOAT'),
                                                                    privacy_usage = {'epsilon': 0.1},
                                                                    data_lower = 0.,
                                                                    data_upper = 100_000.,
                                                                    data_n = max(1, count.value)
                                                                    )
        analysis.release()
        priv_mean_income_dict['__'.join(combination)] = min(max(0, mean.value), 100_000)
        priv_median_income_dict['__'.join(combination)] = min(max(0, median.value), 100_000)
        priv_min_income_dict['__'.join(combination)] = min(max(0, _min.value), 100_000)
        priv_max_income_dict['__'.join(combination)] = min(max(0, _max.value), 100_000)

    return(count_dict, priv_count_dict, mean_income_dict, priv_mean_income_dict, median_income_dict, priv_median_income_dict, min_income_dict, priv_min_income_dict, max_income_dict, priv_max_income_dict)

def find_correct_5_ways(combination, five_way_interactions):
    five_way_combination_set = []
    for comb in five_way_interactions:
        if len(set(combination).intersection(comb)) == len(combination):
            five_way_combination_set.append(comb) 
    return(five_way_combination_set)

def create_elem_dicts(count_dict, priv_count_dict, five_way_interactions, five_way_interactions_names):
    elem_dict = dict()
    priv_elem_dict = dict()
    
    for five_way, five_way_name in zip(five_way_interactions, five_way_interactions_names):
        if count_dict[five_way_name] > 0:
            elem_dict[five_way] = ['{0}_{1}'.format(five_way_name, i) for i in range(count_dict[five_way_name])]
        if priv_count_dict[five_way_name] > 0:
            priv_elem_dict[five_way] = ['{0}_{1}'.format(five_way_name, i) for i in range(priv_count_dict[five_way_name])]

    return(elem_dict, priv_elem_dict)

def get_applications(five_way_interactions, five_way_interactions_names,
                    plausible_variable_combinations, plausible_variable_combinations_names, 
                    count_dict, priv_count_dict, mean_income_dict, priv_mean_income_dict, 
                    median_income_dict, priv_median_income_dict, min_income_dict, priv_min_income_dict, 
                    max_income_dict, priv_max_income_dict, elem_dict, priv_elem_dict, lowest_allowable_count,
                    use_medians, use_mins, use_maxes):
    applications = []
    priv_applications = []

    # enforce monotonically increasing income within the 5-way interaction level and ensure median is correct
    # (can do this because elements are indistuingishable at this level)
    for combination, combination_name in zip(five_way_interactions, five_way_interactions_names):
        # monotonically increasing within level of indistinguishability
        for index in range(count_dict[combination_name] - 1):
            applications.append('{0}_{1} <= {0}_{2}'.format(combination_name, index, index+1))
            priv_applications.append('{0}_{1} <= {0}_{2}'.format(combination_name, index, index+1))

        # enforce correct min/max/median
        if count_dict[combination_name] >= lowest_allowable_count:
            # enforce median
            if use_medians == True:
                n_comb = count_dict[combination_name]
                median_index = math.floor(n_comb / 2)
                if n_comb % 2 == 1:
                    applications.append('{0}_{1} == {2}'.format(combination_name, median_index, median_income_dict[combination_name]))
                else:
                    applications.append('{0}_{1}+{0}_{2} == {3}'.format(combination_name, median_index - 1, median_index, 2 * median_income_dict[combination_name]))

            # enforce min
            if use_mins == True:
                applications.append('{0}_0 == {1}'.format(combination_name, min_income_dict[combination_name]))
            
            # enforce max
            if use_maxes == True:
                applications.append('{0}_{1} == {2}'.format(combination_name, count_dict[combination_name]-1, max_income_dict[combination_name]))

        if priv_count_dict[combination_name] >= lowest_allowable_count:
            # enforce median
            if use_medians == True:
                priv_n_comb = priv_count_dict[combination_name]
                priv_median_index = math.floor(priv_n_comb / 2) 
                if priv_n_comb % 2 == 1:
                    priv_applications.append('{0}_{1} == {2}'.format(combination_name, priv_median_index, priv_median_income_dict[combination_name]))
                else:
                    priv_applications.append('{0}_{1}+{0}_{2} == {3}'.format(combination_name, priv_median_index - 1, priv_median_index, 2 * priv_median_income_dict[combination_name]))            
            
            # enforce min
            if use_mins == True:
                priv_applications.append('{0}_0 == {1}'.format(combination_name, priv_min_income_dict[combination_name])) 

            # enforce max
            if use_maxes == True:
                priv_applications.append('{0}_{1} == {2}'.format(combination_name, priv_count_dict[combination_name]-1, priv_max_income_dict[combination_name])) 


    ''' enforce income applications (5-way and more general) '''
    # all incomes >= 0
    flattened_elem_values = []
    priv_flattened_elem_values = []
    
    for elem in elem_dict.values():
        flattened_elem_values.extend(elem)
    for elem in priv_elem_dict.values():
        priv_flattened_elem_values.extend(elem)


    for elem in flattened_elem_values:
        applications.append('{0} >= 0'.format(elem))
    for elem in priv_flattened_elem_values:
        priv_applications.append('{0} >= 0'.format(elem))

    # get correct sums at various levels
    i = 1
    l = len(plausible_variable_combinations_names)
    for combination,combination_name in zip(plausible_variable_combinations, plausible_variable_combinations_names):
        # print('run {0} of {1}'.format(i, l))
        i += 1
        component_combinations = find_correct_5_ways(combination, elem_dict.keys()) # find corresponding 5-way interactions
        priv_component_combinations = find_correct_5_ways(combination, priv_elem_dict.keys()) # find corresponding 5-way interactions

        # non-private
        if count_dict[combination_name] >= lowest_allowable_count:
            income_applications = []
            for component_combination in component_combinations:
                if count_dict['__'.join(component_combination)] > 0:
                    income_applications.extend(elem_dict[component_combination])
            if len(income_applications) > 0:
                # ensure mean is correct within level
                applications.append('{0} == {1}'.format('+'.join(income_applications), int(count_dict[combination_name] * mean_income_dict[combination_name])))

        # private
        if priv_count_dict[combination_name] >= lowest_allowable_count:
            priv_income_applications = []
            for priv_component_combination in priv_component_combinations:
                if priv_count_dict['__'.join(component_combination)] > 0:
                    priv_income_applications.extend(priv_elem_dict[priv_component_combination])
            if len(priv_income_applications) > 0:
                # ensure mean is correct within level
                priv_applications.append('{0} == {1}'.format('+'.join(priv_income_applications), int(priv_count_dict[combination_name] * priv_mean_income_dict[combination_name])))
        
    return(applications, priv_applications)

def applications_to_solver(applications):
    # try building applications one by one
    solver = z3.Solver()
    solver_list = []

    for application in applications:
        l, m, r = application.split(' ')
        l_c = z3.Sum( [z3.Int(elem) for elem in l.split('+')] )
        try:
            r_c = float(r)
            r_c_lb = r_c - 1
            r_c_ub = r_c + 1
        except:
            r_c = z3.Int(r)

        # all of type elem_1 <= elem_2
        if m == '<=':
            solver.add(l_c <= r_c)
            solver_list.append(l_c <= r_c)
        # all of type elem == int
        elif m == '==':
            # NOTE: works only if we allow a margin of error -- is this coming from the conversion from mean to sum?
            solver.add(l_c >= r_c_lb)
            solver.add(l_c <= r_c_ub)
            solver_list.append(l_c >= r_c_lb)
            solver_list.append(l_c <= r_c_ub)
            # solver.add(l_c == r_c)
            # solver_list.append(l_c == r_c)
        # all of type elem >= 0
        elif m == '>=':
            solver.add(l_c >= r_c)
            solver_list.append(l_c >= r_c)

    return(solver, solver_list)

def check_solution(solver):
    if solver.check() == z3.sat:
        return solver.model()
    else:
        return False

def reconstruct_data(model, elem_dict):
    full_elem_list = []
    for elem in elem_dict.values():
        full_elem_list.extend(elem)

    df = pd.DataFrame(columns = ['educ', 'race', 'agebinned', 'sex', 'married', 'income'])
    for elem in full_elem_list:
        row = []
        values = elem.split('__')
        for value in values:
            components = value.split('_')
            row.append(components[1])
        row.append( model[z3.Int(elem)].as_long() )
        df = df.append(pd.DataFrame([row], columns = df.columns))
        df['educ'] = df['educ'].astype('int').astype('category')
        df['race'] = df['race'].astype('int').astype('category')
        df['sex'] = df['sex'].astype(int)
        df['married'] = df['married'].astype(int)
        df['income'] = df['income'].astype(float)
    return(df)

def get_models(F, M):
    result = []
    s = z3.Solver()
    s.add(F)
    while len(result) < M and s.check() == z3.sat:
        m = s.model()
        result.append(m)
        # Create a new application the blocks the current model
        block = []
        for d in m:
            # d is a declaration
            if d.arity() > 0:
                raise z3.Z3Exception("uninterpreted functions are not supported")
            # create a constant from declaration
            c = d()
            if z3.is_array(c) or c.sort().kind() == z3.Z3_UNINTERPRETED_SORT:
                raise z3.Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(z3.Or(block))
    return(result)

def compare_data(orig_data, recon_data):
    ''' compare original and reconstructed data '''
    # update column ordering to be consistent with recon_data
    orig_data = orig_data[recon_data.columns]

    # sort data
    orig_data = orig_data.sort_values(by = list(orig_data.columns)).reset_index().drop('index', axis = 1) 
    recon_data = recon_data.sort_values(by = list(recon_data.columns)).reset_index().drop('index', axis = 1)

    exact_rows = 0
    exact_indices = []
    inexact_indices = []
    problems = []
    for i in range(orig_data.shape[0]):
        if np.all(orig_data.iloc[i] == recon_data.iloc[i]):
            exact_rows += 1
            exact_indices.append(i)
        else:
            problems.append( (i, orig_data.iloc[i], recon_data.iloc[i]) )
            inexact_indices.append(i)

    # check for answers within range of allowable error
    within_2k = 0
    within_5k = 0
    for orig,recon in zip(orig_data['income'], recon_data['income']):
        if abs(orig - recon) <= 2000:
            within_2k += 1
        if abs(orig - recon) <= 5000:
            within_5k += 1

    return(orig_data, recon_data, exact_rows, within_2k, within_5k)
