#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <stdlib.h>
#include <stdio.h>

static const std::string OPENCV_WINDOW = "Image window";

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  
public:
  ImageConverter()
    : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    image_sub_ = it_.subscribe("/kinect2/sd/image_depth", 1, 
      &ImageConverter::imageCb, this);
    image_pub_ = it_.advertise("/image_converter/output_video", 1);

    cv::namedWindow(OPENCV_WINDOW, CV_WINDOW_NORMAL);
    cv::resizeWindow(OPENCV_WINDOW, 1000, 500);
  }

  ~ImageConverter()
  {
    cv::destroyWindow(OPENCV_WINDOW);
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }
    
    int scale = 1;
    int delta = 0;
    int ddepth = CV_16S;
    
    // Blur the frame using a Gaussian filter
    //cv::GaussianBlur( cv_ptr->image, cv_ptr->image, cv::Size(3,3), 0, 0, cv::BORDER_DEFAULT );
    
    // Generate grad_x and grad_y
    cv::Mat grad_x, grad_y;
    cv::Mat abs_grad_x, abs_grad_y;
    
    // Gradient X
    cv::Sobel( cv_ptr->image, grad_x, ddepth, 1, 0, 3, scale, delta, cv::BORDER_DEFAULT );
    cv::convertScaleAbs( grad_x, abs_grad_x );
    
    // Gradient Y
    cv::Sobel( cv_ptr->image, grad_y, ddepth, 0, 1, 3, scale, delta, cv::BORDER_DEFAULT );
    cv::convertScaleAbs( grad_y, abs_grad_y );
    
    // Total Gradient (approximate)
    cv::Mat grad;
    addWeighted( abs_grad_x, 0.5, abs_grad_y, 0.5, 0, grad );
    
    // Convert gradient image into RGB form
    cv::cvtColor( grad, grad, CV_GRAY2RGB );
    
    // Coordinates of closest flat surface
    int i_c = 280;
    int j_c = 260;
    int val_c = 9999999;
    
    // Bound flat surface with red rectangle
    cv::Scalar m;
    for( int i = 50; i < 350; i=i+20)
    {
        for( int j = 140; j < 220; j=j+20)
        {
            m = cv::mean(grad(cv::Rect(i,j,20,20)));
            if( m[0] < 10 && cv_ptr->image.at<int>(i,j) < 45000000 )
            {
                printf("x: %d, y: %d, depth: %d\n", i, j, cv_ptr->image.at<int>(i,j));
                cv::rectangle(grad, cv::Point(i_c,j_c), cv::Point(i_c+20,j_c+20), CV_RGB(0, 255, 0), 1, 8);
                if( m[0] < val_c )
                {
                    //printf("depth: %d\n", cv_ptr->image.at<int>(i,j));
                    i_c = i;
                    j_c = j;
                    val_c = m[0];
                }
            }
        }
    }
    for( int i = 255; i < 355; i=i+20)
    {
        for( int j = 220; j < 280; j=j+20)
        {
            m = cv::mean(grad(cv::Rect(i,j,20,20)));
            if( m[0] < 10 && cv_ptr->image.at<int>(i,j) < 45000000 )
            {
                printf("x: %d, y: %d, depth: %d\n", i, j, cv_ptr->image.at<int>(i,j));
                cv::rectangle(grad, cv::Point(i_c,j_c), cv::Point(i_c+20,j_c+20), CV_RGB(0, 255, 0), 1, 8);
                if( m[0] < val_c )
                {
                    //printf("depth: %d\n", cv_ptr->image.at<int>(i,j));
                    i_c = i;
                    j_c = j;
                    val_c = m[0];
                }
            }
        }
    }
    printf("x: %d, y: %d, depth: %d\n", i_c, j_c, cv_ptr->image.at<int>(i_c, j_c));
    printf("--------------------------------------------\n");
    if( val_c != 999999999 )
    {
        cv::rectangle(grad, cv::Point(i_c,j_c), cv::Point(i_c+20,j_c+20), CV_RGB(255, 0, 0), 1, 8);
    }
    //printf("x: %d, y: %d\n", i_c, j_c);
    //cv::rectangle(grad, cv::Point(50,100), cv::Point(52,102), CV_RGB(255, 0, 0), 1, 8);
    //cv::rectangle(grad, cv::Point(400,340), cv::Point(402,342), CV_RGB(255, 0, 0), 1, 8);
    //cv::rectangle(grad, cv::Point(50,340), cv::Point(52,342), CV_RGB(255, 0, 0), 1, 8);
    //cv::rectangle(grad, cv::Point(400,100), cv::Point(402,102), CV_RGB(255, 0, 0), 1, 8);
    //cv::rectangle(grad, cv::Point(260,220), cv::Point(262,222), CV_RGB(255, 0, 0), 1, 8);
    //cv::rectangle(grad, cv::Point(150,100), cv::Point(102,102), CV_RGB(255, 0, 0), 1, 8);
    // Update GUI Window
    cv::imshow(OPENCV_WINDOW, grad);
    cv::waitKey(3);
    
    // Output modified video stream
    image_pub_.publish(cv_ptr->toImageMsg());
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "image_converter");
  ImageConverter ic;
  ros::spin();
  return 0;
}
