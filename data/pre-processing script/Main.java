package com.company;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.io.FileReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.Writer;
import java.io.BufferedWriter;
import java.io.FileWriter;
import com.google.gson.*;


public class Main {
    public static Writer output = null;
    public static JSONParser parse = new JSONParser();
    public static Gson gson = new GsonBuilder().setPrettyPrinting().create();
    public static JsonParser jp = new JsonParser();


    //see google doc

    /**
     * 1. average ingredients vector for each cuisine
     * 2. calculate distance between vectors (???) look online
     * 3. use mean absolute error/mean squared error (???) look online
     * @return
     */
    public static int complexEvaluater(){
        return 0;
    }
    public static void preprocess(){
        try {
            File dir = new File("/Users/David/Desktop/data/jsons");
            File [] dirListing = dir.listFiles();
            if(dirListing != null) {
                for(File jsonFile : dirListing) {
                    try {
                        File newFile = new File("/Users/David/Desktop/data/out/" + jsonFile.getName());
                        output = new BufferedWriter(new FileWriter(newFile));
                        Object obj = parse.parse(new FileReader(jsonFile));
                        JSONArray jsonArray = (JSONArray) obj;
                        for(Object o : jsonArray) {
                            JSONObject j = (JSONObject) o;
                            j.remove("course");
                            j.remove("name");
                            j.remove("flavors");
                            j.put("cuisine", j.get("cuisine").toString().toLowerCase());
                        }
                        JsonElement je = jp.parse(jsonArray.toJSONString());
                        String prettyJsonString = gson.toJson(je);
                        output.write(prettyJsonString);
                        output.close();
                    } catch(Exception e) {
                        System.out.println("file not found");
                    }
                }
            } else {
            }
        } catch(Exception e) {
            System.out.println("idk");
        }
    }

    public static void main(String[] args) {
       preprocess();
    }
}
