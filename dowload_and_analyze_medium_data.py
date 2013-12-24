#!/usr/bin/env python
# encoding: utf-8
"""
download_and_analyze_medium_data.py

Created by James H. Faghmous (jfagh@cs.umn.edu) on 2013-12-11.

"""

import requests
import re
import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np
from pylab import *
import json
import logging
from mpl_toolkits.axes_grid1 import make_axes_locatable

logging.basicConfig(level=logging.DEBUG) #this is still in dev so I have debugging on

def plot_stats(postData, followerData, activityData):
	#plot the post statistics and the log of the post statistics since the distribution is skewed
	post_array_data = np.array(postData)
	post_log_data = np.log(post_array_data+1)
	plt.figure(1)
	plt.subplot(2,1,1)
	plt.xlabel('# Posts per collection')
	plt.ylabel('# of collections')
	plt.title("Distribution of number of posts in a Medium collection")
	n_posts, bins_posts, patches_posts = plt.hist(post_array_data, bins=[0,10,50,100,250,500,1000,2000,3000,4000,5000]) #these are uneven bins because data is skewe. If you prefer you can just call hist(x)
	plt.subplot(2,1,2)
	n_log_posts, bins_log_posts, patches_log_posts = plt.hist(post_log_data)
	plt.xlabel('Log(# Posts per collection)')
	plt.ylabel('# of collections')
	plt.title("Log distribution of number of posts in a Medium collection")
	# plot the follower data
	follower_array_data = np.array(followerData)
	follower_log_data = np.log(follower_array_data+1) # add 1 bc log(0) is undefined
	plt.figure(2)
	plt.subplot(2,1,1)
	n_log_followers, bins_log_followers, patches_log_followers = plt.hist(follower_log_data)
	plt.xlabel('Log(# Followers per collection)')
	plt.ylabel('# of collections')
	plt.title("Log distribution of number of followers in a Medium collection")
	plt.subplot(2,1,2)
	plt.xlabel('# Followers per collection')
	plt.ylabel('# of collections')
	plt.title("Distribution of number of followers in a Medium collection")
	n_followers, bins_followers, patches_followers = plt.hist(follower_array_data,bins=[0,1,2,3,4,5,6,7,8,9,10,50,100,1000,10000,50000,100000,250000,500000]) #these are uneven bins because data is skewed. If you prefer you can just call hist(x)
	plt.show()
	# plot the activity data
	activity_array_data = np.array(activityData)
	activity_log_data = np.log(activity_array_data)
	plt.figure(3)
	plt.subplot(2,1,1)
	n_log_activity, bins_log_activity, patches_log_activity = plt.hist(activity_log_data)
	plt.xlabel('Log(last activity in minutes per collection)')
	plt.ylabel('# of collections')
	plt.title("Distribution of the Log of duration in minutes since the last update of a Medium collection")
	plt.subplot(2,1,2)
	plt.xlabel('Minutes since last update per collection')
	plt.ylabel('# of collections')
	plt.title("Distribution of the duration in minutes since the last update of a Medium collection")
	n_activity, bins_activity, patches_activity = plt.hist(activity_array_data, bins=[0,60,360,1440,10080,20160,43200,129600,259200,500000,900000]) #keep in mind these are minutes
	plt.show()
	
	#scatter plots for followers and activity. The size of each data point is the number of posts in that collection
	fig, ax = plt.subplots()
	x = log(post_array_data+1)**2 #raise it to the power of 2 becasue the size of the points is too subtle
	y = log(follower_array_data+1)
	z = log(activity_array_data)
	ax.scatter(y,z,s=x)
	ax.grid(True)
	fig.tight_layout()
	plt.show()
	fig2, ax2 = plt.subplots()
	x = post_array_data
	y = follower_array_data
	z = activity_array_data
	ax2.scatter(y,z)
	plt.xlabel('# followers')
	plt.ylabel('Minutes since last update')
	plt.title('#Followers Vs. Minutes since last update for Medium collections -- size of the bubles is the number of posts per collection')
	ax2.grid(True)
	plt.show()

def make_scatter_w_hists(followerData,postData):
	#make a scatter plot of follower vs. post data and display the histograms of each
	x = log(np.array(followerData)+1)
	y = log(np.array(postData)+1)
	fig, axScatter = plt.subplots(figsize=(10,10))
	# the scatter plot:
	axScatter.scatter(x, y)
	axScatter.set_aspect(1.)
	plt.xlabel("Log(# followers)")
	plt.ylabel("Log(# posts)")
	figure_title = "Log of # followers Vs. # posts and associated histograms of each dataset"
	plt.text(-1,-3.08,figure_title) #position the ttile manually because of this unusal figure
	# create new axes on the right and on the top of the current axes
	# The first argument of the new_vertical(new_horizontal) method is
	# the height (width) of the axes to be created in inches.
	divider = make_axes_locatable(axScatter)
	axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=axScatter)
	axHisty = divider.append_axes("right", 1.2, pad=0.15, sharey=axScatter)
	# make some labels invisible
	plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),
	         visible=False)
	# now determine nice limits by hand:
	binwidth = 0.25
	xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
	lim = ( int(xymax/binwidth) + 1) * binwidth
	axHistx.hist(x) #you could also set the bins by hand
	axHisty.hist(y,orientation='horizontal')
	# the xaxis of axHistx and yaxis of axHisty are shared with axScatter,
	# thus there is no need to manually adjust the xlim and ylim of these
	# axis.
	for tl in axHistx.get_xticklabels():
	    tl.set_visible(False)
	axHistx.set_yticks([0, 250,500]) #manuallu set the height of the x/y axis for looks
	for tl in axHisty.get_yticklabels():
	    tl.set_visible(False)
	axHisty.set_xticks([0, 250, 500])
	plt.draw()
	plt.show()
	
#pase_collection_activity(activity_string):
# takes a string that has last activity information and returns an integer that contains the last activity in MINUTES
# these are rough estimates for instance I don't worry if a month has 28 or 31 days
def parse_collection_activity(activity_string):
	value = 365
	activity = activity_string.split()
	if "minute" in activity:
		value = 1
	elif "minutes" in activity:
		value = int(activity[0])
	elif "hour" in activity:
		value = 60
	elif "hours" in activity:
		value = int(activity[0]) * 60 #60 minutes in an hour
	elif "day" in activity:
		value = 60*24
	elif "days" in activity:
		value = int(activity[0]) * (60*24) #24*60 minutes in a day
	elif "month" in activity:
		value = 60*24*30 #24*60*30 minutes in a month
	elif "months" in activity:
		value = int(activity[0])* (60*24*30) 
	elif "year" in activity:
		value = 60*24*365
	elif "years" in activity:
		value = int(activity[0]) * (60*24*365) #60*24*365 minutes in a year
	else:
		value = 60*24*365 #this is if the activity is "null"
	return value
	
def get_collection_data(session):
	# go to medium.com/collection and seach for the following keywords and grab the data from collections associated thease keywords
	# TODO: change this list from a predfined list to a random sample of a text corpus
	# TODO: parse using Beautiful Soup instead of brute force parsing
	keywords={'machine learning','learning','data','science','dream','beats','beast','gentle','hope','president','late night','escort','rent','real','fake','real estate','property','laugh','short','affair','sequin','velvet','store','engagement','entourage','france','paris','eating','finance','politics','new york','tourism','travel','style','gadgets','twitter','linkedin','computers','cars','racing','reviews','books','literature','harry potter','video games','sports','basketball','fashion','e-commerce','analytics','republican','democrat','greek','english','french','activity','workout','driving','videos','online','women','men','mother','father','children','nobel','medecine','public health','epidemiology','cooking','recipes','stock','investing','banking','journalism','dating','sex','' 'buddha','twilight','entrepreneurship','star wars','art','philosophy','love','dating','finance','marriage','news','investing','islam','god','judaism','israel','ghandi','war','peace','happiness','snow','stories','fiction','novel','romance','drama','thriller','music','orchestra','sarcasm','experience','opinion','guide','design','ux','ui','user','beautiful','ugly','conversation','advertising','mandela','happy','movies','reviews','lean','religion','marketing','heros','medium','blog','math','algebra','psychology','facebook','writing','crying','soul','music','career','internet','romance','email','programming','coding','code','count','muppets','twist','minor','major','tank','luck','wish','spatial','temporal','mobile','geospatial','influence','convince','fundraising','funding','grants','vc','links','wonder','conquer','director','traffic','project','management','pc','apple','mac','linux','windows','private','public','conversation','direct','local','coffee','trade','fair','conversion','magic','kindness','style','advice','sale','shirt','garment','dress'}
	collection_stats = {}
	for k in keywords:
		logging.debug('Current keyword: '+k) #I have some logging in place since Medium doesn't have an API yet
		params={'q':k}
		try:
			r = session.get('https://medium.com/search/collections', params=params)
			logging.debug('Keyword status code: '+str(r.status_code))
		except Exception, ex:
			logging.exception("Something is wrong with the request!")
		user_list_index = r.text.find('"users"')# find where the user information from the Medium response starts and ignore it
		response = r.text[16:user_list_index-2] #clean up the response to only include collection infotmation
		collection_start_index = []
		collection_end_index = []
		for c in re.finditer('Collection',response):
			if response[c.start()-1:c.end()+1] == '"Collection"': #this is to make sure that we don't get fooled if the description includes the word 'collection' which we are not interested in
				collection_start_index.append(c.start()) #get the start and end of each collection group to further parse it
				collection_end_index.append(c.end())
		collection_start_index.append(len(response)) #append the the end of the list to avoid outofbounds
		for i in xrange(0,len(collection_start_index)-1):
			current_collection_info = response[collection_end_index[i]:collection_start_index[i+1]].encode('ascii','ignore')
			name_idx = current_collection_info.find('name') #find the index of the "name" tag
			slug_idx = current_collection_info.find('slug') #find the index of the "slug" tag
			current_collection_name = current_collection_info[name_idx+7:slug_idx-3]
			postCount_idx = current_collection_info.find('postCount') #find the index of the "postCount" tag
			followerCount_idx = current_collection_info.find('followerCount') #find the index of the "followerCount" tag
			current_collection_postCount = current_collection_info[postCount_idx+11:followerCount_idx-2]
			activeAt_idx = current_collection_info.find('activeAt') #find the index of the "activeAt" tag
			current_collection_followerCount = current_collection_info[followerCount_idx+15:activeAt_idx-2]
			activeAtRelative_idx = current_collection_info.find('activeAtRelative')
			end_of_active_idx =  current_collection_info.find('}',activeAtRelative_idx) 
			current_collection_activeAt = current_collection_info[activeAtRelative_idx+19:end_of_active_idx-1]
			logging.debug('Collection Name: '+current_collection_name+' , FollowerCount:'+current_collection_followerCount+', PostCount: '+current_collection_postCount+', Last active: '+current_collection_activeAt)
			current_collection_data={'postCount':int(current_collection_postCount),'followerCount':int(current_collection_followerCount),'lastActive':current_collection_activeAt}
			collection_stats[current_collection_name]=current_collection_data
	#save_collection_json(collection_stats,'json_file') #a helper function in case you want to save the results from a large corpus
	return collection_stats
	

### some helper functions to save and load collection data ###
def load_collection_stats_json(file_path):
	print 'Loading data from JSON file...'
	json_data=open(file_path)
	data = json.load(json_data)
	print 'Data loaded!'
	return data
def save_collection_json(collection_data,file_path):
	save_file = open(file_path, 'w')
	save_file.write( json.dumps(collection_data) )
	
#prints basic stats about a collection -- this readable for followers and posts. For activity you need to convert all activiy from minutes to your desired time-span (i.e. days)
def print_basic_collecton_statistics(collection_array, quantity):
	data_array = np.array(collection_array)
	data_mean = mean(data_array)
	data_std = std(data_array)
	data_median = median(data_array)
	q90 = percentile(data_array,90)
	#print stats and make some basic transformations for the 'minutes since last update' to make it human readable
	if quantity == 'followers' or quantity == 'posts':
		print '========================= '+ quantity.upper() + ' stats ' + '========================='
		print 'The mean number of ' + quantity.upper() + ' per collection is: ' + str(data_mean)
		print 'The standard deviaton of ' + quantity.upper() + ' per collection is: ' + str(data_std)
		print 'The median of ' + quantity.upper() + ' per collection is: ' + str(data_median) #the median is the number in a population that has as many numbers higher than it and lower than it
		print 'Ninty percent of collections have ' + str(q90) + ' or less ' + quantity.upper()
		print str((float(len(where(data_array ==0)[0]))/ len(data_array))  * 100.)+ ' percent of collections had 0 ' + quantity.upper()
		print str((float(len(where(data_array ==1)[0]))/ len(data_array))  * 100.)+ ' percent of collections had 1 ' + quantity.upper()
		print str((float(len(where(data_array <=100 )[0]))/ len(data_array))  * 100.)+ ' percent of collections had 100 or less ' + quantity.upper()
		print str((float(len(where(data_array >=1000 )[0]))/ len(data_array))  * 100.)+ ' percent of collections had 1000 or more ' + quantity.upper()
	else: #assuming the only othr quatity is minutes since last update
		print '========================= '+ quantity.upper() + ' stats ' + '========================='
		print 'The mean number of ' + quantity.upper() + ' per collection is: ' + str(data_mean) + ' or ' + str(data_mean/(60*24)) + ' days'
		print 'The standard deviaton of ' + quantity.upper() + ' per collection is: ' + str(data_std) + ' or ' + str(data_std/(60*24)) + ' days'
		print 'The median of ' + quantity.upper() + ' per collection is: ' + str(data_median) +' or ' + str(data_median/(60*24)) + ' days' #the median is the number in a population that has as many numbers higher than it and lower than it
		print 'Ninty percent of collections have ' + str(q90) + ' or less ' + quantity.upper()
		print str((float(len(where(data_array <=24*60)[0]))/ len(data_array))  * 100.)+ ' percent of collections have been updated in the last 24 hours ' 
		print str((float(len(where(data_array <=24*60*7)[0]))/ len(data_array))  * 100.)+ ' percent of collections have been updated in the last week '
		print str((float(len(where(data_array <=4*60*30)[0]))/ len(data_array))  * 100.)+ ' percent of collections have been updated a month ago'
		print str((float(len(where(data_array >=525600.0)[0]))/ len(data_array))  * 100.)+ ' percent of collections have been updated a year ago'
	
############## main ##################
def main():
	saved = 1 #set this 0 if you have no data saved
	if saved==0:
		s = requests.Session()
		s.headers.update({'accept': 'application/json'})
		collection_stats = get_collection_data(s)
	else:
		file_name="json_file" #set the path to your saved collection data
		collection_stats = load_collection_stats_json(file_name)
	#store each data in their own array
	postCount_data = []
	followerCount_data = []
	activity_data=[]
	names=[]
	for c in collection_stats.keys():
		names.append(c)
		current_dict = collection_stats[c]
		postCount_data.append(current_dict['postCount'])
		followerCount_data.append(current_dict['followerCount'])
		activity_data.append(parse_collection_activity(current_dict['lastActive']))
	
	#uncomment below to plot some basic stats
	#plot_stats(postCount_data,followerCount_data,activity_data)	
	#make_scatter_w_hists(followerCount_data,postCount_data)
	
	#uncomment below to print some basic stats about each collection metric
	#print_basic_collecton_statistics(followerCount_data, 'followers')
	#print_basic_collecton_statistics(postCount_data, 'posts')
	#print_basic_collecton_statistics(activity_data, 'minutes since last update')
	


if __name__ == '__main__':
	main()

