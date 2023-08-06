<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/hyopt.py#L78)</span>
### CMongoTrials

```python
concise.hyopt.CMongoTrials(db_name, exp_name, ip='ouga03', port=1234, kill_timeout=None)
```

`hyperopt.MonoTrials` extended with the following methods:

- get_trial(tid) - Retrieve trial by tid (Trial ID).
- get_param(tid) - Retrieve used hyper-parameters for a trial.
- best_trial_tid(rank=0) - Return the trial with lowest loss.
	- rank - rank=0 means the best model, rank=1 means second best, ...
- optimal_epochs(tid) - Number of optimal epochs (after early-stopping)
- delete_running(timeout_last_refresh=0, dry_run=False) - Delete jobs stalled in the running state for too long
	- timeout_last_refresh, int: number of seconds
	- dry_run, bool: If True, just simulate the removal but don't actually perform it.
- valid_tid() - List all valid tid's
- train_history(tid=None) - Get train history as pd.DataFrame with columns: `(epoch, loss, val_loss, ...)`
	- tid: Trial ID or list of trial ID's. If None, report for all trial ID's.
- get_ok_results - Return a list of trial results with an "ok" status
- load_model(tid) - Load a Keras model of a tid.
- as_df - Returns a tidy `pandas.DataFrame` of the trials database.

__Arguments__

- __db_name__: str, MongoTrials database name
- __exp_name__: strm, MongoTrials experiment name
- __ip__: str, MongoDB IP address.
- __port__: int, MongoDB port.
- __kill_timeout__: int, Maximum runtime of a job (in seconds) before it gets killed. None for infinite.
- __**kwargs__: Additional keyword arguments passed to the `hyperopt.MongoTrials` constructor.


----

<span style="float:right;">[[source]](https://github.com/avsecz/concise/blob/master/concise/hyopt.py#L405)</span>
### CompileFN

```python
concise.hyopt.CompileFN(db_name, exp_name, data_fn, model_fn, add_eval_metrics=[], optim_metric='loss', optim_metric_mode='min', valid_split=0.2, cv_n_folds=None, stratified=False, random_state=None, use_tensorboard=False, save_model='best', save_results=True, save_dir='/s/project/deepcis/hyperopt/')
```

Compile an objective function that

- trains the model on the training set
- evaluates the model on the validation set
- reports the performance metric on the validation set as the objective loss

__Arguments__

- __db_name__: Database name of the CMongoTrials.
- __exp_name__: Experiment name of the CMongoTrials.
- __data_fn__: Tuple containing training data as the x,y pair at the first (index=0) element:
	 `((train_x, test_y), ...)`. If `valid_split` and `cv_n_folds` are both `None`,
	 the second (index=1) tuple is used as the validation dataset.
- __add_eval_metrics__: Additional list of (global) evaluation
	metrics. Individual elements can be
	a string (referring to concise.eval_metrics)
	or a function taking two numpy arrays: `y_true`, `y_pred`.
	These metrics are ment to supplement those specified in
	`model.compile(.., metrics = .)`.
- __optim_metric__: str; Metric to optimize. Must be in
	`add_eval_metrics` or `model.metrics_names`.
- __optim_metric_mode__: one of {min, max}. In `min` mode,
	training will stop when the optimized metric
	monitored has stopped decreasing; in `max`
	mode it will stop when the optimized metric
	monitored has stopped increasing; in `auto`
	mode, the direction is automatically inferred
	from the name of the optimized metric.
- __valid_split__: Fraction of the training points to use for the validation. If set to None,
		 the second element returned by data_fn is used as the validation dataset.
- __cv_n_folds__: If not None, use cross-validation with `cv_n_folds`-folds instead of train, validation split.
		Overrides `valid_split` and `use_data_fn_valid`.
- __stratified__: boolean. If True, use stratified data splitting in train-validation split or cross-validation.
- __random_state__: Random seed for performing data-splits.
- __use_tensorboard__: If True, tensorboard callback is used. Each trial is written into a separate `log_dir`.
- __save_model__: It not None, the trained model is saved to the `save_dir` directory as hdf5 file.
		If save_model="best", save the best model using `keras.callbacks.ModelCheckpoint`, and
		if save_model="last", save the model after training it.
- __save_results__: If True, the return value is saved as .json to the `save_dir` directory.
- __save_dir__: Path to the save directory.


----

### test_fn


```python
test_fn(fn, hyper_params, n_train=1000, tmp_dir='/tmp/concise_hyopt_test/')
```


Test the correctness of the compiled objective function (CompileFN). I will also test
model saving/loading from disk.

__Arguments__

- __fn__: CompileFN instance
- __hyper_params__: pyll graph of hyper-parameters - as later provided to `hyperopt.fmin`
- __n_train__: int, number of training points
- __tmp_dir__: Temporary path where to write the trained model.


----

### eval_model


```python
eval_model(model, test, add_eval_metrics={})
```


Evaluate model's performance on the test-set.

__Arguments__

- __model__: Keras model
- __test__: test-dataset. Tuple of inputs `x` and target `y` - `(x, y)`.
- __add_eval_metrics__: Additional evaluation metrics to use. Can be a dictionary or a list of functions
accepting arguments: `y_true`, `y_predicted`. Alternatively, you can provide names of functions from
the `concise.eval_metrics` module.

__Returns__

dictionary with evaluation metrics

