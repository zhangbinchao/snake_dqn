# -------------------------
# Project: Deep Q-Learning on Snake
# Author: bc_zhang
# Date: 2019.7.4
# -------------------------

import cv2
import sys
sys.path.append("game/")
import GluttonousSnake as game
from BrainDQN_Nature import BrainDQN
import numpy as np


# preprocess raw image to 80*80 gray image
def preprocess(observation):
	observation = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)#灰度转化
	ret, observation = cv2.threshold(observation,127,255,cv2.THRESH_BINARY)
	# cv2.imwrite("3.jpg",observation,[int(cv2.IMWRITE_JPEG_QUALITY),5])#输出二值化的图片
	return np.reshape(observation,(80,80,1))

def playSnake():
	# Step 1: init BrainDQN
	actions = 4
	top = 0
	brain = BrainDQN(actions)
	# Step 2: init Plane Game
	GluttonousSnake = game.GameState()
	# Step 3: play game
	# Step 3.1: obtain init state
	action0 = np.array([0,0,0,1])  # [1,0,0]do nothing,[0,1,0]left,[0,0,1]right
	observation0, reward0, terminal,score = GluttonousSnake.frame_step(action0)

	observation0 = cv2.cvtColor(cv2.resize(observation0, (80, 80)), cv2.COLOR_BGR2GRAY)
	ret, observation0 = cv2.threshold(observation0,1,255,cv2.THRESH_BINARY)
	# cv2.imwrite("3.jpg",observation0,[int(cv2.IMWRITE_JPEG_QUALITY),5])

	brain.setInitState(observation0)

	# Step 3.2: run the game
	while 1!= 0:
		action = brain.getAction()
		nextObservation,reward,terminal,score = GluttonousSnake.frame_step(action)
		nextObservation = preprocess(nextObservation)
		brain.setPerception(nextObservation,action,reward,terminal)
		if score > top:
			top = score

		print('top:%u' % top)

def main():
	playSnake()

if __name__ == '__main__':
	main()