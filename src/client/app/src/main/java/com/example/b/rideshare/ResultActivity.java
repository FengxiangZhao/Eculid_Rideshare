package com.example.b.rideshare;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class ResultActivity extends Activity implements AdapterView.OnItemClickListener {
    private ListView listview;
    private String token;
    private ArrayList<String> timeList = new ArrayList<String>();
    private ArrayList<Double> originlatList = new ArrayList<Double>();
    private ArrayList<Double> originlonList = new ArrayList<Double>();
    private ArrayList<Double> destlatList = new ArrayList<Double>();
    private ArrayList<Double> destlonList = new ArrayList<Double>();
    private ArrayList<String> matchedList = new ArrayList<>();






    @Override
        protected void onCreate (Bundle savedInstanceState){
            super.onCreate(savedInstanceState);
            setContentView(R.layout.content_result);
        token = getIntent().getExtras().getString("token");
        String url ="https://api.extrasmisc.com/rider/";

        RequestQueue requestQueue = Volley.newRequestQueue(ResultActivity.this);

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET, url, new JSONObject(), new com.android.volley.Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Log.i("result ","success");
                Log.i("result","response:" + response.toString());
            }

        }, new com.android.volley.Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.i("result",error.toString());
                String body = error.toString();
                if (body.contains("id"))
                    Log.i("timelist","added 0");
                {
                    for (int i = 1; i < body.split("\"is_cancelled\"").length; i++) {
                        originlatList.add(Double.parseDouble(body.split("\"origin_lat\":\"")[i].split("\"")[0]));
                        originlonList.add(Double.parseDouble(body.split("\"origin_lon\":\"")[i].split("\"")[0]));
                        destlatList.add(Double.parseDouble(body.split("\"destination_lat\":\"")[i].split("\"")[0]));
                        destlonList.add(Double.parseDouble(body.split("\"destination_lon\":\"")[i].split("\"")[0]));
                        if (!body.split("\"matched_driver\"")[i].split("\\}")[0].contains("null")) {
                            Log.i("matching",body.split("\"matched_driver\"")[i].split("\\}")[0]);
                            matchedList.add(body.split("\"matched_driver\"")[i].split("\\}")[0]);
                            timeList.add("\n[Matched]Rider\n" + body.split("\"scheduled_departure_datetime\":\"")[i].substring(0, 16).replace("T", " ") + "\n");
                            Log.i("timelist","added 1");
                        }
                        else {
                            matchedList.add("None");
                            timeList.add("\n[Unmatched]Rider\n" + body.split("\"scheduled_departure_datetime\":\"")[i].substring(0, 16).replace("T", " ") + "\n");
                            Log.i("timelist","added 2");
                        }
                    }
                }
               // Toast toast = Toast.makeText(ResultActivity.this, "Unable to log in with provided credentials.", Toast.LENGTH_SHORT);
             //   toast.show();
                ListAdapter adapter = new ArrayAdapter<String>(ResultActivity.this,
                        android.R.layout.simple_list_item_1, timeList);
                listview = (ListView) findViewById(R.id.listview);
                listview.setAdapter(adapter);
                listview.setOnItemClickListener(ResultActivity.this);


            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("Content-Type","application/json");
                params.put("Authorization","JWT " + token);
                return params;
            }
        };


        url ="https://api.extrasmisc.com/driver/";
        JsonObjectRequest jsonObjectRequest2 = new JsonObjectRequest(Request.Method.GET, url, new JSONObject(), new com.android.volley.Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Log.i("result ","success");
                Log.i("result","response:" + response.toString());

                /*
                try {
                    // do nothing
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                */

            }

        }, new com.android.volley.Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.i("result",error.toString());
                String body = error.toString();
                if (body.contains("id")) {
                    for (int i = 1; i < body.split("\"car_capacity\"").length; i++) {
                        originlatList.add(Double.parseDouble(body.split("\"origin_lat\":\"")[i].split("\"")[0]));
                        originlonList.add(Double.parseDouble(body.split("\"origin_lon\":\"")[i].split("\"")[0]));
                        destlatList.add(Double.parseDouble(body.split("\"destination_lat\":\"")[i].split("\"")[0]));
                        destlonList.add(Double.parseDouble(body.split("\"destination_lon\":\"")[i].split("\"")[0]));
                        if (!body.split("\"matched_rider\"")[i].split("]")[0].equals(":[")) { // matched
                            matchedList.add(body.split("\"matched_rider\"")[i].split("]")[0]);
                            timeList.add("\n[Matched]Driver\n" + body.split("\"scheduled_departure_datetime\":\"")[i].substring(0, 16).replace("T", " ") + "\n");
                        }
                        else {
                            matchedList.add("None");
                            timeList.add("\n[Unmatched]Driver\n" + body.split("\"scheduled_departure_datetime\":\"")[i].substring(0, 16).replace("T", " ") + "\n");
                        }
                    }
                }
                // Toast toast = Toast.makeText(ResultActivity.this, "Unable to log in with provided credentials.", Toast.LENGTH_SHORT);
                //   toast.show();

                ListAdapter adapter = new ArrayAdapter<String>(ResultActivity.this,
                        android.R.layout.simple_list_item_1, timeList);
                listview = (ListView) findViewById(R.id.listview);
                listview.setAdapter(adapter);
                listview.setOnItemClickListener(ResultActivity.this);

            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("Content-Type","application/json");
                params.put("Authorization","JWT " + token);
                return params;
            }
        };

        requestQueue.add(jsonObjectRequest);
        requestQueue.add(jsonObjectRequest2);



    }

        @Override
        public void onItemClick(AdapterView < ? > parent, View view,int position, long id){
           // Toast.makeText(ResultActivity.this, "clicked " + position , Toast.LENGTH_SHORT).show();
            Intent intent = new Intent(ResultActivity.this, ResultMapActivity.class);
            intent.putExtra("originLat",originlatList.get(position));
            intent.putExtra("originLon",originlonList.get(position));
            intent.putExtra("destLat",destlatList.get(position));
            intent.putExtra("destLon",destlonList.get(position));
            intent.putExtra("time",timeList.get(position));
            intent.putExtra("match",matchedList.get(position));
            startActivity(intent);
        }


    }

