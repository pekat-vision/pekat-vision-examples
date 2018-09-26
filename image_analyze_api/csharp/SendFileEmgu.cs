using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Emgu.CV; // download this library with NuGet


namespace PekatVisionExamples
{
    class SendFileEmguExample
    {
        static async Task Run()
        {
            HttpClient client = new HttpClient();

            //capture frame from camera
            Mat frame = CvInvoke.Imread(@"cat.jpg");

            //send frame to PEKAT VISION
            String url = "http://127.0.0.1:8000/analyze_raw_image?";

            url += "width=" + frame.Width;
            url += "&height=" + frame.Height;

            ByteArrayContent content = new ByteArrayContent(frame.GetData());
            var response = await client.PostAsync(url, content);
    }

        static void Main()
        {
            Run().Wait();
        }
    }
}
