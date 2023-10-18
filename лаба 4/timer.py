from main import *
import timeit


start = timeit.default_timer()
fill_ar_na()
print('Fill NaN in numpy array:', timeit.default_timer() - start)
start = timeit.default_timer()
fill_df_na()
print('Fill NaN in pandas dataframe:', timeit.default_timer() - start, end=f'\n{"="*50}\n')

start = timeit.default_timer()
normalize_ar()
print('Normalization in numpy array:', timeit.default_timer() - start)
start = timeit.default_timer()
normalize_df()
print('Normalization in pandas dataframe:', timeit.default_timer() - start, end=f'\n{"="*50}\n')

start = timeit.default_timer()
plotting_ar('community', (10, 100), (100, 200), (200, 300), (300, 400), (400, 500), (500, 600), (600, 700), (700, 800),
                         (800, 900), (900, 1000))
print('Plotting in numpy array:', timeit.default_timer() - start)
start = timeit.default_timer()
plotting_df('community', (10, 100), (100, 200), (200, 300), (300, 400), (400, 500), (500, 600), (600, 700), (700, 800),
                         (800, 900), (900, 1000))
print('Plotting in pandas dataframe:', timeit.default_timer() - start, end=f'\n{"="*50}\n')

start = timeit.default_timer()
cor_plot_ar('community', 'householdsize')
print('Plotting in numpy array:', timeit.default_timer() - start)
start = timeit.default_timer()
cor_plot_df('community', 'householdsize')
print('Plotting in pandas dataframe:', timeit.default_timer() - start, end=f'\n{"="*50}\n')

start = timeit.default_timer()
pearson_ar('community', 'householdsize')
print('Pearson coef. in numpy array:', timeit.default_timer() - start)
start = timeit.default_timer()
pearson_df('community', 'householdsize')
print('Pearson coef. in pandas dataframe:', timeit.default_timer() - start, end=f'\n{"="*50}\n')

start = timeit.default_timer()
one_hot_ar()
print('One hot in numpy array:', timeit.default_timer() - start)
start = timeit.default_timer()
one_hot_df()
print('One hot in pandas dataframe:', timeit.default_timer() - start, end=f'\n{"="*50}\n')

start = timeit.default_timer()
viz_3d_ar()
print('3D in numpy array:', timeit.default_timer() - start)
start = timeit.default_timer()
viz_3d_df()
print('3D in pandas dataframe:', timeit.default_timer() - start, end=f'\n{"="*50}\n')

start = timeit.default_timer()
np_reg()
print('Regression in numpy array:', timeit.default_timer() - start)
start = timeit.default_timer()
df_reg()
print('Regression in pandas dataframe:', timeit.default_timer() - start, end=f'\n{"="*50}\n')
