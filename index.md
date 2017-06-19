# TRiCAM_BostonAQ

## Team Air Quality Work Statement

**Team Members**: Anthony DePinho\*, Tara Ippolito\*, Biyonka Liang\*, Kaela Nelson\*, Annamira O’Toole\*

**Postdoc Advisor**: Weiwei Pan

**Sponsor**: Gary Adamkiewicz, Pavlos Protopapas

**Table of Contents:**

[I. Abstract](#Abstract)

[II. Intro](#Intro)

[III. Problem Statement and Methods](#Problem)

[IV. Deliverables](#Deliverables)

[V. Data Sources](#Data)

[VI. Computational Resources](#Computational)

[VII. Timeline](#Timeline)

[VIII. References](#References)

[IX. Code and Data](#Code)

<a name="Abstract"></a>
### I. Abstract
Air pollution is a significant concern for urban and suburban settings. The wide range of personal, industrial, and natural activities that take place in an urban space each contribute to the air pollution in their own way. Several key pollutants are released in varying concentrations and, though chemically and physically diverse, all pose significant health concerns for residents in urban centers. 

This project will be conducted through widespread collection of data, application of advanced statistical models, and computational mathematics techniques. Our end goal is to create an interface that will both enhance the quality of urban life in Boston and be accessible to all people, regardless of academic background.  The acquisition of data for this project will span various sources in the greater Boston area that pertain to air quality and its intersection with urban living, primarily transportation, land use, and weather, in addition to data on the air pollutants themselves. 

Our plan for our final deliverable is an accessible demonstration of the results of this rigorous modeling that can help city residents make more informed decisions on how to live a cleaner life, with a particular emphasis on aiding people potentially more vulnerable to air pollution, such as people with respiratory illnesses or allergies, pedestrians, and cyclists.
 
<a name="Intro"></a>
### II. Intro
Air pollution data, particularly in the city of Boston, is increasingly important to analyze in health and environmental settings. Our sponsors informed us that the pollutants Sulfur Dioxide (SO₂), Nitrogen Dioxide (NO₂), and Fine Particulate Matter (PM₂.₅ ) are the most detrimental to human health. Therefore, we have collected and will continue to collect data on these compounds. 

While pollutants have serious impacts on the environmen - for example, Sulfur Dioxide contributes to acid rain - we are focusing on the human health impacts. Sulfur Dioxide comes from multiple sources such as power plants and has been linked to cardiovascular and respiratory issues. Nitrogen Dioxide, whose source is primarily combustion, affects the respiratory systems and is also an indicator of other carcinogenic chemicals that are not widely measured. Fine Particulate Matter contributes to increased cortisone levels and hormone irregularities. In addition, Fine Particulate Matter, which comes upwind from the midwest and is produced by local combustion, is one of the most damaging pollutants as the small particle size allows the particles to enter the alveolar sacs of the lungs and enter the bloodstream directly [1]. The Environmental Protection Agency sets standard levels for each of these pollutants that are deemed acceptable for public health. We are using these standards as a baseline for our model.

There are currently only 5 sensors in Boston collecting data on air quality. Due to this limited amount of data, we would like to simulate more data from our collection data on air quality, which is a similar approach to the data simulation methods implemented in the Zurich study [2]. We also plan to utilize data on Boston transit routes, land use, traffic, green spaces, bike lanes, and weather in our model. 

In addition, we have been inspired by scientists who completed a study on air pollution and active travel to use optimization methods in order to create a routing system that we could implement in our web interface [3]. This ultimately would advise people a mode of transportation, i.e. biking, walking, public transport, given the levels of air pollutants measured in a particular day. 

<a name="Problem"></a>
### III. Problem Statement and Methods
One of our most obvious problems is Boston’s lack of air quality data. Boston only has five sensor stations, each of which collects different numbers and types of air pollutants. To develop an accurate model, we must infer and simulate based on other data sources. Our main goals are to mine more data on the concentration of NO₂, PM₂.₅ and SO₂ in Boston’s air throughout the course of a day, and to optimize the placement of a new sensor using statistical air quality models. 

For building our statistical models, we will gather, clean and merge other data on transportation, weather and land use patterns. Our intended sources of this data can be found in our Data Sources section. We expect that many of these data sources will not be easily accessible, as we already know some have rate limits, outdated or nonexistent APIs and strange formatting. 

Our goal for our final deliverable is to not only identify “danger spots” for those with health concerns such as asthma, COPD and allergies, but also offer optimized routes that minimizes pollution exposure. We expect that adapting existing air quality models and route algorithms to fit this goals will be a major challenge, given the specificity of our goal. We must also take into account common pitfalls like accuracy, model overfitting, and visualization of high dimensional spaces. 

<a name="Deliverables"></a>
### IV. Deliverables
The goal of our midterm deliverable consist of two parts. One is to implement a baseline statistical model of Boston’s air quality. The other is a proof of concept web interface for a live Boston pollution tracker. After week 6, we will work to implement a route planner for our web interface as well as improve upon our previous work. In our first week at Harvard, we have brainstormed several additional ambitious ideas. If time permits, we would like to use our air quality simulations in combination with optimization algorithms to provide urban planning tools for Boston policymakers. Ideally, the models we create would be compatible with and useful to other cities around the world.  

<a name="Data"></a>
### V. Data Sources
We will gather our data from various governmental and nongovernmental institutions. These may consist of but are not limited to:


- Air quality data from the Environmental Protection Agency (EPA)
- Boston area traffic data from the Google Maps API
- Topological data from Harvard’s Center for Geographical Analysis (CGA)
- Bike lane and road design data from massGIS, bostonGIS and/or arcGIS
- Boston area green space data on NASA’s normalized difference vegetation index (NDVI)
- Weather data from National Oceanic and Atmospheric Administration (NOAA) 
- MBTA public transit route data and schedules
If time permits, we will also gather:
- Twitter data to extrapolate allergy hotspots
- Data on population movement within Boston


<a name="Computational"></a>
### VI. Computational Resources

- We will conduct our data exploration and research with IPython 3 and Jupyter Notebook
- SciPy, scikit-learn for modeling, and Matplotlib for static visualization
- Land use regression, linear regression, optimization in Python
- D3, CSS and HTML for our web application’s interface we will use
- Amazon Web Services for cloud computing to store and process data
- GitHub for project collaboration, organization, and file backup

<a name="Timeline"></a>
### VII. Timeline
 
**Week 1:** 
- Learning the Basics,
- Building foundation in data science, statistical modeling, Python and time series analysis
- Meet with Gary to discuss details and general plan for project

 
**Week 2:** 
- Data collection: Gather preliminary data, in every aspect. In general order of priority: MBTA (Anthony), land use (Kaela), green space (Tara), traffic (Biyonka), GIS for bike lane data (Tara), weather data (Annamira). Wishlist: recollect air quality data, building height, population data, twitter data for allergen data, topography
- Workshop in D3 and advanced GIT
- Set up computing environments using Amazon AWS
- Workshop in statistical models: theoretically understanding the models we intend to use


 
**Week 3:** 
- Run some simple models, such as land use regression
- Design interface: PDF storyboard
- Meeting with Gary and adjust plan
 
**Week 4-6:** 
- Implementation of advanced models: additional reading if needed
- Report back to Gary a geographical cost analysis to suggest sensor placement
- Work on implementing design interface in D3.js. Basic functionalities like page layout, importing the base map visualization, air quality animations, etc.
- Prepare presentation for midterm deliverable
 
<a name="References"></a>
### VII. References
[1] Much of the information on the health impacts of the pollutants we are studying comes from Dr. Jaime Hart from the Harvard T.H. Chan School of Public Health.

[2] Hasenfratz, David, Olga Saukh, Christoph Walser, Christoph Hueglin, Martin Fierz, Tabita Arn, Jan Beutel, and Lothar Thiele. "Deriving High-resolution Urban Air Pollution Maps Using Mobile Sensor Nodes." Pervasive and Mobile Computing 16 (2015): 268-85. Web.

[3] Hankey, Steve, Greg Lindsey, and Julian D. Marshall. "Population-Level Exposure to Particulate Air Pollution during Active Travel: Planning for Low-Exposure, Health-Promoting Cities." Environmental Health Perspectives 125.4 (2016): n. pag. Web.
 
<a name="Code"></a>
### VIII. Code and Data
https://github.com/onefishy/TRiCAM_BostonAQ
