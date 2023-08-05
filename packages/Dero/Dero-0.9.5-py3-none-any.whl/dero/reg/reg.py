from statsmodels import api as sm

from .tools import _to_list_if_str, _to_list_if_tuple
from .fe import fixed_effects_reg_df_and_cols_dict, extract_all_dummy_cols_from_dummy_cols_dict
from .interact import create_interaction_variables, delete_interaction_variables, _collect_variables_from_interaction_tuples

def reg(df, yvar, xvars, robust=True, cluster=False, cons=True, fe=None, interaction_tuples=None):
    """
    Returns a fitted regression. Takes df, produces a regression df with no missing among needed
    variables, and fits a regression model. If robust is specified, uses heteroskedasticity-
    robust standard errors. If cluster is specified, calculated clustered standard errors
    by the given variable.

    Note: only specify at most one of robust and cluster.

    Required inputs:
    df: pandas dataframe containing regression data
    yvar: str, column name of outcome y variable
    xvars: list of strs, column names of x variables for regression

    Optional inputs:
    robust: bool, set to True to use heterskedasticity-robust standard errors
    cluster: False or str, set to a column name to calculate standard errors within clusters
             given by unique values of given column name
    cons: bool, set to False to not include a constant in the regression
    fe: None or str or list of strs. If a str or list of strs is passed, uses these categorical
    variables to construct dummies for fixed effects.
    interaction_tuples: tuple or list of tuples of column names to interact and include as xvars

    Returns:
    If fe=None, returns statsmodels regression result
    if fe is not None, returns a tuple of (statsmodels regression result, dummy_cols_dict)
    """
    fe = _set_fe(fe)
    interaction_tuples = _set_interaction_tuples(interaction_tuples)
    regdf, y, X, dummy_cols_dict = _get_reg_df_y_x(df, yvar, xvars, cluster, cons, fe, interaction_tuples)

    mod = sm.OLS(y, X)

    result = _estimate_handling_robust_and_cluster(regdf, mod, robust, cluster)

    # Only return dummy_cols_dict when fe is active
    if fe is not None:
        return result, dummy_cols_dict
    else:
        return result


def _estimate_handling_robust_and_cluster(regdf, model, robust, cluster):
    assert not (robust and cluster)  # need to pick one of robust or cluster

    if robust:
        return model.fit(cov_type='HC1')

    if cluster:
        groups = regdf[cluster].unique().tolist()
        group_ints = regdf[cluster].apply(lambda x: groups.index(x))
        return model.fit(cov_type='cluster', cov_kwds={'groups': group_ints})

    return model.fit()

def _get_reg_df_y_x(df, yvar, xvars, cluster, cons, fe, interaction_tuples):
    all_xvars = _collect_all_variables_from_xvars_and_interaction_tuples(xvars, interaction_tuples)
    regdf = _drop_missings_df(df, yvar, all_xvars, cluster, fe)
    y, X, dummy_cols_dict = _y_X_from_df(regdf, yvar, xvars, cons, fe, interaction_tuples)

    return regdf, y, X, dummy_cols_dict

def _drop_missings_df(df, yvar, xvars, cluster, fe):
    drop_set = [yvar] + xvars
    if cluster:
        drop_set += [cluster]
    if fe is not None:
        drop_set += fe

    return df.dropna(subset=drop_set)

def _y_X_from_df(regdf, yvar, xvars, cons, fe, interaction_tuples):

    if fe is not None:
        regdf, dummy_cols_dict = fixed_effects_reg_df_and_cols_dict(regdf, fe)
        model_xvars = xvars + extract_all_dummy_cols_from_dummy_cols_dict(dummy_cols_dict)
    else:
        dummy_cols_dict = None
        model_xvars = xvars.copy()

    if interaction_tuples:
        interaction_vars = create_interaction_variables(regdf, interaction_tuples)
        model_xvars += interaction_vars

    y = regdf[yvar]
    X = regdf.loc[:, model_xvars]

    if cons:
        X = sm.add_constant(X)

    return y, X, dummy_cols_dict

def _set_fe(fe):
    if fe is None:
        return None
    else:
        return _to_list_if_str(fe)

def _set_interaction_tuples(interaction_tuples):
    if interaction_tuples is None:
        return []
    else:
        return _to_list_if_tuple(interaction_tuples)

def _collect_all_variables_from_xvars_and_interaction_tuples(xvars, interaction_tuples):
    interaction_vars = _collect_variables_from_interaction_tuples(interaction_tuples)
    return list(set(xvars + interaction_vars))