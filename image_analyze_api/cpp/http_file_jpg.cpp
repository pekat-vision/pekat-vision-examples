#include <sstream>

#include <cstdlib>
#include <cstdio>
#include <cstring>

#include <curlpp/cURLpp.hpp>
#include <curlpp/Easy.hpp>
#include <curlpp/Options.hpp>
#include <curlpp/Exception.hpp>

#include <cv.h>
#include <highgui.h>

enum class byte : std::uint8_t {};

using namespace std;

int main(int argc, char* argv[])
{
    string url = "http://127.0.0.1:8000";
    cv::Mat img2 = cv::imread("/path/image.jpg");

    // add method to url
    url += "/analyze_raw_image";
    // add image shape to url
    url += "?width=" + to_string(img2.cols) + "&height=" + to_string(img2.rows);

    int size = img2.total() * 3;

    // create stream
    std::istringstream is;
    is.rdbuf()->pubsetbuf(reinterpret_cast<char*>(&img2.data[0]), size);

    try {
        curlpp::Cleanup cleaner;
        curlpp::Easy request;

        using namespace curlpp::Options;
        request.setOpt(new Verbose(true));
        request.setOpt(new ReadStream(&is));
        request.setOpt(new InfileSize(size));
        request.setOpt(new Upload(true));
        request.setOpt(new Url(url));

        request.perform();
    }
    catch (curlpp::LogicError& e) {
        std::cout << e.what() << std::endl;
    }
    catch (curlpp::RuntimeError& e) {
        std::cout << e.what() << std::endl;
    }
    return 0;
}