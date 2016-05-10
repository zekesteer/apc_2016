//#define TRAIN

#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <stdlib.h>
#include <stdio.h>
#include <ros/console.h>
#include <std_msgs/String.h>

using namespace cv;
using namespace std;

static const std::string OPENCV_WINDOW = "Image window";

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  ros::Publisher pos_pub_;
  cv::Mat median_;
  cv::Mat empty_;
  int i_;

public:
  ImageConverter(cv::Mat empty)
    : it_(nh_)
  {
    empty_ = empty;

    // Subscrive to input video feed and publish output video feed
    image_sub_ = it_.subscribe("/kinect2/sd/image_depth", 1, 
      &ImageConverter::imageCb, this);
    image_pub_ = it_.advertise("/image_converter/output_video", 1);

    pos_pub_ = nh_.advertise<std_msgs::String>("dep_obj_pub", 1000);

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
    cv::addWeighted( abs_grad_x, 0.5, abs_grad_y, 0.5, 0, grad );

    cv::Mat thresh;
    cv::threshold(grad, thresh, 25, 255, cv::THRESH_BINARY_INV);

    if (i_ == 0)
      median_ = cv::Mat::zeros(thresh.size(), CV_32FC1);            
    else
      cv::accumulateWeighted(thresh, median_,0.05);
    i_++;

    cv::Mat abs_median;
    cv::convertScaleAbs(median_, abs_median);

    Mat sub = abs_median.clone();

#if defined (TRAIN)
    if (i_ == 100)
      imwrite("empty.png", abs_median);
#else
    for (int y = 0; y < abs_median.rows; y++)
    {
      for (int x = 0; x < abs_median.cols; x++)
      {
        uchar m = abs_median.at<uchar>(y, x);
        uchar e = empty_.at<uchar>(y, x);

        sub.at<uchar>(y, x) = (uchar)(((m - e) / 2) + 128);
      }   
    }
#endif

    cv::Mat canny;
    cv::Canny(sub, canny, 200, 600, 3);

    // Convert gradient image into RGB form
    cv::Mat out;
    cv::cvtColor( grad, out, CV_GRAY2RGB );

    std::vector< std::vector<cv::Point> > cnts;
    std::vector<Vec4i> hierarchy;
    std::vector<cv::Point3i> centers;

    cv::findContours(canny, cnts, hierarchy, CV_RETR_CCOMP, cv::CHAIN_APPROX_SIMPLE, cv::Point(0, 0)); // RETR_EXTERNAL
    
    if (!cnts.empty() && !hierarchy.empty())
    {
      for (int i = 0; i < cnts.size(); i++)
      {
        cv::drawContours(out, cnts, i, cv::Scalar(255, 0, 0));
        cv::Rect r = cv::boundingRect(cnts[i]);
        int area = r.area();

        if ((area > 1000) && (area < 100000))
        {
          if (hierarchy[i][2] != -1)
          {
            int center_x = r.x + r.width/2;
            int center_y = r.y + r.height/2;
            cv::Point center = cv::Point(center_x, center_y);

            if ((center.x > sub.cols/4) && (center.x < sub.cols - sub.cols/4) && 
                (center.y > sub.rows/4) && (center.y < sub.rows - sub.rows/4))
            {
              centers.push_back(cv::Point3i(center_x, center_y, (cv_ptr->image).at<int>(center_y, center_x)));

              cv::rectangle(out, r.tl(), r.br(), cv::Scalar(0, 0, 255));
              cv::circle(out, center, 5, cv::Scalar(0, 255, 0));
            }   
          }
        }
      }
    }

    cv::rectangle(out, cv::Point(225, 255), cv::Point(229, 259), cv::Scalar(0, 255, 0));
    cv::rectangle(out, cv::Point(240, 215), cv::Point(244, 219), cv::Scalar(0, 255, 0));

    if (ros::ok())
    {
      std_msgs::String msg;
      std::stringstream ss;

      for (int i = 0; i < centers.size(); i++)
      {
        ss << centers[i].x << "," << centers[i].y << "," << centers[i].z << ";";
      }

      msg.data = ss.str();
      pos_pub_.publish(msg);
    }

    cv::imshow(OPENCV_WINDOW, out);

    cv::waitKey(3);
    
    // Output modified video stream
    image_pub_.publish(cv_ptr->toImageMsg());
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "image_converter");

#if defined (TRAIN)
  cv::Mat empty;
#else
  cv::Mat empty = imread("empty.png", CV_8U);

  if (!empty.data)
  {
    ROS_ERROR("No training data!");
    return -1;
  }
#endif
  ImageConverter ic(empty);

  ROS_INFO("image_converter running...");

  ros::spin();
  return 0;
}