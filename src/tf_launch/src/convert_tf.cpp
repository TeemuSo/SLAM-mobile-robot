
#include <ros/ros.h>
#include <iostream>
#include <tf/transform_broadcaster.h>

int main(int argc, char** argv){
  ros::init(argc, argv, "robot_tf_publisher");
  ros::NodeHandle n;

  ros::Rate r(100);

  tf::TransformBroadcaster broadcaster;
  
  // Use user guided transform frames
  std::cout << "How many transforms? ";
  int amountOfTf;
  std::cin >> amountOfTf;

  std::string tfs[amountOfTf][2];

  int iterator = 0;
  while(iterator < amountOfTf){
    std::cout << "From: ";
    std::cin >> tfs[iterator][0]; std::cout << std::endl;

    std::cout << "To: ";
    std::cin >> tfs[iterator][1]; std::cout << std::endl;
    iterator++;
  }
  
  std::cout << "Transforms created!";
  while(n.ok()){
    try
    {
          
      iterator = 0;
      
      while(iterator < amountOfTf){
        broadcaster.sendTransform(
        tf::StampedTransform(
            // Change Quaternion(pitch,roll,yaw,magnitude) to match with angular difference
            // Change Vector3(x,y,z) coordinates accordingly with robot tf
          tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.0, 0.0, 0.0)),
          // Transform timestamp = now
          // Parent node camera_link, child node grid_map
          ros::Time::now(), tfs[iterator][0], tfs[iterator][1]));
      
        iterator++;
      }    
      r.sleep();
    }
    catch(const std::exception& e)
    {
      std::cerr << e.what() << '\n';
    }

  }
}