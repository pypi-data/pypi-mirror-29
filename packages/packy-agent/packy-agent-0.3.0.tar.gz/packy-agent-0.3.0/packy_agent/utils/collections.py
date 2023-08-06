from __future__ import absolute_import


def deep_update(base_dict, update_with):
    for key, value in update_with.items():
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
            else:
                base_dict[key] = value
        else:
            base_dict[key] = value


def set_if(dict_, key, value, if_callable=lambda x: x):
    if if_callable(value):
        dict_[key] = value
