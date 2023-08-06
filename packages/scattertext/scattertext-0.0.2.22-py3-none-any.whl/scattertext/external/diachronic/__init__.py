import pandas as pd

from scattertext import RankDifference
from scattertext.termranking import AbsoluteFrequencyRanker


class GanttChart(object):
	def __init__(self,
	             corpus,
	             category_to_datetime_func,
	             is_gap_between_sequences_func,
	             timesteps_to_lag=4,
	             num_top_terms_each_timestep=10,
	             num_terms_to_include=40,
	             starting_time_step=None,
	             term_ranker=AbsoluteFrequencyRanker,
	             term_scorer=RankDifference):
		'''
		Parameters
		----------
		corpus
		category_to_datetime_func
		is_gap_between_sequences_func
		timesteps_to_lag
		num_top_terms_each_timestep
		num_terms_to_include
		term_ranker
		term_scorer
		'''
		self.corpus = corpus
		self.timesteps_to_lag = timesteps_to_lag
		self.num_top_terms_each_timestep = num_top_terms_each_timestep
		self.num_terms_to_include = num_terms_to_include
		self.is_gap_between_sequences_func = is_gap_between_sequences_func
		self.category_to_datetime_func = category_to_datetime_func
		self.term_ranker = term_ranker
		self.term_scorer = term_scorer
		categories = list(sorted(self.corpus.get_categories()))
		if len(categories) <= timesteps_to_lag:
			raise Exception("The number of categories in the term doc matrix is <= "
			                + str(timesteps_to_lag))
		if starting_time_step is None:
			starting_time_step = categories[timesteps_to_lag + 1]
		self.starting_time_step = starting_time_step

	def make_chart(self):
		task_df = self.get_task_df()
		import altair as alt
		chart = alt.Chart(task_df).mark_bar().encode(
			x='start',
			x2='end',
			y='term',
		)
		return chart

	def get_task_df(self):
		data = []
		for cat in sorted(self.corpus.get_categories()):
			if cat >= self.starting_time_step:
				scores = st.RankDifference().get_scores(
					tdf[sorted([x for x in tdf.columns if x < cat])[-timesteps_to_lag:]].sum(axis=1),
					tdf[cat].astype(int))
				for term in tdf.index[np.argsort(-scores)[:num_top_terms_each_timestep]]:
					data.append({'time': category_to_datetime(cat),
					             'term': term,
					             'top': 1})
		term_time_df = pd.DataFrame(data)
		terms_to_include = (term_time_df
		                    .groupby('term')
		                    ['top']
		                    .sum()
		                    .sort_values(ascending=False)
		                    .iloc[:num_terms_to_include].index)
		task_df = (term_time_df[term_time_df
			.term.isin(terms_to_include)][['time', 'term']]
			.groupby('term')
			.apply(lambda x: pd.Series(self._find_sequences(x['time'])))
			.reset_index()
			.rename({0: 'sequence'}, axis=1)
			.reset_index()
			.assign(start=lambda x: x['sequence'].apply(lambda x: x[0]))
			.assign(end=lambda x: x['sequence'].apply(lambda x: x[1]))
		[['term', 'start', 'end']])
		return task_df

	def _find_sequences(self, time_steps):
		min_timestep = None
		last_timestep = None
		gaps = []
		for cur_timestep in sorted(time_steps):
			if min_timestep is None:
				min_timestep = cur_timestep
			elif self.is_gap_between_sequences_func(cur_timestep, last_timestep):
				gaps.append([min_timestep, last_timestep])
				min_timestep = cur_timestep
			last_timestep = cur_timestep
			if gaps == [] or gaps[-1][1] != cur_timestep:
				gaps.append([min_timestep, cur_timestep])
		return gaps
