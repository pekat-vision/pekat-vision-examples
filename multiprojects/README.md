#Inspection of multiple types of objects
In some manufacturing environments one assembly line can produce various types of products. It is then necessary to change inspection based on the product type.
This example shows an example GUI application which switches project based on text input - it is expected the text input comes from a barcode reader.
###Use-case scenario
Operator of the assembly line changes the inspection type by scanning barcode of the box of products which should be inspected. The scanned barcode comes into the input text field. The application switches the type of inspection - by switching project. In configuration file of this application is a project-map defining for which barcode (key) should be opened which project.

You have to set path to PEKAT VISION destination and paths to projects and their keys (string).
For example:
```
{
  "pekat_path": "C:\Program Files\PekatVision",
  "camera_settings": "C:\camera_config.pfs",
  "projects_map": [
    {
      "key": "barcode1",
      "path": "C:\Users\Peter\PekatVisionProjects\ProjectA"
    },
       {
      "key": "barcode2",
      "path": "C:\Users\Peter\PekatVisionProjects\ProjectB"
    },
  ],
  "port": 8100
}
```
The application runs in an infinite loop.
If the app receive `barcode1\n` to the text input, it starts the project on port `8100`.
If any project is already running, it will be stopped.

### Premise
* Basler camera include config file (.pfs)