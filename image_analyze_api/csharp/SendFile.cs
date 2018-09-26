using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Imaging;

namespace PekatVisionExamples
{
    class SendFileExample
    {

        private static  byte[] ConvertBitmap(Bitmap bitmap)
        {
            //Code excerpted from Microsoft Robotics Studio v1.5
            BitmapData raw = null;  //used to get attributes of the image
            byte[] rawImage = null; //the image as a byte[]

            try
            {
                //Freeze the image in memory
                raw = bitmap.LockBits(
                    new Rectangle(0, 0, (int)bitmap.Width, (int)bitmap.Height),
                    ImageLockMode.ReadOnly,
                    PixelFormat.Format24bppRgb
                );

                int size = raw.Height * raw.Stride;
                rawImage = new byte[size];

                //Copy the image into the byte[]
                System.Runtime.InteropServices.Marshal.Copy(raw.Scan0, rawImage, 0, size);
            }
            finally
            {
                if (raw != null)
                {
                    //Unfreeze the memory for the image
                    bitmap.UnlockBits(raw);
                }
            }
            return rawImage;
        }


        static async Task Run()
        {
            HttpClient client = new HttpClient();
            // load image
            Bitmap img = (Bitmap)Bitmap.FromFile(@"cat.jpg");

            // convert image to byte array
            byte[] data = ConvertBitmap(img);

            //send frame to PEKAT VISION
            String url = "http://127.0.0.1:8000/analyze_raw_image?";
            url += "width=" + img.Width;
            url += "&height=" + img.Height;

            ByteArrayContent content = new ByteArrayContent(data);
            var response = await client.PostAsync(url, content);
        }

        static void Main()
        {
            Run().Wait();
        }

    }
}
