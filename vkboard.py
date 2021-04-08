from vk_api import VkUpload,vk_api


def GetBoardUsers(vk, group_id, topic_id):
	try:
		boardtext = vk.board.getComments(group_id=group_id,topic_id=topic_id,count=1)
		boardtext = boardtext['items'][0]['text']
		return '\n'.join(list(boardtext.split(' ')[1] for boardtext in boardtext.splitlines()))
	except:
		return 0

def GetInstaUsers(following_users):
	sortedusers = sorted(list('instagram.com/{}'.format(following_users['username']) for following_users in following_users))
	enumeratedusers = ''
	for num, user in enumerate(sortedusers):
		enumeratedusers += '[{}] {}\n'.format(num+1, user)
	return '\n'.join(sortedusers), enumeratedusers

def CompareUsers(vk, group_id, topic_id, following_users):
	boardusers = GetBoardUsers(vk, group_id, topic_id)
	instausers, enumeratedusers = GetInstaUsers(following_users)	
	if boardusers == 0:
		return
	if boardusers != instausers:
		vk.board.editComment(group_id=group_id, topic_id=topic_id, comment_id=2, message=enumeratedusers)
		print('VK.BOARD HAS CHANGED')

