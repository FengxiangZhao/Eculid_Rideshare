package com.example.b.rideshare;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class RegisterActivity extends AppCompatActivity {

    private TextView username, password, email, phone;
    private boolean startRegister = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
        username = findViewById(R.id.username);
        password = findViewById(R.id.password);
        email = findViewById(R.id.email);
        phone = findViewById(R.id.phone);
    }

    public void register(View v) {

    /*    if (!email.getText().toString().endsWith("@case.edu")) {
            email.setError("Must be Case Mail");
            startRegister = false;
        }

        if (password.getText().toString().length() < 4) {
            password.setError("Password too short");
            startRegister = false;
        }

        if (startRegister) {
            Log.i("register", "start");
            Log.i("login","Start auth");
            HashMap data = new HashMap();
            data.put("username",username.getText().toString());
            data.put("password",password.getText().toString());
            data.put("email",email.getText().toString());
            data.put("phone",phone.getText().toString());*/

        Log.i("register", "start");
        Log.i("login","Start auth");
        HashMap data = new HashMap();
        data.put("username","test3");
        data.put("password","qwer1234");
        data.put("email","fxz121@case.edu");
        data.put("phone","216000002");


            String url = "https://api.extrasmisc.com/account/register/";

            RequestQueue requestQueue = Volley.newRequestQueue(RegisterActivity.this);

            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, new JSONObject(data), new com.android.volley.Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    Log.i("register", "start1");
                    Log.i("register", "success");
                    finish();
                    Toast toast = Toast.makeText(RegisterActivity.this, "Register Success!", Toast.LENGTH_SHORT);
                    toast.show();


                }
            }, new com.android.volley.Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    Log.i("register","failed");
                    Toast toast = Toast.makeText(RegisterActivity.this, "Unable to register.", Toast.LENGTH_SHORT);
                    //decryted byte message
                    String body = new String(error.networkResponse.data);
                    if (body.contains("username")) {
                        username.setError("username already used by others");
                    }
                    if (body.contains("email")) {
                        email.setError("email already used by others");
                    }

                    if (body.contains("phone")) {
                        phone.setError("phone already used by others");
                    }
                    Log.i("register",new String(error.networkResponse.data));
                    toast.show();

                }
            });

            requestQueue.add(jsonObjectRequest);
        //}

        startRegister = true;


    }

    public void cancel(View v) {
        finish();
    }

}
