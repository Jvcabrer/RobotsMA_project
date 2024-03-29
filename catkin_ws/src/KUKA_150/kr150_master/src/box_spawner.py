#!/usr/bin/env python3

import rospy, tf, rospkg
from gazebo_msgs.srv import DeleteModel, SpawnModel, GetModelState
from geometry_msgs.msg import Quaternion, Pose, Point

class CubeSpawner():

	def __init__(self) -> None:
		self.rospack = rospkg.RosPack()
		#Ruta donde estan los urdf a exportar, los cubos
		self.path = self.rospack.get_path('kr150_gazebo')+"/urdf/"
		self.cubes = []
		self.cubes.append(self.path+"red_cube.urdf")
		self.cubes.append(self.path+"green_cube.urdf")
		self.cubes.append(self.path+"blue_cube.urdf")
		self.col = 0

		self.sm = rospy.ServiceProxy("/gazebo/spawn_urdf_model", SpawnModel)
		self.dm = rospy.ServiceProxy("/gazebo/delete_model", DeleteModel)
		self.ms = rospy.ServiceProxy("/gazebo/get_model_state", GetModelState)

	def checkModel(self):
		res = self.ms("cube", "world")
		return res.success

	def getPosition(self):
		res = self.ms("cube", "world")
		return res.pose.position.z

	def spawnModel(self):
		# print(self.col)
		cube = self.cubes[self.col]
		with open(cube,"r") as f:
			cube_urdf = f.read()
		
		quat = tf.transformations.quaternion_from_euler(0,0,0)
		orient = Quaternion(quat[0],quat[1],quat[2],quat[3])
		#Donde se va a aubicar el objeto caja
		# 0.75 
		pose = Pose(Point(x=0 ,y=-2,z=1), orient)
		self.sm("cube", cube_urdf, '', pose, 'world')
		if self.col<2:
			self.col += 1
		else:
			self.col = 0
		rospy.sleep(1)

	def deleteModel(self):
		self.dm("cube")
		rospy.sleep(1)

	def shutdown_hook(self):
		self.deleteModel()
		print("Shutting down")


if __name__ == "__main__":
	print("Waiting for gazebo services...")
	rospy.init_node("spawn_cubes")
	rospy.wait_for_service("/gazebo/delete_model")
	rospy.wait_for_service("/gazebo/spawn_urdf_model")
	rospy.wait_for_service("/gazebo/get_model_state")
	r = rospy.Rate(15)
	cs = CubeSpawner()
	#service = ServiceProxy("/conveyor/control", ConveyorBeltState)
	rospy.on_shutdown(cs.shutdown_hook)
	while not rospy.is_shutdown():
		if cs.checkModel()==False:
			cs.spawnModel()
			#response = rosservice.call("/conveyor/control", {"power": 20.0})
			#response = service(20.0)
			#rint(response)
		elif cs.getPosition()<0.05:
		#elif ciclo_completado:
			cs.deleteModel()
		r.sleep()
		