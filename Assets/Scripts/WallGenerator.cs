using System.Collections;
using System.Collections.Generic;
using System.IO;
using System;
using UnityEngine;
using System.Text.RegularExpressions;
using System.Drawing;
using System.Linq;
public class WallGenerator : MonoBehaviour
{  
    GameObject Wall;
    Vector2 P0;
    Vector2 P1;
    Vector2 P2;
    List<Vector2> vertices;
    int num_points;
    void Start()
    {
        Wall = GameObject.Find("Wall");     
        CreateArea();
    }
    void CreateArea()
    {       
        vertices = new List<Vector2>(); // initialize list
        vertices.Clear();
        List<string> PolygonList = new List<string>();
        List<double> PointXList = new List<double>();
        List<double> PointYList = new List<double>();
        //StreamReader streamReader = new StreamReader("C:\\Users\\Yinzi\\Desktop\\NewVR\\Data\\buildingFootprint_geometry.csv");
        StreamReader streamReader = new StreamReader("C:\\Users\\Yinzi\\Desktop\\NewVR\\Data\\Group02_building_footprint.csv");
        string headerLine = streamReader.ReadLine();
        string data_String;
        while((data_String = streamReader.ReadLine()) != null){
            Regex CSVParser = new Regex(",(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))");
            string[] data_values = CSVParser.Split(data_String);
            PolygonList.Add(data_values[16]);
        }
        for(int h=0; h<PolygonList.Count; h++){
            Dictionary<string, string> _replacements = new Dictionary<string, string>();
            _replacements["POLYGON"] = "";
            _replacements["MULTI"] = "";
            _replacements["(("] = "";
            _replacements["))"] = "";
            _replacements["((("] = "((";
            _replacements[")))"] = "))";
            string s = PolygonList[h].Replace("POLYGON", _replacements["POLYGON"]); 
            string s1 = s.Replace("MULTI", _replacements["MULTI"]);
            string s2 = s1.Replace("(((", _replacements["((("]);
            string s3 = s2.Replace(")))", _replacements[")))"]);
            string[] data_values2 = s3.Split("), (");
            for(int k=0; k < data_values2.Length; k++){
                string s4 = data_values2[k].Replace("))", _replacements["))"]);
                string s5 = s4.Replace("((", _replacements["(("]);    
                string s6 = s5.Remove(0,1);
                string s7 = s6.Remove(s6.Length-1);
                var rawPoints = s7.Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries).ToList();
                foreach (var rawPoint in rawPoints){
                    var splitPoint = rawPoint.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                    double pointX = Double.Parse(splitPoint[0]);
                    double pointX02 = (pointX + 73.9778011419138)*100000;
                    PointXList.Add(pointX);
                    double pointY = Double.Parse(splitPoint[1]);
                    double pointY02 = (pointY - 40.7622181496387)*100000;
                    PointYList.Add(pointY);
                    //float coord_x1 = (float) pointX;
                    //float coord_y1 = (float) pointY;
                    float coord_x1 = (float) pointX02;
                    float coord_y1 = (float) pointY02;
                  //  Vector2 center_point = new Vector2 (-739700.0f, 407600.0f);
                   // float X1 = coord_x1*10000 - center_point.x;
                   // float Y1 = coord_y1*10000 - center_point.y;
                   // Vector2 point = new Vector2(X1, Y1);
                   Vector2 point = new Vector2(coord_x1, coord_y1);
                    vertices.Add(point);
                }
                int num_points = vertices.Count;
                CreateBuildingBlock(num_points);
                vertices.Clear(); 
            }
        } 
    // create one building block accroding to the vertices
    void CreateBuildingBlock(int num_points)
    {
      for (int i=0; i < num_points; i++){
          CreateWall(i);
      }
    } 
    // create one wall 
    void CreateWall(int i)
    {  
        if (i == 0){
             P0 = vertices[0];
             P1 = vertices[0];
             P2 = vertices[1];   
        }
        else if (i==vertices.Count-1){
             P0 = vertices[i-1];
             P1 = vertices[i];
             P2 = vertices[0];   
        }
        else{
            P0 = vertices[i-1];
            P1 = vertices[i];
            P2 = vertices[i+1];
        }
        // calculate the distance between two points - The wall's size
        float WallLength = Vector2.Distance(P1, P2);
        //float WallWidth =4; 
        float WallWidth =12;
        //float WallDepth = 0.05f; 
        float WallDepth = 0.5f;
        // wall's center point position
        float A = (P1.x + P2.x)/2.0f; 
        float B = WallWidth/2.0f;
        float C = (P1.y+P2.y)/2.0f;
        // calculate the angle between (P2-Center_point) and (Co_Center_point - Center_point)
        Vector2 Center_point= new Vector2(A, C);
        Vector2 Co_Center_point = new Vector2(-A, C); // parallel to x axis
        Vector2 V1 = Co_Center_point - Center_point;
        Vector2 V2 = P2 - Center_point;
        float X_angle = (float) (Math.Acos(Vector2.Dot((Vector2)Vector3.Normalize(V1), (Vector2)Vector3.Normalize(V2)))*(180/Math.PI));
        // Create Wall
        GameObject BuildWall = Instantiate(Wall, new Vector3(A, B, C), Quaternion.identity);
        BuildWall.transform.localScale = new Vector3(WallLength, WallWidth, WallDepth);
        BuildWall.tag = "Wall";
        // if the wall parallel to x axis, then we don't need to rotate it. otherwise, we need to rotate the wall 
        if ((X_angle !=0) && (X_angle !=180)) {
         Vector3 P11 = new Vector3(P1.x, 0, P1.y);
         Vector3 P22 = new Vector3(P2.x, 0, P2.y);
         Vector3 M = P22-P11;
         Quaternion rotation=Quaternion.LookRotation(Vector3.Cross(M, Vector3.up).normalized);
         BuildWall.transform.rotation  = rotation; 
        } 
        Rigidbody BuildWallrbdy = BuildWall.AddComponent<Rigidbody>();
        BuildWallrbdy.isKinematic = true;
    }
  }
}
        
    


