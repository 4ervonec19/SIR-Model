# Mathematical epidemiology: Study notes


Couple of scientific notes were studied and here's presented some discussion.
The first one tells us about SIR system of ODE's solutions which represents the spreading of pandemic in time.
Using the SciPy and Runge-Kutta method we received the Infected Group population function of the time by solving Cauchy problem for normal distribution
of initial conditions. As a result: red line is probably expected & blue variants are stochastic.

![](Graph_1.png)

The second one reveals the Markov Chains Approach in Interaction of Networks:
Acturally, Pandemic and Aware, Fair of Pandemic respectively. Unfortunately, authors haven't shown the scrips of simulation and just tried to build up the plots by solving the problem I had established by myself. Here you may see both results

![](gr1.png)

![](gr2.png)

For sure, probability can't be greater than 1, but if we got some assumption, we might realize the similar trends of plotted lines.

# Update

Decision was modified by analyzing the article's text. New approach was considered, function markov_chain_approach was defined. Stochastic realization based on example from link: https://www.datacamp.com/tutorial/markov-chains-python-tutorial 
revealed to more effective results than shown above

![](Nice_plot_bro.png)

# Flatten result

![](nice_plot_flatten.png)


