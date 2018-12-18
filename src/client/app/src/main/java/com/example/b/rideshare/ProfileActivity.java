package com.example.b.rideshare;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class ProfileActivity extends AppCompatActivity {

    private String token;
    private EditText phone,email,username,id;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);


        username = findViewById(R.id.username);
        id = findViewById(R.id.id);
        email = findViewById(R.id.email);
        phone = findViewById(R.id.phone);

        token = getIntent().getExtras().getString("token");
        String url ="https://api.extrasmisc.com/account/";

        RequestQueue requestQueue = Volley.newRequestQueue(ProfileActivity.this);

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET, url, new JSONObject(), new com.android.volley.Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Log.i("login","success");
                Log.i("login","response:" + response.toString());
                try {
                    phone.setText(response.getString("phone"));
                    username.setText(response.getString("username"));
                    email.setText(response.getString("email"));
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }

        }, new com.android.volley.Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.i("login",error.networkResponse.headers.toString());
                Toast toast = Toast.makeText(ProfileActivity.this, "Unable to log in with provided credentials.", Toast.LENGTH_SHORT);
                toast.show();

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
    }

    public void change(View v) {
        finish();
    }



}
