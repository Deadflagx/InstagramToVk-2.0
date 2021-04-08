# -*- coding: utf-8 -*-
from InstagramAPI import InstagramAPI
import requests
from vk_api import VkUpload,vk_api

from io import BytesIO
import io
import traceback
from datetime import datetime, timedelta
import time
import re
from random import randint as rnd

from settings import group_id, topic_id, token, inst_login, inst_password

from vkboard import CompareUsers


#VK AUTH
vk = vk_api.VkApi(token=token) 
vk._auth_token()
vk = vk.get_api()
upload = VkUpload(vk)
session = requests.Session()

#INST AUTH
api = InstagramAPI(inst_login, inst_password) #13091091211
api.login()  
time.sleep(5)


def GenerateModel():
	InstagramAPI.DEVICE_SETTINTS['model'] = rnd(10,1000)

def GetFollowingUsers():
	try:
		api.getTotalSelfFollowings()
		get = api.LastJson
		users = get['users']
		time.sleep(5)
		return users
	except (Exception) as e:
		print("GetFollowingUsers\n",traceback.format_exc())

def GetCaption(caption):
	if caption == None:
		return '',''
	else:
		text = caption['text']
		regexp = r'[#][а-яА-Яa-zA-Z0-9_]+'
		regtext = re.findall(regexp,text)
		hashtags = ' '.join(regtext)
		return text, hashtags

def MediaChecker(items, username, text, alllist):
	if items['pk'] not in pks:
		"""
		if 'carousel_media' in GetFeed['items'][y]:
			for x in GetFeed['items'][y]['carousel_media']:
				media_type = x['media_type']
				if media_type == 1:
					link_photo = x['image_versions2']['candidates'][0]['url']
					alllist += photo(link_photo,'Photo was taken from Instagram : ' + username + '\n\n' + text)+','
				if media_type == 2:
					link_video = x['video_versions'][0]['url']
					alllist += video(link_video,'Video was taken from Instagram : ' + username + '\n\n' + text,'vk.com/shibasandakitas    ' + username)+','
		"""
		if 'video_versions' in items:
			link_video = items['video_versions'][0]['url']
			attach_id =UploadVideo(link_video,'Video was taken from Instagram : ' + username + '\n\n' + text,'vk.com/shibasandakitas    ' + username)
		elif 'video_versions' not in items:
			link_photo = items['image_versions2']['candidates'][0]['url']
			attach_id =UploadPhoto(link_photo,'Photo was taken from Instagram : ' + username + '\n\n' + text)
		return attach_id

def wallpost(alllist, username, linkonpost, hashtags):
	try:
		post_id = vk.wall.post(owner_id=-+group_id, from_group=True, attachment=alllist, message='Instagram : ' + username + '\nLink on post : ' + linkonpost + '\n\n' + hashtags)
		#pks.append(pk)
		print("POST IS SUCCESSFUL", post_id['post_id'],'\n\n')
	except:
		print('VK.WALLPOST EXCEPTION', traceback.format_exc())


def UploadPhoto(image_url, caption):
	try:
		response = requests.get(image_url)
		content = BytesIO(response.content)
		photo_list = upload.photo_wall(photos=content,group_id=group_id,caption=caption)
		attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
		print('Photo already uploaded', attachment)
		return attachment
	except:
		print('UPLOAD PHOTO EXCEPTION\n',image_url , traceback.format_exc())
		return 0

def UploadVideo(video_url, description, name):
	try:
		response = requests.get(video_url)
		video_data = BytesIO(response.content)
		video_list = upload.video(name=name, video_file=video_data, group_id=group_id, description=description)
		video_id = "video"+str(video_list['owner_id'])+"_"+str(video_list['video_id'])
		print('Video already uploaded', video_id)
		return video_id
	except:
		print('UPLOAD VIDEO EXCEPTION\n', video_url, traceback.format_exc())
		return 0


pks = []
alllist = ''



while True:
	FollowingUsers = GetFollowingUsers()
	CompareUsers(vk, group_id, topic_id, FollowingUsers)
	for EachUser in FollowingUsers:
		api.getUserFeed(EachUser['pk'],minTimestamp=int(datetime.timestamp(datetime.now() - timedelta(minutes=140))))
		GetFeed = api.LastJson
		time.sleep(10)
		UserName = 'instagram.com/'+EachUser['username']
		if GetFeed['items'] != []:
			for items in GetFeed['items']:
				InstCaption, hashtags = GetCaption(items['caption'])
				linkonpost = 'instagram.com/p/' + items['code']
				alllist = MediaChecker(items, UserName, InstCaption , alllist)
				if alllist != 0:
					wallpost(alllist, UserName, linkonpost, hashtags)
					pks.append(items['pk'])
				alllist = ''
		time.sleep(5)
	time.sleep(7800)














