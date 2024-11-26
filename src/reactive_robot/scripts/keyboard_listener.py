#!/usr/bin/env python3

import rospy
from pynput import keyboard
from pynput.keyboard import Listener
from geometry_msgs.msg import Twist
import time

# Initialize a global message
msg = Twist()

def on_press(key):

    """
    Callback function when a key is pressed.
    Updates the Twist message based on the key.
    """

    global msg
    msg = Twist() # Reset message on each key press

    try:

        if key.char == 'w':
            msg.linear.x += 1  # Move forward
        if key.char == 's':
            msg.linear.x -= 1  # Move backvard
        if key.char == 'a':
            msg.angular.z += 1  # Move left
        if key.char == 'd':
            msg.angular.z -= 1 # Move right


        if msg.linear.x > 0:
            rospy.loginfo("Moving forward")
        elif msg.linear.x < 0:
            rospy.loginfo("Moving backward")

        if msg.angular.z > 0:
            rospy.loginfo("Rotating left")
        elif msg.angular.z < 0:
            rospy.loginfo("Rotating right")

    except Exception as e:
        
        rospy.logerr(e)
        rospy.loginfo(f"Key broken")

#
def on_release(key):

    """
    Callback function when a key is released.
    Resets the Twist message to stop movement.
    """

    global msg
    msg = Twist()  # Reset motion before stop

    # Exit the listener loop when ESC is pressed
    if key == keyboard.Key.esc:
        return False

if __name__ == '__main__':
    rospy.init_node('keyboard_listener', anonymous=True)

    # Publisher for /cmd_vel
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # 10 Hz publishing rate
    rate = rospy.Rate(10)

    # Define start time
    start_time = time.time()

    # Start the keyboard listener
    listener = Listener(on_press=on_press, on_release=on_release, suppress=False)
    listener.start()

    rospy.loginfo("Keyboard listener is running. Press ESC to quit.")

    try:

        while listener.running and not rospy.is_shutdown():
            # Calculate past time
            elapsed_time = time.time() - start_time
            
            # Stop node after 60 seconds
            if elapsed_time >= 60:
                rospy.loginfo("Time is up. Node stopping")
                msg = Twist() #Reset motion
                pub.publish(msg)

                break

            # Publish the current motion command
            pub.publish(msg) 
            
            # Sleep to maintain loop rate
            rate.sleep()
        
    except:
        rospy.loginfo("Ros interrupted. Node shutting down.")

    finally:
        listener.stop()
        rospy.loginfo("Keyboard listener stopped")

        #Node stopping
        rospy.signal_shutdown("Node shutting down due to timeout")