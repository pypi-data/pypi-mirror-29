"""
Copyright (C) 2013-2017 Calliope contributors listed in AUTHORS.
Licensed under the Apache 2.0 License (see LICENSE file).

optional.py
~~~~~~~~~~~

Optionally loaded constraints.

"""

import pyomo.core as po  # pylint: disable=import-error


def ramping_rate(model):
    """
    Ramping rate constraints.

    Depends on: node_energy_balance, node_constraints_build

    """
    m = model.m
    time_res = model.data['_time_res'].to_series()

    # Constraint rules
    def _ramping_rule(m, loc_tech, t, direction):
        x, y = loc_tech.split(":", 1)
        # e_ramping: Ramping rate [fraction of installed capacity per hour]
        ramping_rate_value = model.get_option(y + '.constraints.e_ramping')
        if ramping_rate_value is False:
            # If the technology defines no `e_ramping`, we don't build a
            # ramping constraint for it!
            return po.Constraint.NoConstraint
        else:
            # No constraint for first timestep
            # NB: From Pyomo 3.5 to 3.6, order_dict became zero-indexed
            if m.t.order_dict[t] == 0:
                return po.Constraint.NoConstraint
            else:
                carrier = model.get_option(y + '.carrier', default=y + '.carrier_out')
                if isinstance(carrier, dict): # conversion_plus technology
                    carrier = model.get_carrier(y, 'out', primary=True)
                diff = ((m.c_prod[carrier, loc_tech, t]
                         + m.c_con[carrier, loc_tech, t]) / time_res.at[t]
                        - (m.c_prod[carrier, loc_tech, model.prev_t(t)]
                           + m.c_con[carrier, loc_tech, model.prev_t(t)])
                        / time_res.at[model.prev_t(t)])
                max_ramping_rate = ramping_rate_value * m.e_cap[loc_tech]
                if direction == 'up':
                    return diff <= max_ramping_rate
                else:
                    return -1 * max_ramping_rate <= diff

    def c_ramping_up_rule(m, loc_tech, t):
        return _ramping_rule(m, loc_tech, t, direction='up')

    def c_ramping_down_rule(m, loc_tech, t):
        return _ramping_rule(m, loc_tech, t, direction='down')

    # Constraints
    m.c_ramping_up = po.Constraint(m.loc_tech, m.t, rule=c_ramping_up_rule)
    m.c_ramping_down = po.Constraint(m.loc_tech, m.t, rule=c_ramping_down_rule)


def group_fraction(model):
    """
    Constrain groups of technologies to reach given fractions of e_prod.

    """
    m = model.m

    def sign_fraction(group, group_type):
        o = model.config_model
        sign, fraction = o.group_fraction[group_type].get_key(group)
        return sign, fraction

    def group_set(group_type):
        try:
            group = model.config_model.group_fraction[group_type].keys()
        except (TypeError, KeyError):
            group = []
        return po.Set(initialize=group)

    def techs_to_consider(supply_techs, group_type):
        # Remove ignored techs if any defined
        gfc = model.config_model.group_fraction
        if 'ignored_techs' in gfc and group_type in gfc.ignored_techs:
            return [i for i in supply_techs
                    if i not in gfc.ignored_techs[group_type]]
        else:
            return supply_techs

    def equalizer(lhs, rhs, sign):
        if sign == '<=':
            return lhs <= rhs
        elif sign == '>=':
            return lhs >= rhs
        elif sign == '==':
            return lhs == rhs
        else:
            raise ValueError('Invalid sign: {}'.format(sign))

    supply_techs = (model.get_group_members('supply') +
                    model.get_group_members('supply_plus') +
                    model.get_group_members('conversion') +
                    model.get_group_members('conversion_plus'))

    # Sets
    m.output_group = group_set('output')
    m.capacity_group = group_set('capacity')
    m.demand_power_peak_group = group_set('demand_power_peak')

    # Constraint rules
    def c_group_fraction_output_rule(m, c, output_group):
        sign, fraction = sign_fraction(output_group, 'output')
        techs = techs_to_consider(supply_techs, 'output')
        rhs_loc_techs = [":".join([x, y]) for y in techs for x in m.x]
        lhs_loc_techs = [":".join([x, y]) for y in
                         model.get_group_members(output_group) for x in m.x]
        rhs = (fraction * sum(m.c_prod[c, loc_tech, t]
            for loc_tech in rhs_loc_techs for t in m.t))
        lhs = sum(m.c_prod[c, loc_tech, t]
            for loc_tech in lhs_loc_techs for t in m.t)
        return equalizer(lhs, rhs, sign)

    def c_group_fraction_capacity_rule(m, c, capacity_group):  # pylint: disable=unused-argument
        sign, fraction = sign_fraction(capacity_group, 'capacity')
        techs = techs_to_consider(supply_techs, 'capacity')
        rhs_loc_techs = [":".join([x, y]) for y in techs for x in m.x]
        lhs_loc_techs = [":".join([x, y]) for y in
                         model.get_group_members(capacity_group) for x in m.x]
        rhs = (fraction * sum(m.e_cap[loc_tech] for loc_tech in rhs_loc_techs))
        lhs = sum(m.e_cap[loc_tech]  for loc_tech in lhs_loc_techs)
        return equalizer(lhs, rhs, sign)

    def c_group_fraction_demand_power_peak_rule(m, c, demand_power_peak_group):
        sign, fraction = sign_fraction(demand_power_peak_group,
                                       'demand_power_peak')
        margin = model.config_model.system_margin.get_key(c, default=0)
        peak_timestep = model.t_max_demand.power
        y = 'demand_power'
        lhs_loc_techs = [":".join([x, y]) for y in
            model.get_group_members(demand_power_peak_group) for x in m.x]
        # Calculate demand peak taking into account both r_scale and time_res
        peak = (float(sum(model.m.r[":".join([x, y]), peak_timestep]
                      * model.get_option(y + '.constraints.r_scale', x=x)
                      for x in model.m.x))
                / model.data.time_res_series.at[peak_timestep])
        rhs = fraction * (-1 - margin) * peak
        lhs = sum(m.e_cap[loc_tech] for loc_tech in lhs_loc_techs)
        return equalizer(lhs, rhs, sign)

    # Constraints
    m.c_group_fraction_output = \
        po.Constraint(m.c, m.output_group, rule=c_group_fraction_output_rule)
    m.c_group_fraction_capacity = \
        po.Constraint(m.c, m.capacity_group, rule=c_group_fraction_capacity_rule)
    grp = m.demand_power_peak_group
    m.c_group_fraction_demand_power_peak = \
        po.Constraint(m.c, grp, rule=c_group_fraction_demand_power_peak_rule)

def max_r_area_per_loc(model):
    """
    ``r_area`` of all technologies requiring physical space cannot exceed the
    available area of a location. Available area defined for parent locations
    (in which there are locations defined as being 'within' it) will set the
    available area limit for the sum of all the family (parent + all descendants).

    To define, assign a value to ``available_area`` for a given location, e.g.::

        locations:
            r1:
                techs: ['csp']
                available_area: 100000

    To avoid including descendants in area limitation, ``ignore_descendants``
    can be specified as True for the location, at the same level as ``available_area``.

    """
    m = model.m
    locations = model._locations


    def _get_descendants(x):
        """
        Returns all locations in the family tree of location x, in one list.
        """
        descendants = []
        children = list(locations[locations._within == x].index)
        if not children:
            return []
        for child in children:
            descendants += _get_descendants(child)
        descendants += children
        return descendants

    def c_available_r_area_rule(m, x):
        available_area = model.config_model.get_key(
                            'locations.{}.available_area'.format(x), default=None)
        if not available_area:
            return po.Constraint.Skip
        if model.config_model.get_key(
            'locations.{}.ignore_descendants'.format(x), default=False):
            descendants = []
        else:
            descendants = _get_descendants(x)
        all_x = descendants + [x]
        loc_techs = [i for i in m.loc_tech_area
            if i.split(":")[0] in all_x
            and i not in m.loc_tech_demand]
        r_area_sum = sum(m.r_area[loc_tech] for loc_tech in loc_techs)
        # r_area_sum will be ``0`` if either ``m.y_r_area`` or ``all_x`` are empty
        return (r_area_sum <= available_area)

    m.c_available_r_area = po.Constraint(m.x, rule=c_available_r_area_rule)
