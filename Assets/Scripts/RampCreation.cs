using System.Collections;
using System.Collections.Generic;
using System.IO;
using System;
using UnityEngine;
using System.Text.RegularExpressions;
//using System.Drawing;
using System.Linq;
public class RampCreation : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        // calling function
        RampRendering();
    }
    void RampRendering()
    { // reading file from location
        //StreamReader streamReader = new StreamReader("C:\\Users\\Yinzi\\Desktop\\NewVR\\Data\\pedestrian_ramp.csv");
        StreamReader streamReader = new StreamReader("C:\\Users\\Yinzi\\Desktop\\NewVR\\Data\\Group02_ramp.csv");
        string headerLine = streamReader.ReadLine();
        string data_String;
        while((data_String = streamReader.ReadLine()) != null)
        {
            Regex CSVParser = new Regex(",(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))");
            string[] data_values = CSVParser.Split(data_String);
            for(int i=0; i < data_values.Length; i++){
                if (i==31){
                   //Debug.Log(data_values[i]);
                   Dictionary<string, string> _replacements = new Dictionary<string, string>();
                   _replacements["MULTIPOINT"] = "";
                   _replacements["("] = "";
                   _replacements[")"] = "";
                   string s = data_values[i].Replace("MULTIPOINT", _replacements["MULTIPOINT"]);
                   string s1 = s.Replace("(", _replacements["("]);
                   string s2 = s1.Replace(")", _replacements[")"]);
                   string s3 = s2.Remove(0,1);
                   string s4 = s3.Remove(s3.Length-1);
                   var rawPoints = s4.Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries).ToList();
                   foreach (var rawPoint in rawPoints){
                    var splitPoint = rawPoint.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                    double pointX = Double.Parse(splitPoint[0]);
                    double pointX02 = (pointX + 73.9778011419138)*100000;
                    double pointY = Double.Parse(splitPoint[1]);
                    double pointY02 = (pointY - 40.7622181496387)*100000;
                    float coord_x1 = (float) pointX02;
                    float coord_y1 = (float) pointY02;
                    //float coord_x1 = (float) pointX;
                    //float coord_y1 = (float) pointY;
                    //Vector2 center_point = new Vector2 (-739700.0f, 407600.0f);
                    //float X_longitude = coord_x1*10000 - center_point.x;
                    //float Y_latitude = coord_y1*10000 - center_point.y;
                    float X_longitude = coord_x1;
                    float Y_latitude = coord_y1;
                    GameObject ramp = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                    ramp.transform.position = new Vector3(X_longitude, 1.5f, Y_latitude);
                    var sphereRenderer = ramp.GetComponent<Renderer>();
                    sphereRenderer.material.SetColor("_Color", Color.red);
                    ramp.tag = "Ramp";
                    Rigidbody ramprbdy = ramp.AddComponent<Rigidbody>();
                    ramprbdy.isKinematic = true;
                   }
                }
            }
        }
    }
}
