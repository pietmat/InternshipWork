import datetime
import PySimpleGUI as sg
import cv2
import pyrealsense2 as rs
import numpy as np
# print("now =", today)
# dd/mm/YY H:M:S
def time():
	# today = datetime.today()
	# print ('Todays date: ', today)
	e = datetime.datetime.now()
	print("Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))
	# prints date in DD/MM/YYYY format
	print("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
	# prints current time in HH:MM:SS format
def ui():
	sg.theme('DarkRed1')

	# buttons
	employee = sg.Button('Employee', size=(15, 7), font=('Helvetica', 24), button_color=('black', 'green'))
	guest = sg.Button('Guest', size=(8, 4), font=('Helvetica', 14))
	cancel = sg.Button('Cancel', size=(8,4), font=('Helvetica', 14), button_color=('black', 'yellow') )
	welcone = sg.Text('Welcome Screen', font=('Helvetica', 18))
	# This button should be pressed for emergency reasons. For example - Logging in with PIN.
	emergency = sg.Button('Sign In with PIN', target=(-2, 1)) # not using this button anywhere, yet.
	lunchtime = sg.Button('12:30')
	l_notification = [[sg.Text('You are signed up for lunch now.')]]
	l_guest = [[sg.Text('Wait for an authorized employee!')]]
	lunch = [[sg.Text('Sign up for lunch')],
			 [sg.Text('Possible timeslots:')],
			 [lunchtime]]
	layout = [[welcone],
		# [sg.Text("now =", today)],
			 [employee],
			 [guest],
			 # [emergency],
			 [cancel]]
		# Create the Window
	#layout2 = [[sg.Text('recognizing face.....')],
			   # [sg.Button('Quit')]]

	# Main layout, which is supposed to be shown first, on top of camera feed
	window = sg.Window('Window Title', layout, element_justification='c',finalize=True)
	# Guest information to wait for an authorized employee
	g_window = sg.Window('Information', l_guest)
	# Pop up with possible timeslots for lunch
	lunch_window = sg.Window('Information', lunch, element_justification='c')
	l_notification = sg.Window('Success',l_notification, element_justification='c')
	# window2= sg.Window('Employee face recognition', layout2, element_justification='c', finalize=True)
	window.Maximize()
	# window2.Maximize()
	# Event Loop to process 
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
			break
		elif event == 'Employee':
			# here the output form the camera should show up.
			camdepth()		#it is a function declared below. Using a code from intel site just to read the camera with some small tweaks of mine.
			lunch_window()
			if event == sg.WIN_CLOSED:
				break
			if event == '12:30':	# This part does not work properly yet.
				l_notification()
				window.close()
				break
				# lunch_window()
				# if event == sg.WIN_CLOSED or event == 'Quit':
					# break
		elif event == 'Guest':
			g_window()
			if event == sg.WIN_CLOSED:
				break
	window.close()

def camdepth():
	###############################################
	##      Open CV and Numpy integration        ##
	###############################################
	# Configure depth and color streams
	pipeline = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

	# Start streaming
	pipeline.start(config)

	try:
		while True:

			# Wait for a coherent pair of frames: depth and color
			frames = pipeline.wait_for_frames()
			depth_frame = frames.get_depth_frame()
			color_frame = frames.get_color_frame()
			if not depth_frame or not color_frame:
				continue
			# Convert images to numpy arrays
			depth_image = np.asanyarray(depth_frame.get_data())
			color_image = np.asanyarray(color_frame.get_data())

			# Apply colormap on depth image (image must be converted to 8-bit per pixel first)
			depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

			# Stack both images horizontally
			images = np.hstack((color_image, depth_colormap))

			# Show images
			cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
			cv2.imshow('RealSense', images)
			key = cv2.waitKey(1)
			# Press esc or 'q' to close the image window
			if key & 0xFF == ord('q') or key == 27:
				cv2.destroyAllWindows()
				break
	finally:

		# Stop streaming
		pipeline.stop()

if __name__ == "__main__":
	time()
	ui()
