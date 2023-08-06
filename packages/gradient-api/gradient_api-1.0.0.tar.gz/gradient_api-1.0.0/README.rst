**news_api**
==================

*Usage:*
--------


>>> from gradient_api import gradient

>>> r1 = gradient.generate(expr_or_poly1d='x**2+1')
>>> r2 = gradient.generate(expr_or_poly1d=[1,1])

>>> print(r1 == r2)
True

>>> print(r1)
{'X': -0.00011417981541647683, 'Y': 1.0000000130370303, 'Gradient': -0.00022835963083295366, 'Numloop': 51}


*Tips:*
-------

>>> generate(expr_or_poly1d,init_x=-10.0,step=0.1,num_iters=None,showPlot=True)

