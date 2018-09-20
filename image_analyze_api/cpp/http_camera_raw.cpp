#include <curlpp/cURLpp.hpp>
#include <curlpp/Easy.hpp>
#include <curlpp/Options.hpp>
#include <curlpp/Exception.hpp>
#include <cv.h>
#include <highgui.h>

using namespace cv;

int main(int, char**)
{
    VideoCapture cap(0); // open the default camera

    if (!cap.isOpened()) // check if we succeeded
        return -1;

    for (;;) {

        Mat frame;
        cap >> frame; // get a new frame from camera

        string url = "http://127.0.0.1:8000";

        // add method to url
        url += "/analyze_raw_image";
        // add image shape to url
        url += "?width=" + std::to_string(frame.cols) + "&height=" + std::to_string(frame.rows);

        int size = frame.total() * 3;

        // create stream
        std::istringstream is;

        is.rdbuf()->pubsetbuf(reinterpret_cast<char*>(&frame.data[0]), size);

        try {
            curlpp::Cleanup cleaner;
            curlpp::Easy request;

            std::stringstream result;

            using namespace curlpp::Options;
            request.setOpt(new ReadStream(&is));
            request.setOpt(new InfileSize(size));
            request.setOpt(new Upload(true));
            request.setOpt(new Url(url));
            request.setOpt(new TcpNoDelay(1));
            // response in string
            request.setOpt(cURLpp::Options::WriteStream(&result));
            request.perform();
        }
        catch (curlpp::LogicError& e) {
            std::cout << e.what() << std::endl;
        }
        catch (curlpp::RuntimeError& e) {
            std::cout << e.what() << std::endl;
        }
    }
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}
