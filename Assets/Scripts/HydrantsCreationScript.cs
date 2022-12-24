using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Text.RegularExpressions;
public class HydrantsCreationScript : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        // calling function
        HydrantsLocation();
    }
    void HydrantsLocation()
    {
        // reading file from location
       // StreamReader streamReader = new StreamReader("C:\\Users\\Yinzi\\Desktop\\NewVR\\Data\\hydrants.csv");
        StreamReader streamReader = new StreamReader("C:\\Users\\Yinzi\\Desktop\\NewVR\\Data\\Group02_hydrant.csv");
        string headerLine = streamReader.ReadLine();
        string data_String;
        while((data_String = streamReader.ReadLine()) != null)
        {
            Regex CSVParser = new Regex(",(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))");
            string[] data_values = CSVParser.Split(data_String);
            for(int i=0; i < data_values.Length; i++){
                if (i==3){  // /////// change to 2 when play on the other dataset //////////////////////
                   double latitude = double.Parse(data_values[i]);
                   double longitude = double.Parse(data_values[i+1]);
                   double longitude02 = (longitude + 73.9778011419138)*100000;
                   double latitude02 = (latitude - 40.7622181496387)*100000;
                   float X_longitude = (float) longitude02;
                   float Y_latitude = (float) latitude02;
                   GameObject hydrant = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                   hydrant.transform.position = new Vector3(X_longitude, 1.5f, Y_latitude);
                   var sphereRenderer = hydrant.GetComponent<Renderer>();
                   sphereRenderer.material.SetColor("_Color", Color.yellow);
                   hydrant.tag = "Hydrant";
                   Rigidbody hydrantrbdy = hydrant.AddComponent<Rigidbody>();
                   hydrantrbdy.isKinematic = true;
                }
            }
        }
    }
}
