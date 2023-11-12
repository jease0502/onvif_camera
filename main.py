import cv2
import datetime
import os

class Camera(object):
    def __init__(self, ip, save_dir = 'videos',record_duration = 10 * 60):
        self.ip = ip
        self.save_dir = save_dir
        self.record_duration = record_duration
        
    def record(self):
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        # Set the directory where the videos will be saved
        os.makedirs(self.save_dir, exist_ok=True)

        # Open the camera device
        cap = cv2.VideoCapture(self.ip)  # Change the device index if needed

        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open video stream.")
            exit()

        # Get the width and height of the frame
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        # Start the loop to capture and save video
        while True:
            # Create a new video file with the current timestamp
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.avi'
            filepath = os.path.join(self.save_dir, filename)
            out = cv2.VideoWriter(filepath, fourcc, 20.0, (frame_width, frame_height))

            # Record the video for 'record_duration' seconds
            start_time = datetime.datetime.now()
            while (datetime.datetime.now() - start_time).seconds < self.record_duration:
                ret, frame = cap.read()  # Capture frame-by-frame
                if not ret:
                    print("Error: Failed to read frame from camera stream.")
                    break

                # Write the frame into the file 'out'
                out.write(frame)
                show_frame = cv2.resize(frame, (960, 540))
                # Display the resulting frame
                cv2.imshow('realtime image', show_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the current video writer object
            out.release()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

        


if __name__ == '__main__':
    camera = Camera("rtsp://admin:123456@192.168.1.105:554/profile1" , "videos" , record_duration=10*60)
    camera.record()