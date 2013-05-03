def analyze_links(exd_manager):
    # Construct ids maps

    ids_sets = {}
    ids_limits = {}
    ids_nums = {}

    for category_name in exd_manager.get_categories():
        if category_name.find('/') == -1:
            data = exd_manager.get_category(category_name).get_data()
            data_ln = data[list(data.keys())[0]]
            ids_sets[category_name] = set(data_ln.keys())
            ids_limits[category_name] = (min(ids_sets[category_name]), max(ids_sets[category_name]))
            ids_nums[category_name] = len(ids_sets[category_name])

    ids_to_analyze = {}
    for category_name in exd_manager.get_categories():
        if category_name.find('/') == -1:
            data = exd_manager.get_category(category_name).get_data()
            data_ln = data[list(data.keys())[0]]
            data_ln_id = data_ln[list(data_ln.keys())[0]]

            for index, member in enumerate(data_ln_id):
                if type(member) == int:
                    result_set = set([data_ln[id][index] for id in data_ln.keys()]) - set([-2, -1])
                    if len(result_set) > 9:
                        if not category_name in ids_to_analyze:
                            ids_to_analyze[category_name] = {}
                        ids_to_analyze[category_name][index] = result_set 

    results = {}
    for category_name in ids_to_analyze.keys():
        category_data = ids_to_analyze[category_name]
        for index in category_data.keys():
            values_set = category_data[index]

            limits_eligible_categories = []
            for limits_category_name, (min_value, max_value) in ids_limits.items():
                if min_value <= min(values_set) and max_value >= max(values_set):
                    limits_eligible_categories.append(limits_category_name)

            strict_eligible_categories = []
            for limits_category_name in limits_eligible_categories:
                if values_set.issubset(ids_sets[limits_category_name]):
                    strict_eligible_categories.append(limits_category_name)

            if len(strict_eligible_categories) > 0:
                num_values = len(values_set)

                if not category_name in results:
                    results[category_name] = {}

                results[category_name][index] = {
                    eligible_category_name: ((num_values/ids_nums[eligible_category_name]) * 100) for eligible_category_name in strict_eligible_categories
                }

    return results
                